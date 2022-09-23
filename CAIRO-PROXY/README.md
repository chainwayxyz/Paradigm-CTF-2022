## CAIRO-PROXY Challenge

This challenge required the player to set its token balance to an arbitrary number. (49999999999999995805696)

For a long time, we thought the solution to the challenge was to acquire the ownership of the proxy contract or to somehow write to its state.

After our numerous attempts to exploit the proxy contract, we realized that the attack vector was in the ERC20 implementation.

```
@external
func burn{
    syscall_ptr : felt*,
    pedersen_ptr : HashBuiltin*,
    range_check_ptr,
    }(account : felt, amount : Uint256):
    alloc_locals

    uint256_check(amount)
    let (account_balance) = balances.read(account=account)

    let (enough_balance) = uint256_le(account_balance, amount)
    assert enough_balance = TRUE

    let (new_account_balance) = uint256_sub(account_balance, amount)

    balances.write(account=account, value=new_account_balance)

    return()
end
```

Inside the burn function, we found three problems:
1.  The amount check is entirely wrong, it is expected that the acccount balance is smaller than the amount to be burned - should be the other way around.
2.  No underflow check when substracting.
3.  Anybody can burn anyone's tokens (unrelated to our solution)

Starting token balance of the player is 0. So the solution is to burn exactly `2**256 - 49999999999999995805696` tokens and cause underflow on the token balance.

Again, interacting with starknet was a mini-challenge: Since the backend used a different way calculate the player account address, we had to go look at the sandbox repo and use the same way in our solution.

In [`soln/`](soln/), you can find the python script we used to send the burn transaction.
