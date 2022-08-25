# Miscellaneous-200

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=2922d6ba-c90d-493f-ac22-13272de6f760_2)

附件下载下来是一个文本文件。打开是一堆数字的组合

![文本文件内容](https://github.com/C0nstellati0n/-CTF-/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/file.png)

我一看到255，255，255的组合就立刻想到了RGB值。思路非常简单直白，读取文本文件的每一行，把每一行都当作一个像素的RGB值，全部拼在一起应该可以出来一张图片，内容就是flag。

不过我不是很会用PIL，在网上搜了一下后得到了下面的代码:
```
from PIL import Image
x=503   #由整数分解计算得到
y=122
result=Image.new("RGB",(x,y))   #创建一个新的空白图片
with open("你的文本文件绝对路径",'r') as f:       #打开txt所在路径。使用with可以省去最后f.close()这一步，不用担心更多的问题
    for i in range(x):
        for j in range(y):
            line=f.readline()
            rgb=line.split(",")
            #print(rgb)
            try:    #最后一行是空格，会报错。就用一下比较丑陋的代码跳过就行了
                result.putpixel((i,j),(int(rgb[0]),int(rgb[1]),int(rgb[2])))    #putpixel用法:第一个参数为像素放置的坐标，第二个参数为rgb像素值
            except:
                pass
result.show()   #直接展示图片
```

这个x和y值我是通过一个[网站](https://www.alpertron.com.ar/ECM.HTM)整数分解得到的。因为整个文本文件的行数为61366，整数分解后的结果如下：

![分解结果](https://github.com/C0nstellati0n/-CTF-/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/code.png)

分析一波：图片只有长和宽，三个数字肯定不对。又由于前面两个数字比较小，就乘起来变成122。我盲猜这张图片是扁的（也就是x比y大），所以就这么安排了上方代码的x和y值。没想到一下子就猜对了。

运行就能直接得到图片了。
![Flag](https://github.com/C0nstellati0n/-CTF-/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/flag.png)