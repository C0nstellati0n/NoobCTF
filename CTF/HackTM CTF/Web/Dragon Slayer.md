# Dragon Slayer

[题目](https://github.com/kangsangsoo/CTF-Writeups/blob/main/dragon_slayer_contracts.zip)

我把智能合约题也归到web里了，web3怎么不算web呢ʕ •ᴥ•ʔ？当然我对智能合约一窍不通，所以此为[wp](https://www.youtube.com/watch?v=poqu6STdkOE)的笔记。

首先来看看Setup.sol(markdown好像不支持solidity这门语言的高亮）。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./Knight.sol";

//contract相当于class
contract Setup {
    Knight public knight;

    bool public claimed;

    constructor() {
        //创建一个Knigh实例
        knight = new Knight();
        //装备id为1和2的武器
        knight.equipItem(1);
        knight.equipItem(2);
    }
    //external关键字仅外部访问（在内部也只能用外部访问方式访问）
    //等我们连接上挑战后，在我们自己的合约里（也就是外部，external）调用该函数即为开始挑战
    function claim() external {
        //https://codedamn.com/news/solidity/what-is-require-in-solidity 有详细解释，第一个参数是要检查的条件，只有条件为True才能继续往下执行，否则报错。第二个参数可选，是条件为False时的报错语句（有点像自定义错误版本的assert？）
        require(!claimed, "ALREADY_CLAIMED");
        claimed = true;
        //https://docs.openzeppelin.com/contracts/2.x/api/ownership ，将所有权转移到参数msg.sender，是Ownable的函数所以在Knight.sol里看不到详细定义（不过Knigh继承于Ownable）
        //在knight被创建出来时，knight的所有权归属于Setup，调用后就归属于我们（后面的exploit.sol）了
        knight.transferOwnership(msg.sender);
    }
    //获取flag的条件
    function isSolved() external view returns (bool) {
        return knight.health() > 0 && knight.dragon().health() == 0;
    }
}
```

为什么这里要把控制权转给我们？看Knight.sol。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./openzeppelin-contracts/access/Ownable.sol";

import "./Shop.sol";
import "./Bank.sol";
import "./Dragon.sol";
//继承于Ownable
contract Knight is Ownable {
    
    Shop public shop;
    Item public item;
    Bank public bank;
    GoldCoin public goldCoin;
    Dragon public dragon;
    uint public health;
    uint public swordItemId;
    uint public shieldItemId;
    uint public attack;
    uint public defence;
    bool public hasAntiFire;

    constructor() {
        bank = new Bank();
        goldCoin = bank.goldCoin();
        shop = new Shop(address(goldCoin));
        item = shop.item();
        dragon = new Dragon(address(this));

        health = 10;
    }

    modifier onlyAlive() {
        require(health > 0, "GAME_OVER");
        _;
    }
    //onlyOwner修饰符要求调用方等同于所有者，require(msg.sender == owner);
    function equipItem(uint itemId) public onlyOwner onlyAlive {
        require(item.balanceOf(address(this), itemId) > 0, "NO_ITEM");
        (,,Shop.ItemType itemType,uint itemAttack,uint itemDefence,bool itemHasAntiFire) = shop.items(itemId);
        if (itemType == Shop.ItemType.SWORD) {
            _equipSword(itemId, itemAttack);
        } else if (itemType == Shop.ItemType.SHIELD) {
            _equipShield(itemId, itemDefence, itemHasAntiFire);
        } else {
            revert("NOT_EQUIPPABLE");
        }
    }

    function unequipItem(uint itemId) public onlyOwner onlyAlive {
        (,,Shop.ItemType itemType,,,) = shop.items(itemId);
        if (itemType == Shop.ItemType.SWORD) {
            require(swordItemId == itemId, "NOT_EQUIPPED");
            _unequipSword();
        } else if (itemType == Shop.ItemType.SHIELD) {
            require(shieldItemId == itemId, "NOT_EQUIPPED");
            _unequipShield();
        } else {
            revert("NOT_UNEQUIPPABLE");
        }
    }

    function _equipSword(uint itemId, uint itemAttack) private {
        swordItemId = itemId;
        attack = itemAttack;
    }

    function _unequipSword() private {
        swordItemId = 0;
        attack = 0;
    }

    function _equipShield(uint itemId, uint itemDefence, bool itemHasAntiFire) private {
        shieldItemId = itemId;
        defence = itemDefence;
        hasAntiFire = itemHasAntiFire;
    }

    function _unequipShield() private {
        shieldItemId = 0;
        defence = 0;
        hasAntiFire = false;
    }

    function buyItem(uint itemId) public onlyOwner onlyAlive {
        (,uint price,,,,) = shop.items(itemId);
        require(goldCoin.balanceOf(address(this)) >= price, "NOT_ENOUGH_GP");
        goldCoin.approve(address(shop), price);
        shop.buyItem(itemId);
        equipItem(itemId);
    }

    function sellItem(uint itemId) public onlyOwner onlyAlive {
        if (swordItemId == itemId || shieldItemId == itemId) {
            unequipItem(itemId);
        }
        shop.sellItem(itemId);
    }

    function bankDeposit(uint amount) external onlyOwner onlyAlive {
        goldCoin.approve(address(bank), amount);
        bank.deposit(amount);
    }

    function bankWithdraw(uint bankNoteId) external onlyOwner onlyAlive {
        bank.withdraw(bankNoteId);
    }
    
    function bankMerge(uint[] memory bankNoteIdsFrom) external onlyOwner onlyAlive {
        bank.merge(bankNoteIdsFrom);
    }
    
    function bankSplit(uint bankNoteIdFrom, uint[] memory amounts) external onlyOwner onlyAlive {
        bank.split(bankNoteIdFrom, amounts);
    }
    
    function bankTransferPartial(uint bankNoteIdFrom, uint amount, uint bankNoteIdTo) external onlyOwner onlyAlive {
        bank.transferPartial(bankNoteIdFrom, amount, bankNoteIdTo);
        
    }
    
    function bankTransferPartialBatch(uint[] memory bankNoteIdsFrom, uint[] memory amounts, uint bankNoteIdTo) external onlyOwner onlyAlive {
        bank.transferPartialBatch(bankNoteIdsFrom, amounts, bankNoteIdTo);
        
    }

    function fightDragon() public onlyOwner onlyAlive {
        (uint dragonDamage, bool isFire) = dragon.doAttack();
        _receiveAttack(dragonDamage, isFire);
        if (health > 0) {
            dragon.receiveAttack(attack);
        }
    }

    function _receiveAttack(uint damage, bool isFire) private {
        if (isFire && hasAntiFire) {
            return;
        }
        uint damageDone;
        if (damage > defence) {
            damageDone = damage - defence;
        }
        if (damageDone > health) {
            damageDone = health;
        }
        health -= damageDone;
    }
    //这是一个来自于ERC 721（https://docs.openzeppelin.com/contracts/2.x/api/token/erc721）的callback函数，这里为标准函数实现（见https://stackoverflow.com/questions/71646570/how-to-implement-onerc721received-function），官方文档也有写
    function onERC721Received(address, address, uint256, bytes calldata) public pure returns (bytes4) {
        return this.onERC721Received.selector;
    }
    //类似地，这个来自于ERC 1155（https://docs.openzeppelin.com/contracts/3.x/api/token/erc1155）
    function onERC1155Received(address, address, uint256, uint256, bytes calldata) public pure returns (bytes4) {
        return this.onERC1155Received.selector;
    }
}
```

接下来我们看Shop.sol，看看装备的两个item都是什么。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./Item.sol";
import "./GoldCoin.sol";

contract Shop {

    GoldCoin public goldCoin;
    Item public item;

    enum ItemType {
        NONE,
        SWORD,
        SHIELD
    }

    struct ItemProperties {
        string name;
        uint price;
        ItemType itemType;
        uint attack;
        uint defence;
        bool hasAntiFire;
    }

    mapping(uint => ItemProperties) public items;

    constructor(address goldCoin_) {
        goldCoin = GoldCoin(goldCoin_);
        item = new Item();

        item.mint(address(this), 1, 10, "");
        //加上下面的Wooden Shield，很明显不够打龙
        items[1] = ItemProperties(
            "Bronze Dagger",
            10 ether,
            ItemType.SWORD,
            1,
            0,
            false
        );
        item.mint(address(this), 2, 10, "");
        items[2] = ItemProperties(
            "Wooden Shield",
            10 ether,
            ItemType.SHIELD,
            0,
            1,
            false
        );
        //这个和下面那个就很厉害了，不过非常贵，目前没有钱买
        item.mint(address(this), 3, 10, "");
        items[3] = ItemProperties(
            "Abyssal Whip",
            1_000_000 ether,
            ItemType.SWORD,
            1_000_000,
            0,
            false
        );

        item.mint(address(this), 4, 10, "");
        items[4] = ItemProperties(
            "Dragonfire Shield",
            1_000_000 ether,
            ItemType.SHIELD,
            0,
            1_000_000,
            true
        );

        item.mint(msg.sender, 1, 1, "");
        item.mint(msg.sender, 2, 1, "");
    }

    function buyItem(uint itemId) external {
        goldCoin.transferFrom(msg.sender, address(this), items[itemId].price);
        item.mint(msg.sender, itemId, 1, "");
    }

    function sellItem(uint itemId) external {
        item.burn(msg.sender, itemId, 1);
        goldCoin.transfer(msg.sender, items[itemId].price);
    }
}
```

是时候去bank.sol看看了，这个文件也是主要的漏洞点。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./openzeppelin-contracts/utils/Counters.sol";

import "./GoldCoin.sol";
import "./BankNote.sol";

contract Bank {
    using Counters for Counters.Counter;

    uint constant INITIAL_AMOUNT = 10 ether;
    
    Counters.Counter private _ids;

    GoldCoin public goldCoin;
    //转账利用bankNote实现
    //bankNote像一个凭据，比如我们存10个金币，bank就会返回我们一个bankNote，上面写着我们有10个金币
    BankNote public bankNote;
    //bankNote本身不记录值，bankNote到底价值多少由mapping（https://www.tutorialspoint.com/solidity/solidity_mappings.htm）记录，像字典
    mapping(uint => uint) public bankNoteValues;

    constructor() {
        goldCoin = new GoldCoin();
        bankNote = new BankNote();

        goldCoin.mint(msg.sender, INITIAL_AMOUNT);
    }
    function deposit(uint amount) external {
        require(amount > 0, "ZERO");

        goldCoin.burn(msg.sender, amount);

        _ids.increment();
        uint bankNoteId = _ids.current();

        bankNote.mint(msg.sender, bankNoteId);
        bankNoteValues[bankNoteId] = amount;
    }

    function withdraw(uint bankNoteId) external {
        require(bankNote.ownerOf(bankNoteId) == msg.sender, "NOT_OWNER");

        bankNote.burn(bankNoteId);
        goldCoin.mint(msg.sender, bankNoteValues[bankNoteId]);
        bankNoteValues[bankNoteId] = 0;
    }

    function merge(uint[] memory bankNoteIdsFrom) external {
        uint totalValue;

        for (uint i = 0; i < bankNoteIdsFrom.length; i++) {
            uint bankNoteId = bankNoteIdsFrom[i];

            require(bankNote.ownerOf(bankNoteId) == msg.sender, "NOT_OWNER");
            bankNote.burn(bankNoteId);
            totalValue += bankNoteValues[bankNoteId];
            bankNoteValues[bankNoteId] = 0;
        }

        _ids.increment();
        uint bankNoteIdTo = _ids.current();
        //转账给msg.sender，调用msg.sender的onERC721Received
        bankNote.mint(msg.sender, bankNoteIdTo);
        bankNoteValues[bankNoteIdTo] += totalValue;
    }
    //这里可以把一个bankNote的金额分成两个bankNote。比如价值10金币的bankNote可以分成两个价值5金币的bankNote。
    function split(uint bankNoteIdFrom, uint[] memory amounts) external {
        uint totalValue;
        require(bankNote.ownerOf(bankNoteIdFrom) == msg.sender, "NOT_OWNER");

        for (uint i = 0; i < amounts.length; i++) {
            uint value = amounts[i];

            _ids.increment();
            uint bankNoteId = _ids.current();

            bankNote.mint(msg.sender, bankNoteId);
            bankNoteValues[bankNoteId] = value;
            totalValue += value;
        }

        require(totalValue == bankNoteValues[bankNoteIdFrom], "NOT_ENOUGH");
        bankNote.burn(bankNoteIdFrom);
        bankNoteValues[bankNoteIdFrom] = 0;
    }

    function transferPartial(uint bankNoteIdFrom, uint amount, uint bankNoteIdTo) external {
        require(bankNote.ownerOf(bankNoteIdFrom) == msg.sender, "NOT_OWNER");
        require(bankNoteValues[bankNoteIdFrom] >= amount, "NOT_ENOUGH");

        bankNoteValues[bankNoteIdFrom] -= amount;
        bankNoteValues[bankNoteIdTo] += amount;
    }

    function transferPartialBatch(uint[] memory bankNoteIdsFrom, uint[] memory amounts, uint bankNoteIdTo) external {
        uint totalValue;

        for (uint i = 0; i < bankNoteIdsFrom.length; i++) {
            uint bankNoteId = bankNoteIdsFrom[i];
            uint value = amounts[i];

            require(bankNote.ownerOf(bankNoteId) == msg.sender, "NOT_OWNER");
            require(bankNoteValues[bankNoteId] >= value, "NOT_ENOUGH");

            bankNoteValues[bankNoteId] -= value;
        }

        bankNoteValues[bankNoteIdTo] += totalValue;
    }
}
```

所以BankNote是什么？看BankNote.sol。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./openzeppelin-contracts/access/Ownable.sol";
import "./openzeppelin-contracts/token/ERC721/ERC721.sol";
//继承于ERC721，这也是为什么刚才的Knight要重写其中一个回调函数。这类ERCxxx是货币等物品的模拟
contract BankNote is ERC721, Ownable {

    constructor() ERC721("BankNote", "BN") { }
    //转账tokenId代表的物品到to
    function mint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }
    //销毁tokenId代表的物品
    function burn(uint256 tokenId) public onlyOwner {
        _burn(tokenId);
    }
}
```

Item.sol和BankNote.sol差不多。

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

import "./openzeppelin-contracts/access/Ownable.sol";
import "./openzeppelin-contracts/token/ERC1155/ERC1155.sol";
//这个继承于ERC1155，也在Knight里见过相应的回调
contract Item is ERC1155, Ownable {

    constructor() ERC1155("Item") { }

    function mint(address to, uint256 id, uint256 amount, bytes memory data) public onlyOwner {
        _mint(to, id, amount, data);
    }

    function burn(address from, uint256 id, uint256 amount) public onlyOwner {
        _burn(from, id, amount);
    }
}
```

代码审计差不多就这样了。本题的攻击方法为[Re-Entrancy Attack](https://steemit.com/cn/@chenlocus/reentrancy)（重入攻击）。查看Bank的代码，里面调用mint（内部为_safeMint）函数进行转账，但是mint会调用回调函数onERC721Received。我们可以创建一个新合约，让该合约去和bank交互，于是bank会给新合约一个bankNote。转账bankNote这个操作会调用mint，然后调用新合约里实现的回调函数onERC721Received。我们可以在onERC721Received动些手脚，实施Re-Entrancy Attack。

选用bank的split函数作为跳板。

```
//举个该函数的例子。假设我们的bankNoteIdFrom是1，价值10，然后我们想将其分为5和5。
//最开始是1:10
//执行后是1:0;2:5;3:5
function split(uint bankNoteIdFrom, uint[] memory amounts) external {
        uint totalValue;
        require(bankNote.ownerOf(bankNoteIdFrom) == msg.sender, "NOT_OWNER");

        for (uint i = 0; i < amounts.length; i++) {
            uint value = amounts[i];

            _ids.increment();
            uint bankNoteId = _ids.current();

            bankNote.mint(msg.sender, bankNoteId);
            bankNoteValues[bankNoteId] = value;
            totalValue += value;
        }

        require(totalValue == bankNoteValues[bankNoteIdFrom], "NOT_ENOUGH");
        bankNote.burn(bankNoteIdFrom);
        bankNoteValues[bankNoteIdFrom] = 0;
    }
```

为什么选它呢？首先是因为里面调用了bankNote.mint，但更重要的是它在调用mint之后才调用了burn销毁split前的id。这正是重入攻击的一个典型特征——先操作后改状态。此题我们将Re-Entrancy Attack搭配[fastLoan](https://www.coindesk.com/learn/what-is-a-flash-loan/)。我在注释里写的例子是正常情况下的执行结果，但是如果是不正常的情况呢？我们的bankNoteIdFrom还是1，但价值是0。接着将其分割为2000000和0。我们自己过一遍函数的执行过程。首先require语句没问题，1号note确实是我们自己的。接着遍历amounts数组，取出每个amount的value，这里是2000000。然后_ids增加，创建出一个新的bankNote，转账给msg.sender（此处执行我们的回调函数）。接着赋值bankNoteValues value，totalValue累加，两者的值都是2000000。接着for循环进入第二轮，一切照旧只不过value是0。注意，此时调用bankNote.mint就出问题了，我们之前那个价值2000000的bankNote还在呢，是不是意味着我们可以在回调函数里用这个bankNote了？

想想我们要干什么。首先买那两个极品装备，然后装在knight身上，把龙杀掉。但还没完。split函数在for循环结束后还有个require，里面会检查totalValue是否等于bankNoteIdFrom的value，而我们肯定是不符合这个条件的。soliduty里的合约状态在函数执行完成后才会存储，中间因为require断掉后一切就重来了，龙白杀了。所以我们在杀完龙后要把两件装备卖掉，得到2000000，紧接着去bank调用deposit把这2000000存起来，最后再调用bank的transfer函数把2000000转到id为1的最开始的那个bankNote。此时require的条件就为True了。虽然split函数的最后把那2000000销毁了，但是龙已经死了。

最后的问题，我们如何拥有一个bankNote？答案是调用bank的merge函数。

```
function merge(uint[] memory bankNoteIdsFrom) external {
        uint totalValue;

        for (uint i = 0; i < bankNoteIdsFrom.length; i++) {
            uint bankNoteId = bankNoteIdsFrom[i];

            require(bankNote.ownerOf(bankNoteId) == msg.sender, "NOT_OWNER");
            bankNote.burn(bankNoteId);
            totalValue += bankNoteValues[bankNoteId];
            bankNoteValues[bankNoteId] = 0;
        }

        _ids.increment();
        uint bankNoteIdTo = _ids.current();
        //转账给msg.sender，调用msg.sender的onERC721Received
        bankNote.mint(msg.sender, bankNoteIdTo);
        bankNoteValues[bankNoteIdTo] += totalValue;
    }
```

我们可以往里面传个空数组，这样就不会进for循环，但是仍然会执行bankNote.mint，这样就得到了一个空的bankNote。脚本可以参考[这里](https://aaronesau.com/blog/post/12)或者[这里](https://gss1.tistory.com/entry/HackTM-CTF-Quals-2023-smart-contractDragon-Slayer-Diamond-Heist)的，两者的exploit.sol都差不多，不过前者用js释放合约，后者用python释放。

## Flag
> HackTM{n0w_g0_g3t_th4t_run3_pl4t3b0dy_b4af5ff9eab4b0f7}