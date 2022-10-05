# babyheap

[题目地址](https://music.163.com/#/song?id=1319020350)

从这题开始连[答案](https://blog.csdn.net/seaaseesa/article/details/103173435)也抄不了了。等我几年后换个好点的电脑再补，现在的电脑就是纯纯废物，无法调试无法运行，不排除我也是废物的原因。

-   Arch:     amd64-64-little
    <br>RELRO:    Full RELRO
    <BR>Stack:    Canary found
    <BR>NX:       NX enabled
    <BR>PIE:      PIE enabled

麻了，大佬的世界太恐怖了。现在看到保护全开就ptsd。过一遍吧，我也不知道怎么做，可能是攻防世界那边换libc了还是什么,提示fastbin memory corruption。没关系，反正早就分析wp摆烂了。

```c
void main(EVP_PKEY_CTX *param_1)

{
  int iVar1;
  
  init(param_1);
  do {
    while( true ) {
      while( true ) {
        list();
        iVar1 = get_choice();
        if (iVar1 != 2) break;
        delete();
      }
      if (2 < iVar1) break;
      if (iVar1 == 1) {
        create();
      }
      else {
LAB_00100ca1:
        puts("Wrong choice");
      }
    }
    if (iVar1 != 3) {
      if (iVar1 == 4) {
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      goto LAB_00100ca1;
    }
    show();
  } while( true );
}
```

堆真的好难，一直不开窍，大概是对堆结构不熟的原因。这题倒简化了一点，只有删除，创建和打印，常见的修改操作没有，反而不是一件好事。

```c
void delete(void)

{
  uint uVar1;
  
  puts("Index: ");
  uVar1 = get_choice();
  if (uVar1 < 7) {
    free(*(void **)(heap_list + (ulong)uVar1 * 8));
    *(undefined8 *)(heap_list + (ulong)uVar1 * 8) = 0;
  }
  return;
}
```

无uaf。

```c
void create(void)

{
  int iVar1;
  void *__ptr;
  int i;
  
  puts("Size: ");
  iVar1 = get_choice();
  __ptr = malloc((long)iVar1);
  if (__ptr != (void *)0x0) {
    i = 0;
    while ((i < 7 && (*(long *)(heap_list + (long)i * 8) != 0))) {
      i = i + 1;
    }
    if (i == 7) {
      puts("List is Full!\n");
      free(__ptr);
    }
    else {
      puts("Data: ");
      read_input(__ptr,iVar1);
      *(void **)(heap_list + (long)i * 8) = __ptr;
    }
  }
  return;
}
```

最多只能创建7个堆块，创建时可输入数据。具体输入数据的实现如下。

```c
void read_input(long param_1,int param_2)

{
  ssize_t sVar1;
  long in_FS_OFFSET;
  char local_15;
  int i;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  for (i = 0; i < param_2; i = i + 1) {
    sVar1 = read(0,&local_15,1);
    if ((int)sVar1 < 0) {
      puts("Read error!\n");
    }
    if (local_15 == '\n') break;
    *(char *)(i + param_1) = local_15;
  }
  *(undefined *)(param_1 + i) = 0;
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

有个null off by one漏洞。这个漏洞很好理解，本来堆块的大小只有param_2，使用的for循环已经读入这么多数据了，最后还加了个0，导致新增的0溢出到下一个堆块。展示函数只是普通的打印数据，我们只有这个漏洞。

```c
void show(void)

{
  uint i;
  
  for (i = 0; (int)i < 7; i = i + 1) {
    if (*(long *)(heap_list + (long)(int)i * 8) != 0) {
      printf("%d : %s \n",(ulong)i,*(undefined8 *)(heap_list + (long)(int)i * 8));
    }
  }
  return;
}
```

首先肯定是泄露地址，基地址是一切的基础。既然只有堆溢出一个null字节的漏洞，我们就要想想有关堆溢出的特性。第一个问题：这个溢出的null去哪了？阅读glibc内存管理，可以知道chunk之间会发生空间共用，也就是下一个的chunk的prev_size域给当前chunk当做数据域使用，这种情况只出现在malloc的大小为8的奇数倍(32位为4的奇数倍)的情况。考虑到unsorted bin的表头会有libc中的main_arena+88的地址，我们先来点unsorted bin。

创建5个堆块，chunk0-4，chunk0、chunk1、chunk4大小在unsorted bin范围，chunk2-3 data域大小为0x68，总共0x70（chunk头也占几个字节），属于fastbin。当chunk0-4 free后就进入了unsorted bin，并且相邻的chunk会进行unlink合并。回答问题，假设我们让chunk3溢出，这个null会跑到chunk4的size域，覆盖低一字节位0，那么就标志了chunk4的前一chunk处于空闲状态。这时我们free chunk4，chunk4就会与它的前一chunk合并。glibc是如何定义前一chunk的？依赖于当前chunk的prev_size，由于chunk3的大小为0x68，是8的奇数倍，因此它会把chunk4的prev_size域作为数据域，因此,prev_size我们可以自己指定大小，比如(0x110+0x110+0x70+0x70 = 0x300)。两个条件配合，free时会合并会合并chunk0、chunk1、chunk2、chunk3、chunk4。

然而因为没有编辑功能，我们只能delete(3)后再重新create分配到那个位置，同时构造payload溢出到chunk4。不能一步做的原因比较简单，chunk4挨着chunk3分配，先构造payload溢出不到我们想要的地方，只能等chunk3和4排列好后delete chunk3再尝试溢出。毕竟fastbin后进先出，delete后再create还能得到一个位置的指针。

做到这一步时free会报错，因为chunk4的size被我们覆盖成了0x100，而原本是0x111，意味着现在按照之前的偏移取到的nextsize是chunk4数据域里偏移0x90+8处的数据，而不是下一个chunk的size。大佬的处理让我看不懂了：为了避免后续的其他类似的错误，我们把chunk4留下的那(0x110-0x100=0x10的空间伪装成一个chunk5)。

伪装后free就能成功了。目前fastbin里有chunk2（不是很懂chunk2怎么跑到的fastbin），待会fastbin attack能用到；而unsorted bin里因为unlink向前合并，只剩下一个chunk0，另外还有个main_arena+88，它们组成了双向链表。

现在，假如我们create(0x100)，那么glibc就会从unsorted bin中的表头(chunk0)处开始，切割出0x110的空间给我们，然后表头变成了chunk0+0x110。那么chunk0+0x110处的chunk的fd和bk会被设置为main_arena+88。等一下，chunk0 + 0x110不就是chunk1吗，还记得chunk1并没有被我们free，它只是参与了合并，因此它的指针存在于数组中，并没有被清0。那么，当我们show()的时候，就会把chunk1的fd值打印出来，从而泄露了main_arena+88的地址。

由于main_arena+88和malloc_hook物理位置上在同一页，并且靠的很近，因此，它们的地址只有后三位不一样，正好后3位不会变，我们在elf里看到的静态地址后3位和实际加载时是一样的。那么我们就能计算出malloc_hook的地址，接着计算出libc基地址，从而获取将要使用的gadget的地址。

现在一些需要的信息我们都得到了，我们接下来是想办法把gadget的地址写入到malloc_hook里，这样当程序再次malloc时，便会触发gadget，从而get shell。上fastbin attack，让系统分配一块靠近malloc_hook的区域，比如malloc_hook-0x23，这里最常用。这时候就是大佬的铺垫时刻了，chunk2大小0x68不是乱来的，之前也说过实际申请大小是0x70；而malloc_hook-0x23处偏移0x8处的数据为0x7F，与0x70大小相当。fastbin分配chunk时只检查chunk的size域是否符合要求，我们的chunk2的size也与目标大小相当，那么，我们想办法把chunk2的fd指向malloc_hook-0x23这个假chunk处，这样，chunk2和malloc_hook-0x23处构成了单向链表，当我们第二次申请0x68大小的堆时，就会申请到malloc_hook-0x23处。

很明显fastbin attack的要求是能覆盖到chunk2的fd。怎么做？假如我们create(0x118,payload),由于之前已经create(0x100)过一次，那么这次chunk分配的范围就是chunk0 + 0x110 ~ chunk0+0x110+0x128也就是chunk1~chunk2+0x18处，正好可以把chunk2的fd给覆盖了。堆重叠，关键就在于我们之前把这些chunk全部unlink了。

看似完成了，不不不，8分的题就这么被你白拿了那还得了？实际操作下，gadget因为栈的问题变得不可用,执行不成功。我们还要用进阶[mallocl_hook](https://blog.csdn.net/A951860555/article/details/115462494)搭配技巧——通过realloc_hook来调整堆栈环境使one_gadget可用。

realloc_hook开头有一堆push寄存器，相应的末尾有一堆pop寄存器。可以将realloc_hook设置为选择好的one_gadget，将malloc_hook设置为realloc函数开头某一push寄存器处。push和pop的次数是一致的，若push次数减少则会压低堆栈，改变栈环境。这时one_gadget就会可以使用。具体要压低栈多少要根据环境决定。经过测试，我们只需在realloc函数地址向下偏移2就可以使栈环境正常。

后面的事情不用多说，我没有做出来，可恶的[fastbin](https://blog.csdn.net/qq_29343201/article/details/66473140)。