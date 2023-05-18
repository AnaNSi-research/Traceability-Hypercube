import json
from web3 import Web3, HTTPProvider

blockchain_address = "http://localhost:8545"
chain_id = 1337

web3 = Web3(HTTPProvider(blockchain_address))
first_account = web3.eth.accounts[0]
private_key = "0x4d633117b6cc5572178c07ae35330570df896f1cfa91199309cc40d462349545"

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/CarFactory.json'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract_bytecode = contract_json['bytecode']

# Fetch deployed contract reference
car_factory = web3.eth.contract(bytecode=contract_bytecode, abi=contract_abi)

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

deployed_car_factory = web3.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)

for i in range(10):
    create_car_tx = deployed_car_factory.functions.createCar(i).transact({"from": web3.eth.accounts[i]})
    create_car_tx_receipt = web3.eth.wait_for_transaction_receipt(create_car_tx)
    receipt_car = web3.eth.get_transaction_receipt(create_car_tx)

cars = deployed_car_factory.functions.getCars().call()

print(len(cars))
