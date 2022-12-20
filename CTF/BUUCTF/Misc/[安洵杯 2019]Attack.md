# [安洵杯 2019]Attack

[题目地址](https://buuoj.cn/challenges#[%E5%AE%89%E6%B4%B5%E6%9D%AF%202019]Attack)

浅浅追踪一下tcp流，感觉是在扫目录，很多404 not found。目标是flag，那就做个过滤，`tcp contains flag`。还真在第824个流发现了内含flag.txt的zip。保存下来，却发现要密码，提示“这可是administrator的秘密”。那不就密码吗？可是去哪里找密码呢？

[wp](https://blog.csdn.net/mochu7777777/article/details/109556707)用了一种更简单的办法，直接导出http object，发现一个名为lsass.dmp的文件。这种文件都可以直接用[mimikatz](https://github.com/ParrotSec/mimikatz)分析，三步获取密码。

```
privilege::debug
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords full
```

密码是W3lc0meToD0g3。有了密码就能解压压缩包得到flag了。结果我发现一个坑，之前第824个流发现的压缩包解压出来只有提示的内容，没有flag！还是foremost最管用。直接foremost pcap就能出来正确的压缩包了。

## Flag
> flag{3466b11de8894198af3636c5bd1efce2}