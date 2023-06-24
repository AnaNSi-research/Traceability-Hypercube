from solcx import compile_files, install_solc
from eth_utils import address
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
import ipfshttpclient
import json
import os


class Client:
    def __init__(self, blockchain_addr="http://localhost:8545", chain_id="1337", ipfs_addr="/ip4/127.0.0.1/tcp/5001", hypercube_addr="localhost:8880", private_key = None):
        self.blockchain_addr = blockchain_addr
        self.chain_id = chain_id
        self.ipfs_addr = ipfs_addr
        self.hypercube_addr = hypercube_addr
        self.private_key = private_key

        self.ipfs = ipfshttpclient.connect(ipfs_addr)
        self.w3 = Web3(Web3.HTTPProvider(blockchain_addr))
        
        if private_key is None:
            self.acct = self.w3.eth.accounts[0]
        else:
            self.acct = Account.from_key(private_key).address
        self.w3.eth.default_account = self.acct
        print("Using account", self.acct)

        install_solc('0.8.19')

    def compile_contract(self, sol_path):        
        compiled_sol = compile_files([sol_path], output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_sol.popitem()

        abi = contract_interface['abi']
        bytecode = contract_interface['bin']

        return abi, bytecode

    def deploy_factory(self, abi, bytecode, args={}):
        contract_bin = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract_bin.constructor(**args).transact({'from': self.acct})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi,
            bytecode=bytecode
        )

        print(f"Contract deployed to {tx_receipt.contractAddress}")

        return self.contract
    
    def create_car(self, brand, colour, img_path=None): #TODO test
        if img_path is not None:
            ipfs_img_addr = self.ipfs.add(img_path)['Hash']
        else:
            ipfs_img_addr = ""
        print(ipfs_img_addr)

        create_car_tx = self.contract.functions.createCar(brand, colour, ipfs_img_addr).transact({"from": self.acct})
        create_car_tx_receipt = self.web3.eth.wait_for_transaction_receipt(create_car_tx)
        receipt_car = self.web3.eth.get_transaction_receipt(create_car_tx)
        print(receipt_car)
        #TODO add deployed car on hypercube

    #TODO search cars on the hypercube by keyword(s)
    
    #TODO retrieve a specific car data from the blockchain

    #TODO use also IPFS for car images

    #TODO (optional) attach to an already deployed factory