# crackme

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=17497be7-120a-4c50-a7e3-b73b4e58d258_2)

这题没什么说的，唯一的考点就是脱壳。提供非常详细的[wp](https://blog.csdn.net/xiao__1bai/article/details/120230397)，如果不想看这么长的也可以去[ctf wiki](https://ctf-wiki.org/reverse/windows/unpack/esp/)简单了解一下esp定律。

不过我没脱壳工具。破电脑下载不了东西啊。脱壳后的程序是一个简单的异或加密，找到key和数据很容易就能复原了。

```python
byte_402130 = "this_is_not_flag"
dword_402150 = [ 0x12, 4, 8, 0x14, 0x24, 0x5C, 0x4A, 0x3D, 0x56, 0x0A, 0x10, 0x67,
0, 0x41, 0, 1, 0x46, 0x5A, 0x44, 0x42, 0x6E, 0x0C, 0x44, 0x72, 0x0C, 0x0D,
0x40, 0x3E, 0x4B, 0x5F, 2, 1, 0x4C, 0x5E, 0x5B, 0x17, 0x6E, 0x0C, 0x16, 0x68,
0x5B, 0x12, 0, 0, 0x48 ]

x = ''

for i in range(0,42):
    x += chr(dword_402150[i]^ord(byte_402130[i%16]))

print(x)
```

- ### Flag
  > flag{59b8ed8f-af22-11e7-bb4a-3cf862d1ee75}