import yaml
import os
import numpy as np
import scipy.interpolate as interpol


def check_and_create_dir(directory):
    exist = os.path.isdir(directory)
    if not exist:
        os.mkdir(directory)
    return exist


def get_config():
    with open("config/config.yml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_sun_params():
    return get_config()['sun']


def get_proton_params():
    return get_config()['proton']


def get_proton_mass_density():
    rhor = np.genfromtxt('results/rho.csv', delimiter=',')
    rho_against_r = interpol.interp1d(rhor.T[0], rhor.T[1],
                                      bounds_error=False,
                                      fill_value="extrapolate")
    return rho_against_r
