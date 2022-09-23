## SOURCECODE Challenge

The challenge was to create a "quine", a computer program which takes no input and produces a copy of its own source code as its only output.

Normally this wouldn't be such a hard challenge, however, certain opcodes were prohibited.

```
function safe(bytes memory code) private pure returns (bool) {
    uint i = 0;
    while (i < code.length) {
        uint8 op = uint8(code[i]);

        if (op >= 0x30 && op <= 0x48) {
            return false;
        }

        if (
                op == 0x54 // SLOAD
            || op == 0x55 // SSTORE
            || op == 0xF0 // CREATE
            || op == 0xF1 // CALL
            || op == 0xF2 // CALLCODE
            || op == 0xF4 // DELEGATECALL
            || op == 0xF5 // CREATE2
            || op == 0xFA // STATICCALL
            || op == 0xFF // SELFDESTRUCT
        ) return false;
        
        if (op >= 0x60 && op < 0x80) i += (op - 0x60) + 1;
        
        i++;
    }
    
    return true;
}
```

From google we found the following [quine example in evm bytecode](https://gist.github.com/karmacoma-eth/220b58b7cd32d649fa1a15e70b6d8bff). Unfortunately this "quine" used the 0x34 opcode which was prohibited.

So we modified the program like this:
```
push32 0x80607f6000536001526021526041600013000000000000000000000000000000
                    # --- stack ---
dup1                # code code

# (7f is push32)
push1 Ox7f          # 7f code code
push1 Ox00          # offset=0 7f code code
mstore8             # code code
                    # mem = [7f]
push1 1             # 1 code code
mstore              # mem = [7fcode]

push1 33            # 33 code
mstore              # mem = [7fcodecode]


push1 65            # size
push1 0             # offset=0 size
return              # out = [7fcodecode]
```

In [`soln/`](soln/) you can find the script and the bytecode we used to solve the challenge.