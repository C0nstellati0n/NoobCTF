# Reverse-it

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=82fde4fc-9f83-4e60-b3b0-5a3c0e1ea546_2)

题目名称说Reverse，逆向？可这不是Misc题吗？算了直接开始吧。

附件没有后缀名，file命令只说这是个data，binwalk直接哑巴，什么都没找出来。16进制打开会发现里面乱七八糟，没有什么规律，也没有藏flag字样。那这还能咋样呢？

Misc的技巧之一是，遇到文件一般先看头和尾。既然现在头没有东西，那就看看尾。

![tail](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/tail.png)

这个尾巴好像也没啥……整个文件搜索字符串也没啥有用的东西。等一下这个尾巴好像有点怪怪的？如果你做多了Misc题，那么你应该可以和常见的文件头混个眼熟。8D FF不知道是啥，FF D8可是我们的老朋友，jpg图片文件头。

> #### 常见图像文件头
> - JPEG (jpg)：FFD8FF
> - PNG (png)：89504E47
> - GIF (gif)：47494638
> - Windows Bitmap (bmp)：424D

现在再回头看一眼题目，敢情是个文字游戏。Reverse是字面意义上的Reverse——把整个文件的数据倒过来。写个python脚本来实现。

```python
import binascii
with open("你的附件地址","rb") as f:
    s=binascii.b2a_hex(f.read())
    s=s[::-1]
with open("你要保存的图片地址",'wb') as f:
    f.write(binascii.a2b_hex(s))
```

上次介绍过wb了，那么rb大家应该也能猜到了：read bytes，以二进制形式读取文件流。binascii.b2a_hex()方法返回所读取二进制数据的十六进制表示形式。binascii.a2b_hex()就是反过来。那为啥不能直接读取二进制倒过来再直接写进去呢？这里我们可以做个实验。

```python
with open("你的附件地址","rb") as f:
    result=f.read()
    print(hex(result[-5]))
    print(hex(result[-1]))
```

根据上面的图，我们可以得知倒数第五位（也就是这里索引的-5）应该是0x00，而最后一位是0xff。直接读取后的result是以10进制存储的，那么转换回16进制后你会发现0x00变成0x0了。这可不行，我们必须保留两个0。用上面的方法就可以实现这一点。

接下来第二个知识点：[::-1]为啥能逆转整个文件？这里有一篇[文章](https://www.codingem.com/reverse-slicing-in-python/)讲得很清楚，不过是英文的，我就做个省流管家，简略介绍一下。

> #### python切片语法
> - 可切片元素[<起始>:<结束>:<步长>]

这里我们没有指定起始和结束，意味着切片整个元素。步长是-1，在python里-1索引代表最后一个，那么我们就会从后面往前开始切片，每次切一个。完成的结果就是把整个元素倒过来了。

运行代码我们就得到图片了。

![ctf](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/ctf.jpg)

但是被镜像了，这里使用photoshop或者找个镜子就能看出来了。

 > #### Flag
 > - SECCON{6in_tex7}