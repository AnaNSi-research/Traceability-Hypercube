import os
import argparse

def generate_compose(hypercube_size, init_port = 8880, superset_threshold = 10, client_service = True):
    str = "version: '3.9'"

    common_variables = f"""
\nx-common-variables: &common-variables
  HYPERCUBE_SIZE: {hypercube_size}
  SUPERSET_THRESHOLD: {superset_threshold}
  INIT_PORT: {init_port}"""
    str += common_variables

    hypercube_services = "\n\nservices:"
    for i in range(0, 2**hypercube_size):
        hypercube_services += f"""
  hypercube_{i}:
    network_mode: 'host'
    image: hypercube:latest
    environment:
      <<: *common-variables
      NODE_PORT: {init_port + i}"""
    str += hypercube_services

    if client_service:        
        client_tracing_service = """
  hypercube-client-tracing:
    network_mode: 'host'
    image: hypercube-client-tracing:latest
    environment:
      <<: *common-variables
      BLOCKCHAIN_ADDRESS: http://localhost:8545
      CHAIN_ID: 1337
    volumes:
      - ./data/client:/client_data
      - ./client-tracing/contracts:/client_data/contracts
      - ./client-tracing/objects:/client_data/objects"""
        str += client_tracing_service

        ipfs_service = """
  ipfs:
    network_mode: 'host'
    image: ipfs/go-ipfs::v0.8.0
    environment:
      IPFS_PROFILE: server
      IPFS_PATH: /ipfsdata
    volumes:
      - ./data/ipfs:/ipfsdata"""
        str += ipfs_service

        ganache_service = """
  ganache:
    network_mode: 'host'
    image: trufflesuite/ganache-cli:latest
    volumes:
      - ./data/ganache:/ganache_data
    command: --seed 42 --db=/ganache_data"""
        str += ganache_service
    
    return str

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--size", required=True, help="hypercube size", type=int)
    ap.add_argument("-p", "--port", default=8880, help="init port", type=int)
    ap.add_argument("-t", "--threshold", default=10, help="superset threshold", type=int)
    args = vars(ap.parse_args())

    compose = generate_compose(hypercube_size=args['size'], init_port=args['port'], superset_threshold=args['threshold'])

    with open("docker-compose.yml", "w") as file:
        file.write(compose)