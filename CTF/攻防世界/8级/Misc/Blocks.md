# Blocks

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f54cdbd5-2a8f-4d29-afba-b6f27c9302f3_2&task_category_id=1)

什么都能掰到异或去。

解压出来一张无后缀的图片。不怕，直接file命令，得到为png文件。改后缀后打开图片寻思着像二维码但是又跟真正的二维码差远了。扔到stegsolve里看看，在Alpha plane 0发现了一个很小的东西，我还没法放大看。半路卡住了，看[wp](https://blog.wujiaxing.cn/2019/09/25/e4a0a49e/)。

那个很小的玩意和大图片其实是一个分辨率的，都是19*19。两个图片的题容易想到盲水印，但这回两张图片长的不一样，不太可能。于是想到异或，“同样大小”是异或的关键线索。

```python
from PIL import Image

img = Image.open('stego_100_f78a3acde659adf7ceef546380e49e5f.png')
m1 = m2 = ''
# 取大图二进制
for y in range(0, img.size[0], 19):
    for x in range(0, img.size[1], 19):
        r,g,b,a = img.getpixel((x,y))
        m1 += str(r & 1)
# 取中间隐写图二进制
for y in range(171, 171 + 19):
    for x in range(171, 171 + 19):
        r,g,b,a = img.getpixel((x,y))
        m2 += str(a & 1)
# 二进制串取异或
xor = ''.join(str(int(A)^int(B)) for A,B in zip(m1,m2))
# 二进制转字符串并输出
print(''.join(chr(int(xor[i:i+8], 2)) for i in range(0, len(xor), 8)))
```

## Flag
> ASIS_08213db585ffe1c93c8f04622c319594