all: build-docker

test:
	./ipwarn -h

build-docker:
	docker build . -t pablogcaldito/ipwarn:$(VERSION)
