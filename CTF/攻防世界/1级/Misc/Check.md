# Check

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f89e09ca-13c4-11ed-9802-fa163e4fa66d&task_category_id=1)

记录16进制的另一种形式。

stegsolve发现是lsb隐写，没啥说的，例行检查。不过我第一时间没看出来这是啥。

- &#x6  6;\&#x6c;  \&#x61;&#  x67;&#x7  b;\&#x68;  \&#x30;&#  x77;&#x5  f;\&#x34;  \&#x62;&#  x6f;&#x7  5;\&#x54;  \&#x5f;&#  x65;&#x6  e;\&#x63;  \&#x30;&#  x64;&#x6  5;\&#x5f;  \&#x34;&#  x6e;&#x6  4;\&#x5f;  \&#x70;&#  x6e;&#x4  7;&#x7d

就在我打到markdown里面的时候还被识别成字符了。确实如此，搜索发现就是unicode，但是是hex形式。cyberchef的fromhex选项直接搞定。

- ### Flag
  > flag{h0w_4bouT_enc0de_4nd_pnG}