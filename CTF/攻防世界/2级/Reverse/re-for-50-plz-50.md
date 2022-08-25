# re-for-50-plz-50

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d4125a54-8eaa-482b-b467-dca63e53fae6_2)

这道题其实挺简单的，只要你当一个赌狗（但是赌对了不就是赌神了吗？）

首先Ghidra反编译附件还用了挺长时间的（跟其他简单的挑战相比），而这个文件的格式也是之前没见过的：MIPS。这是一种采取精简指令集（RISC）的处理器架构。这里只需要知道IDA对这种架构的反编译局限性很高，不过我用的是Ghidra，看起来一切尚好。

![main](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/main.png)

虽然不知道main函数里的两个参数是干啥的（无法运行这个文件），但是我们可以清楚看到有两个分支，而下面那个就肯定是我们要去的分支了。往上看，发现有个叫meow的数组。点开看有一堆数据，数量正好符合for循环的31。猜测这是要被逆向的目标。

- #### Tips
- > Ghidra菜单->Window->Bytes选项可以轻松在内存中选取想要的bytes.

来到了我最不理解的地方。从函数逻辑里可以很清楚地看出param2是加上4在加上i后才跟0x37进行异或的。但是当我按照这个逻辑编写脚本时，出来的结果却并不是flag。

- PP=M>rXjhRdVQ[ZfKbRXQZPTLQIBLS[

于是我试了只加4，只加i，但是都不对。最后一个都不加直接异或反而对了。我真搞不明白了，看了其他人的writeup发现别人是直接看汇编的。但我的汇编里也有这几步……这回赌对了不知道下次还行吗？

```python
s='63 62 74 63 71 4c 55 42 43 68 45 52 56 5b 5b 4e 68 40 5f 58 5e 44 5d 58 5f 59 50 56 5b 43 4a'
flag=''
numbers=s.split(' ')
for i in range(len(numbers)):
    numbers[i]=int(numbers[i],16)
def rev(number):
    return (number^0x37)
for i in range(len(numbers)):
    flag+=chr(rev(i,numbers[i]))
print(flag)
```

- #### Flag
- > TUCTF{but_really_whoisjohngalt}