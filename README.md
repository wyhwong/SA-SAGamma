# SAM-SAGA
Semi Analytical Method for simulating Solar Atmospheric GAmma-ray flux

---

## 2021 CUHK Physics SURIP Poster Presentation

In the repo, please find our poster [here](https://github.com/wyhwong/SA-SAGamma/tree/main/presentation). We are glad to share that the poster [`Proton Motion`](https://github.com/wyhwong/SA-SAGamma/blob/main/presentation/Proton%20Motion%20in%20the%20Sun%20with%20PFSS%20Model.pdf) obtained Best Poster Award 3rd Prize in SURIP 2021 in CUHK Physics!

---

## Description and Usage
This repository simulates the SAγ flux with a semi-analytical method to reduce the time cost of a full simulation. We combined the observational data of solar magnetic field and the simulation on cosmic-ray protons' motion.

Please run the following to compute the simulate the trajectory of cosmic-ray protons' motion in the Sun:
```bash
# Build docker image
make build

# After modifying config/config.yml for configuration of simulation
# Start docker container
make start

# If you want to check the available Carrington Rotations
make args="--show" start

# If you need to download HMI map data
make email=<your email> start

# Remove all docker container
make clean
```

---

## Jupyter Server
Please run the following to set up the Jupyter server for development or data visualization:
```bash
# Set up Jupyter server (default port=8888 if no input)
# This is for development or data visualization
make port=<port> jupyter_up

# Kill Jupyter server
make jupyter_down
```
After set up the server, you can go to [here](https://localhost:8888) and the password is `samsaga`.

---

## Authors
[@wyhwong](https://github.com/wyhwong)
