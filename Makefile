# Makefile

IMAGE_NAME=dns-homelab-generator
TAG=latest

.PHONY: build
build:
    docker build -t $(IMAGE_NAME):$(TAG) .

.PHONY: run
run:
    docker-compose up --build

.PHONY: push
push:
    docker tag $(IMAGE_NAME):$(TAG) $(DOCKER_USERNAME)/$(IMAGE_NAME):$(TAG)
    docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(TAG)
