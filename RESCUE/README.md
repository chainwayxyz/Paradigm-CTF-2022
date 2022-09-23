## RESCUE Challenge

The challenge was to somehow bring down MasterChefHelper contract's WETH balance to 0.


The only function you could call in the contract was `swapTokenForPoolToken`. It does two things:
1.  Given a Uniswap pool and some amount of token X, swap token X for pool's underlying tokens.
2.  Add those tokens back to the pool and get pool tokens.

We started with inspecting provided pools. In the soln folder you can find the pools.py script where we printed out information about the pools.

There were 29 pools, 3 of which we deemed important -will come back to this part in a bit.

The token X I talked about above, came in and went out at exactly the same amount, since it was only swapped. We realized that only way the balance for a specific token could decrease was that the contract had to provide more to the pool than it had acquired by swapping. (See last line of the code below)

```
function swapTokenForPoolToken(uint256 poolId, address tokenIn, uint256 amountIn, uint256 minAmountOut) external {
    (address lpToken,,,) = masterchef.poolInfo(poolId);
    address tokenOut0 = UniswapV2PairLike(lpToken).token0();
    address tokenOut1 = UniswapV2PairLike(lpToken).token1();

    ERC20Like(tokenIn).approve(address(router), type(uint256).max);
    ERC20Like(tokenOut0).approve(address(router), type(uint256).max);
    ERC20Like(tokenOut1).approve(address(router), type(uint256).max);
    ERC20Like(tokenIn).transferFrom(msg.sender, address(this), amountIn);

    // swap for both tokens of the lp pool
    _swap(tokenIn, tokenOut0, amountIn / 2);
    _swap(tokenIn, tokenOut1, amountIn / 2);

    // add liquidity and give lp tokens to msg.sender
    _addLiquidity(tokenOut0, tokenOut1, minAmountOut); // the MasterChefHelper contract doesn't have control over the amounts here.
}
```

So the contract had to add WETH as liquidity. The problem is, you have to find a token that traded against WETH and some other token, which also traded against WETH.

This is where those 3 "important pools" come in handy. (Can be found in [`soln/important_pools.txt`](soln/important_pools.txt). Token "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599" (called ATTACK_TOKEN in the [`soln`](soln/soln.ipynb) textbook) trades against WETH and "0x5dbcF33D8c2E976c6b560249878e6F1491Bca25c" (called SIDE_TOKEN in the soln textbook)

So the solution is:
1.  Buy lots of WETH
2.  Buy some ATTACK_TOKEN
3.  **Drive up SIDE_TOKEN's price, so that when the contract adds liquidity it has to provide more WETH than it got by swapping** (when adding liquidity, you have to match the ratio in the pool)
4.  Call `swapTokenForPoolToken` against the 25th pool (SIDE_TOKEN - WETH pool) swapping ATTACK_TOKEN with the amount of player's entire balance.

In the [`soln/`](soln/) folder you can find the jupyther notebook we used to send neccessary transactions.
