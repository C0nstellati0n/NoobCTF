# [Zer0pts2020]Can you guess it?

[题目地址](https://buuoj.cn/challenges#[Zer0pts2020]Can%20you%20guess%20it?)

考点非常简单，然而不知道考点再简单也没用。

网站叫我们猜值。猜个鬼，直接看源代码。

```php
<?php
include 'config.php'; // FLAG is defined in config.php

if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

if (isset($_GET['source'])) {
  highlight_file(basename($_SERVER['PHP_SELF']));
  exit();
}

$secret = bin2hex(random_bytes(64));
if (isset($_POST['guess'])) {
  $guess = (string) $_POST['guess'];
  if (hash_equals($secret, $guess)) {
    $message = 'Congratulations! The flag is: ' . FLAG;
  } else {
    $message = 'Wrong.';
  }
}
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Can you guess it?</title>
  </head>
  <body>
    <h1>Can you guess it?</h1>
    <p>If your guess is correct, I'll give you the flag.</p>
    <p><a href="?source">Source</a></p>
    <hr>
<?php if (isset($message)) { ?>
    <p><?= $message ?></p>
<?php } ?>
    <form action="index.php" method="POST">
      <input type="text" name="guess">
      <input type="submit">
    </form>
  </body>
</html>
```

最开始以为是[hash_equals](https://www.php.net/manual/zh/function.hash-equals.php)的问题，后面看[wp](https://www.cnblogs.com/Article-kelp/p/16045800.html)才知道不是，考点在我完全没注意的`highlight_file(basename($_SERVER['PHP_SELF']));`上。

[$_SERVER['PHP_SELF']](http://www.5idev.com/p-php_server_php_self.shtml)表示当前 php 文件相对于网站根目录的位置地址，例如：

```
http://www.5idev.com/php/ ：/php/index.php
http://www.5idev.com/php/index.php ：/php/index.php
http://www.5idev.com/php/index.php?test=foo ：/php/index.php
http://www.5idev.com/php/index.php/test/foo ：/php/index.php/test/foo
```

[basename](https://www.php.net/manual/zh/function.basename.php)则是返回路径中的文件名部分。但是basename有个特性，如果文件名是一个不可见字符，便会将上一个目录作为返回值。比如：

```php
$var1="/config.php/test"
basename($var1)	=> test
$var2="/config.php/%ff"
basename($var2)	=>	config.php
```

所以我们结合两者，要让basename里面包含config.php，又不能让\$_SERVER['PHP_SELF']的末尾是config.php。这似乎是不可能的，然而php本身就有一个url解析的特性，当我们访问一个`存在的文件/不存在的文件`这个url时，php会自动忽略多余的不存在的部分，比如下面两种url：

```
/index.php
/index.php/dosent_exist.php
```

都能访问到index.php。自己试验一下就知道了，下面这个url可以正常进入index.php。

- http://18122d3a-c67f-48c1-8f6b-beec3998f9e1.node4.buuoj.cn:81/index.php/sdfa

再结合正则，找到答案了。

```php
<?php
$s="config.php/s";
if(preg_match("/config\.php\/*$/i",$s)){
    echo 'no';
}
else{
    echo 'yes';
}
//yes
//当s是config.php时为no，说明后面必须跟上东西
```

原本后面跟上东西时虽然能绕过正则，却让basename读取不到config。现在有了php的url解析特性，我们可以随便在后面加上个东西，不用担心url无效了。构造payload时首先构造index.php/config.php，虽然index.php下没有config.php，但是还是能获取到index.php。这样过不了正则，那就在后面加上个/%ff这个不可见字符，正则能过，basename也可以因为特性获取到前面的config.php。

- http://18122d3a-c67f-48c1-8f6b-beec3998f9e1.node4.buuoj.cn:81/index.php/config.php/%ff/?source

## Flag
> flag{3b7fbbe9-3085-4983-8357-6edda5624830}