import os
import numpy as np
import sunpy.map
from glob import glob
from sunpy.net import Fido
from sunpy.net import attrs as net_attrs
import astropy.units as astrounit
import pfsspy.utils


# Convert the vector in "strumfric" coordinates to Cartesian coordinates
# here a is the vector being converted, b is the "strumfric" coordinates
def strum2cart(a, b):
    c_x = (a[0]*np.sin(np.arccos(b[1]))*np.cos(b[2]) - a[1]*b[1]*np.cos(b[2])/np.sqrt(1-b[1]**2) - a[2]*np.sin(np.arccos(b[1]))*np.sin(b[2]))
    c_y = (a[0]*np.sin(np.arccos(b[1]))*np.sin(b[2]) - a[1]*b[1]*np.sin(b[2])/np.sqrt(1-b[1]**2) + a[2]*np.sin(np.arccos(b[1]))*np.cos(b[2]))
    c_z = (a[0]*b[1] + a[1])
    c = np.array([c_x, c_y, c_z])
    return c


def get_hmi_list():
    time = net_attrs.Time('2010/01/01', '2010/01/01')
    series = net_attrs.jsoc.Series('hmi.synoptic_mr_polfil_720s')
    return Fido.search(time, series)


def get_hmi_map(CAR_ROT):
    time = net_attrs.Time('2010/01/01', '2010/01/01')
    series = net_attrs.jsoc.Series('hmi.synoptic_mr_polfil_720s')
    crot = net_attrs.jsoc.PrimeKey('CAR_ROT', CAR_ROT)
    email = os.environ['EMAIL']
    fits = Fido.search(time, series, crot,
                         net_attrs.jsoc.Notify(email))
    Fido.fetch(fits, path=f'config/CR{CAR_ROT}')


def load_hmi_map(CAR_ROT):
    path = glob(f'config/CR{CAR_ROT}/*.fits')[0]
    hmi_map = sunpy.map.Map(path)
    pfsspy.utils.fix_hmi_meta(hmi_map)
    return hmi_map


# resolution_phi, resolution_theta are in degree
def resample_hmi_map(hmi_map, resolution_phi, resolution_theta):
    # Resample the HMI map to spare computing time cost (Not necessary)
    # Convert the map resolution to a smaller one
    hmi_map = hmi_map.resample([resolution_phi, resolution_theta] * astrounit.pix)
    return hmi_map


def get_pfss_model(hmi_map, nrho=100, rss=2.5):
    pfss_input = pfsspy.Input(hmi_map, nrho, rss)
    pfss_model = pfsspy.pfss(pfss_input)
    return pfss_model
