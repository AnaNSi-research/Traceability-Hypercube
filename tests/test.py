import json
from web3 import Web3, HTTPProvider

blockchain_address = "http://localhost:8545"
chain_id = 1337

web3 = Web3(HTTPProvider(blockchain_address))
first_account = web3.eth.accounts[0]
private_key = "0x4d633117b6cc5572178c07ae35330570df896f1cfa91199309cc40d462349545"

# Path to the compiled contract JSON file
car_factory_contract_path = 'build/contracts/CarFactory.json'
car_contract_path = 'build/contracts/Car.json'

with open(car_factory_contract_path) as file:
    car_factory_contract_json = json.load(file)  # load contract info as JSON
    car_factory_contract_abi = car_factory_contract_json['abi']  # fetch contract's abi - necessary to call its functions
    car_factory_contract_bytecode = car_factory_contract_json['bytecode']

# Fetch deployed contract reference
car_factory = web3.eth.contract(bytecode=car_factory_contract_bytecode, abi=car_factory_contract_abi)

contract_data = car_factory.constructor(web3.eth.accounts[1]).build_transaction(
    {
        'from': first_account
    }
)
tx_hash = web3.eth.send_transaction(contract_data)
print("Deploying Contract...")

# Wait for the transaction to be mined, and get transaction receipt
print("Waiting for Transaction to finish...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract Deployed(Car Factory) to {tx_receipt.contractAddress} \n")

deployed_car_factory = web3.eth.contract(address=tx_receipt.contractAddress, abi=car_factory_contract_abi)


create_car_tx = deployed_car_factory.functions.createCar("ferrari", "rosso").transact({"from": web3.eth.accounts[1]})
create_car_tx_receipt = web3.eth.wait_for_transaction_receipt(create_car_tx)
receipt_car = web3.eth.get_transaction_receipt(create_car_tx)

cars = deployed_car_factory.functions.getCars().call()


with open(car_contract_path) as file:
    car_contract_json = json.load(file)
    car_contract_abi = car_contract_json['abi']
    car_contract_bytecode = car_contract_json['bytecode']

first_car = web3.eth.contract(address=cars[0], abi=car_contract_abi)

colour = first_car.functions.getColour().call({"from": web3.eth.accounts[2]})
brand = first_car.functions.getBrand().call({"from": web3.eth.accounts[2]})

print(colour, brand)
