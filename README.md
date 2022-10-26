# Semi-analytical method for simulating solar atmospheric gamma-ray flux

## 2021 CUHK Physics SURIP Poster Presentation

In the repo, please find the poster [here](https://github.com/wyhwong/SA-SAGamma/tree/main/presentation). We are glad to share that the poster [`Proton Motion`](https://github.com/wyhwong/SA-SAGamma/blob/main/presentation/Proton%20Motion%20in%20the%20Sun%20with%20PFSS%20Model.pdf) obtained Best Poster Award 3rd Prize in SURIP.

---

## Description of Repo
To be updated. The refactor of scripts are not done yet.

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
