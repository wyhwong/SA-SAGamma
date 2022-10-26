export DOCKER_BUILDKIT=1

port ?= 8888
email ?=
args ?=

build:
	port=${port} docker-compose build

start:
	port=${port} email=${email} args=${args} docker-compose up sagamma

jupyter_up:
	port=${port} email=${email} docker-compose up -d sagamma_jupyter

jupyter_down:
	port=${port} docker-compose kill sagamma_jupyter

clean:
	port=${port} docker-compose down --remove-orphans