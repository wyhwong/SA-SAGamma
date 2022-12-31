#!/usr/bin/env python3
import argparse
import logging
from scipy import constants
from utils.pfss import *
from utils.common import *

def main(args):
    if args.show:
        logging.info(get_hmi_list())
        exit()
    sun_params = get_sun_params()
    fits_dir = f"config/CR{sun_params['cr_number']}"
    exist = check_and_create_dir(fits_dir)
    if not exist:
        logging.info("HMI fits does not exist. Downloading fits...")
        get_hmi_map(sun_params['cr_number'])

    logging.info("Loading HMI map...")
    hmi_map = load_hmi_map(sun_params['cr_number'])

    logging.info("Resampling HMI map...")
    hmi_map = resample_hmi_map(hmi_map,
                               resolution_phi=sun_params['resolution']['theta'],
                               resolution_theta=sun_params['resolution']['phi'])

    logging.info("Constructing PFSS model")
    pfss_model = get_pfss_model(hmi_map, sun_params['resolution']['r'], rss=sun_params['rss'])

    # Array form of magnetic field: B[phi][s][rho][Brho Bs Bphi]
    magnetic_field = pfss_model.bg

    # logging.info("Loading proton mass density")
    # mass_density_function = get_proton_mass_density()

    bfield_rescalar = 5.586e22 * constants.e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Setting of parser, inputting parameters
    parser = argparse.ArgumentParser(description="Setting of the distinguishability test")
    parser.add_argument("--show", action="store_true",
                        default=False,
                        help="Show HMI map info.")
    parser.add_argument("--num_proton", type=int,
                        default=100,
                        help="Number of proton being simulated")          
    args = parser.parse_args()
    logging.info(f"Input parameters: {args}")
    main(args)
