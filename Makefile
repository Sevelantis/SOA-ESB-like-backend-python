clean:
	docker rmi -f $(shell docker images -aq)
	docker rm -f $(shell docker ps -aq)
	docker ps -a
	docker images -a

REGISTRY := registry.deti:5000
NAMESPACE := egs-conv
SERVICE := composer-service
VERSION := latest

build:
	docker buildx build --platform linux/amd64 --network=host -t ${REGISTRY}/$(NAMESPACE)/$(SERVICE):$(VERSION) .

push:
	docker push ${REGISTRY}/$(NAMESPACE)/$(SERVICE):$(VERSION)
