# Rabbit

其实这题超简单的，但是我被误导了两次！我是菜狗！

图片用16进制打开就能看见末尾有一串加密内容，或者直接zsteg。

- ########(=^-^=)###U2FsdGVkX1+EPlLmNvaJK4Pe06nW0eLquWsUpdyv3fjXM2PcDBDKlXeKupnnWlFH\r\newFEGmqpGyC1VdX8

base64解密后开头是Salted__，我认为是openssl，之前也做过类似的题，当时的加密方式是openssl的aes系列。我就以为这也是aes，疯狂猜密码，每次都bad decrypt，人都要疯了。我以为我的openssl坏了，就找了个在线的，也不行。中途遇见了Rabbit加密，尝试猜密码使用Rabbit解密也不行。我好疑惑啊，甚至于猜了各种密码：

- Rabbit,rabbit,RABBIT,########(=^-^=)###,(=^-^=)

到后面越来越离谱，16进制编码rabbit，凯撒rabbit等等。绝望的我去问了我的好群友，发现他发过来的工具我之前用过。不甘心继续尝试，还是不行。悲伤地去睡觉。快睡着的时候想到“有没有可能没有密码呢？”立刻跳起来解密（要把\r\n去掉），成了……了……

不要想太复杂了。

- ### Flag
  > moectf{We1c0m3_t0_moectf_an7_3n7oy_y0urse1f}