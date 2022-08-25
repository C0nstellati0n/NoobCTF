# Decode_The_File

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=25c52cec-141d-4f84-90ae-369bc1becd20_2)

此decode非彼decode。

附件一堆base64，解码是个文档，好像是讲des的。看了一下和flag没啥关系。这里就要介绍一下新东西了：base64加密。base64虽然很常用，但你知道它的[加密原理](https://blog.csdn.net/m0_37948170/article/details/107387926)吗？

防止你懒得点开那个链接，在这里也简单讲一下。首先借用刚刚那个链接的图。

![encode](../../images/20200717142400527.png)

可以说是很清晰了。将原文转为二进制，然后以6位一组分成几块，每块再转为10进制，对应64进制编码表（A-Z，a-z，0-9，+/，索引以0开始）编码。为什么会出现等于号呢？因为有的时候六个一组分不完全，比如H的二进制编码01001000分成6个一组就是010010和00，后面的00不够6位，所以再补上四个0，构成000000。如果补了两个0就在末尾加一个等于号，四个0就两个。所以H的base64编码是SA==

由此可看出等于号用于标记末尾没用的补位0的位数。解码就是反过来，把SA转为二进制010010和000000，看到两个等于号舍去末尾四个0，得到01001000，完成解码H。

你可能就有问题了，补位为什么要0？这就是base64加密的核心逻辑。反正后面都要舍掉的，是不是0又有什么关系呢？我放点自己要藏的数据不就行了？到这里我们就可以写脚本了。

```python
from string import ascii_lowercase, ascii_uppercase, digits
from Crypto.Util.number import long_to_bytes
with open("你的文件地址") as f:
    content=f.read().split('\n')[:-1]
b64=ascii_uppercase+ascii_lowercase+digits+'+/'
temp=[]
for i in content:
    if '==' in i:
        temp.append(bin(b64.find(i[-3]))[2:].rjust(6,'0')[2:])
    elif '=' in i:
        temp.append(bin(b64.find(i[-2]))[2:].rjust(6,'0')[4:])
flag=''.join(temp)
print(long_to_bytes(int(flag[:flag.rfind('1')+1],2)))
```

- ### bin
  > 返回一个整数 int 或者长整数 long int 的二进制表示。
  - 语法：bin(x)
    > x -- int 或者 long int 数字

- ### rjust
  > 返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串。
  - 语法：str.rjust(width[, fillchar])
  - 参数
    > width -- 指定填充指定字符后中字符串的总长度.
    > fillchar -- 填充的字符，默认为空格。
  - 举例：'test'.rjust(8,'a')，输出aaaatest

- ### rfind
  > 返回字符串最后一次出现的位置，如果没有匹配项则返回 -1。
  - 语法：str.rfind(str, beg=0 end=len(string))
  - 参数
    > str -- 查找的字符串
    > beg -- 开始查找的位置，默认为 0
    > end -- 结束查找位置，默认为字符串的长度。

base64加密的原理决定了一次最多只能隐藏4位，因为base64末尾最多有两个==号，标记末尾最多只有4位无用位。如果末尾有两个等于号，我们找到倒数第三位的字母，并在b64这个编码表中找到它的索引。将其bin转换为2进制后从第三位截取（因为bin转换结果是0bxxxxx，索引从0开始），得到无0b的二进制数。rjust对齐base64编码时的分组6位，取后四位。一个等于号的逻辑也类似。

最后flag\[:flag.rfind('1')+1]的原因是最后一位是0，直接转成int会在末尾添加很多无用byte。去掉最后1个0直接就是flag了，当然不去也无伤大雅。

- ### Flag
  > ROIS{base_GA_caN_b3_d1ffeR3nT}