# rust

没读懂逻辑，但是隐隐约约觉得flag是一个字符一个字符检查的，可以直接爆破（能side channel谁逆向啊？）
```py
from string import ascii_lowercase, ascii_uppercase
flag='moectf{'
def Debug(p,file,breakpoints):
    p.sendlineafter("pwndbg>",f"file {file}")
    for i in breakpoints:
        p.sendlineafter("pwndbg>",f"b *{i}")
    p.sendlineafter("pwndbg>",f"r")
letters=ascii_lowercase+"_"+ascii_uppercase
while flag[-1]!='}':
    for letter in letters:
        p=process("gdb")
        Debug(p,"./rust",[0x55555555f930])
        p.sendlineafter("And please input the flag:\n",(flag+letter).ljust(30,'a'))
        for i in range(len(flag)):
            p.sendlineafter("pwndbg>","c")
        p.sendlineafter("pwndbg>","s")
        if p.recvline()!=b' \x01\x1b[0m\x1b[31m\x1b[0m\x0219\tin \x1b[32msrc/main.rs\x1b[m\n': #调试得到的奇怪结果
            flag+=letter
            print(flag)
            p.close()
            break
        p.close()
```
倒数第二个字符是1，爆破不出来（因为字符集为了之前爆破快没加上数字）。但是很容易推测出来是1

我好像知道为什么我逆向能力1年没长进了

## Flag
> moectf{Rust_rev_will_be_awfu1}