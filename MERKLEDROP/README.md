## MERKLEDROP Challenge

This task looks like a simple whitelist-airdrop code. There is a merkle tree, and a user can claim the amount whitelisted.

There are three files:
- `MerkleProof.sol` - It has a simple function `verify()` which verifies the merkle path from leaf to root. Nearly the same file can be found here on openzeppelin contracts: https://github.com/MerkleBlue/tokenmint/blob/master/contracts/open-zeppelin-contracts/cryptography/MerkleProof.sol
- `MerkleDistributor.sol` - This is the contract which has access to tokens, and users claim their airdrop. We found nearly the same contract on the internet: https://gitlab.infothinker.com/airdrop/airdrop/-/blob/main/AirdropTokenDistributor.sol
But there is a catch. In that version, the amount is uint256, but in the CTF, the amount is uint96. That is suspicious and I will come back to it.

- `Setup.sol` - The setup contract is simple, it creates a new ERC20-like token and a new MerkleDistributor with the newly created ERC20 tokens and the root of the merkle tree. Also, there is an isSolved function which has two conditions to accept the solution. The first condition is that there should not be any balance in the MerkleDistributor contract, and the second condition is that there should be at least one account who has not claimed their amount. But when we add up all the amounts in the merkle tree, it is exactly the total amount in the contract (which is 75000 * 10^18).

- `tree.json` - It has the values of merkle trees. All 64 leaves and their proofs to the root.


### Why the amount is uint96
Let’s think about it, maybe we can create some proof not from the leaf but from some parents of the leaves, is that even possible?

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/4f8af2dceb0fbc36cb32eb2cc14f80c340b9022e/test/utils/cryptography/MerkleProof.test.js#L28

Here it says,
>For demonstration, it is also possible to create valid proofs for certain 64-byte values *not* in elements:

So let's look if the encoded values can be 64-byte values.

`keccak256(abi.encodePacked(index, account, amount));`

- the index is uint256: 32 bytes
- the account is address: 20 bytes
- the amount is uint96: 12 bytes

So 32 + 20 + 12 = 64.

##  That's the reason why the amount is uint96 not uint256!

So we know that merkle leaves are a hash of some concatenated 64-byte values. So how can we hack this merkle tree?

We know that every node in that tree is a hash of two 32-byte values concatenated.

So if we can somehow find two siblings in the tree, and concatenate them, giving the first 32 bytes as the index, the next 20 bytes as the account, and the last 12 bytes as the amount. And then we can create a valid proof.

We can create a valid proof because there is not any check of the length of the proof as well as there is not any check of accounts and index being less than 64.

### How we could find a hash that makes a total of 75000 * 10^18.

```json
"0x8a85e6D0d2d6b8cBCb27E724F14A97AeB7cC1f5e": {
    "index": 37,
    "amount": "0x5dacf28c4e17721edb",
    "proof": [
        "0xd48451c19959e2d9bd4e620fbe88aa5f6f7ea72a00000f40f0c122ae08d2207b",
        "0x8920c10a5317ecff2d0de2150d5d18f01cb53a377f4c29a9656785a22a680d1d",
        "0xc999b0a9763c737361256ccc81801b6f759e725e115e4a10aa07e63d27033fde",
        "0x842f0da95edb7b8dca299f71c33d4e4ecbb37c2301220f6e17eef76c5f386813",
        "0x0e3089bffdef8d325761bd4711d7c59b18553f14d84116aecb9098bba3c0a20c",
        "0x5271d2d8f9a3cc8d6fd02bfb11720e1c518a3bb08e7110d6bf7558764a8da1c5"
    ]
},
```

As we can see the first element of proof array in “0xd48451c19959e2d9bd4e620fbe88aa5f6f7ea72a00000f40f0c122ae08d2207b” ends with 00000f40f0c122ae08d2207b which is 72033437049132565012603 in decimal. And this is the only hash that ends with a value less than 75000 * 10^18. So we are sure that we will use this as a fake proof.

But there is another challenge where we should make the balance 0. Underflow is not possible since it will revert. So to make the balance 0, we need to claim an amount exactly to 2966562950867434987397.

```json
"0x249934e4C5b838F920883a9f3ceC255C0aB3f827": {
    "index": 8,
    "amount": "0xa0d154c64a300ddf85",
    "proof": [
        "0xe10102068cab128ad732ed1a8f53922f78f0acdca6aa82a072e02a77d343be00",
        "0xd779d1890bba630ee282997e511c09575fae6af79d88ae89a7a850a3eb2876b3",
        "0x46b46a28fab615ab202ace89e215576e28ed0ee55f5f6b5e36d7ce9b0d1feda2",
        "0xabde46c0e277501c050793f072f0759904f6b2b8e94023efb7fc9112f366374a",
        "0x0e3089bffdef8d325761bd4711d7c59b18553f14d84116aecb9098bba3c0a20c",
        "0x5271d2d8f9a3cc8d6fd02bfb11720e1c518a3bb08e7110d6bf7558764a8da1c5"
    ]
},
```
 The amount given in this index is 0xa0d154c64a300ddf85 which is exactly the amount we are searching for. So by claiming these two proofs we can fulfill the two conditions to solve the challenge.
