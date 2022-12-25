# [ZJCTF 2019]Login

[题目地址](https://buuoj.cn/challenges#[ZJCTF%202019]Login)

本题是划时代的一题。因为从这题开始我有ida用了！因此不会再放出代码了，毕竟ida大家都看得到（其实根本原因是我复制不出来）。

c++，之前没搞过c++的pwn啊，完全不会。看了[wp](https://www.cnblogs.com/Theffth-blog/p/12674951.html)才知道这道题其实非常简单。我们先在左侧的funcion window看一眼，能找到一个名为`Admin::shell`的函数，点进去可以知道是个后门。那这题的一个可能思路就是找溢出点然后覆盖返回地址为后门。

关注和接收输入有关的函数`User::read_name`和`User::read_password`。不幸的是两个函数都只会往s接收0x4f大小的数据，而s距离ebp有整整0x60。现在只能把所有函数都看一遍，找找有没有猫腻。

在签名比较长的`password_checker`函数中，一个奇怪的函数调用方式应该能引起你的注意。第11行代码取出a1这个2级指针指向的东西然后当作函数调用。什么玩意，这个函数里根本就没有a1啊？遇到这种情况说明我们要看一下汇编代码了。可以清楚地看到一句`call rax`。有点意思，找一下rax中的值是哪里来的。上面的mov语句把rax赋值为`rbp+var_68`，在最上面的变量声明中可以知道var_68单纯就是`-0x68`而已。再往上看还有一句mov将`rbp+var_68`赋值为rdi。rdi大家都熟悉，当前函数的第一个参数。查找当前函数引用，得知第一个参数是main函数里的v8变量。v8又来自于password_checker的返回值。

到这似乎就卡住了。password_checker的参数是v3，不是我们能够控制的。然而这题就是要教你看汇编代码的重要性。查看password_checker的汇编，加上我们知道rax寄存器里存着函数返回值这个知识点，可以看见rax=rbp+var_18。接下来是关键：由于这里的函数都是在main()函数中调用的，所以password_checker()函数退栈后，read_password()函数在同一位置开栈（被调用函数都在同一位置上开栈）。这句话表明虽然我们不能控制password_checker()函数的rbp+var_18，但是read_password()函数里可以啊，正好s是可以溢出到var_18的。两者差距0x68-0x18=0x48，正确密码长14，我们还需要58个填充字符。

```python
from pwn import *
p=remote('node4.buuoj.cn',28967)
system_call=0x400e88
payload=b'2jctf_pa5sw0rd'+b'\x00'*58+p64(0x400E88)
p.sendline("admin")
p.sendline(payload)
p.interactive() 
```

## Flag
> flag{47079381-af67-410a-aab1-b08b7bb4a0bb}