# easyphp

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=5e5ff94c-3a5a-11ed-abf3-fa163e4fa609)

不要再来php了啊！

```php
<?php
highlight_file(__FILE__);
$key1 = 0;
$key2 = 0;

$a = $_GET['a'];
$b = $_GET['b'];

if(isset($a) && intval($a) > 6000000 && strlen($a) <= 3){
    if(isset($b) && '8b184b' === substr(md5($b),-6,6)){
        $key1 = 1;
        }else{
            die("Emmm...再想想");
        }
    }else{
    die("Emmm...");
}

$c=(array)json_decode(@$_GET['c']);
if(is_array($c) && !is_numeric(@$c["m"]) && $c["m"] > 2022){
    if(is_array(@$c["n"]) && count($c["n"]) == 2 && is_array($c["n"][0])){
        $d = array_search("DGGJ", $c["n"]);
        $d === false?die("no..."):NULL;
        foreach($c["n"] as $key=>$val){
            $val==="DGGJ"?die("no......"):NULL;
        }
        $key2 = 1;
    }else{
        die("no hack");
    }
}else{
    die("no");
}

if($key1 && $key2){
    include "Hgfks.php";
    echo "You're right"."\n";
    echo $flag;
}
```

先看下面，得到flag的条件是key1和key2都是1。先看key1的条件。

```php
if(isset($a) && intval($a) > 6000000 && strlen($a) <= 3)
```

要求get参数传参a，同时a的数字值大于6000000且长度小于3。乍一看感觉不可能啊，3个字符怎么表示7位数？只能说php太智能了，查询[intval](https://www.runoob.com/php/php-intval-function.html)函数，翻到下面的示例，赫然发现支持科学计数法。

```php
echo intval(1e10);                    // 1410065408
```

利用类似的方法进行构造很容易就能找打符合条件的a值了。比如6e9。

```php
if(isset($b) && '8b184b' === substr(md5($b),-6,6))
```

要求get参数传参b且其md5值且从索引-6开始的6个字符为8b184b。[substr](https://www.runoob.com/php/func-string-substr.html)是php里的切割函数，举个例子：

```php
echo substr("Hello_world",-6,6);    //_world
```

md5这种只能爆破，写个脚本就是了。建议写php，python有点难受。

```php
<?php
for($i=0;$i<=10000;$i++){
	if('8b184b'===substr(md5($i),-6,6)){
		echo $i;      //53724
	}
}
?>
```

至此key1完成，到key2了。

```php
$c=(array)json_decode(@$_GET['c']);
if(is_array($c) && !is_numeric(@$c["m"]) && $c["m"] > 2022)
```

c需要从get传入json数据。is_array($c)不知道有啥用，前面不是已经转换成array了吗？不管那么多，后面要求c["m"]不是数字但是大于2022。我记得php里面字符串和数字比较是看第一个字符的ascii值（不确定，小心被误导，但是纯字符串永远小于2022），因此按照一般思路，is_numeric为false就是字符，而字符小于数字，绕不过去。

但是php它智能啊，php在数字和字符串比较之前还会尝试将字符串转为数字，能转的部分拿出来比较，不能转才会到第一种情况。假如我们的payload是2023a，is_numeric为false，因为多了个a；比较也通过，因为能转数字的部分2023比2022大。

```php
if(is_array(@$c["n"]) && count($c["n"]) == 2 && is_array($c["n"][0]))
```

要求键n处是一个数组，且键n处数组要有两个元素，且第一个元素是数组。嵌套一下就能过了。

```php
$d = array_search("DGGJ", $c["n"]);
$d === false?die("no..."):NULL;
foreach($c["n"] as $key=>$val){
    $val==="DGGJ"?die("no......"):NULL;
}
```

[array_search](https://www.runoob.com/php/func-array-search.html)搜索的是数组中的键值，并返回对应的键。如果没找到就返回false。看起来我们要让数组里有值为DGGJ。但是接下来一个foreach要求数组的值里面没有DGDJ。又矛盾了，说明我们又要找找看php的智能之处了。

我们可以传入一个数字型数组，因为array_search搜寻的是DGGJ这个字符串，那么php就会把DGGJ转为0，此时查找的就是0在数组里的位置了。我们可以把0放在索引为1的地方，这样1===false不成立，绕过第一个die。接着foreach不用多说，肯定没有。成功让key2为1。最终payload如下。

- http://61.147.171.105:63294/?a=1e9&b=53724&c=%7B%22m%22:%222023a%22,%22n%22:%5B%5B2,3%5D,0%5D%7D

%7B%22m%22:%222033%2500%22,%22n%22:%5B%5B2,3%5D,0%5D%7D是{"m":"2023a","n":[[2,3],0]}的url编码形式。逗号不用编码了，反正没影响。n这个数组里面2，3值随便改，我们分析过没有影响。0只要不在第0位索引就行了。

- ### Flag
  > cyberpeace{9309f5b2935b06712ec1520c5ded07d9}