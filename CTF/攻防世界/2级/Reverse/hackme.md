# hackme

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d57739a5-a00f-40cf-bbf9-8841d9b81a77_2)

附件下载下来放到Ghidra里分析后没发现main。虽然有个Entry，但是点进去发现又是函数黑洞，函数之间疯狂套娃，很明显不是我们想要的。不过这次的附件在linux上可运行，那么我们可以运行一下看看输出的是什么。

- Give me the password: dksjf
- Oh no!

这样我们就可以根据输出的字符串在Ghidra里找到真正的入口点了。

- #### 如何在Ghidra中搜索字符串并找到引用？
- > 菜单栏->Search->Program Text->左下角勾上All Fields->在输入框中输入要搜索的字符串
- > 点击搜索出来的结果会跳转到有关的上下文。这个有关的上下文所在的函数就是这个字符串被引用的地点
- > 注意：此方法有可能会在windows exe中失败

![entry](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/realEntry.png)

上面是最核心的逻辑。最上面的空for循环我猜是用来判断输入的位数的，因为j值跟input数组的长度有关，紧接着又判断了j是否等于22，而判断的结果在下面也有用到。目前猜测password长度为22。

接下来的代码虽然不长，但很有误导性。这里不知道是不是Ghidra的原因，我完全看不出来UnknownFunction的用途，自然也无法得知unknown变量的值。而unknown变量在下文又有使用，难道就没有办法了吗？

我们还可以硬着头皮继续往下看。不难发现unknown%0x16仅被用作了flag数组和input数组的索引，后面就没有再使用了。既然这个变量仅仅用来取值，没有参与后面的数值运算，是不是意味着没有知道它的值的必要性呢？

我们的目标是让keyVariable不会变成0，意味着local_29必须等于flag\[local_28]。local_29又从local_22异或local_18得来，local_18的值也很简单，从上面的for循环得来。那么逆向的逻辑基本已经捋顺了，最后的问题在于determineLoop变量为什么设定在10？

首先这个while循环只会执行10次，同时我们的值unknown%0x16的值必须在22以内（因为被用作索引，再大就越界了）。那么我们可以推断这个逻辑每次只会判断10位，至于是哪10位我们根本不在乎，因为只要逆向出完整的密码后，无论取哪10位进行比对肯定都是对的。

这样前面的问题就迎刃而解了，unknown就让它继续unknown吧，我们直接出发去找flag。

```python
s='5f f2 5e 8b 4e 0e a3 aa c7 93 81 3d 5f 74 a3 09 91 2b 49 28 93 67'
s=s.split(' ')
flag=[]
s_flag=''
for i in s:
    flag.append(int('0x'+i,16))
for j in range(len(flag)):
    local_20=j
    local_18=0
    local_21=flag[local_20]
    index=local_20+1
    for i in range(index):
        local_18=local_18* 0x6d01788d+ 0x3039
    s_flag+=chr((flag[j]^local_18)&0xff)
print(s_flag)
```

直接将循环次数设置为flag数组的长度，逆向出全部的密码。最后&0xff是为了不让整形溢出。虽然python里没有整形溢出这个问题，但是这里面调用了c的底层方法，所以要将位数控制在8位以内，跟0xff按位与就行了。

- #### Flag
- > flag{d826e6926098ef46}