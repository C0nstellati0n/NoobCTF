# streamgame1

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=2a4e8758-df1c-42b1-acf1-f33658de31c4_2&task_category_id=5)

我的crypto还是一如既往的菜。

题目附件是一个python脚本和一个key文件。key应该是被加密后的flag。脚本内容如下：

```python
from flag import flag
assert flag.startswith("flag{")
# 作用：判断字符串是否以指定字符或子字符串开头flag{
assert flag.endswith("}")
# 作用：判断字符串是否以指定字符或子字符串结尾}，flag{}，6个字节
assert len(flag)==25
# flag的长度为25字节，25-6=19个字节
#3<<2可以这么算，bin(3)=0b11向左移动2位变成1100，0b1100=12(十进制)
def lfsr(R,mask):
    output = (R << 1) & 0xffffff    #将R向左移动1位，bin(0xffffff)='0b111111111111111111111111'=0xffffff的二进制补码
    i=(R&mask)&0xffffff             #按位与运算符&：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0
    lastbit=0
    while i!=0:
        lastbit^=(i&1)    #按位异或运算符：当两对应的二进位相异时，结果为1
        i=i>>1
    output^=lastbit
    return (output,lastbit)



R=int(flag[5:-1],2)
mask    =   0b1010011000100011100

f=open("key","ab")   #以二进制追加模式打开
for i in range(12):
    tmp=0
    for j in range(8):
        (R,out)=lfsr(R,mask)
        tmp=(tmp << 1)^out   #按位异或运算符：当两对应的二进位相异时，结果为1
    f.write(chr(tmp))  #chr() 用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符。
f.close()
```

很贴心地写上了许多注释。按位左移可以逆向，逆向操作是右移；右移反之亦然。异或也可以逆向，操作是它自己，a^b=c,c^b=a。但是按位与&和按位或｜似乎是没有反向操作的，至少我没有搜到，实验也没成功。这里又是一个小经验：像这种给脚本的逆向一般有两种思路：常规的按已有逻辑逆向，或者直接爆破。爆破的情况适用于加密逻辑过于复杂，无法逆向，但是加密结果可能性较少且知道明文大概的格式。

爆破完全适用于这道题。注释里有写“flag的长度为25字节，25-6=19个字节”，而“R=int(flag\[5:-1],2)”这行代码告诉我们被加密的只有flag内部的内容，且flag一定是数字形式，毕竟非数字字符是没办法直接int的。int的第二个参数表示了int转换时使用的进制，说明原flag是19位的2进制数。

flag格式知道了，现在算可能性。n位的二进制数最多可以表示2的19次方那么多数字，不算太多。满足爆破条件，直接脚本。

```python
def check(list1, list2):
    for i in range(12):
        if list1[i] != list2[i]:
            return False
    return True
def lfsr(R ,mask):
    output = (R << 1) & 0xffffff    #将R向左移动1位，bin(0xffffff)='0b111111111111111111111111'=0xffffff的二进制补码
    i=(R&mask)&0xffffff             #按位与运算符&：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0
    lastbit=0
    while i!=0:
        lastbit^=(i&1)    #按位异或运算符：当两对应的二进位相异时，结果为1
        i=i>>1
    output^=lastbit
    return (output,lastbit)
with open("你的key文件地址",'rb') as f:
    content = f.read()
    s_list = []
    for c in content:
        s_list.append(c)
    mask = 0b1010011000100011100
    for i in range(1 << 19):
        tmp_list = []
        R = i
        for j in range(12):
            tmp = 0
            for k in range(8):
                (R, out) = lfsr(R, mask)
                tmp = (tmp << 1) ^ out  # 按位异或运算符：当两对应的二进位相异时，结果为1
            tmp_list.append(tmp)
 
        if (check(s_list, tmp_list)):
            print(bin(i))
            break
```
代码来自于[这里](https://www.codeleading.com/article/66904819141/)，因为自己写的不知道为啥跑不出来。加密逻辑基本抄原脚本，我们要添加的仅仅只有判断每次加密的结果是不是与已知密文相等。

- ### Flag
  > flag{1110101100001101011}