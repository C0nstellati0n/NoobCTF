# IgniteMe

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4d4f7511-028a-4e2b-a25c-6a3df268dbb1_2)

这道题完美体现了IDA的牛逼和Ghidra的不足。如果你是IDA用户，那么这道题卡了我很久的地方你完全就不用理。我会在后面说明。

这次的附件是一个exe执行文件。这意味着非windows环境的我无法运行了，而且我还没有装虚拟机。不慌，先放进Ghidra里看一下。逆向的第一步一般从main开始，所以我们直接进入main函数……我的main呢？

![noMain](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/noMain.png)

这种情况下如果执行文件函数不多我会选择运行一下然后手工找main。但是这次函数挺多的，我还无法运行。于是我决定使用radare2打印出程序中全部的字符串，根据字符串的地址找到main。（我真不会用Ghidra，网上也几乎搜不到多少教程。可能会找一天看一下官网的教程，到时候把我觉得有用的翻译到这里）

![radare2](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/radare2.png)

此处【r2 文件】命令打开radare2主程序进行分析（radare2有很多模块，这次先不介绍）。aaa命令对程序进行最完整的分析，不过速度较慢。大型项目不建议直接使用aaa，不过CTF基本可以放心用。aa？可以获取所有跟aa有关的命令的帮助（大部分命令都可以这样做）。

![strings](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/strings.png)

iz命令可以获取程序内所有的字符串，开头的几个字符串非常可疑，而且像"Congratulations!"这种语句很有可能出现在main函数。直接把这个字符串的地址复制下来并在Ghidra中找到（Ghidra中按g键可以前往任意地址）

![ghidra](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/ghidra.png)

你会发现有亿点乱，没有IDA那么简洁明了。幸运的是根本的逻辑都是一样的。既然是逆向，那么切入点也要倒着来。我们想要的结果是输出"Congratulations!"，那么就直接从那个分支开始看。想要进入这个分支就要保证cVar1不等于0，而cVar1又从CheckFlag中得到。去里面看看。

![CheckFlag](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/CheckFlag.png)

根据index的值这个线索可以发现，flag的判断从第四位开始。第一个while循环仅仅是将inputFlag复制一份。然后第二个while循环可能就有点奇怪了，拿char和int比较大小是在干啥？其实这里是在拿char的ascii值和这些数字比对。那比这个东西有什么意义呢？我们可以在python中一探究竟。

```
from string import ascii_lowercase, ascii_uppercase
for letter in ascii_lowercase:
    print(f"{letter}: {ord(letter)}")
for letter in ascii_uppercase:
    print(f"{letter}: {ord(letter)}")
```
运行这段代码就会发现，大写字母的ascii值在65-90内，而小写字母则在97-122内。那这个逻辑就简单明了了，它是在判断当前的char是大写还是小写字母。那后面-32又是什么鬼？

```
from string import ascii_lowercase
letters=ascii_lowercase
for letter in letters:
    print(letter)
    letter=(ord(letter)-0x20)
    print(chr(letter))
```
运行这段代码就会发现，将小写字母的ascii值减去32可以将其变为大写字母，反之亦然。那这段的逻辑已经明白了，继续往下看ManipulateFlag函数。

![ManipulateFlag](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/ManipulateFlag.png)

不要在意那个for循环在干啥，你会发现唯一起作用的就是那个return语句。这意味着你可以当作这个函数只有这一句return语句。普通的异或和相减操作，继续往下，你会发现程序把从ManipulateFlag得到的返回值再与target进行比较。双击target就可以看到里面的内容。程序的最后一段是判断上面整个逻辑是不是与 GONDPHyGjPEKruv{{pj]X@rF 相同。可以开始写逆向脚本了，只需要把上面的过程反过来就行了。

```
from string import ascii_lowercase, ascii_uppercase
flag=[]
target=[13, 19, 23, 17, 2, 1, 32, 29, 12, 2, 25, 47, 23, 43, 36, 31, 30, 22, 9, 15, 21, 39, 19, 38, 10, 47, 30, 26, 45, 12, 34, 4]#[0x13, 0x19, 0x23, 0x17, 0x2, 0x1, 0x32, 0x29, 0x12, 0x2, 0x25, 0x47, 0x23, 0x43, 0x36, 0x31, 0x30, 0x22, 0x9, 0x15, 0x21, 0x39,
 #0x19, 0x38, 0x10, 0x47, 0x30, 0x26, 0x45, 0x12, 0x34, 0x4]
target2='GONDPHyGjPEKruv{{pj]X@rF'
def ManipulateFlag(letter):
    result=(letter-72)^0x55
    return chr(result)
for i in range(len(target2)):
    letter=target[i]^ord(target2[i])
    letter=ManipulateFlag(letter)
    if letter in ascii_lowercase:
        flag.append(chr(ord(letter)-32))
    elif letter in ascii_uppercase:
        flag.append(chr(ord(letter)+32))
    else:
        flag.append(letter)
print(''.join(flag))
```

我也不知道Ghidra怎么提取数据，所以我手抄下来的。注意这里不能使用16进制，否则会报错。运行程序就可以得到flag了……吗？提交后你会发现不对。回想一下，上面的逻辑从第4位以后开始判断，那前4位是什么？Ghidra里没有显示，不过IDA里非常清晰，是 EIS{ 。难受，迟早我要换成IDA。

Flag：EIS{wadx_tdgk_aihc_ihkn_pjlm}