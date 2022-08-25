# Avatar

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=cfb0eb7d-f28a-4045-87f3-95ead0dd1e9d_2)

这题就是认识新工具，没啥特殊的。但是让我发现了一个白嫖的好方法。

附件是一个羊毛绒玩具。binwalk不行，stegsolve不行，zsteg也不行。放进16进制编辑器里发现开头有点奇怪，但除此之外也没别的了。

看writeup发现要outguess工具，下载了直接用就行了。可是我不想，于是在网上找了一个在线运行[outguess](https://cyber.meme.tips/joutguess/)。

没想到还真能用，运行结果就是flag。

- ### Flag
- > We should blow up the bridge at midnight