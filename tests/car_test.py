from web3 import Web3, HTTPProvider
import json

car_factory_contract_path = 'build/contracts/CarFactory.json'

with open(car_factory_contract_path) as file:
    car_factory_contract_json = json.load(file)  # load contract info as JSON
    car_factory_contract_abi = car_factory_contract_json['abi']  # fetch contract's abi - necessary to call its functions
    car_factory_contract_bytecode = car_factory_contract_json['bytecode']


blockchain_address = "http://localhost:8545"
chain_id = 1337

web3 = Web3(HTTPProvider(blockchain_address))

address = "0x792c2a0EBD62A74Bd02F51bbA4e6233bB58D45b2"

deployed_car_factory = web3.eth.contract(address=address, abi=car_factory_contract_abi, bytecode=car_factory_contract_bytecode)
create_car_tx = deployed_car_factory.functions.createCar("ferrari", "rosso").transact({"from": web3.eth.accounts[1]})
create_car_tx_receipt = web3.eth.wait_for_transaction_receipt(create_car_tx)
receipt_car = web3.eth.get_transaction_receipt(create_car_tx)