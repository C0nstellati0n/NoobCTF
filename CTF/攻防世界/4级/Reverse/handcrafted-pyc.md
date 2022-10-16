# handcrafted-pyc

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=116db784-e981-4e67-8898-a22b8872c1c0_2)

这个世界有各种类型的汇编，总会漏几个学不到的。所以我选择直接摆烂不学了:-)

附件没有后缀，file命令先查看一下是什么文件。

```bash
file 10315a5543d0464a9c13fa750bd79d9d.py_bc552f58fe2709225ca0768c131dd14934a47305
10315a5543d0464a9c13fa750bd79d9d.py_bc552f58fe2709225ca0768c131dd14934a47305: Python script text executable, ASCII text, with very long lines (1006), with CRLF line terminators
```

就是普通的python脚本。里面的内容也很普通。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marshal, zlib, base64

exec(marshal.loads(zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ=='))))
```

好像也不是很普通。打印了一下b64decode的内容，全是乱码。[zlib](https://docs.python.org/zh-cn/3/library/zlib.html)和[marshal](https://docs.python.org/zh-cn/3/library/marshal.html)搭配起来应该是读取机器码。头疼，真的头疼。zlib解压，marshal反序列化，我尝试打印反序列化后的内容无果，那就打印解压后的结果试试。发现打印出来的内容很像平时看到的pyc文件了。保存一下反编译看看(记得用python2）。

```python
import base64
import zlib
data=zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ=='))
with open("ctf.pyc",'w') as f:
    f.write(data)
```

然而没法反编译。查[wp](https://blog.csdn.net/xiao__1bai/article/details/120568154)，原来是少了文件头。差的文件头如下：

- 03 F3 0D 0A

这是python2生成的pyc文件的标准文件头，python3会不一样。其实是有8个字节的，但是后4个字节是时间戳，不同的会不一样。我靠网站没编译出来，于是找到了个直接出内容的办法。python不是自带了字节码反编译器[dis](https://docs.python.org/zh-cn/3/library/dis.html)吗？直接用不就行了（还是python2）？

```python
import base64
import zlib
import marshal
import dis
data=marshal.loads(zlib.decompress(base64.b64decode('eJyNVktv00AQXm/eL0igiaFA01IO4cIVCUGFBBJwqRAckLhEIQmtRfPwI0QIeio/hRO/hJ/CiStH2M/prj07diGRP43Hs9+MZ2fWMxbnP6mux+oK9xVMHPFViLdCTB0xkeKDFEFfTIU4E8KZq8dCvB4UlN3hGEsdddXU9QTLv1eFiGKGM4cKUgsFCNLFH7dFrS9poayFYmIZm1b0gyqxMOwJaU3r6xs9sW1ooakXuRv+un7Q0sIlLVzOCZq/XtsK2oTSYaZlStogXi1HV0iazoN2CV2HZeXqRQ54TlJRb7FUlKyUatISsdzo+P7UU1Gb1POdMruckepGwk9tIXQTftz2yBaT5JQovWvpSa6poJPuqgao+b9l5Aj/R+mLQIP4f6Q8Vb3g/5TB/TJxWGdZr9EQrmn99fwKtTvAZGU7wzS7GNpZpDm2JgCrr8wrmPoo54UqGampFIeS9ojXjc4E2yI06bq/4DRoUAc0nVnng4k6p7Ks0+j/S8z9V+NZ5dhmrJUM/y7JTJeRtnJ2TSYJvsFq3CQt/vnfqmQXt5KlpuRcIvDAmhnn2E0t9BJ3SvB/SfLWhuOWNiNVZ+h28g4wlwUp00w95si43rZ3r6+fUIEdgOZbQAsyFRRvBR6dla8KCzRdslar7WS+a5HFb39peIAmG7uZTHVm17Czxju4m6bayz8e7J40DzqM0jr0bmv9PmPvk6y5z57HU8wdTDHeiUJvBMAM4+0CpoAZ4BPgJeAYEAHmgAUgAHiAj4AVAGORtwd4AVgC3gEmgBBwCPgMWANOAQ8AbwBHgHuAp4D3gLuARwoGmNUizF/j4yDC5BWM1kNvvlxFA8xikRrBxHIUhutFMBlgQoshhPphGAXe/OggKqqb2cibxwuEXjUcQjccxi5eFRL1fDSbKrUhy2CMb2aLyepkegDWsBwPlrVC0/kLHmeCBQ==')))
print(dir(data))
dis.dis(data)
dis.dis(data.co_consts[1])
```

[dir](https://www.runoob.com/python/python-func-dir.html)可以查看当前范围内的变量、方法和定义的类型列表等。co_consts中就有反编译出来的主要部分代码。有点长就不放了，几千多行，全是python字节码。不会，抄一段内容记录一下。

```
Python字节码结构如下：
源码行号 | 跳转注释符 | 指令在函数中的偏移 | 指令符号（助记符） | 指令参数 | 实际参数值
.
字节码操作的详细信息：
starts_line（源码行号）：以此操作码开头的行（如果有），否则 None
is_jump_target（跳转注释符）：True 如果其他代码跳转到这里，否则 False
Offset（指令在函数中的偏移）：字节码序列中操作的起始索引
opcode：操作的数字代码，对应于下面列出的操作码值和操作码集合中的字节码值。
opname（指令符号（助记符））：人类可读的操作名称
arg（指令参数）：操作的数字参数（如果有），否则 None
argval：解析的 arg 值（如果已知），否则与 arg 相同
Argrepr（实际参数值）：操作参数的人类可读描述
.
例如：
1 0 LOAD_GLOBAL 0 ‘chr’
该字节码指令在源码中对应1行
此处不是跳转
0该字节指令的字节码偏移
操作指令对应的助记符为LOAD_GLOBAL
指令参数为0
操作参数对应的实际值为’chr’
.
LOAD_GLOBA：将全局变量co_names[namei]加载到堆栈上。这里是第0个变量
LOAD_FAST(var_num)：将对本地co_varnames[var_num]的引用推入堆栈。一般加载局部变量的值，也就是读取值，用于计算或者函数调用传参等。
STORE_FAST(var_num)：将TOS存储到本地co_varnames[var_num]中。一般用于保存值到局部变量。
LOAD_CONST：推入一个实整数值到计算栈的顶部。，比如数值、字符串等等，一般用于传给函数的参数。这里是108。
.
ROT_TWO：交换最顶部的两个堆栈项。
BINARY_ADD：二元运算从堆栈中删除堆栈顶部 (TOS) 和第二个最顶部堆栈项 (TOS1)。他们执行操作，并将结果放回堆栈中，实施.TOS = TOS1 + TOS。这里是两个字符的相加，而不是ASCII码数字的相加。
```

看这些机器码，大部分都是ROT_TWO和BINARY_ADD的搭配。看最开始一小部分就知道是什么套路了。

```python
0 LOAD_GLOBAL              0 (chr)
3 LOAD_CONST               1 (108)
6 CALL_FUNCTION            1
9 LOAD_GLOBAL              0 (chr)
12 LOAD_CONST               1 (108)
15 CALL_FUNCTION            1
18 LOAD_GLOBAL              0 (chr)
21 LOAD_CONST               2 (97)
24 CALL_FUNCTION            1
27 LOAD_GLOBAL              0 (chr)
30 LOAD_CONST               3 (67)
33 CALL_FUNCTION            1
36 ROT_TWO             
37 BINARY_ADD          
38 ROT_TWO             
39 BINARY_ADD          
40 ROT_TWO             
41 BINARY_ADD          
```

108是l，97是a，67是C。CALL_FUNCTION指的是调用chr函数，LOAD_GLOBAL里有提到chr（虽然不知道是不是这种关系）。把这些值压栈后顺序如下：

```
l
l
a
C
```

不知道为什么先压进去的反而在栈顶，可能就是这么规定的吧。36行开始操作，将顶上2个字符交换位置，然后相加，存到栈顶。

```
ll
a
C
```

38继续交换顶上2个。

```
a
ll
C
```

39行相加。

```
all
C
```

交换后相加。

```
Call
```

后面基本都是这样，加载值，然后交换相加。倒是可以写个脚本帮我们做这些操作，但是仔细想想，这些代码就相当于美加载4个字符后倒序拼在一起，我们看看这些加载的字符都是啥？把刚刚打印出来的内容复制后保存到另一个文件里,然后用下面的脚本[正则](https://blog.csdn.net/u010412858/article/details/83062200)匹配数字。

```python
import re
with open("ctf.txt") as f:
    data=f.read().split('\n')
for i in data:
    if 'LOAD_CONST' in i:
        print(chr(int(re.findall("\d+",i)[-1])),end='')
```

得到的内容如下。

- llaC em yP aht notriv lauhcamni !eac Ini npreterP tohty ntybdocese!!!ctihN{noy woc uoc naipmoa eldnur yP nnohttyb doceni euoy rb ria}!napwssro :dorWp gnssadrow...elP  esa yrtaga .ni oD tonurbf etecro)= 

看见flag了，但是我发现不仅仅是翻转4个字符那么简单。还是抄了wp。

```python
with open("ctf.txt",'r') as f:
    line = []
    for i in range(1000):
        line.append(f.readline())#加载1000行指令
        
def ROT_TWO(List): #定义ROT_TWO函数
    a = List.pop()
    b = List.pop()
    List.append(a)
    List.append(b)
    return List

def BINARY_ADD(List): #定义BINARY_ADD函数
    a = List.pop()
    b = List.pop()
    List.append(b+a)
    return List

cipher ="llaC em yP aht notriv lauhcamni !eac Ini npreterP tohty ntybdocese!!! ctihN{noy woc uoc naipmoa eldnur yP nnohttyb doceni euoy rb ria}!napwssro :dorWp gnssadrow...elP  esa yrtaga .ni oD tonurbf etecro)= ."

cipher = list(cipher)

s =[]
j=0
for i in line:
    if 'LOAD_CONST' in i and j < len(cipher):
        s.append(cipher[j])
        j += 1
    elif 'ROT_TWO' in i:
        s = ROT_TWO(s)
    elif 'BINARY_ADD' in i:
        s = BINARY_ADD(s)
print (s)
```

注意此处的ctf.txt和之前不一样了，把main函数部分删掉，也就是把  1           0 LOAD_GLOBAL              0 (chr)这段内容前面的东西全删掉。之前没删导致跑不出来。

- ### Flag
  > hitcon{Now you can compile and run Python bytecode in your brain!}