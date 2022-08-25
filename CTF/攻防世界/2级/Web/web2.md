# web2

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=ebfb48d9-b6db-4f66-a0d3-0784df71111_2)

这道题其实挺简单的，但是我因为php配置环境踩了好多坑……另外这道题和web一点关系都没有，纯纯reverse，难道因为用的是php语言所以才归到web？

进入网站直接就是要逆向的php脚本。

```php
<?php
$miwen="a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws";

function encode($str){
    $_o=strrev($str);
    // echo $_o;
        
    for($_0=0;$_0<strlen($_o);$_0++){
       
        $_c=substr($_o,$_0,1);
        $__=ord($_c)+1;
        $_c=chr($__);
        $_=$_.$_c;   
    } 
    return str_rot13(strrev(base64_encode($_)));
}

highlight_file(__FILE__);
/*
   逆向加密算法，解密$miwen就是flag
*/
?>
```

这个加密算法可以说是很简单了。这里复习一下php基础知识。

- ### PHP
- > 定义变量：$变量名
- > . 符号：拼接字符串
- > strrev()：反转字符串
- > strlen():返回字符串的长度
- > substr():切割字符串，第一个参数是要切割的目标字符串，第二个参数是起始位置，第三个参数是切割长度。
- > str_rot13()：将字符串以rot13方式进行加密/解密
- > highlight_file():对文件进行语法高亮显示

这里完全可以把上面的脚本照抄，除了要把ord()方法后面的+1改成-1。我怎么都配置不好PHP环境，所以不想浪费太多时间了，直接找了个在线的php运行[网站](https://www.dooccn.com/php/)

```php
<?php
$s='a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws';
$s=base64_decode(strrev(str_rot13($s)));
$_=null;
for($i=0;$i<strlen($s);$i++){
    $_c=substr($s,$i,1);
    $__=ord($_c)-1;
    $_c=chr($__);
    $_=$_.$_c;
}
echo strrev($_);
?>
```

注意这里有个坑：不能把$miwen字符串先在外面进行rot13解密后再把结果放进来进行逆向。我最开始用python写逆向脚本，因为没有现成的rot13解密方法所以我现在外面解密了再粘贴进来，以为这样可以省一步，没想到结果很诡异，不断让我怀疑自己的逆向能力。没想到是str_rot13()方法的问题。

- ### Flag
- > flag:{NSCTF_b73d5adfb819c64603d7237fa0d52977}