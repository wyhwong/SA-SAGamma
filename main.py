#!/usr/bin/env python3
import argparse
import logging
import shutil
from concurrent.futures import ProcessPoolExecutor, wait
from glob import glob
from utils.proton import Proton
from utils.plot import *
from utils.pfss import *
from utils.common import *

def simulate_proton_motion(proton_id, magnetic_field, rss):
    logging.info(f"Simulating Proton {proton_id}")
    proton = Proton(magnetic_field, rss)
    trajectory = proton.get_trajectory()
    logging.info(f"The simulation of Proton {proton_id} is ended")
    return trajectory, proton.escaped, proton.entered

def main(args):
    output_dir = get_output_dir()
    if args.show:
        logging.info(get_hmi_list())
        exit()
    marker = int(len(glob(f"{output_dir}/*.npy")) + 1)
    shutil.copyfile("config/config.yml", f"{output_dir}/config_{marker}.yml")
    sun_params = get_sun_params()
    proton_params = get_proton_params()
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

    logging.info("Injecting protons")
    magnetic_field = pfss_model.bg
    with ProcessPoolExecutor(max_workers=20) as Executor:
        futures = [Executor.submit(simulate_proton_motion, n, magnetic_field, sun_params['rss']) for n in range(proton_params['amount'])]
    wait(futures)

    trajectories = []
    number_of_escaped = 0
    number_of_entered = 0

    _, ax = get_base_plot_3D(title="Trajectories of simulated protons")
    for proton_id, future in enumerate(futures):
        trajectory, escaped, entered = future.result()
        trajectories.append(trajectory)
        if escaped:
            number_of_escaped += 1
        if entered:
            number_of_entered += 1
        ax.plot(trajectory.y[0], trajectory.y[1], trajectory.y[2], linewidth=0.1, label=f"Trajectory of {proton_id}")
        logging.info(f"Visualized the trajectory of Proton {proton_id}")

    plt.savefig(f"{output_dir}/trajectories_{marker}.pdf", facecolor="w")
    logging.info("Saved visualization of simulated trajectories.")

    (r, theta, phi) = proton_params['injection_pos']['r'], proton_params['injection_pos']['theta']*np.pi, proton_params['injection_pos']['phi']*np.pi
    (x, y, z) = pfsspy.coords.sph2cart(r, theta, phi)
    ax.set(xlim3d=[x-0.01, x+0.01], ylim3d=[y-0.01, y+0.01], zlim3d=[z-0.01, z+0.01])
    plt.savefig(f"{output_dir}/trajectories_zoomed_{marker}.pdf", facecolor="w")
    logging.info("Saved visualization of simulated trajectories.")

    logging.info(f"Number of protons escaped source surface: {number_of_escaped}")
    logging.info(f"Number of protons entered corona: {number_of_entered}")

    plot_rss_surface(ax=ax, rss=sun_params['rss'])

    plt.savefig(f"{output_dir}/trajectories_rss_{marker}.pdf", facecolor="w")
    plt.close()
    logging.info("Saved visualization of simulated trajectories with rss sphere.")

    np.save(f"{output_dir}/trajectories_{marker}.npy", trajectories)
    logging.info("Saved simulated trajectories as .npy file")

    # logging.info("Loading proton mass density")
    # mass_density_function = get_proton_mass_density()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Setting of parser, inputting parameters
    parser = argparse.ArgumentParser(description="Setting of the distinguishability test")
    parser.add_argument("--show", action="store_true",
                        default=False, help="Show HMI map information.")
    parser.add_argument("--output_dir", type=str,
                        default="results", help="Path of the results directory.")
    args = parser.parse_args()
    logging.info(f"Input parameters: {args}")
    main(args)
