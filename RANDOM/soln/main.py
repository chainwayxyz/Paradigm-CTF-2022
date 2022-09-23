from web3 import Web3
from eth_account import Account
import json


web3 = Web3(Web3.HTTPProvider(""))


private_key = ""
ACC_ADDRESS = Account.from_key(private_key)


setup_addr = ""
setup_abi = json.load(open("abi.json", "r"))
setup_contract = web3.eth.contract(
    address=Web3.toChecksumAddress(setup_addr), abi=setup_abi)


contract_address = setup_contract.functions.random().call()
abi = json.load(open("rand.json", "r"))


contract = web3.eth.contract(
    address=Web3.toChecksumAddress(contract_address), abi=abi)


nonce = web3.eth.get_transaction_count(ACC_ADDRESS)
print("Nonce:", nonce)
transaction = contract.functions.solve(
    4
).buildTransaction({
    "value": 0,
    'nonce': nonce,
    'maxFeePerGas': 0,
    'maxPriorityFeePerGas': 0,
    'from': ACC_ADDRESS
}
)


signed_transaction = web3.eth.account.sign_transaction(
    transaction, private_key=private_key)
web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
