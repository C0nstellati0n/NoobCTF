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
4. intval截断
- 在老版本的php中，intval会截断科学计数法下的字符串。但这样的字符串进行运算后会返回其运算后的值。比如`intval("1e4")`结果为1；`intval("1e4"+1)`结果为10001。该特性在php7修复
- 特征：php版本小于7
- 关键词：intval

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
3. 无字母数字
- 即使在所有字母和数字都被过滤的情况下，仍然可以用部分特殊符号和php的自增语法组建出全部字母的数字
- 特征：已获取rce，但题目有过滤。此技巧可用来绕过滤
- 关键词：无字母数字