# Miscellaneous-300

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=539526e5-7dff-4049-8e38-43a4da054d4e_2)

这题看了答案也没自己试出来。电脑直接炸在第一步。

题目描述原地tp，就是个指向题目地址的链接。附件倒是有个zip，但是被加密了。好家伙上来就加密，而且根据全局加密位不是伪加密。这个时候就能上ARCHPR了。不过我没有，我是猜出来的，发现要提取的zip文件名是一串没啥规律的数字，输进去发现就是密码。

在重复以上操作5次后我觉得事情不对。套娃？得想个办法用python自动化解密，毕竟谁也不知道出题人到底套了多少层。冲浪！

```python
import zipfile
import re
zipname = "起始的zip文件名"
while True:
    try:
        ts1 = zipfile.ZipFile(zipname)
        res = re.search('[0-9]*',ts1.namelist()[0])
        passwd = res.group()
        ts1.extractall("存放解压完成的zip的路径",pwd=passwd.encode('ascii'))
        zipname = "存放解压完成的zip的路径"+ts1.namelist()[0]
    except:
        print("find")
```

到这我就不行了。电脑已经可以煎肉了都还没跑出来。完整看一遍wp才知道有1000多个……狠人。学习一下python中zip的解压和简单正则。

- ### ZipFile
  > 打开一个 ZIP 文件，file 为一个指向文件的路径（字符串），一个类文件对象或者一个 path-like object。
  - 声明：class zipfile.ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True, compresslevel=None, *, strict_timestamps=True)

- ### extractall
  > 从归档中提取出所有成员放入当前工作目录。
  - 声明：ZipFile.extractall(path=None, members=None, pwd=None)
  - 参数：path 指定一个要提取到的不同目录。 members 为可选项且必须为 namelist() 所返回列表的一个子集。 pwd 是用于解密文件的密码。

- ### namelist
  > 返回按名称排序的归档成员列表。

- ### re.search
  > 扫描整个字符串并返回第一个成功的匹配。
  - 语法：re.search(pattern, string, flags=0)
  - 参数
    > pattern	匹配的正则表达式<br>string	要匹配的字符串。<br>flags	标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。

- ### group
  > 匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。
  - 语法：group(num=0)
  - 分组索引从1开始；默认索引为0，表示匹配到的结果。

[0-9]*表示匹配任意多个数字。最后的zip里面有个wav文件，还要靠APCHPR。爆破出密码为b0yzz。wav文件放到audicity里转频谱图就能看见flag了。

- ### Flag
  > BallsRealBolls

终于不是很烫了。