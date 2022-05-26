# Jupiter Docker Swarm Deployment Resources

These utilities are available to initialize a Docker Swarm environment for the Jupiter Inventory Mangement Console, Jupiter Collector Service, Jupiter Curated Inventory Service, and their respective data stores as well as automatically generated credentials that are stored in Docker Secrets.

## Minimum Requirements
* Docker 19.03.6
* Docker Compose 1.17.1
* Python 3.6.9

## Usage
1. Ensure your Docker host has Docker Swarm initialized
1. Clone repo to the Docker host
   `git clone https://github.com/xpert98/jupiter-docker.git`
1. Run the jupiter_init.py script, providing a version for the deployments/secrets
   * `jupiter_init.py -v 1`
   * Take note of database credentials and JWT bearer tokens that were generated - they're only shown once
   * A docker-compose.yaml file should be generated
1. Deploy the Swarm stack
   * `sudo docker stack deploy jupiter -c docker-compose.yaml`
