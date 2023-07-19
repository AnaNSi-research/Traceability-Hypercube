from solcx import compile_files, install_solc
from web3 import Web3
from eth_account import Account
from hypercube_requests import HypercubeRequests
from keywords import Brand, Colour
import ipfshttpclient


class Client:

    def __init__(self, blockchain_addr="http://localhost:8545", chain_id="1337", ipfs_addr="/ip4/127.0.0.1/tcp/5001", hypercube_addr="http://localhost:8880", private_key=None):
        self.blockchain_addr = blockchain_addr
        self.chain_id = chain_id
        self.ipfs_addr = ipfs_addr
        self.hypercube_addr = hypercube_addr
        self.private_key = private_key

        self.hypercube_requests = HypercubeRequests(hypercube_addr)

        self.ipfs = ipfshttpclient.connect(ipfs_addr)
        self.w3 = Web3(Web3.HTTPProvider(blockchain_addr))

        if private_key is None:
            self.acct = self.w3.eth.accounts[0]
        else:
            self.acct = Account.from_key(private_key).address
        self.w3.eth.default_account = self.acct
        print("Using account", self.acct)

        print("Initializing Factory")
        install_solc('0.8.19')

        # factory_abi, factory_bytecode = self.compile_contract("./contracts/CarFactory.sol")
        factory_abi, factory_bytecode = self.compile_contract(
            "contracts/CarCloneFactory.sol", "CarCloneFactory")
        # TODO deploy base car to be cloned and pass that address as an argument to the constructor of the clone factory
        self.contract = self.deploy_contract(factory_abi, factory_bytecode)

        self.car_abi, self.car_bytecode = self.compile_contract("contracts/Car.sol", "Car")

    def compile_contract(self, source_file, contract_name):
        compiled = compile_files([source_file], output_values=['abi', 'bin'])[f"{source_file}:{contract_name}"]

        abi = compiled['abi']
        bytecode = compiled['bin']

        return abi, bytecode

    def deploy_contract(self, abi, bytecode, args={}):
        contract_bin = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract_bin.constructor(self.w3.eth.accounts[1]).transact({'from': self.acct})
        # contract_data = contract_bin.constructor(self.w3.eth.accounts[1]).build_transaction({'from': self.acct})
        # tx_hash = self.w3.eth.send_transaction(contract_data)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.attach_contract(abi, bytecode, tx_receipt.contractAddress)

        print(f"Contract deployed to {tx_receipt.contractAddress}")
        print(f"Gas used: {tx_receipt.gasUsed}")

        return self.contract
    
    def attach_contract(self, abi, bytecode, address):
        self.contract = self.w3.eth.contract(
            address=address,
            abi=abi,
            bytecode=bytecode
        )

    def create_keyword(self, brand, colour):
        return brand + colour + (max(Brand) - 1) * brand
    
    def create_keyword_onehot(self, brand, colour):
        b = (2 ** brand) if brand is not None else 0
        c = (2 ** (max(Brand) + colour + 1)) if colour is not None else 0
        
        return b + c
    
    def create_car(self, brand, colour, img_path=None):
        # Add car image on IPFS
        if img_path is not None:
            ipfs_img_addr = self.ipfs.add(img_path)['Hash']
            print("IPFS image address:", ipfs_img_addr)
        else:
            ipfs_img_addr = ""
            print("No IPFS image uploaded")

        # Create new car through the car factory
        tx = self.contract.functions.createCar(brand, colour, ipfs_img_addr).transact({"from": self.acct})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx)
        # retrieve retun value through log of emitted events by the transaction
        car_address = self.contract.events.CarCreated().process_receipt(tx_receipt)[0]['args']['_car']
        print(f"Created new car at {car_address}")
        print(f"Gas used: {tx_receipt.gasUsed}")

        # Add car on hypercube
        keyword = self.create_keyword_onehot(brand, colour)
        print("Keyword", keyword)

        res = self.hypercube_requests.add_obj(car_address, keyword)
        print("Add car on hypercube:", res.text)

        return res

    def search_car(self, brand, colour):
        keyword = self.create_keyword_onehot(brand, colour)

        res = self.hypercube_requests.pin_search(keyword)
        print("Objects with keyword {}:\n".format(keyword), res.text)

        return res

    def car_info(self, address):
        contract = self.w3.eth.contract(address=address, abi=self.car_abi)

        brand = Brand(contract.functions.brand().call())
        colour = Colour(contract.functions.colour().call())
        owner = contract.functions.owner().call()
        ipfs_img = contract.functions.ipfs_img().call()

        print(brand.name, colour.name, owner, ipfs_img)

        self.ipfs.get(ipfs_img, target='/client_data/downloads')

        return brand, colour, owner, ipfs_img

    def remove_car(self, address, brand, colour):
        keyword = self.create_keyword_onehot(brand, colour)

        res = self.hypercube_requests.remove_obj(address, keyword)
        print(res)

        return res
    
    def superset_search(self, brand=None, colour=None, threshold=10):
        assert(brand is None or colour is None)
        assert(brand is not None or colour is not None)

        keyword = self.create_keyword_onehot(brand, colour)

        res = self.hypercube_requests.superset_search(keyword, threshold)
        print(res)
        print(res.text)

        return res



    # TODO (optional) attach to an already deployed factory
