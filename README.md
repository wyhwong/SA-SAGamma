# Semi-analytical method for simulating solar atmospheric gamma-ray flux

## Description of Repo
To be updated

---

## Simulation (To be completed)
Please run the following to compute the simulate the trajectory of cosmic-ray protons' motion in the Sun:
```bash
# Build docker image
make build

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

## Configs
The configs of the Sun and cosmic-ray protons can be adjusted at `config/config.yaml`.

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
After set up the server, you can go to [here](https://localhost:8888) and the password is `sagamma`.

---

## Authors
[@wyhwong](https://github.com/wyhwong)
