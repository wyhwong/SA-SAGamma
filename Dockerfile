FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip -y
RUN pip3 install jupyterthemes notebook pyyaml lxml zeep drms requests astropy numpy matplotlib pfsspy sunpy scipy p_tqdm
RUN jt -t monokai
