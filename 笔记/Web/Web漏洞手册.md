# Web漏洞手册

是时候整理一下笔记了，顺便写篇个人的"web参考手册"。以下仅为个人习惯

首先判断题目考点。第一步一般只能判断考点的大分类。题目要是给出了admin bot url，基本宣告了这题为xss等需要外部介入的题。然后我会看一眼源码，根据语言继续细分

然后看一眼网站。当然还是根据情况判断。要是源码很少我就直接看源码了；要是源码很多我会稍微瞄一眼然后看网站。有些时候虽然源码很多，但实际网站上的操作不多。可根据能执行的操作定位源码的重要部分

最后就是找bug了。一定要把源码的每个部分都看一眼，包括dockerfile和使用的dependencies。注意安装的软件、依赖项版本。一般都会安最新的或者稳定版，如果刻意安装了某个特定版本，最好搜一下`软件/依赖项名 版本`，看看有没有已知漏洞。就算没有也不要掉以轻心。有些时候某个库单独没任何漏洞，但存在可被其他库/代码逻辑利用的gadget

如果是那种脚本题（没有bug，只需按照源码的指示即可得到flag），直接莽吧，chatgpt对这种题有奇效

这边按照源码语言/漏洞类型整理一下我所见过的漏洞。我会在这里记录漏洞的简单描述、关键词和特征。若在题目里看到类似该特征的代码/内容可以考虑此漏洞（本人才疏学浅，总结的特征不完全准确。拥有该特征并不完全等于有此漏洞）。确认是该漏洞后在Web笔记处ctrl+f搜索漏洞关键词就能拿到该漏洞的相关例题。注意同一关键词可能搜出来不同语言里的漏洞，请自行根据目前所在语言/漏洞项过滤

## Python

### Flask

1. 模板注入
- flask渲染模板时可使用表达式，语法为`{{expression}}`。若没有正确过滤用户输入内容，直接将用户输入内容插入template并渲染，攻击者可利用此语法获取rce
- 特征
  - 网站会回显用户输入内容。此时可将输入内容换为`{{7*7}}`，返回49则确定漏洞
  - 无过滤直接拼接用户输入至某个字符串并将该字符串传入`render_template_string`函数
  - `Template(str).render()`
- 关键词
  - 模板注入
  - ssti
2. Werkzeug密码破解
- flask内部使用Werkzeug，而Werkzeug使用的密码格式可以爆破。不到最后一步不要考虑此漏洞
- 特征
  - 可以获取网站内部存储的Werkzeug密码。密码以`pbkdf2:sha256`开头
  - 有些题目会特别提供一个wordlist
- 关键词：(Werkzeug) password encryption
3. session伪造
- flask用来验证身份/保存用户数据的session cookie可以伪造。但需要得知服务器用来签名session的密钥，或者爆破
- 特征
  - 题目泄露了网站使用的密钥（`app.config['SECRET_KEY']`）
  - 题目提到密钥较简单或给出wordlist
- 关键词
  - session/cookie伪造
  - secret key/`secret_key`
4. debug console pin码伪造
- flask运行app时若添加了`debug=True`选项，网站会自动添加路径`/console`。使用pin码解锁console后就能得到python shell。pin码的计算需要服务器上的私密信息和文件，因此该漏洞之前可能有诸如任意文件读取，代码执行等前置漏洞
- 特征：访问`/console`弹出输入pin码的窗口
- 关键词：debug console
5. 内存马
- 题目已有rce，但远程机器无法出网，eval/exec等函数的执行结果难以回显。此时可利用flask框架里已有的gadget添加一个自定义路由，访问该路由会调用自定义匿名函数，便能轻松回显命令执行结果。见 https://www.cnblogs.com/gxngxngxn/p/18181936
- 特征：flask框架下已获取rce，但题目描述里说明或经测试发现题目机器不出网
- 关键词：内存马
6. 解析差异（http参数）
- 遇到重复的http参数时（如`a=1&a=2`），flask取第一个值。但其他框架不一定如此。例如php取最后一个值。两者的差异可能会导致程序里的逻辑漏洞
- 特征：遇见php和python flask搭配的网站需要特别注意。这类题目通常由前后端构成。前端针对http传入的参数进行检查，无异常后传入后端。但前后端并不使用同一种语言搭建，导致前端的检查走到后端时失效
- 关键词：HTTP parameter pollution
7. 解析差异（http header）
- 在flask（Werkzeug）中，下划线(`_`)会被看作`-`。如果发两个header `Content-Length`和`Content_Length`，go-proxy只会考虑第一个`Content-Length`，而flask会考虑第二个`Content_Length`（第一个header的值被第二个覆盖了）。可能存在请求走私（request smuggling）漏洞
- 特征：flask和go-proxy搭配使用
- 暂无关键词，因为此漏洞相关题目的wp损坏了……具体题目名为`Notes V1`
8. `safe`的错误使用
- flask里可用`{{content | safe}}`跳过对content的默认转义。如果程序之前也没有过滤content，有xss的风险
- 特征：在源码里看到safe的使用。一般不会莫名其妙加这个关键词的，毕竟多一层转义的保护总比没有好
- 关键词：`| safe`
9. 依赖项（dependency）投毒/源码文件覆盖
- flask运行app时若添加`debug=True`选项，则在文件内引用的外部库或是文件本身发生变化时，应用会自动重启。将app使用的文件替换成其他代码即可获取rce
- 特征
  - 能修改/覆盖源码文件
  - `app.run(debug=True)`
  - 可以使程序崩溃后重启
- 关键词
  - dependency
  - `render_template`
  - `TEMPLATES_AUTO_RELOAD`
- 注意：若覆盖的文件是template文件，则flask在调用`render_template`函数渲染文件后会保存文件内容至cache。后续覆盖template文件后不会影响cache，自然也不会影响`render_template`的结果（与`debug=True`无关）。有两种方式解决：
  - 覆盖从未被渲染过的template文件
  - 使程序崩溃后重启
  - 程序里有`app.config['TEMPLATES_AUTO_RELOAD'] = True`选项。该选项表示修改template后无需重启app，程序会自动重新加载修改后的template文件

### 第三方库

python第三方库相关的漏洞与特性

1. PIL/Pillow RCE
- Ghostscript中存在大量漏洞，并影响任何内部使用Ghostscript的图像处理库。如python的PIL/Pillow
- 特征：安装依赖项时使用了Ghostscript `9.24`前的版本
- 关键词：ghostscript
2. aiohttp路径穿越
- 配置错误会导致提供静态文件的路径出现路径穿越
- 特征：`web.static('/files', './files', follow_symlinks=True)`
- 关键词：aiohttp
3. gitPython RCE
- gitPython是一个用于和git仓库交互的python第三方库。该库在`3.1.30`之前都存在RCE漏洞
- 特征：安装的gitPython小于`3.1.30`
- 关键词：gitPython
4. reportlab RCE
- reportlab是一个动态生成pdf的第三方库。该库曾出现过两个不同的rce漏洞
- 特征：`reportlab==3.6.12`
- 关键词：reportlab
5. [PyYAML](https://github.com/yaml/pyyaml)反序列化
- PyYAML库支持python对象的序列化，因此反序列化时就容易出问题
- 特征：`yaml.load`
- 无关键词，原wp链接已损坏。此为补充的漏洞介绍链接： https://book.hacktricks.xyz/pentesting-web/deserialization/python-yaml-deserialization
6. [Starlette](https://www.starlette.io)框架条件竞争
- 此框架中存在条件竞争，允许攻击者下载文件大小为零（`os.stat`给出大小）的`/proc`目录下的文件
- 特征：网站使用starlette框架的FileResponse
- 关键词：Starlette

### 其他

python语法/内置库和函数本身的漏洞和特性。该项可能省略部分特征与关键词，因漏洞名本身就是特征和关键词

1. pickle反序列化
- pickle是python中一个序列化/反序列化对象的模块。反序列化时python会调用加载对象的魔术方法`__reduce__`。自定义一个`__reduce__`函数使其执行恶意代码即可获得rce
- 特征
  - `pickle.loads`
  - `numpy.load(file, allow_pickle=True)`
  - `hummingbird.ml.load`
  - 网站使用bottle框架且用户可控制cookie内容
- 关键词：pickle
2. 变量存储位置
- python将对象、变量等内容存储在堆上。可以利用`/proc/self/maps`和`/proc/self/mem`读取到变量的内容。注意`/proc/self/mem`内容较多而且存在不可读写部分，直接读取会导致程序崩溃。因此需要搭配`/proc/self/maps`获取堆栈分布，结合maps的映射信息来确定读的偏移值
- 特征：题目有任意文件读取或暴露`/proc/self/maps`和`/proc/self/mem`文件
- 关键词：`/proc/self/maps+/proc/self/mem`
3. json处理差异
- python与mariadb处理json重复键名时的操作不同。python看最后一个key，mariadb看第一个
- 特征：处理json时混用了两个处理器
- 关键词：json-interoperability
4. 格式化字符串漏洞
- 若`str.format`执行之前str本身包含用户可控制的内容，则可以注入出全局变量等内容。请与c语言的里的同名漏洞区分。python的格式化字符串漏洞仅能用于泄漏信息
- 特征：`str.format`，str包含攻击者可控制内容
- 关键词：格式化字符串漏洞
5. float计算缺陷
- 任何数与python里的float上限`1.8e+308`相加都会返回inf
- 特征：注意程序处理算术逻辑时是否能正确处理inf
- 关键词：Floating point type confusion
6. int_parsing_size错误
- 当整数过大时，将其转为字符串会报错
- 特征：一个该漏洞的使用案例。假如有算式x+a，a可控，目标是得到x。可以利用"是否报错"进行binary search找到x
- 关键词：int_parsing_size
7. class pollution
- 类似js的原型链污染。该漏洞可以添加/修改全局变量，还能配合其他第三方库的gadget实现其他效果（污染flask session）
- 特征：题目里出现 https://book.hacktricks.xyz/generic-methodologies-and-resources/python/class-pollution-pythons-prototype-pollution 里的merge函数
- 关键词：class pollution
8. `os.path.join`/pathlib的`Path.joinpath`
- 这两个函数都是路径拼接函数。在其中一个参数为绝对路径时，函数会舍弃前面的参数。利用这个特点可以绕过一些路径限制
- 关键词：`path.join`
9. `os.path.splitext`
- 此函数无法正确提取出扩展名。例：
```py
>>> splitext('a/a.html')
('a/a', '.html')
>>> splitext('a/.html')
('a/.html', '')
```
10. urllib3请求走私
- `urllib3.PoolManager().request()`可以发送请求。该函数有个可选参数headers，允许用户以字典的形式传入自定义header。如果攻击者可以控制任意header名及其值，会出现请求走私
- 特征：可控制headers字典键值对
- 关键词：`http.request`
11. urllib url解析漏洞
- 在url前面加个空格会导致urllib认为该url的scheme为空
- 特征：urllib版本小于`3.11.4`
- 关键词：urllib

## PHP

### 特性/漏洞

php语言本身的特性和相关可利用的漏洞

1. 模板注入
- 原理类似Python/Flask/模板注入，只不过是不同语言的不同模板引擎
- 特征
  - 网站会回显用户输入内容
  - 不对用户输入做过滤
- 关键词
  - twig
  - smarty
2. preg_replace命令执行
- preg_replace函数有个`/e`选项。该选项使preg_replace将 replacement 参数当作 PHP 代码（在替换完成之后）执行。要确保 replacement 构成一个合法的 PHP 代码字符串，否则 PHP 会报告在包含 preg_replace 的行中出现语法解析错误
- 特征：preg_replace函数使用了`/e`选项
- 关键词：preg_replace
3. md5相关特性
- php中md5函数的可利用特性如下
  - `md5($val,true)`表示将hash结果以原始二进制格式返回。意味着结果可能千奇百怪。一个常见的用法是sql注入
  - php的弱等于`==`会先将两边的变量类型转化成相同的类型，再进行比较。如果两个变量的md5结果都以`0e`开头，则弱等于结果为true
  - 如果传入md5的参数不是字符串，而是数组；md5函数无法解出其数值时，会报警告。但是还能得到`===`强比较的相等
- 特征
  - md5函数的第二个参数为true
  - 比较时使用了弱等于
  - 攻击者可控制md5的参数类型（常见于post或get传参）
- 关键词
  - raw md5
  - md5相关特性
  - 绕过md5
4. intval截断
- 在老版本的php中，intval会截断科学计数法下的字符串。但这样的字符串进行运算后会返回其运算后的值。比如`intval("1e4")`结果为1；`intval("1e4"+1)`结果为10001。该特性在php7修复
- 特征：php版本小于7
- 关键词：intval
5. 反序列化
- 序列化（serialize）将对象的属性名，属性值，属性类型转换成字符串；反序列化（unserialize）则将字符串还原回对象。如果能控制unserialize函数的参数，就可以伪造当前语境下任意一个对象。见 https://blog.csdn.net/qq_45521281/article/details/105891381 。注意序列化时无法序列化对象的函数，所以反序列化漏洞利用的一般是当前语境下已有的函数，并通过修改对象的属性得到恶意代码执行
- 特征
  - 攻击者可控制unserialize函数的参数
  - 可以上传phar文件，且可以控制文件系统函数的参数，使其用`phar://`伪协议解析phar文件
- 关键词：反序列化
6. 序列化字符串逃逸
- 序列化字符串遵循特定格式，在序列化完成后对序列化字符串做修改可能导致攻击者可以伪造、修改序列化结果
- 特征：程序在序列化完成后修改序列化字符串
- 关键词：反序列化逃逸
7. 传参特性
- PHP会将传参中的空格` `、小数点`.`自动替换成下划线
- 特征：这个特性本身没有任何问题，但要注意由此衍生的解析差异
- 关键词：`[MRCTF2020]套娃`
8. pcre回溯限制
- php的正则使用了NFA引擎。NFA引擎运行时有回溯操作，而这个操作有上限，默认是100万。如果输入字符串执行正则时回溯次数超过了这个上限，就会返回`PREG_BACKTRACK_LIMIT_ERROR`。这个结果不强等于0，但可以被放在if语句里强制转换成false
- 特征
  - preg_match
  - 用户可以输入任意长度的内容
  - 使用`if(preg_match('xxx', $input))`作为条件
- 关键词：pcre
9. basename特性
- basename函数返回路径中的文件名部分。但如果文件名是一个不可见字符，便会将上一个目录作为返回值：
```php
$a="/c.php/test"
basename($a) => test
$b="/c.php/%ff"
basename($b) => c.php
```
- 关键词：basename
10. url解析
- 当访问一个`存在的文件/不存在的文件`url时，php会自动忽略不存在的部分。比如`/index.php`和`/index.php/dosent_exist.php`都能访问到`index.php`
- 关键词：url解析特性
11. mt_rand种子爆破
- mt_rand函数生成的随机数是伪随机数，不能用于生成安全令牌、核心加解密key等内容。给出mt_rand的几个输出，可以恢复其seed，进而预测接下来的随机数
- 程序使用mt_rand且可以得知连续的几个输出
- 关键词：`mt_rand`
9. exif_imagetype绕过
- exif_imagetype函数读取文件开头的几个字节。如果这些字节在已知的图片签名内，返回true；否则返回false。只需要在文件开头加上一些特殊的字节就能使任意文件被伪装成图片
- 关键词：exif_imagetype
10. open_basedir绕过
- open_basedir是PHP中为了防御PHP跨目录进行文件（目录）读写的设置。但存在绕过手段使攻击者可以读取限制之外的文件
- 特征：phpinfo中记录了open_basedir的值
- 关键词：open_basedir
11. create_function代码注入
- create_function是php里用于动态生成函数的函数，在新版本已废弃。其内部实现可能与拼接有关，见以下payload：
```php
$newfunc = create_function('', '}eval($_POST["cmd"]);//');
```
结果如下：
```php
function newfunc(){
}eval($_POST["cmd"]);//}
```
- 特征：可以控制create_function的参数
- 关键词：create_function
12. 绕过require_once函数
- require_once函数保证一个文件只能被包含一次。但函数的实现有瑕疵，允许攻击者用`/proc/self`目录绕过限制
- 关键词：require_once
13. parse_url绕过
- 在path前多加几个斜线`/`可以绕过部分过滤
- 关键词：parse_url
14. hash_hmac函数特性
- `hash_hmac($algo, $data, $key)`：当传入的data为数组时，加密得到的结果固定为NULL
- 关键词：hash_hmac
15. bcrypt password_verify永真hash
- 由于password_verify函数的错误实现，存在特殊的hash可以匹配所有密码，让函数返回true。见 https://github.com/php/php-src/security/advisories/GHSA-7fj2-8x79-rjf4
- 特征：可以控制`password_verify("pwd", 'hash')`的hash部分
- 关键词：password_verify

### 技巧

题目中常见的技巧

1. 伪协议
- php里的伪协议众多，能干的事情从文件读取到rce。详细的介绍见 https://segmentfault.com/a/1190000018991087
- 特征:能控制以下任一函数的参数
  - include
  - require
  - file_get_contents
  - file_put_contents
- 关键词：伪协议
2. 反引号和`<?=`
- php中，反引号可用来直接执行系统命令。`<?=`是echo的别名用法，用来输出命令执行结果
- 特征：已获取rce，但题目有过滤。此技巧可用来绕过滤
- 关键词：反引号
3. 无字母数字/引号
- 即使在所有字母和数字都被过滤的情况下，仍然可以用部分特殊符号和php的自增语法组建出全部字母的数字
- 特征：已获取rce，但题目有过滤。此技巧可用来绕过滤
- 关键词
  - 字母数字
  - 字母引号
4. extract变量覆盖
- [extract](https://www.php.net/manual/en/function.extract.php)是php里的一个函数。利用这个函数攻击者可以自定义/覆盖任何变量及其值
- 特征：将用户控制的数组作为extract的参数，如`extract($_POST)`
- 关键词：extract
5. 魔术方法
- [魔术方法](https://www.php.net/manual/zh/language.oop5.magic.php)是php中一系列以`__`开头的函数，会在对象执行特定操作时自动调用。常在反序列化漏洞中使用，将反序列化链串联起来
- 特征：单纯魔术方法没有任何问题，但同时出现反序列化漏洞时要注意
- 关键词：魔术方法
6. 特殊标签
- 有些程序会过滤常见的php标签。这时可以尝试用特殊标签绕过过滤
- 特征：常配合代码注入使用
- 关键词：特殊标签
7. shell构造技巧
- 部分题目的黑名单/白名单函数比较刁钻。这时构造eval的payload时可以考虑`$_GET[0]($_GET[1])`，用较少的字符实现任意shell
- 特征：eval
- 关键词：数学函数（利用常见数学函数构造shell）
8. 文件操作技巧
- PHP中可以使用POST或者PUT方法进行文本和二进制文件的上传。文件被上传后，默认存储到服务端的默认临时目录中。正常来说该文件会在表单请求结束时被删除。但如果php非正常结束，比如崩溃，那么这个临时文件就会永久的保留。比如，在上传木马的同时用`php://filter/string.strip_tags`使php崩溃重启，存有木马的tmp file就会一直留在tmp目录。进行文件名爆破并连接木马就可以getshell
- 特征
  - 可以得知tmp下目录的文件或允许爆破文件名
  - 可以使php崩溃
  - 有include等文件包含函数包含木马文件
- 关键词：操作trick
9. 伪协议绕过exit
- 有些程序会在文件开头加上一句`exit`，使得后续拼接的shell内容无法执行。此时可以用伪协议绕过开头的exit
- 特征：程序允许写入并上传shell文件，但会在开头加上exit
- 关键词：绕过exit
10. FFI扩展利用
- php 7.4新加了FFI扩展功能，允许php调用C语言写的库。这也为攻击者提供了绕过disable_functions的手段。只需加载libc里的system函数即可执行系统命令
- 特征
  - phpinfo中显示众多disable_functions
  - 配置项`ffi.enable=1`
  - 没有`ffi.enable=preload`
- 关键词：FFI扩展
11. `_SESSION`数组的定义
- `_SESSION`数组在`session_start()`初始化后才产生。如果在`php.ini`中设置`session.auto_start=On`，那么PHP每次处理PHP文件的时候都会自动执行`session_start()`。但是`session.auto_start`默认为Off。与Session相关的另一个叫`session.upload_progress.enabled`，默认为On，在这个选项被打开的前提下在multipart POST的时候传入PHP_SESSION_UPLOAD_PROGRESS，PHP会执行`session_start()`
- 特征:题目使用`isset($_SESSION)`控制文件的访问权限。且只要求`_SESSION`数组被定义，不要求`_SESSION`数组里有值
- 关键词：`SESSION_UPLOAD`
12. getimagesize相关绕过
- 可用以下代码段绕过图片长宽:
```
#define width 1
#define height 1
```
可用 https://github.com/huntergregal/PNG-IDAT-Payload-Generator 往图片里插入木马，并符合getimagesize格式
- 关键词：getimagesize
13. `pearcmd.php`的利用
- `pearcmd.php`是pecl/pear中的文件。pecl是PHP中用于管理扩展而使用的命令行工具，而pear是pecl依赖的类库。在7.3及以前，pecl/pear是默认安装的。如果题目出现本地文件包含漏洞，就能利用这个文件getshell
- 特征
  - 题目已有本地文件包含漏洞
  - 环境内有`pearcmd.php`
- 关键词：pearcmd
14. 文件包含rce
- 当可以完全控制require/include的文件名时，就能使用[PHP filter chain generator](https://github.com/synacktiv/php_filter_chain_generator) getshell
- 关键词：filter chain

## XSS

### 通用技巧

只要符合要求就能用的技巧，与网站是什么语言搭建的无关

1. 绕过csp
- Content Security Policy(CSP)为网站设置执行代码，引入资源等内容时的安全策略。xss payload常与这几项有关，因此csp会阻挡payload的执行。大部分题目都会设置csp来提高构造payload的难度，所以需要学习常用的绕过csp的方法
- 特征/关键词
  - `script-src 'self' 'https://ajax.googleapis.com;'`:只能从当前网站和`https://ajax.googleapis.com`导入script。但`https://ajax.googleapis.com`本身存在可利用的xss
  - `default-src 'self'`：阻挡跨域fetch。xss payload不能用fetch带出数据，但可以用`window.location`
  - `default-src www.youtube.com`:youtube存在已知的jsonp端点，允许攻击者执行xss payload。相关题目的关键词是jsonp
  - `default-src 'self';script-src 'none'`：条件比较苛刻，具体见例题。关键词:Noscript
  - `default-src 'none';style-src 'unsafe-inline';script-src 'unsafe-eval' 'self';connect-src xxx;connect-uri xxx`：可用WebRTC绕过。关键词：WebRTC
    - 如果题目基于chrome且admin bot不断更换自己使用的profile，这个csp下还有另一种做法：使用Credential Management API;如果题目浏览器基于chromium且开启了实验功能，还可以用PendingBeacon API。见题目Elements
  - 如果题目的admin bot是puppeteer且能够控制`page.goto`的url，则可以用`javascript://`获得xss。csp似乎不会阻挡url的xss
  - 如果有办法测量admin bot访问网站的时间或成功与否，可利用这点构建侧信道攻击。可以绕过任何csp。不过大部分题目不会暴露admin bot的状态，因此很多时候用不了。关键词：side channel
2. css injection
- 常在csp较为严格或有过滤时使用。主要利用css语法自带的内容匹配以及外部资源加载功能一点一点泄漏flag
- 特征
  - 能注入html，特别是css相关内容
  - 没有阻止css加载外部资源的csp
  - 要泄漏的内容在当前网页的html里（包括shadow dom，但在cookie等地方不行）
- 关键词：css
3. dom clobbering
- 通过注入特定的html破坏js环境，从而影响代码逻辑。具体例子见 https://portswigger.net/web-security/dom-based/dom-clobbering 。其实和xss没有太大关系，只是js+html的奇怪特性；但不知道为什么目前我见过的例题两者总是一起打配合
- 特征
  - 能够注入html代码
  - 有诸如`if(xxx.xxx)`的逻辑，且if语句里的代码块是目标
  - 需要覆盖、设置某个字段或函数
- 关键词：dom clobbering
4. xs leak
- 目前我见过的xs leak题目基本局限于“注入js代码，利用侧信道攻击泄漏内容“。至于怎么侧信道，要么题目提供了相关的逻辑（比如搜索功能）；要么利用浏览器自身的特性（比如chrome的url长度限制）等。不过xs leak其实有很多类型很多攻击手段，见 https://xsleaks.dev
- 特征：能注入html/js代码，或能构建侧信道oracle
- 关键词
  - xs-search
  - xs-leak
  - xs leak
5. mXss
- 将html插入dom树时，浏览器的渲染引擎会重新整理插入的代码。如果构造得当的话，可以让整理后的结果出现可执行的xss payload。见 https://juejin.cn/post/6844903571578699790
- 特征
  - 题目没有过滤svg，math，p等标签
  - 使用innerHTML属性
- 关键词：mxss
6. Cookie jar overflow
- 浏览器里能设置的cookie数量有限。达到限制后，旧的cookie会被新添加的挤掉。这种方法甚至能移除HttpOnly的cookie。利用这个特点可以实现登出当前账户
- 特征：能执行js代码，需要移除某个已有的cookie
- 关键词：cookie jar overflow
7. /cdn-cgi/trace
- 所有使用cloudflare的网站都有这个路径（在源码里看不到）。这个路径会反射一些内容，比如user-agent。如果让网站用html处理其返回内容，就能在user-agent处插入html代码从而实现xss
- 特征：cloudflare网站
- 关键词：cdn
8. chrome特性
- 在chrome环境下，如果用js创建一个元素并设置其innerHTML，即使这个元素没有被插入dom，innerHTML里的xss payload也会执行
- 特征：可以控制任何元素的innerHTML，即使这个元素不在dom树里
- 关键词：`"div"`
9. cookie tossing
- 假如在`a.b.com`设置了cookie `c=d`，在`b.com`上也可以读取cookie c的值。问题在于`b.com`无法判断得到的d是自己设置的还是`a.b.com`设置的。这个特性不会影响[public suffix list](https://wiki.mozilla.org/Public_Suffix_List)里的domain
- 特征：某个域名读取cookie的值作为xss payload/关键逻辑，且可以构建这个域名下的子域名
- 关键词：toss
10. 编码解析差异
- 应在response中用Content-Type指定文档的字符集。如果服务器不明确指出且html文档里没有设置charset的内容，则具体字符集由浏览器自动检测。字符集ISO-2022-JP非常特殊，包含四种escape sequences，用来切换当前使用的字符集（只要浏览器看见它们就会切换到对应的字符集）。意味着整个文档可以用多种字符集进行渲染。这其中的差异可以用来藏xss payload
- 特征
  - 服务器返回的response报文中没有指定Content-Type
  - 题目有过滤，攻击者需要利用某种方式使过滤时和实际访问时看到内容不一样
- 关键词：ISO-2022-JP