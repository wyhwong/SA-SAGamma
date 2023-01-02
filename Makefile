export DOCKER_BUILDKIT=1

port ?= 8888
email ?=
args ?=

build:
	docker-compose build

start:
	email=${email} args=${args} docker-compose up sagamma

develop:
	email=${email} docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d sagamma
	docker exec -it sagamma bash

jupyter_up:
	port=${port} email=${email} docker-compose up -d sagamma_jupyter

jupyter_down:
	port=${port} docker-compose kill sagamma_jupyter

clean:
	docker-compose down --remove-orphans
