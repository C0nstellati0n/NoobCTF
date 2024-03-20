# Remix+Metamask配置/Web3学习

今天终于做出来了人生第一道blockchain入门题。漏洞实在太明显了，我这种没有啥经验的都能一眼看出来，所以不记录题目内容。卡了我很久的反而是“怎么deploy我的攻击合约啊“？翻看我的笔记，大佬们都用foundry/cast，但是我怎么样都配置不好……最后从笔记里翻出了这篇[wp](https://github.com/skabdulhaq/CTF-learnings/blob/main/CTF-writeups/BytesbanditCTF/blockchain-GuessTheName.md)，使用remix+metamask的配置。简单好上手，个人认为是最适合入门的

首先安装metamask的chrome插件： https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn ，按照步骤创建新账号即可。接着点击右上角三个点，选择“设置”->“网络”->"添加网络"，把blockchain题目给的rpc url填进去。链ID通常是1，不确定的话可以用python的web3模块查看：
```py
from web3 import Web3
web3=Web3(Web3.HTTPProvider("rpc_url"))
print(web3.eth.chain_id)
```
货币符号感觉不重要，随便填一个就行。保存后返回主页，右上角切换网络为刚才创建的题目所处的网络。接着正中央上方为当前所使用的账号，点击后选择"Add account or hardware wallet"->"导入账户",粘贴题目提供的私钥即可导入题目为我们提供的账号。这步很重要，我们自己的默认账号在题目所处的网络上一分钱没有，要是Remix用这个账号会导致没钱释放攻击合约的情况……

然后就可以去[Remix](https://remix.ethereum.org)了。点击倒数第二个图标（Deploy & run transactioins），最上方的ENVIRONMENT选择Inject Provider - MetaMask。绑定账号时一定要选那个有钱的账号，原因之前提过了。如果不小心绑定了没钱的账号，个人当时（本经验不来自于网络）直接重装了metamask，后面想想应该清除cookie就行了。另外提醒一点，metamask里导入的账户可以随时删除，但是自己创建的不能，要想删除的话只能重装插件（我在官网看到这句话时人都傻了）

这样应该就可以了，后面正常写攻击合约正常deploy并调用函数即可，用大白话说就是“Remix该怎么用咱们就怎么用”。顺便再说一句，开头提到的那篇wp确实是最适合初学者入门的，包括里面攻击合约的编写也是最基础的

这里是一个blockchain（solidity）的javascript web3开发教程： https://www.youtube.com/watch?v=gyMwXuJrbJQ