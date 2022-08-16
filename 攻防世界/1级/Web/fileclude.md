# fileclude

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=21301f1c-17ae-11ed-abf3-fa163e4fa609&task_category_id=3)

进来只有一段php代码。

```php
WRONG WAY! <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET["file1"]) && isset($_GET["file2"]))
{
    $file1 = $_GET["file1"];
    $file2 = $_GET["file2"];
    if(!empty($file1) && !empty($file2))
    {
        if(file_get_contents($file2) === "hello ctf")
        {
            include($file1);
        }
    }
    else
        die("NONONO");
}
```

看到include就应该唤起你的DNA了，php典中典文件包含。最开始的“WRONG WAY!”是flag.php输出的内容，因为最开始有一句“include("flag.php");”，但这并不代表我们的目标不是flag.php，flag也可以藏在注释里，自然就不会被输出。

这里只有一个过滤：“if(!empty(\$file1) && !empty($file2))”，要求get参数file2所对应的文件内容是“hello ctf”。注意是文件内容而不是文件名。

- ### file_get_contents
  > 把整个文件读入一个字符串中。
  - 语法：file_get_contents(path,include_path,context,start,max_length)
  - 参数
    > path -- 必需。规定要读取的文件。路径不一定是是本地文件路径，还可以是网络url。
    > include_path -- 可选。如果也想在 include_path 中搜寻文件的话，可以将该参数设为 "1"。
    > context -- 可选。规定文件句柄的环境。context 是一套可以修改流的行为的选项。若使用 null，则忽略。
    > start -- 可选。规定在文件中开始读取的位置。该参数是 PHP 5.1 新加的。
    > max_length -- 可选。规定读取的字节数。该参数是 PHP 5.1 新加的。

很明显这里只用了第一个参数。现在问题来了，我怎么知道服务器上哪个文件的内容是"hello ctf"？甚至可能都没有这个文件。在服务器上找这个文件肯定行不通，那就自己写一个吧。

一个小经验：php的伪协议在文件包含题里有妙用。你甚至都不需要记住全部的伪协议，只要知道有这一个概念，下次遇到了直接搜一般都能找到办法。这次我搜到了一个很相似的[题目](https://www.cnblogs.com/wjrblogs/p/12285202.html)，里面的利用方法也正好适用。伪协议总结可以[看这](https://segmentfault.com/a/1190000018991087)。这里用到的是data，在[这道题](../../2级/Web/Web_php_include.md)也有使用。payload就很简单了。

- ?file1=flag.php&file2=data://text/plain;base64,aGVsbG8gY3Rm

aGVsbG8gY3Rm是hello ctf的base64编码格式。执行后会发现WRONG WAY！在下面出现了，证明成功绕过。我是这么理解的：data://text/plain;base64,aGVsbG8gY3Rm的data://text/plain;base64部分是url，aGVsbG8gY3Rm部分是url对应的内容。所以file_get_contents读取url对应的内容并按照指定的base64进行解码，内容自然是一样的。这个理解可能不对但是看起来很合理(･･;)

接下来就是包含flag.php了。直接包含肯定不行，要包含源码。包含源码也要利用一个php伪协议：php://filter。可以在上面找到，也在[这道题](../../3级/Web/ics-05.md)中有使用。payload如下。

- ?file1=php://filter/read=convert.base64-encode/resource=flag.php&file2=data://text/plain;base64,aGVsbG8gY3Rm

执行后就能拿到源码了。

- PD9waHAKZWNobyAiV1JPTkcgV0FZISI7Ci8vICRmbGFnID0gY3liZXJwZWFjZXs4OTc1ODNkYzI0YTQ3OTJlNzYzMmE3MWVjYjAzZjExNH0=

base64解码后可得flag。

- ### Flag
  > cyberpeace{897583dc24a4792e7632a71ecb03f114}