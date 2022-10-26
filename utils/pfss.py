import os
import sunpy.map
from glob import glob
from sunpy.net import Fido
from sunpy.net import attrs as net_attrs
import astropy.units as astrounit
import pfsspy.utils


def get_hmi_list():
    time = net_attrs.Time('2010/01/01', '2010/01/01')
    series = net_attrs.jsoc.Series('hmi.synoptic_mr_polfil_720s')
    return Fido.search(time, series)


def get_hmi_map(CAR_ROT):
    time = net_attrs.Time('2010/01/01', '2010/01/01')
    series = net_attrs.jsoc.Series('hmi.synoptic_mr_polfil_720s')
    crot = net_attrs.jsoc.PrimeKey('CAR_ROT', CAR_ROT)
    email = os.environ['email']
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
