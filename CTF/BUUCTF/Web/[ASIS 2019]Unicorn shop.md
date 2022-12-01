# [ASIS 2019]Unicorn shop

[题目地址](https://buuoj.cn/challenges#[ASIS%202019]Unicorn%20shop)

怎么看出题人的提示还能被带沟里呢？

环境是一个独角兽商店。很好，商店题发展到2019已经连独角兽都能买了。源代码有几句注释：

```html
<html lang="zh-CN">
<head>
<meta charset="utf-8"><!--Ah,really important,seriously. -->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Unicorn shop</title>
<!-- Don't be frustrated by the same view,we've changed the challenge content.-->
<!-- Bootstrap core CSS -->
<link href="/static/css/bootstrap.min.css?v=ec3bb52a00e176a7181d454dffaea219" rel="stylesheet">
<!-- Custom styles for this template -->
<link href="/static/css/jumbotron-narrow.css?v=166844ff66a82256d62737c8a6fc14bf" rel="stylesheet">
</head>
<!--We still have some surprise for admin.password-->
<body>
<div class="container">
```

然后我看`<!--We still have some surprise for admin.password-->`这句话就以为这题是要成为管理员，独角兽商店就是个幌子。结果并不是啊，这题根本就没有管理员这个东西，看[wp](https://blog.csdn.net/qq_41891666/article/details/107224411)才知道是unicode的问题。

这题的目标其实很简单，买那个最贵的ultra unicorn。那直接买呗，item ID填4，Price填1337。于是就能得到一个报错。

- Only one char(?) allowed!

它说只能填一个字符，1337是4个了。不过吧，灵性的问号告诉我们事情并不简单。没有源码的情况下，大佬们猜出这题price框的字符传到后台会得到其numeric value，因此我们只需要找到一个numeric value大于1337的字符就好了。然而我不是大佬，看wp找到了源码。

```python
# -*- coding:utf-8 -*-
import sys
import unicodedata
import urllib

from sqlalchemy.orm.exc import NoResultFound

from sshop.base import BaseHandler
from sshop.models import Commodity

reload(sys)
sys.setdefaultencoding('utf8')


class ChargeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        commoditys = self.orm.query(Commodity) \
            .order_by(Commodity.price.asc()).all()
        return self.render('charge.html', commoditys=commoditys)

    def post(self, *args, **kwargs):
        commoditys = self.orm.query(Commodity)
        id = self.get_argument('id')
        price = str(self.get_argument('price'))
        try:
            price = urllib.unquote(price).decode('utf-8')   #发现price用utf-8解码
        except UnicodeDecodeError:
            return self.render('charge.html', danger=1, commoditys=commoditys,
                               dangermessage="Error parsing money!")
        if len(price) > 1:
            return self.render('charge.html', danger=1, commoditys=commoditys, dangermessage="Only one char(?) allowed!")
        try:
            unicodedata.numeric(price)
        except ValueError:
            return self.render('charge.html', danger=1, commoditys=commoditys, dangermessage="Error parsing money!")

        # return self.render('charge.html', danger=1, commoditys=commoditys, preview=page - 1, next=page + 1,
        #                    limit=limit,
        #                    dangermessage="测试专用。当前输入字符为：{0}，其Unicode名称为：{1}，其Unicode numeric为：{2}".format(price,
        #                                                                                                  unicodedata.name(
        #                                                                                                      price),unicodedata.numeric(price)))
        try:
            commoditys = self.orm.query(Commodity).filter(Commodity.id == id).one()
        except NoResultFound:

            return self.render('charge.html', danger=1, commoditys=commoditys,
                               dangermessage="No commodity found!")
        if commoditys.english == 'ultra unicorn':
            if unicodedata.numeric(price) >= commoditys.price:   #价格是price的numeric value，大于ultra unicorn的price就给flag
                commoditys = self.orm.query(Commodity) \
                    .order_by(Commodity.price.asc()).all()
                return self.render('charge.html', success=1, commoditys=commoditys,
                                   successmessage="flag{aa4059c8-8d0b-442d-bc89-7f8d8846be26}")
            else:
                commoditys = self.orm.query(Commodity).all()
                return self.render('charge.html', danger=1, commoditys=commoditys,
                                   dangermessage="You don't have enough money!")
        else:
            commoditys = self.orm.query(Commodity).all()
            return self.render('charge.html', danger=1, commoditys=commoditys,
                               dangermessage="Wrong commodity!")
```

[unicodedata.numeric](https://cloud.tencent.com/developer/article/1406445)的用法大致就是把一个表示数字的字符串转换为浮点数返回。那就是说我们要找一个字符，其可以表示1337以上的值。可以来[这](https://www.compart.com/en/unicode/)慢慢找，不过等等。我们用的是中文啊，中文里那么多表示数字的汉字，一下子不就能想到了吗？万？亿？兆？直接冲任意一个字，都能得到flag。

### Flag
> flag{38394120-dbcc-4e7b-97d5-f717070e6daf}