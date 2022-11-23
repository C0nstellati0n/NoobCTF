# [GWCTF 2019]pyre

[题目地址](https://buuoj.cn/challenges#[GWCTF%202019]pyre)

简单的代码也能有迷惑性。

pyc文件，uncompyle6反编译完事。

```python
print 'Welcome to Re World!'
print 'Your input1 is your flag~'
l = len(input1)
for i in range(l):
    num = ((input1[i] + i) % 128 + 128) % 128
    code += num

for i in range(l - 1):
    code[i] = code[i] ^ code[(i + 1)]

print code
code = ['\x1f', '\x12', '\x1d', '(', '0', '4', '\x01', '\x06', '\x14', '4', ',', '\x1b', 'U', '?', 'o', '6', '*', ':', '\x01', 'D', ';', '%', '\x13']
```

我最开始有点懵，input1是输入，虽然程序中没有明显的input1=input()这种代码。然而后面的code我就不懂了，以为直接是程序里面的，结果是期望输出。好吧，习惯把输出注释起来的出题方法了。异或的for语句很好逆向，倒着来就行了。像下面这样：

```
加密时：
a_=a^b
b_=b^c
c_=c^d

解密时：
c=d^c_
b=c^b_
a=b^a_
```

结果第一个for语句我看不出来怎么逆。其实分析一下会发现，循环每次取出input的每个字符的ord然后加上i，由于输入肯定是可见字符，故第一个模有两种情况。第一种`(input1[i]+i)%128`还是等于`(input1[i]+i)`（大小不足128），第二种`(input1[i]+i)%128`等于`(input1[i]+i)-128`，因为加上了i后超过了128。然后加上128，得到`(input1[i]+i)+128`或者`(input1[i]+i)`。最后再模128，得到`(input1[i]+i)+128%128`等于`(input1[i]+i)+128-128`，会发现直接就等于`(input1[i]+i)`。这是当第一个模是第一种情况的结果。如果是第二种情况就等于`(input1[i]+i)-128+128-128`,需要再加上128。不如我们之接全部加上128再模128处理第二种情况，而这样的处理也不影响第一种。

```python
code = ['\x1f', '\x12', '\x1d', '(', '0', '4', '\x01', '\x06', '\x14', '4', ',', '\x1b', 'U', '?', 'o', '6', '*', ':', '\x01', 'D', ';', '%', '\x13']
for c in range(len(code)-2,-1,-1):
    code[c]=chr(ord(code[c])^ord(code[c+1]))
for c in range(len(code)):
    num = (ord(code[c]) -c+128)%128
    print(chr(num),end='')
```

## Flag
> flag{Just_Re_1s_Ha66y!}