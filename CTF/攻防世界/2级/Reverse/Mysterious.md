# Mysterious

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a36e4bbc-5306-4292-9e60-d342e4a0a6fc_2)

附件是exe，倒吸一口凉气，因为Ghidra反编译的exe文件我不熟悉，很容易被带到坑里。扔进Ghidra查找字符串，找到了个well done，查找引用后便发现了入口点。

![main](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/Entry.png)

Ghidra用户的必备技能——盲猜和信念。这里可以看见想要到well done就要先进入最上面的else if分支，也就是param2等于273。这里param2我没有放在截图里，因为这是main函数的参数，在没法运行和调试的情况下无法知道这个参数的值。那现在还能咋办，只能先看下面well done所在的if分支了。

可以很容易地发现有个FID_conflict:_strcat函数似乎在打印一些值（根据传入的参数和函数名猜测不熟悉函数的作用），熟悉的大括号提示着我们这可能是flag。local_210的作用未知，猜测可能是最后打印的结果，因为整个local_210在最后传入MessageBoxA函数，而MessageBoxA根据名字就可以想到作用是提示消息。那根据以上的逻辑，我们想要知道完整flag还缺个local_314的值。往上找这个变量，发现了__itoa(local_10c,local_314,10)。

- ### itoa()
- > 函数原型：char *itoa(int i,char *s,int radix)
- > 功能：用于把整数转换成字符串
- > i为要转换为字符的数字,*s为转换后的指向字符串的指针,radix为转换数字的进制数

所以这里的意思是把local_10c这个数字转为字符串后传入local_314,使用10进制。所以现在我们继续去找local_10c。在if判断语句里看见了local_10c==123。虽然我们不知道local_10c是根据什么得到的（其实是我们的输入，在ida里很清楚但是在Ghidra里就绕了很大一个弯），不过既然已经进入if语句了，local_10c的值就是123。

于是当你把123跟其他的字符串拼起来是，你会发现你对了。不至于吧，这题怎么感觉过于简单了，if语句中多判断的几个值告诉我们事情没那么简单。

![stack](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/stack.png)

查看栈上变量分布可以发现，if语句判断的local_10c(local_10c的值等于这里的local_108，后面用一堆很迷惑的操作赋值了，不是重点)，local_105,local_103,local_104在栈上是挨着的。local_108的大小为3，再往下看看接收输入的函数。

- GetDlgItemTextA(param_1,0x3ea,(LPSTR)local_108,0x104)

发现往里面可不止放了3个byte。同时查看整个函数你会发现没有地方给local_105,local_103和local_104赋值。所以进入那个if分支正确的方法是传入123xyz，123留在local_108里，剩下的x，y，z分别溢出到local_105,local_103和local_104里（这三个变量都是1byte长）。这样就能进入if判断了。

不过这题根本没那么麻烦，不知道是不是出题者有意而为，简单分析后就能直接得出flag。

- ### Flag
- > flag{123_Buff3r_0v3rf|0w}