# cr2-many-time-secrets

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a83a65e4-2ea2-4dc1-8c95-dde0a2974c1b_2)

新知识点，脚本小子出击！

附件只有一串看着像16进制但是解码后是乱码的字符串。

- 0529242a631234122d2b36697f13272c207f2021283a6b0c7908
<br>2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908
<br>322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012
<br>283f652c2b31661426292b653a292c372a2f20212a316b283c09
<br>29232178373c270f682c216532263b2d3632353c2c3c2a293504
<br>613c37373531285b3c2a72273a67212a277f373a243c20203d5d
<br>243a202a633d205b3c2d3765342236653a2c7423202f3f652a18
<br>2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c
<br>263e203d63232f0f20653f207f332065262c3168313722367918
<br>2f2f372133202f142665212637222220733e383f2426386b

攻防世界没写，但原题是有提示的：

- This time Fady learned from his old mistake and decided to use onetime pad as his encryption technique, but he never knew why people call it one time pad! Flag will start with ALEXCTF{

大概就是说Fady决定使用一次性密码本来加密，可是他不理解为什么人们叫它一次性密码本呢？flag格式为ALEXCTF{。大坑啊，攻防世界没有让人上哪去猜？由提示我们可以猜测，Fady把密钥重用了很多次。一次性密码本的原理就是异或字符串。取一个和明文一样长的字符串密钥，将两者异或，结果就是密文。由于异或可逆，所以把密文和密钥再异或就得到了明文。当相同的密钥被多次用于加密内容时，这个密钥就不安全了。此处就引入了Crib dragging攻击，原理可以看[这里](https://www.cnblogs.com/labster/p/13703782.html)。是英文的，我把里面最重要的破解步骤按照接下来的逻辑改编一下。

- ### Crib dragging
  > 1.猜密钥或明文里可能会出现的字符串
  > 2.将第一步的字符串编码成16进制
  > 3.将第二步的16进制字符串与密文异或
  > 4.当第三步里出现可打印字符时，根据结果继续往下猜测
  > 5.如果是乱码，就增加偏移继续进行异或。

为啥这样可行呢？密钥很可能是flag，密文由flag和另一段文字异或而成。我们知道flag开头为ALEXCTF{，那与密文进行异或肯定能发现文字中的一些内容。根据一些内容就可以往下猜词，比如出现了Hel，我们就能猜Hello或者Help，再把猜的内容继续异或，又能再往下发现一点flag。拿出发现的flag再异或，又能发现一段文字，继续猜直到flag出现。

这里就用一个[脚本](https://github.com/SpiderLabs/cribdrag)来实现了。python2的，而且破解过程非常折磨人，就不建议各位亲自试了，毕竟也不是技术活。官方推荐使用cryptanalib库，下次可以试试。

- ### Flag
  > ALEXCTF{HERE_GOES_THE_KEY}
