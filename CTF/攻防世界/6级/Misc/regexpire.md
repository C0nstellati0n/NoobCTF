# regexpire

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=5b51af72-d205-45cc-8250-d5be47771b46_2&task_category_id=1)

正则地狱。

看见题目怀疑了一下自己是不是看错分区了。没错确实是misc，可是为什么给了个nc地址？进去看看。

```
Can you match these regexes?
(phone|clementine)[Atm1hBBrmP]+[PLN.Fg7k]h(fish|potato)+I(cat|elephant)+(tomato|phone)qG[oxu4pEGuj]
Timeout
```

正则？不会是叫我输入匹配这些正则的字符串吧？如果说多查或者熟练正则的话，打出一个确实是没问题。然而我正则差到爆炸，关键看了[wp](https://blog.wujiaxing.cn/2019/09/25/e4a0a49e/)发现有1000轮要打。放弃挣扎，大佬不用任何外部库写出了下面的脚本。

```python
import socket,re

def recvuntil(s, tails="\n"):
    data = ""
    while True:
        for tail in tails:
            if tail in data:
                return data.strip('\n')
        data += s.recv(1).decode()

def sendline(s, solution, tail="\n"):
    s.sendall((solution + tail).encode())

def repzkh(matched):
    return '['+matched.group('chars')[0]+']'

def repxkh(matched):
    return '['+matched.group('chars')+']'

def repdkh1(matched):
    num = matched.group('num')
    if len(num) == 0:
        num = "0"
    return '{'+num+'}'

def repdkh2(matched):
    chars = matched.group('chars')
    num = matched.group('num')
    res = ''
    for i in range(int(num)):
        res += chars
    return res

def main():
    url = "61.147.171.105"# 换成自己的ip和端口
    port = 52788
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, port))
    print(recvuntil(s))

    count = 0
    while True:
        count += 1
        print("round %d----------------------------------------"%count)
        reg = recvuntil(s,['\n','Irregular'])
        print("reg: "+reg)
        if reg == 'Irregular':
            break
        elif reg.startswith("flag"):
            break

        match_string = get_match_string(reg)
        print("pre: "+match_string)
        sendline(s, match_string)
        # break
    s.close()

# 替换字典
rep = {'\w':'0','\d':'0','\W':'!','\D':'!'}
# 构造最短的匹配字符串
def get_match_string(reg):
    # 按优先级替换
    # *:匹配零次或多次 +:匹配一次或多次 ?:匹配零次或一次
    # 替换字典
    match_string = reg
    for k,v in rep.items():
        match_string = match_string.replace(k,v)
    # 替换中括号内容
    match_string = re.sub('[\[](?P<chars>[\w!\|\-.]+)[\]]',repzkh,match_string)
    # 替换小括号中内容(优先级最低，但影响不大)
    match_string = re.sub('[\(](?P<chars>[\w!\-.]+)([\|][\w!\-.]+)+[\)]',repxkh,match_string)
    # 去掉*和?
    match_string = re.sub('([\[][\w!\-.]+[\]]|[\w!\-.])[*?]','',match_string)
    # 去掉+
    match_string = match_string.replace('+','')
    # 替换大括号内数字+去掉大括号
    match_string = re.sub('[\{](?P<num>[\d]*)([,|.]\d+)*[\}]',repdkh1,match_string)
    match_string = re.sub('[\[\(](?P<chars>[\w!\-.]+)[\]\)][\{](?P<num>[\d]+)[\}]',repdkh2,match_string)# 有括号+大括号
    match_string = re.sub('(?P<chars>[\w!\-.])[\{](?P<num>[\d]+)[\}]',repdkh2,match_string)# 没括号+大括号
    # 去掉中括号和小括号
    match_string = match_string.replace('[','').replace(']','').replace('(','').replace(')','')

    # print("match: "+str(re.match(reg,match_string) is not None))
    return match_string

# 测试正则
# print("string: "+get_match_string("v*[a-zA-Z]U[a-z]+N*(fish|tomato)+(phone|tomato){2}[\d\d2eh3A]*[aiIZXFoC]{2}[e-j][e-j]{6}[VJ.\WSUZ]{11}(penguin|gazelle)+\D*[vc]"))
main()
```

关于socket交互的函数就不学了，平时都是用pwn库的。这题的知识点还是在正则。[re.sub](https://blog.csdn.net/lovemianmian/article/details/8867613)跟replace很像，只是replace把要替换的的字符写死了，而sub用正则来匹配需要替换的内容。第一个参数是匹配用的正则；第二个参数是要替换为的字符串，可以传入函数，也是这个exp的写法；第三个参数是原字符串。当第二个参数是函数时，正则匹配到的部分会被当作参数传入函数，返回值就是替换为的内容。

[group](https://blog.csdn.net/qq_33472765/article/details/80803227)函数没明确搜到这种用法，不过看到正则里的标签猜测是根据标签分组取结果。测试了一下，确实是拿出正则括号内的内容然后原封不动返回去。不是很理解。剩下的[正则](https://segmentfault.com/a/1190000022242427)交给大家自己看了，我在这里抄一遍也没意思。

## Flag
> flag{^regularly_express_yourself$}