# Diamond Heist

[题目](https://github.com/kangsangsoo/CTF-Writeups/blob/main/diamond_heist_contracts.zip)

我真的看不懂这道题的[wp](https://aaronesau.com/blog/post/12)，加上这篇[wp](https://gss1.tistory.com/entry/HackTM-CTF-Quals-2023-smart-contractDragon-Slayer-Diamond-Heist)也不行。勉强水一篇吧，要不然白费了我几个小时的工夫。

还是来看Setup.sol，一切的起点。

```js
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./VaultFactory.sol";
import "./Vault.sol";
import "./Diamond.sol";
import "./SaltyPretzel.sol";

contract Setup {

    uint constant public DIAMONDS = 100;
    uint constant public SALTY_PRETZELS = 100 ether;
    bool claimed;

    VaultFactory public vaultFactory;
    Vault public vault;
    Diamond public diamond;
    SaltyPretzel public saltyPretzel;

    constructor () {
        vaultFactory = new VaultFactory(); //VaultFactory.sol文件就不看了，总之是用于创建一个vault
        vault = vaultFactory.createVault(keccak256("The tea in Nepal is very hot."));
        diamond = new Diamond(DIAMONDS); //Diamond.sol也不看，是一种ERC20货币，这里初始化100个
        saltyPretzel = new SaltyPretzel(); //一个governance contract
        vault.initialize(address(diamond), address(saltyPretzel));
        diamond.transfer(address(vault), DIAMONDS); //把diamond全部转到vault里
    }

    function claim() external {
        require(!claimed);
        claimed = true;
        saltyPretzel.mint(msg.sender, SALTY_PRETZELS); //转给我们100个SALTY_PRETZELS
    }

    function isSolved() external view returns (bool) {
        return diamond.balanceOf(address(this)) == DIAMONDS; //要求我们获得100个diamond
    }
}
```

这里提到的[governance contract](https://ethereum.org/en/governance/)我一直云里雾里的，这里给的链接是指向Ethereum整体的管理方式，并没有明确指出什么是governance contract。我继续搜，还真搜到了[一个](https://www.rareskills.io/post/governance-contract-solidity)，正好是一天前发出来的。也有类似的名词是governor contract，两者基本都是管理提议，投票等事情的合约。我也在OpenZeppelin[源码库](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/governance)找到了管理系统相关的代码，不过下面审计SaltyPretzel代码时没看见它继承里面相关的合约。难不成是间接继承？那这样我真找不出来了。所以我认为这里的governance contract有可能是一个概念，毕竟里面确实有很多跟刚才提到的特征有关的代码。

目标是获得100个钻石。这方圆百里只有vault里有100个钻石啊，去看看。

```js
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "./openzeppelin-contracts/interfaces/IERC20.sol";
import "./openzeppelin-contracts/interfaces/IERC3156FlashBorrower.sol";
import "./openzeppelin-contracts-upgradeable/proxy/utils/Initializable.sol";
import "./openzeppelin-contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "./openzeppelin-contracts-upgradeable/access/OwnableUpgradeable.sol";

import "./Diamond.sol";
import "./Burner.sol";
import "./SaltyPretzel.sol";

contract Vault is Initializable, UUPSUpgradeable, OwnableUpgradeable {

    uint constant public AUTHORITY_THRESHOLD = 10_000 ether;

    Diamond diamond;
    SaltyPretzel saltyPretzel;

    function initialize(address diamond_, address saltyPretzel_) public initializer {
        __Ownable_init();
        diamond = Diamond(diamond_);
        saltyPretzel = SaltyPretzel(saltyPretzel_);
    }

    function governanceCall(bytes calldata data) external {
        require(msg.sender == owner() || saltyPretzel.getCurrentVotes(msg.sender) >= AUTHORITY_THRESHOLD); //前提是函数调用者是vault拥有者或者函数调用者在saltyPretzel那里获取足够做的票数
        (bool success,) = address(this).call(data); //能够以vault的身份调用任意函数
        require(success);
    }

    function flashloan(address token, uint amount, address receiver) external {
        uint balanceBefore = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(receiver, amount);
        IERC3156FlashBorrower(receiver).onFlashLoan(msg.sender, token, amount, 0, "");
        uint balanceAfter = IERC20(token).balanceOf(address(this));
        require(balanceBefore == balanceAfter);
    }

    function burn(address token, uint amount) external {
        require(msg.sender == owner() || msg.sender == address(this));
        Burner burner = new Burner();
        IERC20(token).transfer(address(burner), amount);
        burner.destruct();
    }
    
    function _authorizeUpgrade(address) internal override view { //如果我们满足函数里的两个require，就能upgrade这个vault
        require(msg.sender == owner() || msg.sender == address(this)); //要求函数调用者等于该金库的拥有者或者就是金库本身
        require(IERC20(diamond).balanceOf(address(this)) == 0); //要求当前金库的钻石数量为0
    }
}
```

[可升级合约](https://docs.openzeppelin.com/learn/upgrading-smart-contracts)又是一个新概念。粗略看了一下文档，感觉可升级合约就是在保持合约当前状态的情况下改变合约内部的代码。改代码？如果我们把vault做个升级，里面的代码改成转账钻石的函数，不就能获取那100个钻石了吗？然而看那两个条件，有大问题：第一，我们怎么伪造身份？第二，我们的目标本来就是靠升级掏空金库里的钻石，这里又要求升级前金库就是空的，隔这玩呢？算了，还是要想办法解决问题。

governanceCall函数有点意思，满足第一个条件。这里就牵扯到一个据说是很经典的漏洞:[sushi-swap double spending bug](https://medium.com/bulldax-finance/sushiswap-delegation-double-spending-bug-5adcc7b3830f)。大概是说在转账中使用delegate()函数可以无限增加vote。我们去看看SaltyPretzel.sol里有没有类似的delegate()函数。

```js
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./openzeppelin-contracts/access/Ownable.sol";
import "./openzeppelin-contracts/token/ERC20/ERC20.sol";

contract SaltyPretzel is ERC20("SaltyPretzel", "SP"), Ownable {
    function mint(address _to, uint256 _amount) public onlyOwner {
        _mint(_to, _amount);
        _moveDelegates(address(0), _delegates[_to], _amount);
    }

    mapping (address => address) internal _delegates;

    struct Checkpoint {
        uint32 fromBlock;
        uint256 votes;
    }

    mapping (address => mapping (uint32 => Checkpoint)) public checkpoints;
    mapping (address => uint32) public numCheckpoints;

    bytes32 public constant DOMAIN_TYPEHASH = keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)");
    bytes32 public constant DELEGATION_TYPEHASH = keccak256("Delegation(address delegatee,uint256 nonce,uint256 expiry)");

    mapping (address => uint) public nonces;

    event DelegateChanged(address indexed delegator, address indexed fromDelegate, address indexed toDelegate); //solidity里的事件，见https://www.geeksforgeeks.org/what-are-events-in-solidity/
    event DelegateVotesChanged(address indexed delegate, uint previousBalance, uint newBalance);

    function delegates(address delegator)
        external
        view
        returns (address)
    {
        return _delegates[delegator];
    }

    function delegate(address delegatee) external {
        return _delegate(msg.sender, delegatee);
    }

    function delegateBySig(
        address delegatee,
        uint nonce,
        uint expiry,
        uint8 v,
        bytes32 r,
        bytes32 s
    )
        external
    {
        bytes32 domainSeparator = keccak256(
            abi.encode(
                DOMAIN_TYPEHASH,
                keccak256(bytes(name())),
                getChainId(),
                address(this)
            )
        );

        bytes32 structHash = keccak256(
            abi.encode(
                DELEGATION_TYPEHASH,
                delegatee,
                nonce,
                expiry
            )
        );

        bytes32 digest = keccak256(
            abi.encodePacked(
                "\x19\x01",
                domainSeparator,
                structHash
            )
        );

        address signatory = ecrecover(digest, v, r, s);
        require(signatory != address(0));
        require(nonce == nonces[signatory]++);
        require(block.timestamp <= expiry);
        return _delegate(signatory, delegatee);
    }

    function getCurrentVotes(address account)
        external
        view
        returns (uint256)
    {
        uint32 nCheckpoints = numCheckpoints[account];
        return nCheckpoints > 0 ? checkpoints[account][nCheckpoints - 1].votes : 0;
    }

    function getPriorVotes(address account, uint blockNumber)
        external
        view
        returns (uint256)
    {
        require(blockNumber < block.number);

        uint32 nCheckpoints = numCheckpoints[account];
        if (nCheckpoints == 0) {
            return 0;
        }

        if (checkpoints[account][nCheckpoints - 1].fromBlock <= blockNumber) {
            return checkpoints[account][nCheckpoints - 1].votes;
        }

        if (checkpoints[account][0].fromBlock > blockNumber) {
            return 0;
        }

        uint32 lower = 0;
        uint32 upper = nCheckpoints - 1;
        while (upper > lower) {
            uint32 center = upper - (upper - lower) / 2;
            Checkpoint memory cp = checkpoints[account][center];
            if (cp.fromBlock == blockNumber) {
                return cp.votes;
            } else if (cp.fromBlock < blockNumber) {
                lower = center;
            } else {
                upper = center - 1;
            }
        }
        return checkpoints[account][lower].votes;
    }

    function _delegate(address delegator, address delegatee)
        internal
    {
        address currentDelegate = _delegates[delegator];
        uint256 delegatorBalance = balanceOf(delegator);
        _delegates[delegator] = delegatee;

        emit DelegateChanged(delegator, currentDelegate, delegatee); //触发事件的关键字，https://aniketengg.medium.com/emit-keyword-in-solidity-242a679b0e1a

        _moveDelegates(currentDelegate, delegatee, delegatorBalance);
    }

    function _moveDelegates(address srcRep, address dstRep, uint256 amount) internal {
        if (srcRep != dstRep && amount > 0) {
            if (srcRep != address(0)) {
                uint32 srcRepNum = numCheckpoints[srcRep];
                uint256 srcRepOld = srcRepNum > 0 ? checkpoints[srcRep][srcRepNum - 1].votes : 0;
                uint256 srcRepNew = srcRepOld - amount;
                _writeCheckpoint(srcRep, srcRepNum, srcRepOld, srcRepNew);
            }

            if (dstRep != address(0)) {
                uint32 dstRepNum = numCheckpoints[dstRep];
                uint256 dstRepOld = dstRepNum > 0 ? checkpoints[dstRep][dstRepNum - 1].votes : 0;
                uint256 dstRepNew = dstRepOld + amount;
                _writeCheckpoint(dstRep, dstRepNum, dstRepOld, dstRepNew);
            }
        }
    }

    function _writeCheckpoint(
        address delegatee,
        uint32 nCheckpoints,
        uint256 oldVotes,
        uint256 newVotes
    )
        internal
    {
        if (nCheckpoints > 0 && checkpoints[delegatee][nCheckpoints - 1].fromBlock == uint32(block.number)) {
            checkpoints[delegatee][nCheckpoints - 1].votes = newVotes;
        } else {
            checkpoints[delegatee][nCheckpoints] = Checkpoint(uint32(block.number), newVotes);
            numCheckpoints[delegatee] = nCheckpoints + 1;
        }

        emit DelegateVotesChanged(delegatee, oldVotes, newVotes);
    }

    function getChainId() internal view returns (uint) {
        uint256 chainId;
        assembly { chainId := chainid() }
        return chainId;
    }
}
```

发现确实有啊，还是一套有点复杂的机制。不过我们只需要关注_delegate和其相关的函数就好了。这里先给出如何将某个地址的SaltyPretzel数量翻倍。

1. 把addrA全部的SaltyPretzel都转给addrB
2. 调用_delegate(addrB,addrA)
3. 把addrB全部的SaltyPretzel转回addrA

现在addrA就有双倍的SaltyPretzel了。为啥？照着步骤演练一遍就明白了。首先，SaltyPretzel合约通过getCurrentVotes函数获取某个地址的SaltyPretzel数量（似乎也是vote）：

```js
    function getCurrentVotes(address account)
        external
        view
        returns (uint256)
    {
        //mapping (address => mapping (uint32 => Checkpoint)) public checkpoints;
        //mapping (address => uint32) public numCheckpoints;
        uint32 nCheckpoints = numCheckpoints[account];
        return nCheckpoints > 0 ? checkpoints[account][nCheckpoints - 1].votes : 0;
    }
```

发现内部是根据checkpoints这个数组获取votes数量的。查看相关定义，就是一个mapping。接下来调用第一步，addrA转给addrB，会调用这个函数：

```js
function mint(address _to, uint256 _amount) public onlyOwner {
        _mint(_to, _amount);
        _moveDelegates(address(0), _delegates[_to], _amount);
    }
```

_mint是框架里的肯定没问题，但是这个_moveDelegates可不是，它会干啥？

```js
function _moveDelegates(address srcRep, address dstRep, uint256 amount) internal {
        if (srcRep != dstRep && amount > 0) {
            if (srcRep != address(0)) {
                uint32 srcRepNum = numCheckpoints[srcRep];
                uint256 srcRepOld = srcRepNum > 0 ? checkpoints[srcRep][srcRepNum - 1].votes : 0;
                uint256 srcRepNew = srcRepOld - amount;
                _writeCheckpoint(srcRep, srcRepNum, srcRepOld, srcRepNew);
            }

            if (dstRep != address(0)) {
                uint32 dstRepNum = numCheckpoints[dstRep];
                uint256 dstRepOld = dstRepNum > 0 ? checkpoints[dstRep][dstRepNum - 1].votes : 0;
                uint256 dstRepNew = dstRepOld + amount;
                _writeCheckpoint(dstRep, dstRepNum, dstRepOld, dstRepNew);
            }
        }
    }
```

此处的srcRep是address(0)，于是只会进入`if (dstRep != address(0))`这个if语句。dstRepNum是dstRep的Checkpoint数量，后续根据此取出dstRepOld（原本的vote数）以及算出dstRepNew（加上amount后的vote数）。进入_writeCheckpoint函数。

```js
function _writeCheckpoint(
        address delegatee,
        uint32 nCheckpoints, //最开始mint时是0
        uint256 oldVotes,
        uint256 newVotes
    )
        internal
    {
        if (nCheckpoints > 0 && checkpoints[delegatee][nCheckpoints - 1].fromBlock == uint32(block.number)) {
            checkpoints[delegatee][nCheckpoints - 1].votes = newVotes;
        } else {//故最开始不会进入上面的if，进下面的else
            checkpoints[delegatee][nCheckpoints] = Checkpoint(uint32(block.number), newVotes); //改动delegatee的vote数为转过来的vote
            numCheckpoints[delegatee] = nCheckpoints + 1;
        }

        emit DelegateVotesChanged(delegatee, oldVotes, newVotes); //调用事件，这里似乎没什么用
    }
```

看来第一步过后，addrB在SaltyPretzel的vote数增加了，数量为addrA给addrB的数量；同时addrB也有了同等数量的SaltyPretzel这种ERC20货币。开始第二步，重复的代码就不放了，放个_delegate。

```js
function _delegate(address delegator, address delegatee)
        internal
    {
        address currentDelegate = _delegates[delegator]; //_delegates是address到address的映射，这一步时是初始值，address(0)，见https://ethereum.stackexchange.com/questions/40559/what-are-the-initial-zero-values-for-different-data-types-in-solidity
        uint256 delegatorBalance = balanceOf(delegator); //获取delegator的SaltyPretzel ERC20货币数量
        _delegates[delegator] = delegatee; //写入映射

        emit DelegateChanged(delegator, currentDelegate, delegatee); //触发事件的关键字，https://aniketengg.medium.com/emit-keyword-in-solidity-242a679b0e1a

        _moveDelegates(currentDelegate, delegatee, delegatorBalance); //因为currentDelegate是address(0)，仍然只会进入if (dstRep != address(0))这个if语句
    }
```

结果我们发现某种意义上等于又mint了一次，addrA的vote数回来了，但是ERC20货币没有改动。意味着我们第三步addrB转回addrA ERC20的操作是合法的，addrA的vote数又增加了。addrA获得了初始SaltyPretzel ERC20货币两倍数量的vote。那接下来就很简单了，我们重复这三步，每次都换个addrB地址，不断增加addrA的vote数，到最后一定是有足够的vote调用Vault的governanceCall函数的。

最后一个问题，怎么保证vault里没钻石？答案是用vault里的[flashloan](https://eips.ethereum.org/EIPS/eip-3156)函数（flashloan直译是闪借，调用这个函数借用货币后，要在函数结束前把钱还回来）。

```js
function flashloan(address token, uint amount, address receiver) external {
        uint balanceBefore = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(receiver, amount);
        IERC3156FlashBorrower(receiver).onFlashLoan(msg.sender, token, amount, 0, "");
        uint balanceAfter = IERC20(token).balanceOf(address(this));
        require(balanceBefore == balanceAfter);
    }
```

根据官方文档，借钱方（receiver）必须实现onFlashLoan回调函数。那我们在白嫖到足够的vote后调用flashloan函数，内部调用governanceCall后把钻石还回来，不就完美解决开始提到的两个问题了吗？脚本在开始的两个wp里，终于写完了。

## Flag
> HackTM{m1ss10n_n0t_th4t_1mmut4ble_58fb67c04fd7fedc}