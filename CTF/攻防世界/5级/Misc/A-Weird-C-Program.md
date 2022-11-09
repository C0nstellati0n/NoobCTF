# A-Weird-C-Program

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=432ad852-89f9-4ec8-ad45-bc322e8c27e3_2)

类似的套路之前见过，不过当时没有记录下来。今天补上。

拿到一个c++程序，程序在干啥我倒是没看，毕竟不懂c++。里面有句英语还是能懂的，提示要有发现不完美的眼睛。vscode很给力，选中一些奇怪的空白，能看出来空格的制表符的区别。必定是用这俩看起来很像的玩意藏二进制了。写个脚本。

```python
with open("ctf.cpp") as f:
    data=f.readlines()
flag=''
for i in data:
    for j in i:
        if j=='\t':
            flag+='1'
        elif j==' ':
            flag+='0'
    flag+=' '
flag=flag.split(' ')
for i in flag:
    if len(i)>5:
        print(chr(int(i,2)),end='')
```

注意这道题要按行来添加0和1，按8这个长度是出不来的。制表符和空白格隐写已经不新鲜了，以后看见任何奇怪空白的东西都要往这里怀疑一下。

## Flag
> flag{WpUAItsadmhak}