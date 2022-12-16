# [UTCTF2020]hill

[题目地址](https://buuoj.cn/challenges#[UTCTF2020]hill)

给了一串不知道是什么东西的密文。这我上哪去猜，直接看[wp](https://blog.csdn.net/m0_52727862/article/details/119118956)。得知是[希尔密码](https://baike.baidu.com/item/%E5%B8%8C%E5%B0%94%E5%AF%86%E7%A0%81/2250150?fromtitle=Hill%E5%AF%86%E7%A0%81&fromid=1435959&fr=aladdin)。希尔密码利用矩阵构建密码，首先将26个字母写为数字0-25，将要加密的数字放入矩阵内，再乘以一个密钥。这个密钥是一个方阵矩阵，因为只有方阵矩阵才有逆，后面解密时才能通过密钥的逆矩阵恢复原文。原文乘以密钥的结果再模26即是加密结果。

然后一个有点坑的地方是，比赛的flag格式为utflag，意味着我们可以通过密文和已知的原文构建方程并求解。构建2行3列的原文和密文矩阵。根据[矩阵乘法](https://zh.wikihow.com/%E8%AE%A1%E7%AE%97%E7%9F%A9%E9%98%B5%E4%B9%98%E6%B3%95)的规则，仅在A矩阵的列数等于B矩阵的行数时，两个矩阵才能相乘。结果矩阵的行数是A矩阵的行数，列数是B矩阵的列数。那么密钥就是2\*2的矩阵,6个方程4个未知数（我不太懂为什么判断密钥是2\*2的矩阵）。构建方程解出密钥矩阵就行了，方程参照[此处](https://blog.csdn.net/weixin_52446095/article/details/118823723)。

```python
a00, a01, a10, a11 = 13, 6, 3, 21 #这里应该是密钥矩阵的逆矩阵的值
dic = 'abcdefghijklmnopqrstuvwxyz'
c = 'wznqcaduqopfkqnwofdbzgeu'
flag = ''
for i in range(0, len(c), 2):
    a, b = dic.index(c[i]), dic.index(c[i+1])
    a0, b0 = (a00*a+a01*b)%26, (a10*a+a11*b)%26 #因为得到了逆，dic和c能看成dic*key=c的关系，key是密钥矩阵。那么c乘上逆矩阵就回到dic了。这里的操作就是矩阵乘法
    flag += dic[a0]
    flag += dic[b0]
print (flag)
```

flag出来还不全，要手动把数字下划线等补上。

## Flag
> flag{d4nger0us_c1pherText_qq}