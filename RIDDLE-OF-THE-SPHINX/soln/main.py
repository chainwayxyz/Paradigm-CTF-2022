import asyncio

from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.networks import TESTNET, MAINNET
from starknet_py.net import AccountClient, KeyPair
from starknet_py.contract import Contract

# Local network
from starknet_py.net.models import StarknetChainId


async def main():
    local_network_client = GatewayClient(
        "", chain=StarknetChainId.TESTNET
    )
    priv_key = ""
    account_client = await AccountClient.create_account(local_network_client, priv_key)

    contract_address = ""
    contract = await Contract.from_address(contract_address, local_network_client)

    calls = [
        contract.functions["solve"].prepare(solution="man")
    ]

    res = await account_client.execute(calls=calls, max_fee=int(0))

    await account_client.wait_for_tx(res.transaction_hash)


asyncio.run(main())
