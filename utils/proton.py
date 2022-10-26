import numpy as np
import pfsspy.coords
from scipy import constants

class Proton():
    def __init__(config, magnetic_field):
        self.config = config
        self.dt = config['sample_rate']
        self.position_record = []
        self.position = np.array(pfsspy.coords.sph2cart(self.config['injection_pos']['r'],
                                                    self.config['injection_pos']['theta']*np.pi,
                                                    self.config['injection_pos']['phi']*np.pi))
        self.position.append(self.init_pos)
        self.KE = np.random.uniform(self.config['KE']['max'],
                                    self.config['KE']['min'])
        c, m = constants.c, config['mass']

        self.velocity = self.position
        while (self.position + self.dt * self.velocity) > self.config['injection_pos']['r']:
            v_r, v_theta, v_phi = self.get_init_velocity(m, c)
            self.velocity = np.array(pfsspy.coords.sph2cart(v_r, v_theta, v_phi))

    def get_init_velocity(m, c):
        v_r = c * np.sqrt(1 - (m**2) * (c**4) / (self.KE + m * (c**2))**2)
        v_theta = np.random.uniform(0., np.pi)
        v_phi = np.random.uniform(0., 2*np.pi)
        return v_r, v_theta, v_phi
