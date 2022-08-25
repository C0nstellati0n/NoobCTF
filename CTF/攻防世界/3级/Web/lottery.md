# lottery

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a27cfc57-607b-424e-969f-29aff623f12a_2)

这题不难，卡就卡在我对php不熟。虽然这次使用的知识点我是知道的，但是由于经验不足还是没有联想到那。

附件给了网站源码，先放一边，看看目标网站是干啥的。

![website](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/website.png)

看来是个买彩票的。我还真玩了一下，纯靠运气最多只能中20，而flag要9990000。啊这，差远了，看来要找点漏洞利用利用。

首先要判断源码到底在哪里可能会有漏洞。这里注册才能玩，但是注册时没要求密码，说明每个账户都是一次性的，漏洞在账户相关内容上的几率很小。检查网站也没发现cookie，同时随便打开几个源码可以发现使用的是session，那cookie相关内容也不用想了。

- account.php		buy.php			config.php		favicon.ico		header.php		js			market.php		robots.txt
- api.php			check_register.php	css			footer.php		index.php		logout.php		register.php

整个文件夹里就这些文件。把账号相关去除，index估计也不用看，最后剩下的内容基本都是和购买flag和彩票逻辑相关的。购买flag里面就是单纯判断已有的钱是否大于flag价格，估计也没啥东西。那就只有彩票环节了。

- ### buy.php
```php
<?php include('check_register.php');include('header.php'); ?>


<h2>Buy a lottery!</h2>

<form method="POST">
<input type="text" name="numbers" id="numbers" minlength="7" maxlength="7" pattern="\d{7}" required placeholder="7 numbers">
<button type="button" id="btnBuy">Buy!</button>
</form>
<script type="text/javascript" src="js/buy.js"></script>
<p id="wait" class="alert alert-info" style="display: none;">Please wait...</p>
<div id="result" style="display: none;">
	<p id="info" class="alert alert-info">Prize: <span id="prize"></span></p>
	<p>
		<span style="width: 10em; display: inline-block;">Winning numbers:</span>
		<div id="win">

		</div>
	</p>
	<p>
		<span style="width: 10em; display: inline-block;">Your numbers:</span>
		<div id="user">
			<span class="number-ball number-ball-red">1</span>
			<span class="number-ball number-ball-gray">6</span>
		</div>
	</p>
</div>

<?php include('footer.php'); ?>
```

这里只有一些展示，不是核心逻辑，继续看别的。

- ### api.php
```php
<?php
require_once('config.php');
header('Content-Type: application/json');

function response($resp){
	die(json_encode($resp));
}

function response_error($msg){
	$result = ['status'=>'error'];
	$result['msg'] = $msg;
	response($result);
}

function require_keys($req, $keys){
	foreach ($keys as $key) {
		if(!array_key_exists($key, $req)){
			response_error('invalid request');
		}
	}
}

function require_registered(){
	if(!isset($_SESSION['name']) || !isset($_SESSION['money'])){
		response_error('register first');
	}
}

function require_min_money($min_money){
	if(!isset($_SESSION['money'])){
		response_error('register first');
	}
	$money = $_SESSION['money'];
	if($money < 0){
		$_SESSION = array();
		session_destroy();
		response_error('invalid negative money');
	}
	if($money < $min_money){
		response_error('you don\' have enough money');
	}
}


if($_SERVER["REQUEST_METHOD"] != 'POST' || !isset($_SERVER["CONTENT_TYPE"]) || $_SERVER["CONTENT_TYPE"] != 'application/json'){
	response_error('please post json data');
}

$data = json_decode(file_get_contents('php://input'), true);
if(json_last_error() != JSON_ERROR_NONE){
	response_error('invalid json');
}

require_keys($data, ['action']);

// my boss told me to use cryptographically secure algorithm 
function random_num(){
	do {
		$byte = openssl_random_pseudo_bytes(10, $cstrong);
		$num = ord($byte);
	} while ($num >= 250);

	if(!$cstrong){
		response_error('server need be checked, tell admin');
	}
	
	$num /= 25;
	return strval(floor($num));
}

function random_win_nums(){
	$result = '';
	for($i=0; $i<7; $i++){
		$result .= random_num();
	}
	return $result;
}


function buy($req){
	require_registered();
	require_min_money(2);

	$money = $_SESSION['money'];
	$numbers = $req['numbers'];
	$win_numbers = random_win_nums();
	$same_count = 0;
	for($i=0; $i<7; $i++){
		if($numbers[$i] == $win_numbers[$i]){
			$same_count++;
		}
	}
	switch ($same_count) {
		case 2:
			$prize = 5;
			break;
		case 3:
			$prize = 20;
			break;
		case 4:
			$prize = 300;
			break;
		case 5:
			$prize = 1800;
			break;
		case 6:
			$prize = 200000;
			break;
		case 7:
			$prize = 5000000;
			break;
		default:
			$prize = 0;
			break;
	}
	$money += $prize - 2;
	$_SESSION['money'] = $money;
	response(['status'=>'ok','numbers'=>$numbers, 'win_numbers'=>$win_numbers, 'money'=>$money, 'prize'=>$prize]);
}

function flag($req){
	global $flag;
	global $flag_price;

	require_registered();
	$money = $_SESSION['money'];
	if($money < $flag_price){
		response_error('you don\' have enough money');
	} else {
		$money -= $flag_price;
		$_SESSION['money'] = $money;
		$msg = 'Here is your flag: ' . $flag;
		response(['status'=>'ok','msg'=>$msg, 'money'=>$money]);
	}
}

function register($req){
	$name = $req['name'];
	$_SESSION['name'] = $name;
	$_SESSION['money'] = 20;

	response(['status'=>'ok']);
}


switch ($data['action']) {
	case 'buy':
		require_keys($data, ['numbers']);
		buy($data);
		break;

	case 'flag':
		flag($data);
		break;

	case 'register':
		require_keys($data, ['name']);
		register($data);
		break;
	
	default:
		response_error('invalid request');
		break;
}
```

这里看起来就是关键了。最初我以为随机数的生成有问题，可能会有什么规律来让我们猜到下一次要生成的数字。但是并不是，虽然使用的随机数生成函数里面有“伪”这个字。

- ### openssl_random_pseudo_bytes()
- > 语法：openssl_random_pseudo_bytes ( int \$length [, bool &$crypto_strong ] ) : string
- > 生成一个伪随机字节串 string ，字节数由 length 参数指定。通过 crypto_strong 参数可以表示在生成随机字节的过程中是否使用了强加密算法。

经过个人的尝试和网上的查找，这个方法似乎并无明显可预测的规律可循。加上还用了强加密算法，可能漏洞点并不在这里。不过你有没有发现上面buy.php的script标签包含了一个叫buy.js的文件，打开看看。

```javascript
function buy(){
	$('#wait').show();
	$('#result').hide();
	var input = $('#numbers')[0];
	if(input.validity.valid){
		var numbers = input.value;
		$.ajax({
		  method: "POST",
		  url: "api.php",
		  dataType: "json",
		  contentType: "application/json", 
		  data: JSON.stringify({ action: "buy", numbers: numbers })
		}).done(function(resp){
			if(resp.status == 'ok'){
				show_result(resp);
			} else {
				alert(resp.msg);
			}
		})
	} else {
		alert('invalid');
	}
	$('#wait').hide();
}

function show_result(resp){
	$('#prize').text(resp.prize);
	var numbers = resp.numbers;
	var win_numbers = resp.win_numbers;
	var numbers_result = '';
	var win_numbers_result = '';
	for(var i=0; i<7; i++){
		win_numbers_result += '<span class="number-ball number-ball-red">' + win_numbers[i] + '</span>';
		if(numbers[i] == win_numbers[i]){
			numbers_result += '<span class="number-ball number-ball-red">' + numbers[i] + '</span>';
		} else {
			numbers_result += '<span class="number-ball number-ball-gray">' + numbers[i] + '</span>';
		}
	}
	$('#win').html(win_numbers_result);
	$('#user').html(numbers_result);
	$('#money').text(resp.money);
	$('#result').show();
	$('#numbers').select()
}

$(document).ready(function(){
	$('#btnBuy').click(buy);	
	$('form').submit(function( event ) {
	  buy();
	  return false;
	});
})
```

发现buy函数里用ajax并使用post向api.php发送了一个请求，ajax这里可以简单理解为异步传输，总之就是用来请求的。data中的内容用json形式包含了我们输入的数字。那么我们就能发现api.php中的buy函数的$numbers变量就是传入的json的numbers的值。这里最重要的地方在于for循环里的判断使用的是==而不是===。

- ### ==和===
- > ===比较两个变量的值和类型；==比较两个变量的值，不比较数据类型。
- > 在php中,如果bool和"任何其他类型"比较,"任何其他类型"会转换为bool。

所以这里取出numbers值的每一位与win_numbers的每一位做判断。这里“每一位”很重要，因为如果直接整个进行判断的话我们就不能使用下面的方法了。这个方法就是我们可以传入一个\[true,true,true,true,true,true,true]的列表，每次取出一位就等同于每次取出一个true，与win_numbers的每一位做比较。可是win_numbers是数字，不是布尔值，所以php就会将其强行转换为布尔值。

- ## 强制转换
- > 在PHP中当转换为 boolean 时，以下值被认为是 FALSE ：
- > (1) 布尔值 FALSE 本身
- > (2) 整型值 0（零）
- > (3)浮点型值 0.0（零）
- > (4)空字符串，以及字符串 “0”
- > (5)不包括任何元素的数组(注意,一旦包含元素,就算包含的元素只是一个空数组,也是true)
- > (6)不包括任何成员变量的对象（仅 PHP 4.0 适用）
- > (7)特殊类型 NULL（包括尚未赋值的变量）
- > (8)从空标记生成的 SimpleXML 对象
- > (9)所有其它值包括-1都被认为是 TRUE （包括任何资源）

0-9的数字很明显就是true。true==true，成立，我们因此就能获得大奖了。用burpsuite抓包更改请求内容。

![success](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/success.png)

一次可能还不够，多来几次就能买到flag了。

- ### Flag
- > cyberpeace{7c6b73377547b8c54cd09f314a7acbf1}