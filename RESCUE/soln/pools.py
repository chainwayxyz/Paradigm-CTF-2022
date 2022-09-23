from web3 import Web3
import json
from eth_account import Account


uni_abi = json.load(open("unipair.json", "r"))
erc20_abi = json.load(open("erc20.json", "r"))
setup_abi = json.load(open("setup.json", "r"))

web3 = Web3(Web3.HTTPProvider(""))


setup_contract = web3.eth.contract(
    address=Web3.toChecksumAddress(""), abi=setup_abi
)


mc_addr = "0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd"
mc_contract = web3.eth.contract(
    address=Web3.toChecksumAddress(mc_addr), abi=json.load(open("masterchef.json", "r")))


mc_helper_addr = setup_contract.functions.mcHelper().call()
print(mc_helper_addr)


for i in range(100):
    lp_addr, x, y, z = mc_contract.functions.poolInfo(i).call()
    print(lp_addr)
    uni_pair_contract = web3.eth.contract(
        address=Web3.toChecksumAddress(lp_addr), abi=uni_abi
    )

    token0 = uni_pair_contract.functions.token0().call()
    token1 = uni_pair_contract.functions.token1().call()

    token0_contract = web3.eth.contract(
        address=Web3.toChecksumAddress(token0), abi=erc20_abi
    )
    token1_contract = web3.eth.contract(
        address=Web3.toChecksumAddress(token1), abi=erc20_abi
    )

    print(i, token0, token1, token0_contract.functions.balanceOf(
        lp_addr).call(), token1_contract.functions.balanceOf(lp_addr).call())
