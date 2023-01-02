export DOCKER_BUILDKIT=1

port ?= 8888
email ?=
args ?=

build:
	docker-compose build

start:
	email=${email} args=${args} docker-compose up samsaga

develop:
	email=${email} docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d samsaga
	docker exec -it samsaga bash

jupyter_up:
	port=${port} email=${email} docker-compose up -d samsaga_jupyter

jupyter_down:
	port=${port} docker-compose kill samsaga_jupyter

clean:
	docker-compose down --remove-orphans
