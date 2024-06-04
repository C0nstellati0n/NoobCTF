# Staker

算blockchain的入门题，但还是耗了我很长的时间。问就是和solidity不熟。来看代码：
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {Token} from "./Token.sol";
import {LpToken} from "./LpToken.sol";
import {StakingManager} from "./StakingManager.sol";

contract Setup {
    StakingManager public stakingManager;
    Token public token;

    constructor() payable {
        token = new Token();
        stakingManager = new StakingManager(address(token));

        token.transfer(address(stakingManager), 86400 * 1e18);

        token.approve(address(stakingManager), 100000 * 1e18);
        stakingManager.stake(100000 * 1e18);
    }

    function withdraw() external {
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }

    function isSolved() public view returns (bool) {
        return token.balanceOf(address(this)) >= 10 * 1e18;
    }
}
```
目标是让Setup合约的Token balance大于等于`10 * 1e18`。看看Token合约：
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    constructor() ERC20("Token", "TKN") {
        _mint(msg.sender, 186401 * 1e18);
    }
}
```
初始会给new这个合约的地址mint `186401 * 1e18`个token。回去看setup的逻辑，setup给stakingManager转了`86400 * 1e18`，又往里stake了`100000 * 1e18`，于是自己还剩1e18个token
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {LpToken} from "./LpToken.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract StakingManager {
    uint256 constant REWARD_PER_SECOND = 1e18;

    IERC20 public immutable TOKEN;
    LpToken public immutable LPTOKEN;

    uint256 lastUpdateTimestamp;
    uint256 rewardPerToken;

    struct UserInfo {
        uint256 staked;
        uint256 debt;
    }

    mapping(address => UserInfo) public userInfo;

    constructor(address token) {
        TOKEN = IERC20(token);
        LPTOKEN = new LpToken();
    }

    function update() internal {
        if (lastUpdateTimestamp == 0) {
            lastUpdateTimestamp = block.timestamp;
            return;
        }

        uint256 totalStaked = LPTOKEN.totalSupply();
        if (totalStaked > 0 && lastUpdateTimestamp != block.timestamp) {
            rewardPerToken = (block.timestamp - lastUpdateTimestamp) * REWARD_PER_SECOND * 1e18 / totalStaked;
            lastUpdateTimestamp = block.timestamp;
        }
    }

    function stake(uint256 amount) external {
        update();

        UserInfo storage user = userInfo[msg.sender];

        user.staked += amount;
        user.debt += (amount * rewardPerToken) / 1e18;

        LPTOKEN.mint(msg.sender, amount);
        TOKEN.transferFrom(msg.sender, address(this), amount);
    }

    function unstakeAll() external {
        update();

        UserInfo storage user = userInfo[msg.sender];

        uint256 staked = user.staked;
        uint256 reward = (staked * rewardPerToken / 1e18) - user.debt;
        user.staked = 0;
        user.debt = 0;

        LPTOKEN.burnFrom(msg.sender, LPTOKEN.balanceOf(msg.sender));
        TOKEN.transfer(msg.sender, staked + reward);
    }
}
```
查看stake和unstakeAll的逻辑，看起来只要调用这两个函数的间隔时间越长，reward就越多。但我试了很多次才发现，光靠这样赚token根本不够。题目instance只会维持30分钟，无论如何我们都没法拿到`10*1e18`个token。重点其实是LpToken：
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LpToken is ERC20 {
    address immutable minter;

    constructor() ERC20("LP Token", "LP") {
        minter = msg.sender;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == minter, "only minter");
        _mint(to, amount);
    }

    function burnFrom(address from, uint256 amount) external {
        _burn(from, amount);
    }
}
```
想要在短时间内获得很多Token就需要提高rewardPerToken的值，而这个值与totalStaked息息相关。totalStaked就是LpToken的totalsuppy，我们可以私底下使用burnFrom函数削减totalsuppy的值。光burn掉自己的LpToken可能不够快，可以把Setup合约的LpToken也burn掉一部分（但是不要太多，数字太大的话数字操作溢出会导致函数调用失败，正好超过isSolve要求的值即可）。用这个方法就能拿到比本金多很多的token，全部转给Setup合约即可

不需要攻击合约，自己在remix里点函数即可。这里顺便说说踩过的坑

1. 无法控制Setup合约自己去调用unstakeAll。挺无语的一个错误。我想当然地认为，msg.sender是调用函数的合约或者account，那我写个攻击合约，里面调用`setup.stakingManager().unstakeAll()`（注意stakingManager虽然是个字段，但是要加括号，因为是个address）不就能把token拿回来了吗？答案是否定的。这样调用的话，msg.sender是攻击合约而不是setup合约。很明显，msg.sender应该是最外层的调用者
2. 做题的时候，我发现没法写个攻击合约，内部调用setup合约withdraw函数。但是自己在remix里拿自己账号的名义去调用withdraw函数就行。目前还没搞清楚为什么，可能是我攻击合约里忘记实现什么接收token的函数了？
3. 卡在自己账号没法调用stake很久。后来发现需要先调用Token里的approve函数（这个函数是从ERC20.sol继承下来）批准StakingManager使用amount个token才行。毕竟stake函数内部会将那么多个token转给自己，不approve的话它没法转。看setup合约里的操作也能看出来
4. 为什么我能burn掉不属于我的setup合约的LpToken？因为LpToken里实现burnFrom时没有检查burn的LpToken必须是msg.sender的，是这题的漏洞。说实话，就不应该让其他合约调用这个函数，应该也在开头加一句`require(msg.sender == minter, "only minter");`