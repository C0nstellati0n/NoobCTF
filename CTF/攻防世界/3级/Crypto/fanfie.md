# fanfie

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=41cc6af0-5263-425f-828d-3a15224918c1_2&task_category_id=5)

又来个密码，继续挖坑，找一天和rsa，ecc一起写数学原理。近几年不行了就我这数学算啥都算不明白。

附件就这么一句话，甚至都不算“话”

- MZYVMIWLGBL7CIJOGJQVOA3IN5BLYC3NHI

base家族都试过了，都不是。立刻没思路了，搜writeup发现原来是有提示的，这是把flag进行某种加密后的密文，flag格式为BITSCTF{xxxxxxxx}。密文看起来更像base32，那就把BITSCTF{用base32加密试试。

- IJEVIU2DKRDHW

把补位的=号去掉，结果就是这个。把两个结果比对一下。

- IJEVIU2DKRDHW
- MZYVMIWLGBL7CIJOGJQVOA3IN5BLYC3NHI

重复的I在下面也重复了，变成了M。那这应该是某种替换密码，比如[仿射密码](https://cryptowikis.com/ClassicalCipher/SubstitutionCiphers/AffineCipher/)。这里讲的比较清晰了，怎么加密，解密和破解都有提到。但是我解密没看懂，主要还是因为不会解线性同余方程组，找机会补吧。

看其他的writeup也没有解释a和b怎么来的，都说“由……得a=13，b=4“。我就很懵啊，怎么得的？没办法只能跟着这个思路走了。a的乘法逆元可以在[这里](https://zh.planetcalc.com/3311/)找到。记得模除32，因为是base32，自然有32个字母，记得看上面的原理。

写了一个半解密脚本。

```python
from string import ascii_uppercase
mod_inv=5
b=4
cipher='MZYVMIWLGBL7CIJOGJQVOA3IN5BLYC3NHI'
alphabets=ascii_uppercase+'234567'
flag=''
for i in cipher:
    flag+=alphabets[pow(mod_inv*(alphabets.index(i)-b),1,32)]
print(flag)
```

base32的字母是a-z加上2-7的数字，=号补位。运行结果如下：

- IJEVIU2DKRDHWUZSKZ4VSMTUN5RDEWTNPU

放到[这里](https://gchq.github.io/CyberChef/#recipe=From_Base32('A-Z2-7%3D',true)&input=SUpFVklVMkRLUkRIV1VaU0taNFZTTVRVTjVSREVXVE5QVQ)解密就能得到flag了。唉我的数学为什么这么拉。

- ### Flag
- > BITSCTF{S2VyY2tob2Zm}