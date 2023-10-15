# H■m■i■g

此为比赛途中个人分析。

附件两个脚本一个输出。输出有点长就不放了，脚本如下。

```python
from secret import mytext#It's in alice's device. We can't know!
from polar_router import send_over_weak_noisy_channel#how it works doesn't matter, u don't need this lib
from Crypto.Util.number import bytes_to_long
from functools import reduce

def hamming_encode(bitsblock):#do u know how it works?
    for t in range(4):
        bitsblock[1<<t]=reduce(
            lambda x,y:x^y ,
            [bit for i,bit in enumerate(bitsblock) if i&(1<<t)]
            )
    return bitsblock

bintxt=bin(bytes_to_long(mytext))[2:]
lenbintxt=len(bintxt)
assert lenbintxt%11==0
blocks=lenbintxt//11
bitlist=list(map(int,bintxt))
raw_msg=[[0]*3+[bitlist[i]]+[0]+bitlist[i+1:i+4]+[0]+bitlist[i+4:i+11] for i in range(0,lenbintxt,11)]

encoded_msg=[hamming_encode(raw_msg[i]) for i in range(blocks)]

send_over_weak_noisy_channel(encoded_msg)#send it
```

```python
from polar_router import recv_over_weak_noisy_channel#how it works doesn't matter, u don't need this lib, just ignore it
from Crypto.Util.number import long_to_bytes#really useful! 

def hamming_correct(bitblock):
    #you should write this function, to help polar decode the msg
    #Good luck and take it easy!
    for i in range(4):
        bitblock[1<<t]
    pass

def decode(msg):
    blocks=len(msg)
    bitlist=[]
    #Let's cancel the noise...
    for i in range(blocks):
        wrongbitpos=hamming_correct(msg[i])
        msg[i][wrongbitpos]=int(not msg[i][wrongbitpos])
        #add corrected bits to a big list
        bitlist.extend([msg[i][3]]+msg[i][5:8]+msg[i][9:16])
    #...then, decode it!
    totallen=len(bitlist)
    bigint=0
    for i in range(totallen):
        bigint<<=1
        bigint+=bitlist[i]
    return long_to_bytes(bigint)

noisemsg=recv_over_weak_noisy_channel()#it's a big matrix!
msg=decode(noisemsg)
print(msg)#Well done
```

先看看加密咋做的。把flag转为数字后再转成二进制，二进制内容的长度可以被11整除。blocks是每块长度11能分成的块数。

- ### map
  > 根据提供的函数对指定序列做映射。第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
  - 语法：map(function, iterable, ...)
  - 参数
    > function -- 函数<br>iterable -- 一个或多个序列
  - 返回一个迭代器，可使用 list() 转换为列表

bitlist=list(map(int,bintxt))遍历bintxt的每一个字符，将其转换为int列表的元素。比如"0101"转换后就变成了[0,1,0,1]。出题人超级喜欢列表生成式，确实很简洁，就是做题不是很快乐。raw_msg=[[0]*3+[bitlist[i]]+[0]+bitlist[i+1:i+4]+[0]+bitlist[i+4:i+11] for i in range(0,lenbintxt,11)] 遍历lenbintxt//11次，i的值从0开始，步长为11。这个式子生成一个名叫raw_msg的列表，列表的每一项为[0,0,0,bitlist[i],0,bitlist[i+1:i+4],0,bitlist[i+4:i+11]]。作用就是从列表索引1和4的位置把bitlist的每一项分成三块，第一块前面补3个0，第一块和第二块和第三块中间各有一个0。

目前看不出用途。这块的逆向也不是我们要干的，因为第二个脚本的decode已经将这一步逆向了，我们要做的只有逆向hamming_encode，看起来很简单实际上很绕，刚刚试了一下没出来，边写笔记边想看看能不能？

```python
def hamming_encode(bitsblock):#do u know how it works?
    for t in range(4):
        bitsblock[1<<t]=reduce(
            lambda x,y:x^y ,
            [bit for i,bit in enumerate(bitsblock) if i&(1<<t)]
            )
    return bitsblock
```

当然要先理解函数。lambda就不说了，匿名函数，参数为x，y，返回值为x^y。

- ### enumerate
  > 将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
  - 语法：enumerate(sequence, [start=0])
  - 参数
    > sequence -- 一个序列、迭代器或其他支持迭代对象。<br>start -- 下标起始位置的值。

- ### reduce
  > 对参数序列中元素进行累积。函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（有两个参数）先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算，最后得到一个结果。
  - 语法：reduce(function, iterable[, initializer])
  - 参数
    > function -- 函数，有两个参数<br>iterable -- 可迭代对象<br>initializer -- 可选，初始参数

这个函数的参数是raw_msg的每一项。[bit for i,bit in enumerate(bitsblock) if i&(1<<t)]这个列表生成式遍历参数bitsblock的每一项，如果第t位的i是1，就把i对应索引的元素添加到返回值列表中。if语句的作用是筛选元素，i&(1<<t)是个二进制下的[小技巧](https://stackoverflow.com/questions/41629583/what-does-the-statement-if-counter-1j-mean-and-how-does-it-work)，作用就是检查第i的第t位是否为1。如果是1那么整个表达式的结果不会为0，python中非0的数字都是True。

可以肯定的是 1<<t 这个表达式的值每次调用函数都是一样的，因为t固定为0-3，1<<t 就固定为1，2，4，8。等于密文的每一行只会有第1，2，4，8个元素被加密了。问题进一步缩小，怎么还原第1，2，4，8位？密文来自于x^y，异或的值就两种，0或1。x和y来自于那个列表生成式。最终问题是怎么利用这个列表生成式找到被加密位的原值？

接下来我不会了，开始胡乱分析。明文和密文有两种情况，明文加密后仍然保留原值或为取反值。可是加密值跟全部列表中的元素都有关系，似乎并没有办法逆向。探索一下每次列表中的元素是什么试试。

```python
def hamming_encode(bitsblock):#do u know how it works?
    for t in range(4):
        bitsblock[1<<t]=reduce(
            lambda x,y:x^y ,
            [bit for i,bit in enumerate(bitsblock) if i&(1<<t)]
            )
        test=[]
        for i in range(len(bitsblock)):
            if i&(1<<t):
                test.append(i)
        print(test)
    print()
    return bitsblock
```
可以发现test记录的索引每次函数运行也都是一样的。正常因为t之前就说过不会变了。每次运行都是这个值。

- [1, 3, 5, 7, 9, 11, 13, 15]
<br>[2, 3, 6, 7, 10, 11, 14, 15]
<br>[4, 5, 6, 7, 12, 13, 14, 15]
<br>[8, 9, 10, 11, 12, 13, 14, 15]

打出来我们可以发现，就算第一次for循环改变了索引为1元素的值，也不会影响后面的元素加密。拿第一个列表推算一下。设x为索引1对应的值，y为索引3, 5, 7, 9, 11, 13, 15的元素的异或的结果，x^y=z，z可从密文索引1获取，y同理，那z^y不就等于x了吗？开始搞解密脚本。

我写完了决定运行测试的时候发现不符合decode方法的要求。我仔细一看才发现decode方法要求hamming_correct返回错误的bit索引，关键一行只会调用一次，意味着只有一个是错的。啊？完全跟我想的不一样。估计我是在哪里想错了。分析一下这个函数先。

```python
def decode(msg):
    blocks=len(msg)
    bitlist=[]
    #Let's cancel the noise...
    for i in range(blocks):
        wrongbitpos=hamming_correct(msg[i])
        msg[i][wrongbitpos]=int(not msg[i][wrongbitpos])
        #add corrected bits to a big list
        bitlist.extend([msg[i][3]]+msg[i][5:8]+msg[i][9:16])
    #...then, decode it!
    totallen=len(bitlist)
    bigint=0
    for i in range(totallen):
        bigint<<=1
        bigint+=bitlist[i]
    return long_to_bytes(bigint)
```

- ### extend
  > 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。
  - 语法：list.extend(seq)
  - 参数：seq -- 元素列表。
  - 该方法没有返回值，但会在已存在的列表中添加新的列表内容。

跟append的区别是append会增加一个新元素，extend会把同一个列表延长。bigint<<=1等同于begint=begint<<1。我开始疑惑了，bitlist.extend([msg[i][3]]+msg[i][5:8]+msg[i][9:16])很明显是去掉之前加的0，那下面的for循环是什么意思？如果bitlist本来就是解密后的二进制flag，那这一步作用是什么呢？

还发现bigint+=bitlist[i]这一步不是单纯末尾追加，这是int所以是相加。这个方法的实现应该是没错的（如果这个是题目准备的混淆项我直接自闭），我需要多分析一下。

我知道那个for循环啥意思了，输出等同于下面这个写法。

```python
#bigint=0
bigint=''
for i in range(totallen):
    #bigint<<=1
    bigint+=str(bitlist[i])
    #bigint+=bitlist[i]
#return long_to_bytes(bigint)
return long_to_bytes(int(bigint,2))
```

就离谱，像我一样的小白不试一下根本看不出来。但是flag不对，还原出来的内容能看出来一点语气和词汇，但是肯定不对。注释有写teke it easy，应该是我想复杂了。可是每次都有四种改变的可能，我怎么知道哪一个被真正改变了？

假设有这样一个列表[x,0,1,1,0,1,0,0],它们的异或结果是1。也就是x^0^1^1^0^1^0^0=1。倒过来求x就是1^0^0^1^0^1^1^0，结果为0。我还发现当有偶数个1的时候结果必为0，奇数个则必为1。0的数量无所谓。这会是突破点吗？我多造几个例子试试。

现在很奇怪的事情出现了,我自己乱写了个明文然后测试，但是复原结果是正确的。

```python
from functools import reduce
def hamming_encode(bitsblock):#do u know how it works?
    for t in range(4):
        bitsblock[1<<t]=reduce(
            lambda x,y:x^y ,
            [bit for i,bit in enumerate(bitsblock) if i&(1<<t)]
            )
    return bitsblock
bintxt='01001001001010010010011001001001010101000101'
print(bintxt)
lenbintxt=len(bintxt)
assert lenbintxt%11==0
blocks=lenbintxt//11
bitlist=list(map(int,bintxt))
raw_msg=[[0]*3+[bitlist[i]]+[0]+bitlist[i+1:i+4]+[0]+bitlist[i+4:i+11] for i in range(0,lenbintxt,11)]
encoded_msg=[hamming_encode(raw_msg[i]) for i in range(blocks)]
def hamming_correct(bitblock):
    #you should write this function, to help polar decode the msg
    #Good luck and take it easy!
    data=[[1, 3, 5, 7, 9, 11, 13, 15]
            ,[2, 3, 6, 7, 10, 11, 14, 15]
            ,[4, 5, 6, 7, 12, 13, 14, 15]
            ,[8, 9, 10, 11, 12, 13, 14, 15]]
    for i in range(4):
        current_data=data[i]
        cipher=bitblock[current_data[0]]
        for j in range(len(current_data)-1,0,-1):
            cipher=cipher^bitblock[current_data[j]]
        bitblock[1<<i]=cipher
    return bitblock
def decode(msg):
    blocks=len(msg)
    bitlist=[]
    #Let's cancel the noise...
    for i in range(blocks):
        #wrongbitpos=hamming_correct(msg[i])
        #msg[i][wrongbitpos]=int(not msg[i][wrongbitpos])
        #add corrected bits to a big list
        msg[i]=hamming_correct(msg[i])
        bitlist.extend([msg[i][3]]+msg[i][5:8]+msg[i][9:16])
    #...then, decode it!
    totallen=len(bitlist)
    bigint=''
    for i in range(totallen):
    #bigint<<=1
        bigint+=str(bitlist[i])
    print(bigint)
decode(encoded_msg)
```

decode方法打印出来的内容等于bintxt。这么诡异的吗？更诡异的还在后头：我尝试解码附件的noisemsg，将得到的内容再进行加密，发现加密结果不等于noisemsg，但再次解密加密的结果的结果等于得到的内容。这我上哪说理去啊？

新进展。之前提到被更改的的可能位置为1，2，4，8。但是1，2，4，8位是raw_msg添加的0位啊，最后decode会被剔除掉的，也就是这几位根本不重要。我在没有调用自己写的解码函数的情况下直接调用decode的打印结果和调用了是一样的。理论上应该直接把那几位去掉就得到flag了，实际却没有。有点奇怪了，加密函数我已经看了很多遍了，也做了实验，还有哪里被我漏掉了？这题最烦的地方是bintxt的长度一定要为11的倍数，没办法随便举个例子进行实验。

我利用脚本进行爆破，找到了aaaaaaa这个明文串的bintxt长度为11的倍数。最诡异的事情发生了：把这串字符按照给的加密算法进行加密后再解密，成功了。至此不是有点诡异了，是很诡异了。难道那串乱码就是结果？

不对，noisemsg有几行是以1开头的，比如这行：[1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0]根据我们之前的推理，第0位索引的元素只能是0。让我找个更随机的字符串继续做实验。

新字符串aOhbuKz，仍然成功。我真的不懂啊，继续。

aNiilBugbxtYQMBgifQNQxntjExjEDvkRQcrlyWWnklCxNvpebWDYyIaVvqHjKLuymHRhXoZkBCMdaSPXykkOnKnsGJIJuscbZkLxVIFoHZLfICSITRlNAFQKzqoKjIWvEiSUXOEaAFCbwBVoKTXaNRaHuJWYwXzPjnfpBZOWlOELuHcJbrpYJgqecccCxltmSFonEJiHlZXB 这个字符串都成功了还有啥啊？你flag还能比这个长？加点符号和数字试试。

aNS95v72EkSRiGkBrGdDexmRoEFldaTwtO516aCy6pOACpN2IzG8IrPV7HmBgqxNqbdQTnbASQn6bkE7}}MjEMsFmatuct8HEP4kkVEDcFGzeF7uSilqNF}fjPgun650J5hqz8S69amUO}ToB4STlwTFEzvQWmHYYWqmVouxG5S3djl6SvnhFR39JJxxakBN64SnKuD98}caUm23RNot6vA3 也成功了。这我真不会了。

两个星期后我突然有了想法。给的noisemsg是通过send_over_weak_noisy_channel这个函数拿到的。虽然不知道这个函数是干啥的，不过看看名字，加噪音的，作用可能是把加密后的内容进行混淆。把解密出来的内容再加密后补充的0位内容不一样，有可能就是噪音的原因。试一下吧。

怎么试？应该是先encode再加的噪音，这我怎么算？

继续问群里的大佬（按照这个速度迟早把整个群里的大佬都骚扰一遍），发现这是一种编码，叫[汉明码](https://blog.csdn.net/qq_19782019/article/details/87452394)，英文hamming code，也就是题目名称。是我笨了，我竟然没想到去搜一下题目名……孤陋寡闻完全没往这个方面去想。

文章里详细介绍了汉明码以及纠错的方式。自己写实现脚本就行了。

```python
def hamming_correct(bitblock):
    result=''
    for t in range(4):
        bits=[bit for i,bit in enumerate(bitblock) if i&(1<<t)]
        if bits.count(1)%2==0:
            result+='0'
        else:
            result+='1'
    return int(result[::-1],2)
```

代码丑陋但有用啊！看那篇文章用的是奇校验，这里用的好像是偶校验。多试试就行了，还原出密文如下。

- Once upon a time, there were 1023 identical bottles, 1022 of which were plain water and one of which was poison. Any creature that drinks the poison will die within a week. Now, with 10 mice and a week, how do you tell which bottle has poison in it? moectf{Oh_Bin4ry_Mag1c_1s_s0o_c0O1!} Great!

- ### Flag
  > moectf{Oh_Bin4ry_Mag1c_1s_s0o_c0O1!}