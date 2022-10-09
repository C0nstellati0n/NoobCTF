# filemanager

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=240f5d83-b4c9-436a-b131-8a1193d5312a_2&task_category_id=3)

文件上传题。直接扫目录，以前没有这个习惯，现在1分钟内没头绪就扫目录。发现/www.tar.gz可以直接下载源码。来吧审计。

```sql
SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS `xdctf`;
CREATE DATABASE xdctf;
USE xdctf;

DROP TABLE IF EXISTS `file`;
CREATE TABLE `file` (
  `fid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `filename` varchar(256) NOT NULL,
  `oldname` varchar(256) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `extension` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
```

数据库的配置。库名和表名都知道了，但光知道这个并没有什么用。继续往下看。

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午7:58
 */

$DATABASE = array(

	"host" => "127.0.0.1",
	"username" => "root",
	"password" => "ayshbdfuybwayfgby",
	"dbname" => "xdctf",
);

$db = new mysqli($DATABASE['host'], $DATABASE['username'], $DATABASE['password'], $DATABASE['dbname']);
$req = array();

foreach (array($_GET, $_POST, $_COOKIE) as $global_var) {
	foreach ($global_var as $key => $value) {
		is_string($value) && $req[$key] = addslashes($value);
	}
}

define("UPLOAD_DIR", "upload/");

function redirect($location) {
	header("Location: {$location}");
	exit;
}
```

又看见了addslashes。我现在基本把addslashes和二次注入绑定在一起了。

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午9:39
 */

require_once "common.inc.php";

if(isset($req['filename'])) {
    $result = $db->query("select * from `file` where `filename`='{$req['filename']}'");
    if ($result->num_rows>0){
        $result = $result->fetch_assoc();
    }

    $filename = UPLOAD_DIR . $result["filename"] . $result["extension"];
    if ($result && file_exists($filename)) {
        $db->query('delete from `file` where `fid`=' . $result["fid"]);
        unlink($filename);
        redirect("/");
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>file manage</title>
    <base href="/">
    <meta charset="utf-8" />
</head>
<h3>Delete file</h3>
<body>
    <form method="post">
        <p>
            <span>delete filename(exclude extension)：</span>
            <input type="text" name="filename">
        </p>
        <p>
            <input type="submit" value="delete">
        </p>
    </form>
</body>
</html>
```

粗略看一遍，感觉没问题。

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午7:46
 */

?>

<!DOCTYPE html>
<html>
<head>
    <title>file manage</title>
    <base href="./">
    <meta charset="utf-8" />
</head>
<body>
    <h3>Control</h3>
    <ul style="list-style: none;">
        <li><a href="./delete.php">Delete file</a></li>
        <li><a href="./rename.php">Rename file</a></li>
    </ul>

    <h3>Content</h3>
    <form action="./upload.php" method="post" enctype="multipart/form-data">
        <input type="file" name="upfile">
        <input type="submit" value="upload file">
    </form>
</body>
</html>
```

首页肯定没问题，首页都出问题了还玩什么呢？

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午9:39
 */

require_once "common.inc.php";

if (isset($req['oldname']) && isset($req['newname'])) {
	$result = $db->query("select * from `file` where `filename`='{$req['oldname']}'");
	if ($result->num_rows > 0) {
		$result = $result->fetch_assoc();
	} else {
		exit("old file doesn't exists!");
	}

	if ($result) {

		$req['newname'] = basename($req['newname']);
		$re = $db->query("update `file` set `filename`='{$req['newname']}', `oldname`='{$result['filename']}' where `fid`={$result['fid']}");
		if (!$re) {
			print_r($db->error);
			exit;
		}
		$oldname = UPLOAD_DIR . $result["filename"] . $result["extension"];
		$newname = UPLOAD_DIR . $req["newname"] . $result["extension"];
		if (file_exists($oldname)) {
			rename($oldname, $newname);
		}
		$url = "/" . $newname;
		echo "Your file is rename, url:
                <a href=\"{$url}\" target='_blank'>{$url}</a><br/>
                <a href=\"/\">go back</a>";
	}
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>file manage</title>
    <base href="/">
    <meta charset="utf-8" />
</head>
<h3>Rename</h3>
<body>
<form method="post">
    <p>
        <span>old filename(exclude extension)：</span>
        <input type="text" name="oldname">
    </p>
    <p>
        <span>new filename(exclude extension)：</span>
        <input type="text" name="newname">
    </p>
    <p>
        <input type="submit" value="rename">
    </p>
</form>
</body>
</html>
```

改文件名的。可能把上传文件看完才能知道到底有没有问题。

```php
<?php
/**
 * Created by PhpStorm.
 * User: phithon
 * Date: 15/10/14
 * Time: 下午8:45
 */

require_once "common.inc.php";

if ($_FILES) {
	$file = $_FILES["upfile"];
	if ($file["error"] == UPLOAD_ERR_OK) {
		$name = basename($file["name"]);
		$path_parts = pathinfo($name);

		if (!in_array($path_parts["extension"], array("gif", "jpg", "png", "zip", "txt"))) {
			exit("error extension");
		}
		$path_parts["extension"] = "." . $path_parts["extension"];

		$name = $path_parts["filename"] . $path_parts["extension"];

		// $path_parts["filename"] = $db->quote($path_parts["filename"]);
		// Fix
		$path_parts['filename'] = addslashes($path_parts['filename']);

		$sql = "select * from `file` where `filename`='{$path_parts['filename']}' and `extension`='{$path_parts['extension']}'";

		$fetch = $db->query($sql);

		if ($fetch->num_rows > 0) {
			exit("file is exists");
		}

		if (move_uploaded_file($file["tmp_name"], UPLOAD_DIR . $name)) {

			$sql = "insert into `file` ( `filename`, `view`, `extension`) values( '{$path_parts['filename']}', 0, '{$path_parts['extension']}')";
			$re = $db->query($sql);
			if (!$re) {
				print_r($db->error);
				exit;
			}
			$url = "/" . UPLOAD_DIR . $name;
			echo "Your file is upload, url:
                <a href=\"{$url}\" target='_blank'>{$url}</a><br/>
                <a href=\"/\">go back</a>";
		} else {
			exit("upload error");
		}

	} else {
		print_r(error_get_last());
		exit;
	}
}
```

发现过滤了文件后缀名，自然没法直接传木马。目标应该是绕过后缀名，这点在上传时肯定无法实现，我们只能上传一些无聊的后缀，就算内容是木马也无法执行。不是有个重命名吗，看看能不能利用？

```php
$req['newname'] = basename($req['newname']);
$re = $db->query("update `file` set `filename`='{$req['newname']}', `oldname`='{$result['filename']}' where `fid`={$result['fid']}");
```

读取了oldname，oldname是之前被addslashes的初始文件名。绝对有二次注入，我们要把炸弹埋在oldname。继续往下看，想一下sql注入要干什么。

```php
$oldname = UPLOAD_DIR . $result["filename"] . $result["extension"];
$newname = UPLOAD_DIR . $req["newname"] . $result["extension"];
if (file_exists($oldname)) {
	rename($oldname, $newname);
}
```

重命名时是新名字拼接后缀名，\$result是查询结果，\$req是网页请求。猛地发现改名界面是没有过滤的啊，newname可以直接提交xxx.php，但是原来的后缀怎么办呢，xxx.php.jpg之类的显然不能执行。除非……后缀名是空？改名前正好有updata语句，正好又有二次注入，可不可以利用二次注入把后缀名改为空？

- ',extension='.txt

在改文件名时，单引号闭合oldname项，自己加个逗号更改extension（这就是给sql结构的原因了，我们知道里面的字段名）为空，最后的引号闭合后一个单引号，txt就是个掩耳盗铃后缀。把这个名字作为一个txt的文件名，上传后数据库中就有了恶意数据。现在我们改个名。

- old filename(exclude extension)：',extension='<br>new filename(exclude extension)： shell.txt

此时改名php脚本里的update语句是这样的。

```sql
update `file` set `filename`='shell.txt', `oldname`='',extension='' where `fid`={$result['fid']}
```

完美。可是为什么不直接改成shell.php呢？因为真正执行改名的函数[rename](https://www.runoob.com/php/func-filesystem-rename.html)还有个过滤。

```php
$oldname = UPLOAD_DIR . $result["filename"] . $result["extension"];
$newname = UPLOAD_DIR . $req["newname"] . $result["extension"];
if (file_exists($oldname)) {
	rename($oldname, $newname);
}
```

newname的值仍然要拼接上原来result的extension，这个result是在update改掉后缀前查询出来的，仍然保留着txt的后缀。如果直接改名shell.php，文件名就会变成shell.php.txt，还是无法执行，且后续无法上传同名文件完成改名。而改名为shell.txt时，虽然原文件被重命名为了shell.txt.txt，但数据库里的记录还是filename=shell.txt，后缀为空。下次我们再传一个shell.txt，然后重命名为shell.php，此时result的extension项就为空了，成功重命名木马。

木马传上去后干啥就不用多说了，直接菜刀或蚁剑拿个快乐shell。

- ### Flag
  > flag{bdda3c944a9e484eae50123afeeff56b}