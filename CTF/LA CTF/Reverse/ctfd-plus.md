# ctfd-plus

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/rev/ctfd-plus)

We were given an ELF file.Open it with Ida, the Ida, the main function is pretty simple.

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  size_t v3; // rax
  __int64 v4; // rsi
  unsigned int *v5; // r8
  char v7[264]; // [rsp+0h] [rbp-108h] BYREF

  puts("Welcome to CTFd+!");
  puts("So far, we only have one challenge, which is one more than the number of databases we have.\n");
  puts("Very Doable Pwn - 500 points, 0 solves");
  puts("Can you help me pwn this program?");
  puts("#include <stdio.h>\nint main(void) {\n    puts(\"Bye!\");\n    return 0;\n}\n");
  puts("Enter the flag:");
  fgets(v7, 256, stdin);
  v3 = strcspn(v7, "\n");
  v4 = 0LL;
  v5 = (unsigned int *)&unk_4060;
  v7[v3] = 0;
  do
  {
    if ( (unsigned __int8)sub_1230(v5[v4]) != v7[v4] )
    {
      puts("Incorrect flag.");
      return 0LL;
    }
    ++v4;
  }
  while ( v4 != 47 );
  puts("You got the flag! Unfortunately we don't exactly have a database to store the solve in...");
  return 0LL;
}
```

v7 is the variable that stores our input.In the if statement, we can see each character of v7 was used to compare with the return value of sub_1230.The parameter of sub_1230 is v5, or unk_4060.Take a closer look at sub_1230.

```c
__int64 __fastcall sub_1230(unsigned int a1)
{
  int v1; // eax
  int i; // ecx
  int v3; // edi

  v1 = 0;
  for ( i = 0; i != 32; ++i )
  {
    v3 = __ROR4__(a1 * a1, i);
    a1 = v1 ^ (4919 * v3 + 69210935);
    v1 += 322376503;
  }
  return HIBYTE(a1) + a1 + HIWORD(a1) + (a1 >> 8);
}
```

Although it's easy, the pseudocode of Ida is hard for me to run the same codes myself.So I decided to debug it, extracting the return value of sub_1230.Using pwntools and gdb, we can write the following script.

```python
from pwn import *
#context.log_level='debug'
payload=b'lactf{'
while True:
    p=process("gdb") #Open gdb.
    p.sendlineafter("(gdb)","file ctfd_plus") #Specify the file.
    p.sendlineafter("(gdb)","b strcspn") #The file uses PIE, so I have to break on a system function, then calculate the base address of the file.
    p.sendlineafter("(gdb)","r") #Run file.
    p.sendlineafter("flag:",payload)
    p.sendlineafter("(gdb)","i s") #Check the stack information, it contains the real address of main function.
    res=p.recvuntil("(gdb)",drop=True)
    main_addr=int(res.split(b'@entry\x1b[m=')[1].split(b", \x1b[36margc=argc")[0],16) #With debugging, I found that I can get the address of main function like this.
    main_offset=0x1070
    base=main_addr-main_offset
    p.sendline(f"b *{base+0x126b}") #Set a breakpoint on the last line of the sub_1230 function.
    for i in range(len(payload)+1):
        p.sendlineafter("(gdb)","c")
    p.sendlineafter("(gdb)","i r") #Check the registers. The return value of each function will be stored in rax. According to the debugging, it is found that the last byte of rax is the flag.
    res=chr(int(p.recvuntil('\n').split(b"          ")[1][-2:],16)).encode()
    payload+=res
    print(payload)
    p.close()
```

Wait for a while, then we get the flag.

## Flag
> lactf{m4yb3_th3r3_1s_s0m3_m3r1t_t0_us1ng_4_db}