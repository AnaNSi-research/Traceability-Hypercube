# Traceability system based on the Ethereum blockchain, IPFS and the Hypercube DHT

This project aims to implement a traceability architecture with a search system
based on three main components:

- Ethereum blockchain
- IPFS
- Hypercube DHT [Zichichi et al.]

The basic idea behind this architecture is to stray away from a standard client-
server model as much as possible by leveraging on the main advantages about
decentralization brought about by its components.\
We imagine as a use case the one where a user wants to track a series of cars
for which various information such as the brand, its colour and an image are
stored by the system.\
The Ethereum blockchain allows to host executable code in the form of Smart
Contracts. Each contract represents a car and stores its brand, its colour and a
link to the corresponding image on IPFS.\
The Hypercube DHT is used to index the cars based on their details (keywords).
This way, each vehicle can then be retrieved on the basis of its brand, its colour
or both.\
More information on the contracts and the Hypercube will be given in the next
sections

## Install with Docker

##### Requirements

- Python 3.x
- Docker
- Docker Compose -> [install](https://docs.docker.com/compose/install/)

##### Commands

```
git clone
cd traceability-DHT/server
docker build -t hypercube .
cd ../client-tracing
docker build -t hypercube-client-tracing .
cd ..
docker-compose up -d
```

## Usage

1. (optional) **Change keywords**\
To change the keywords, you need to edit the file `client-tracing/keywords.py`. You are allowed only to add/remove colours and brands.
2. (optional) **Update the docker compose**\
If you have modified the number of possible keywords, update the docker compose file to generate a different number of hypercube nodes:
   `python generate_compose.py <hypercube_size>`. In this case, because of the keywords encoding of the client, the hypercube size is equal to the total amount of possibile keywords.
3. (optional) **Update the services**\
Run `docker-compose up -d` to start the updated services.
3. **Run the client**\
   `docker-compose run hypercube-client-tracing python main.py`

## Folders

##### ./server

- contains the hypercube and node implementation
- _/hop_counter_ contains an app for counting network hops

##### ./client-tracing

- contains all the client for interacting with nodes

##### ./data

- contains the persistency of the client services
- _/client/downloads_ contains the images of the cars retrieved through IPFS

##### client executables

- _main.py_: script that provides a user-friendly command line UI.

## References

- Zichichi M., Serena L., Ferretti S., D'Angelo G., [Governing Decentralized Complex Queries Through a DAO](https://mirkozichichi.me/assets/papers/14governing.pdf), in Proc. of the Conference on Information Technology for Social Good (GoodIT). 9-11 September 2021
- Zichichi M., Serena L., Ferretti S., D'Angelo G., [Towards Decentralized Complex Queries over Distributed Ledgers: a Data Marketplace Use-case](https://mirkozichichi.me/assets/papers/12towards.pdf) , in Proc. of the 30th IEEE International Conference on Computer Communications and Networks (ICCCN). 3rd International Workshop on Social (Media) Sensing. 19-22 July 2021
