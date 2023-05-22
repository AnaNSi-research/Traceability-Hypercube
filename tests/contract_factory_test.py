import asyncio
import json
from web3 import Web3, HTTPProvider

blockchain_address = "http://localhost:8545"
chain_id = 1337

web3 = Web3(HTTPProvider(blockchain_address))
first_account = web3.eth.accounts[0]

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

def handle_event(event):
    event_json = json.loads(Web3.to_json(event))
    car_addr = event_json["args"]["newCarAddress"]

    print(deployed_car_factory.functions.getCarInfo(car_addr).call())

async def log_loop(event_filter, poll_interval):
    while True:
        for CarCreated in event_filter.get_new_entries():
            handle_event(CarCreated)
        await asyncio.sleep(poll_interval)

def main():
    event_filter = deployed_car_factory.events.CarCreated.create_filter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

if __name__ == "__main__":
    main()
