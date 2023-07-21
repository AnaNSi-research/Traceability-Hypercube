from solcx import compile_files


def compile_contract(source_file, contract_name):
    compiled = compile_files([source_file], output_values=['abi', 'bin'])[f"{source_file}:{contract_name}"]
    abi, bytecode = compiled['abi'], compiled['bin']

    return abi, bytecode

def deploy_contract(w3, account, abi, bytecode, *args):
    contract_bin = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract_bin.constructor(*args).transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt

    # self.attach_contract(abi, bytecode, tx_receipt.contractAddress)

    # print(f"Contract deployed to {tx_receipt.contractAddress}")
    # print(f"Gas used: {tx_receipt.gasUsed}")

    # return self.contract