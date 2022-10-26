import argparse
import logging
import os
from scipy import constants
from utils.pfss import *
from utils.config import *

def main(args):
    if args.show:
        logging.info(get_hmi_list())
        exit
    sun_config = get_sun_config()
    fits_dir = f"config/CR{sun_config['cr_number']}"
    if not os.path.isdir(fits_dir):
        logging.info("HMI fits does not exist. Downloading fits...")
        get_hmi_map(sun_config['cr_number'])

    logging.info("Loading HMI map...")
    hmi_map = load_hmi_map(sun_config['cr_number'])

    logging.info("Resampling HMI map...")
    hmi_map = resample_hmi_map(hmi_map,
                               resolution_phi=360,
                               resolution_theta=180)

    logging.info("Constructing PFSS model")
    pfss_model = get_pfss_model(hmi_map, sun_config['nrho'], rss=sun_config['rss'])
    magnetic_field = pfss.model.bg

    logging.info("Loading proton mass density")
    mass_density_function = get_proton_mass_density()

    bfield_rescalar = 5.586e22 * constants.e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Setting of parser, inputting parameters
    parser = argparse.ArgumentParser(description="Setting of the distinguishability test")
    parser.add_argument("--show", action="store_true",
                        default=False,
                        help="Show HMI map info.")
    args = parser.parse_args()
    logging.info(f"Input parameters: {args}")
    main(args)
