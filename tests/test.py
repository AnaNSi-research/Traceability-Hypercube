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
contract = web3.eth.contract(address=first_account, abi=contract_abi, bytecode=contract_bytecode)

# Submit the transaction deplays the contract
transaction = web3.eth.send_transaction({
    "from": first_account
})

print("Deploying Contract!")

# Wait for the transaction to be mined, and get transaction receipt
print("Waiting for Transaction to finish...")
tx_receipt = web3.eth.wait_for_transaction_receipt(transaction)
print(f"Done! Contract Deployed to {tx_receipt.contractAddress} \n")