# sherlock

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f4c9d8f7-ab03-4f58-b299-0dcd4739ee20_2)

很多时候普通文本中藏的信息大概率都是各种形式的二进制，甚至不止是文本可以这样，任何东西只要能和“两种值”这个概念结合起来都能隐藏二进制。

这里附件还真的是Sherlock Holmes这本书，直接搜索也没有找到flag。通过文本最上面的信息可以发现下面的内容很早就被发表了，但是english首字母没有大写，不太符合规范。再往下看就更离谱了，i没一个大写，而众所周知英语里表示“我”的I都是要大写的。反倒是题目“thE adventuRes Of sherlOck holmes“的一些字母被莫名其妙大写了。把这些大写字母拼起来，“ERO”，而前面还有一个“Z“，ZERO代表0，0就应该唤起你的DNA了，二进制？继续往下看还发现了ONE，那是二进制没跑了。

写个python脚本把这些大写字母提取出来。结果中的ZERO换成真正的0，ONE换成真正的1。最后用Crypto库转成文字。

```python
from string import ascii_uppercase
from Crypto.Util.number import long_to_bytes
with open("你的文本文件地址",'r') as f:
    text=f.read()
data=''
for i in text:
    if i in ascii_uppercase:
        data+=i
data=data.replace("ZERO",'0')
data=data.replace("ONE",'1')
print(long_to_bytes(int(data,2)))
```

- ### Flag
- > BITSCTF{h1d3_1n_pl41n_5173}