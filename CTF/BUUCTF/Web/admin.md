# admin

[题目地址](https://buuoj.cn/challenges#[HCTF%202018]admin)

没flask拿不了flag，心想着[wp](https://www.anquanke.com/post/id/164086)看都看了写篇笔记吧。

进来有两个页面，login和register。随便注册一个用户，检查源代码时发现提示。

```html
<h1 class="nav">Hello a</h1>


<!-- you are not admin -->
<h1 class="nav">Welcome to hctf</h1>
```

那就是要登录成admin？试了一下sql，没有。在打web题时不要放过任何一个页面，所以改密码的地方也要看看。发现意外收获。

```html
<div class="ui grid">
    <div class="four wide column"></div>
    <div class="eight wide column">
        <!-- https://github.com/woadsl1234/hctf_flask/ -->
      <form class="ui form segment" method="post" enctype="multipart/form-data">
        <div class="field required">
          <label>NewPassword</label>
          <input id="newpassword" name="newpassword" required type="password" value="">
        </div>
        <input type="submit" class="ui button fluid" value="更换密码">
      </form>
    </div>
  </div> 
```

是网站的源代码库。看下代码，没什么直接问题，因为这题的关键根本就不在代码上。在cookie中可以发现session，用脚本解码。

```python
import sys
import zlib
from base64 import b64decode
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode

def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)

    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True

    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                         'an exception')

    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                             'decoding the payload')

    return session_json_serializer.loads(payload)

if __name__ == '__main__':
    print(decryption(sys.argv[1].encode()))
```

得到seesion内容。继续查看网站模板，发现登录成admin确实是我们的目标，能看见flag。

```html
{% include('header.html') %}
{% if current_user.is_authenticated %}
<h1 class="nav">Hello {{ session['name'] }}</h1>
{% endif %}
{% if current_user.is_authenticated and session['name'] == 'admin' %}
<h1 class="nav">hctf{xxxxxxxxx}</h1>
{% endif %}
<!-- you are not admin -->
<h1 class="nav">Welcome to hctf</h1>

{% include('footer.html') %}
```

利用seesion什么的绕登录验证也很常见，我们可不可以把自己的sessino改成admin登陆？当然可以，借用大佬的[仓库](https://github.com/noraj/flask-session-cookie-manager)编辑session。编辑时发现需要SECRET_KEY，源代码给了。

```python
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ckj123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adsl1234@db:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
```

用python3生成session后赋值即成为管理员，拿到flag。关于session还有另一篇很好的[文章](https://www.leavesongs.com/PENETRATION/client-session-security.html)。