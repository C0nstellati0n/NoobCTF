# Misc笔记

1. 将tcp流解码为tpkt+openssl检查ASN.1。例题：[arrdeepee](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/6%E7%BA%A7/Misc/arrdeepee.md)
2. mca后缀名文件为游戏Minecraft使用的世界格式。例题:[Russian-zips](https://blog.csdn.net/weixin_44604541/article/details/113741829)
3. 传感器相关知识点（差分曼彻斯特、曼彻斯特编码，crc校验）。[传感器1](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/3%E7%BA%A7/Misc/%E4%BC%A0%E6%84%9F%E5%99%A81.md)
4. 有时候会遇见需要改宽高的情况，一般会根据图片的crc值爆破出正确的宽高。

```python
import binascii
import struct
CRC=0x6D7C7135
with open("dabai.png", "rb") as f:
    crcbp=f.read()
for i in range(2000):
    for j in range(2000):
        data = crcbp[12:16] + \
            struct.pack('>i', i)+struct.pack('>i', j)+crcbp[24:29]
        crc32 = binascii.crc32(data) & 0xffffffff
        if(crc32 == CRC):
            print(i, j)
            print('hex:', hex(i), hex(j))
            break
```

也可以考虑下面这个脚本自动改宽高并生成文件:

```python
#coding=utf-8
import zlib
import struct
#读文件
file = '1.png'
fr = open(file,'rb').read()
data = bytearray(fr[12:29])
crc32key = eval(str(fr[29:33]).replace('\\x','').replace("b'",'0x').replace("'",''))
#crc32key = 0xCBD6DF8A #补上0x，copy hex value
#data = bytearray(b'\x49\x48\x44\x52\x00\x00\x01\xF4\x00\x00\x01\xF1\x08\x06\x00\x00\x00')  #hex下copy grep hex
n = 4095 #理论上0xffffffff,但考虑到屏幕实际，0x0fff就差不多了
for w in range(n):#高和宽一起爆破
    width = bytearray(struct.pack('>i', w))#q为8字节，i为4字节，h为2字节
    for h in range(n):
        height = bytearray(struct.pack('>i', h))
        for x in range(4):
            data[x+4] = width[x]
            data[x+8] = height[x]
            #print(data)
        crc32result = zlib.crc32(data)
        if crc32result == crc32key:
            print(width,height)
            #写文件
            newpic = bytearray(fr)
            for x in range(4):
                newpic[x+16] = width[x]
                newpic[x+20] = height[x]
            fw = open(f"{file}.png",'wb')#保存副本
            fw.write(newpic)
            fw.close
```

5. 遇见webshell查杀题直接用D盾扫。例题:[webshell后门](https://buuoj.cn/challenges#webshell%E5%90%8E%E9%97%A8)
6. 音频隐写题首先考虑audacity打开看波形图和频谱图。发现可疑的线索时多缩放。今天就看见了一道藏摩斯电码然而默认缩放比例下无法展示完全的题：[来首歌吧](https://buuoj.cn/challenges#%E6%9D%A5%E9%A6%96%E6%AD%8C%E5%90%A7)
7. 从宽带备份文件出恢复账户名密码名等信息：使用工具[RouterPassView](https://www.nirsoft.net/utils/router_password_recovery.html)。
8. vmdk后缀文件可以在linux下直接用7z解压。例题：[面具下的flag](https://blog.csdn.net/weixin_45485719/article/details/107417878)
9. 隐写工具：

- zsteg
> zsteg xxx.png(仅图片)
- binwalk
> binwalk xxx(支持任何类型，加上-e可以提取，不过有时候提取不出来，下方的foremost补充使用)
- foremost
- outguess，例题：[Avatar](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/4%E7%BA%A7/Misc/Avatar.md)。注意有时候outguess会需要密码，密码可能藏在exif里。例题:[[ACTF新生赛2020]outguess](https://blog.csdn.net/mochu7777777/article/details/108936734)
- [F5隐写](https://github.com/matthewgao/F5-steganography)，例题：[刷新过的图片](https://blog.csdn.net/destiny1507/article/details/102079695)
- stegsolve
- NtfsStreamsEditor,用于处理NTFS流隐藏文件。例题：[[SWPU2019]我有一只马里奥](https://blog.csdn.net/mochu7777777/article/details/108934265)。当题目涉及到NTFS流时，题目文件都需要用Win RAR解压。

10.  当遇见单独加密的压缩包时，首先确认是不是[伪加密](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/1%E7%BA%A7/Misc/fakezip.md)，如果不是，考虑到没有其它提示的因素，可以尝试直接ARCHPR爆破，常见的爆破掩码为4位数字。
11.  010Editor自带很多文件类型模板，把常用的例如png装上，鼠标悬浮在数据上就能得到那些数据代表的内容。修改单个字节可以鼠标选中要修改的字节，然后菜单栏->编辑->插入/覆盖->插入字节
12.  numpy.loadtxt读取坐标文件+基本matplotlib图像绘制。例题:[梅花香之苦寒来](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Misc/%E6%A2%85%E8%8A%B1%E9%A6%99%E4%B9%8B%E8%8B%A6%E5%AF%92%E6%9D%A5.md)
13.  audacity打开文件发现有两个声道且其中一个声道没用时，可以在最左侧调节左右声道的音量，然后菜单栏->文件->导出。
14.  morse2ascii工具可以解码音频摩斯电码。例题：[穿越时空的思念](https://www.cnblogs.com/tac2664/p/13861595.html)
15.  [盲文解密](https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=mangwen)，形如`⡇⡓⡄⡖⠂⠀⠂⠀⡋⡉⠔⠀⠔⡅⡯⡖⠔⠁⠔⡞⠔⡔⠔⡯⡽⠔⡕⠔⡕⠔⡕⠔⡕⠔⡕⡍=`。
16.  当题目文件出现大量无特征、无规律字符时，考虑是不是字频统计。例题:[[GXYCTF2019]gakki](https://buuoj.cn/challenges#[GXYCTF2019]gakki)
17.  010Editor可以更改阅读文本文件时的编码。菜单栏->视图->字符集。
18.  福尔摩斯跳舞的小人密码。例题:[[SWPU2019]伟大的侦探](https://blog.csdn.net/mochu7777777/article/details/109387134)
19.  音符密码，形如`♭♯♪‖¶♬♭♭♪♭‖‖♭♭♬‖♫♪‖♩♬‖♬♬♭♭♫‖♩♫‖♬♪♭♭♭‖¶∮‖‖‖‖♩♬‖♬♪‖♩♫♭♭♭♭♭§‖♩♩♭♭♫♭♭♭‖♬♭‖¶§♭♭♯‖♫∮‖♬¶‖¶∮‖♬♫‖♫♬‖♫♫§=`。可在[此处](https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=yinyue)直接解密。
20.  AAEncode，特征是颜文字，是将js代码转换位颜文字的编码。可用[网站](http://www.atoolbox.net/Tool.php?Id=703)在线解码。例题:[[SUCTF2018]single dog](https://blog.csdn.net/mochu7777777/article/details/109481013)。
21.  敲击码。类似棋盘密码，只不过与平时的棋盘排版不同，C和K在一个格，形如下方展示，/表示分割。

```
..... ../... ./... ./... ../
  5,2     3,1    3,1    3,2
```

例题:[[SWPU2019]你有没有好好看网课?](https://blog.csdn.net/mochu7777777/article/details/109449494)

22. 不要忘记查看压缩包注释。不装软件的情况下似乎看不到，可以安装Bandzip工具。