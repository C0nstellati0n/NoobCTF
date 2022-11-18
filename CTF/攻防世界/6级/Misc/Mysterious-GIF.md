# Mysterious-GIF

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=335e2243-6856-48f9-9258-e2ad82dc46c7_2&task_category_id=1)

真的太能藏了。

拿到个gif，stegsolve把每一帧都看了一遍，没东西。日常binwalk，walk出一个隐藏的zip。提取后得到一个temp.zip，解压得到一个enc文件。提示信息值得看看。

```
Archive:  temp.zip
warning [temp.zip]:  112464 extra bytes at beginning or within zipfile
  (attempting to process anyway)
 extracting: partke.enc
```

多了11万多个字节？你这没有鬼我不信。继续binwalk，发现里面藏了整整256个zip，都是enc后缀。根据Crypto的经验，看见enc文件就想到rsa，那就需要私钥。strings命令四两拨千斤，-n参数限制一下长度，毕竟私钥肯定不会太短，还能过滤一些无用的字符串。

- strings 382e5c74bb7b4214ac6b855e503a56b9.gif -n 30

确实是出来了一大串16进制，然而解密发现内容不全。[wp](https://www.cnblogs.com/stickonit/p/16424652.html)提供了另一种命令：[identify](https://blog.csdn.net/qq_42303254/article/details/89528108)。这个命令的参数-format可以提取符合某个格式的字符串。

- identify -format "%c" ctf.gif

这回的输出就是完整的了。不过这个私钥缺少了openssl的密钥头和尾，需要手动添上。

```
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
```

然后就能用openssl解密了。

- openssl rsautl -decrypt -inkey privatekey.key -in partaa.enc -out result

问题是256个文件我们手动解要解到什么时候？写个bash脚本来帮忙做。

```bash
#原始加密文件目录位置
src_dir='extracted'
#解密后存放目录位置
dst_dir='flag'

#解压后目录下的文件
files=$(ls  $src_dir)

#nums数组存储了000-268等宽的数字用于命名 
i=0
nums=()
for j in $(seq -w 268);do
        nums[$i]=$j
        ((i++))
done

n=0
for file in $files;do
        openssl rsautl -decrypt -inkey ./test.key -in $src_dir/$file -out $dst_dir/${nums[$n]}
        ((n++))
done

#合并图片

cat flag/* > target.jpg
```

最后得到的图片写着flag。

## Flag
> FelicityIsFun