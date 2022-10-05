# blgdel

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=fd14ca0d-a59e-44eb-8b5c-cab75b24c38b_2)

没题做了，来做web吧。web总是解出人数最多的分区，意味着[wp](https://blog.csdn.net/hxhxhxhxx/article/details/108109579)很多！

一个购物网站，然而我们一分钱都没有，卖的商品也不重要，没有flag。看来关键点不在买东西，有别的地方。注册一个账户后进入个人中心发现可以上传头像。文件包含又来了？结果提示积分不够，最开始还以为不是这个考点，看了一眼wp，这么恶心吗，注册新用户才能得积分。注销后去注册界面注册用户，其他随便写，推荐人写想要刷积分的用户。大概100分就能上传头像。

随便传个图像看看，没给上传路径。不对劲啊，文件上传类题一般都有个路径的。没思路了，看robots.txt。果真有东西，config.txt。里面就是我们想要的源码。

```php
<?php

class master
{
	private $path;
	private $name;
	
	function __construct()
	{
		
	}
	
	function stream_open($path)
	{
		if(!preg_match('/(.*)\/(.*)$/s',$path,$array,0,9))
			return 1;
		$a=$array[1];
		parse_str($array[2],$array);
		
		if(isset($array['path']))
		{
			$this->path=$array['path'];
		}
		else
			return 1;
		if(isset($array['name']))
		{
			$this->name=$array['name'];
		}
		else
			return 1;
		
		if($a==='upload')
		{
			return $this->upload($this->path,$this->name);
		}
		elseif($a==='search')
		{
			return $this->search($this->path,$this->name);
		}
		else 
			return 1;
	}
	function upload($path,$name)
	{
		if(!preg_match('/^uploads\/[a-z]{10}\/$/is',$path)||empty($_FILES[$name]['tmp_name']))
			return 1;
		
		$filename=$_FILES[$name]['name'];
		echo $filename;
		
		$file=file_get_contents($_FILES[$name]['tmp_name']);
		
		$file=str_replace('<','!',$file);
		$file=str_replace(urldecode('%03'),'!',$file);
		$file=str_replace('"','!',$file);
		$file=str_replace("'",'!',$file);
		$file=str_replace('.','!',$file);
		if(preg_match('/file:|http|pre|etc/is',$file))
		{
			echo 'illegalbbbbbb!';
			return 1;
		}
		
		file_put_contents($path.$filename,$file);
		file_put_contents($path.'user.jpg',$file);
		
		
		echo 'upload success!';
		return 1;
	}
	function search($path,$name)
	{
		if(!is_dir($path))
		{
			echo 'illegal!';
			return 1;
		}
		$files=scandir($path);
		echo '</br>';
		foreach($files as $k=>$v)
		{
			if(str_ireplace($name,'',$v)!==$v)
			{
				echo $v.'</br>';
			}
		}
		
		return 1;
	}
	
	function stream_eof()
	{
		return true;
	}
	function stream_read()
	{
		return '';
	}
	function stream_stat()
	{
		return '';
	}
	
}

('php');
stream_wrapper_unregister('phar');
stream_wrapper_unregister('zip');
stream_wrapper_register('master','master');

?>
```

[stream_wrapper_register](https://www.php.net/manual/zh/function.stream-wrapper-register.php)用于注册用户自定义的协议，用法只支持schema://。这个schema对应的应该是类名，举个例子，可以用master://search/path=&name=，也就是类名://方法名/参数1=&参数2=。stream_wrapper_unregister不用说了，肯定就是取消定义的伪协议，这里去掉了phar和zip。[scandir](https://www.runoob.com/php/func-directory-scandir.html)自然就是扫描目录了。[str_ireplace](https://www.runoob.com/php/func-string-str-ireplace.html)替换内容。search函数就是帮忙查找文件而已，不是分析的重点。重点肯定在过滤的正则上。

虽然没有明确指出，但是看upload这个名字可以猜测在upload区被调用。第一个正则不用看，因为过滤的是path，我们无法控制，倒是知道了上传路径是uploads，分析完后去看看。后面连续几个字符串替换ban掉了php小马的必要条件，没法拿webshell了。后面过滤的内容更不用看了，已经没有马可以写了。

uploads去看了看，开了目录遍历。有个很搞心态的点，里面的文件夹全部都是随机名字的，要一个一个找上传位置。点了半天找到了真正的位置。仔细想想，没有过滤文件名，来个[.htaccess](https://blog.csdn.net/solitudi/article/details/116666720)咋样？使用本地文件包含的方法，php_value，在当前路径下所有的php文件开头加上我们要包含的文件内容。我们当然可以把.htaccess和php文件放在一个目录下，最后的问题就是flag叫什么名字了。好心的出题人给了search函数，我们就可以查找flag文件名了。把下面的内容写入一个名叫.htaccess的文件中。如果电脑总是把后缀名搞成txt就直接echo 内容 > 文件名，绝对没有乱七八糟的后缀名。

- php_value auto_append_file master://search/path=%2fhome%2f&name=flag

别忘了再上传一个php后缀的文件。去到uploads下，找到上传路径，flag名字在上传的php文件里。编码是因为在stream_open函数中过滤了/符号。

- hiahiahia_flag

最后再上传一个.htaccess文件。

- php_value auto_append_file /home/hiahiahia_flag

重复以上步骤，好耶flag！

- ### Flag
  > cyberpeace{5a4438362deb6d5db1b866cab5ece7ce}