# DNSKEY to DS Record Converter
This repository contains the code for a web application that converts DNSKEY records into DS records. The web application is built using Python and Flask and can be run as a Docker container.
## Prerequisites
Ensure that Docker is installed on your system. If not, visit the official Docker website and follow the instructions to install it.
## Building the Docker Image
Navigate to the project directory and run the following command to build the Docker image:
``` bash
docker build -t dnskey-to-ds-converter .
```
This creates a Docker image with the name "dnskey-to-ds-converter".
## Running the Docker Container
To start a Docker container from the built image, run the following command:
``` bash
docker run -p 5000:5000 dnskey-to-ds-converter
```
This starts a Docker container and binds the container's port 5000 to port 5000 on your host system.
## Accessing the Web Application
Open a web browser and navigate to http://localhost:5000. You should see the web application where you can enter a domain name to convert its DNSKEY records into DS records.
