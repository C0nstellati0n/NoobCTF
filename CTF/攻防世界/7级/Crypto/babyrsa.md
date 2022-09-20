# babyrsa

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=840228a1-0ad9-4d93-b148-1125735d1ead_2)

到底有多少个扮猪吃老虎的babyrsa啊？

附件无比潦草，就给了e，n和c。n尝试去factordb分解，失败。直接疑惑，那么多rsa攻击方式在这道题里都施展不开啊。回到题目看看，发现给了个nc地址。作用就是把16进制的密文告诉服务器，服务器会返回用私钥解密后的m的奇偶性。这……但凡都点用都不至于一点用都没有。看看[wp](https://zhuanlan.zhihu.com/p/266200199)。

知道m的奇偶性确实没什么用，但是知道2*m mod n的奇偶性可就大有用处了。$m<n$，那么$2m<2n$。2m是偶数，n是奇数，$2m\mod n$如果是偶数，说明$0<=2m<n$；如果是奇数，说明$n<2m<n$。2m小于n的情况很好理解，当2m大于n时，$2m\mod n$相当于求2m-n的奇偶性。偶数-奇数总是奇数。

现在我们要做的就是根据给的信息构造明文是$2m\mod n$的密文。$c\equiv m^e\mod n,2^ec\equiv (2m)^e\mod n,(2^ec\mod n)\equiv ((2m)^e\mod n)\mod n$。

理论在此，爆破非常痛苦。我已经爆破了3次了，每次十几分钟，总是因为一些杂七杂八的原因爆破失败。

```python
from pwn import *
from Crypto.Util.number import long_to_bytes
e = 0x10001
n = 0x0b765daa79117afe1a77da7ff8122872bbcbddb322bb078fe0786dc40c9033fadd639adc48c3f2627fb7cb59bb0658707fe516967464439bdec2d6479fa3745f57c0a5ca255812f0884978b2a8aaeb750e0228cbe28a1e5a63bf0309b32a577eecea66f7610a9a4e720649129e9dc2115db9d4f34dc17f8b0806213c035e22f2c5054ae584b440def00afbccd458d020cae5fd1138be6507bc0b1a10da7e75def484c5fc1fcb13d11be691670cf38b487de9c4bde6c2c689be5adab08b486599b619a0790c0b2d70c9c461346966bcbae53c5007d0146fc520fa6e3106fbfc89905220778870a7119831c17f98628563ca020652d18d72203529a784ca73716db
c = 0x4f377296a19b3a25078d614e1c92ff632d3e3ded772c4445b75e468a9405de05d15c77532964120ae11f8655b68a630607df0568a7439bc694486ae50b5c0c8507e5eecdea4654eeff3e75fb8396e505a36b0af40bd5011990663a7655b91c9e6ed2d770525e4698dec9455db17db38fa4b99b53438b9e09000187949327980ca903d0eef114afc42b771657ea5458a4cb399212e943d139b7ceb6d5721f546b75cd53d65e025f4df7eb8637152ecbb6725962c7f66b714556d754f41555c691a34a798515f1e2a69c129047cb29a9eef466c206a7f4dbc2cea1a46a39ad3349a7db56c1c997dc181b1afcb76fa1bbbf118a4ab5c515e274ab2250dba1872be0
left, right = 0, n
last = 0
while left < right:
   mid = (left + right) // 2
   c = c * pow(2, e, n) % n
   sh = remote('61.147.171.105',59953)
   sh.sendlineafter('You can input ciphertext(hexdecimal) now',str(hex(c)))
   sh.recvline()
   s=sh.recvline()
   if s==b'odd\n':
      left = mid+1
   else:
      right = mid
   sh.close()
print(long_to_bytes(left))
```

- ### Flag
  > QCTF{RSA_parity_oracle_is_fun}