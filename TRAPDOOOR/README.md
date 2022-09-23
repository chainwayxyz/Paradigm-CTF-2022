##  TRAPDOOOR
The challenge required the player to write a smart contract which would factorize a big random prime number.

Even though we didn't hope that it would work, we first tried to factorize the numbers. And as we expected, it didn't work since it's too computationally heavy for the EVM.

Then, we started looking out for possible exploits in the code, and everthing looked normal (except that maybe we could overflow the loggging stack and got our log to be the last one). However, one thing stood out: Forge. The testing framework was mentioned only in the TRAPDOOOR challenge, therefore we started suspecting the solution might have something to do with it.

As we looked through its documentation, we realized that Forge provided developers ways to interact with the operating system through Solidity -a powerful tool.

We can see from `chal.py` that FLAG is from the environment variable:
`FLAG = os.getenv("FLAG", "PCTF{placeholder}")`
So we started to search for a way to read the environment variable FLAG.

With the `envString` function in Forge, we could read environment variables and set the factorizer function outputs to chars from the environment variable. So we rolled up our sleeves and got into the hard work -which is changing which index of the environ. var. we will output and requerying the backend with the new contract bytecode.

In [`soln/`](soln/) you can see the forge script we used to read environment variables.
