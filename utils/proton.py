import numpy as np
import pfsspy.coords
from scipy import constants
from scipy.integrate import solve_ivp
from .pfss import strum2cart
from .common import get_proton_params, get_sun_params


class Proton():
    def __init__(self, magnetic_field, rss):
        config = get_proton_params()
        self.magnetic_field = magnetic_field
        self.dt = config['sample_rate']
        self.runtime_max = config['runtime_max']
        self.mass = config['mass']
        self.charge = config['charge']
        self.rss = rss
        self.r = config['injection_pos']['r']
        self.theta = config['injection_pos']['theta']*np.pi
        self.phi = config['injection_pos']['phi']*np.pi
        self._position = np.array(pfsspy.coords.sph2cart(self.r, self.theta, self.phi))
        self.escaped = False
        self.entered = False
        self.KE = np.random.uniform(config['KE']['max'],
                                    config['KE']['min'])
        self._get_sun_resolution()
        self._get_init_velocity()

    def get_trajectory(self):
        trajectory = solve_ivp(self._apply_magnetic_force, method='RK45', t_span=[0, self.runtime_max], y0=[*self._position, *self._velocity ],
                               t_eval = np.arange(0, self.runtime_max, self.dt))
        return trajectory

    def _get_sun_resolution(self):
        resolution = get_sun_params()['resolution']
        self.res_r = resolution['r']
        self.res_t = resolution['theta']
        self.res_p = resolution['phi']

    def _get_init_velocity(self):
        np.random.seed()
        v_r = constants.c * np.sqrt(1 - (self.mass**2) * (constants.c**4) / (self.KE + self.mass * (constants.c**2))**2)
        v_theta = np.random.uniform(0., np.pi)
        v_phi = np.random.uniform(0., 2*np.pi)
        self._scalarv = v_r
        self._velocity  = np.array(pfsspy.coords.sph2cart(v_r, v_theta, v_phi))
        if np.dot(self._position+self._velocity *self.dt, self._position+self._velocity *self.dt) > self.r**2:
            self._get_init_velocity()

    def _apply_magnetic_force(self, t, y):
        if np.dot(y[:3], y[:3]) > self.rss:
            self.escaped = True
        elif np.dot(y[:3], y[:3]) < 1:
            self.entered = True
        if self.escaped or self.entered:
            return [0., 0., 0., 0., 0., 0.]
        y[3:] *= self._scalarv*2/np.dot(y[3:], y[3:])
        strum_pos = pfsspy.coords.cart2strum(*y[:3])
        index_r, index_t, index_p = round(10**strum_pos[0]/self.rss*self.res_r), round(np.arccos(strum_pos[1])/np.pi*self.res_t), round(strum_pos[2]/(2*np.pi)*self.res_p)
        if index_t > 180:
            index_t = 180 - index_t
        if index_t < 0:
            index_t += 360
        if index_p < 0:
            index_p += 360
        local_magnetic_field = strum2cart(self.magnetic_field[index_p, index_t, index_r], strum_pos) * 5.586e22 * constants.e
        lorentz_f = 1 / np.sqrt(1 - ((y[3:]/constants.c)**2))
        lorentz_f[np.isnan(lorentz_f)] = np.inf
        force = np.float128(self.charge*np.cross(y[3:], local_magnetic_field))
        return [*y[3:], *(force / self.mass / lorentz_f)]
