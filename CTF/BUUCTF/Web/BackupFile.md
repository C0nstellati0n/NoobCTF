# BackupFile

[题目地址](https://buuoj.cn/challenges#[ACTF2020%20%E6%96%B0%E7%94%9F%E8%B5%9B]BackupFile)

恶补基础的一天。

进网站就一句话：

- Try to find out source file!

去了几个特殊目录，robots，www.zip，secret.php之类的，什么都没有改变。既然题目叫backupfile，那应该要找的是php的[备份文件名](https://blog.csdn.net/Karol_agan/article/details/105971293)。常用的有几个，“.git” 、“.svn”、“ .swp”“.~”、“.bak”、“.bash_history”、“.bkf”，试了一下发现index.php.bak可以下载。

```php
<?php
include_once "flag.php";

if(isset($_GET['key'])) {
    $key = $_GET['key'];
    if(!is_numeric($key)) {
        exit("Just num!");
    }
    $key = intval($key);
    $str = "123ffwsfwefwf24r2f32ir23jrw923rskfjwtsw54w3";
    if($key == $str) {
        echo $flag;
    }
}
else {
    echo "Try to find out source file!";
}
```

这个对比有点唬人。要求传入的key和str相等，但是str里面不止数字，key却要求只传数字。但是注意使用了==弱类型比较，PHP在弱比较整数和字符串的时候会将字符串类型转为整数型。字符串转整数型时，如果字符串前几位是数字字符则只取数字字符进行转换，其他字符舍弃。因此str转数字就是123，直接传123就好了。

- http://020bd333-0430-4f8b-967e-50f19a77fbb7.node4.buuoj.cn:81/?key=123

### flag
- flag{5c94c912-8c6f-4cb7-8903-ae4d8a1ff169}