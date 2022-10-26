import yaml
import numpy as np
import scipy.interpolate as interpol

def get_sun_config():
    with open("config/config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)['sun']


def get_proton_config():
    with open("config/config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)['proton']


def get_proton_mass_density():
    rho = np.genfromtxt('config/rho.csv', delimiter=',')
    rho_against_r = interpol.interp1d(rhor.T[0], rhor.T[1],
                                      bounds_error=False,
                                      fill_value="extrapolate")
    return rho_against_r
