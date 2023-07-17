include .env
export

IMAGE_NAME = cat-charity-app
CONTAINER_NAME = fund-app-container
PORT := $(PORT)

start: build run
	echo "___Starting redmine bot___"

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the FastAPI application using the Docker image
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT) $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)