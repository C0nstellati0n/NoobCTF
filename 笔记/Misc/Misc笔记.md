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

也可以考虑下面这个脚本自动改宽高并生成文件(仅限png):

```python
#coding=utf-8
import zlib
import struct
#读文件
file = 'ctf.png'
fr = open(file,'rb').read()
data = bytearray(fr[12:29])
#crc32key = str(fr[29:33]).replace('\\x','').replace("b'",'0x').replace("'",'')
crc32key = 0x1670BAE6 #补上0x，copy hex value
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
如果zsteg输出类似这样的东西：

```
extradata:0         .. file: Zip archive data, at least v2.0 to extract, compression method=AES Encrypted
```

说明这里有文件可以提取。记住开始的字符串，使用以下命令提取：

- zsteg -E "extradata:0" ctf.png > res.zip

- binwalk
> binwalk xxx(支持任何类型，加上-e可以提取，不过有时候提取不出来，下方的foremost补充使用)
- foremost(有时候即使binwalk没有提示任何文件，foremost也能提取出东西。所以binwalk提示没有问题时，也不要忘记试foremost)
- outguess，例题：[Avatar](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/4%E7%BA%A7/Misc/Avatar.md)。注意有时候outguess会需要密码，密码可能藏在exif里。例题:[[ACTF新生赛2020]outguess](https://blog.csdn.net/mochu7777777/article/details/108936734)
- [F5隐写](https://github.com/matthewgao/F5-steganography)，例题：[刷新过的图片](https://blog.csdn.net/destiny1507/article/details/102079695)
- stegsolve
- NtfsStreamsEditor,用于处理NTFS流隐藏文件。例题：[[SWPU2019]我有一只马里奥](https://blog.csdn.net/mochu7777777/article/details/108934265)。当题目涉及到NTFS流时，题目文件都需要用Win RAR解压。
- SilentEye（音频隐写工具）
- steghide（多类型文件隐写工具）
- [Stegosaurus](https://github.com/AngelKitty/stegosaurus)(pyc文件隐写工具)
- [DeepSound](http://jpinsoft.net/deepsound/overview.aspx)（音频隐写工具）

1.   当遇见单独加密的压缩包时，首先确认是不是[伪加密](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/1%E7%BA%A7/Misc/fakezip.md)，如果不是，考虑到没有其它提示的因素，可以尝试直接ARCHPR爆破，常见的爆破掩码为4位数字。
2.   010Editor自带很多文件类型模板，把常用的例如png装上，鼠标悬浮在数据上就能得到那些数据代表的内容。修改单个字节可以鼠标选中要修改的字节，然后菜单栏->编辑->插入/覆盖->插入字节
3.   numpy.loadtxt读取坐标文件+基本matplotlib图像绘制。例题:[梅花香之苦寒来](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/BUUCTF/Misc/%E6%A2%85%E8%8A%B1%E9%A6%99%E4%B9%8B%E8%8B%A6%E5%AF%92%E6%9D%A5.md)
4.   audacity打开文件发现有两个声道且其中一个声道没用时，可以在最左侧调节左右声道的音量，然后菜单栏->文件->导出。
5.   morse2ascii工具可以解码音频摩斯电码。例题：[穿越时空的思念](https://www.cnblogs.com/tac2664/p/13861595.html)
6.   [盲文解密](https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=mangwen)，形如`⡇⡓⡄⡖⠂⠀⠂⠀⡋⡉⠔⠀⠔⡅⡯⡖⠔⠁⠔⡞⠔⡔⠔⡯⡽⠔⡕⠔⡕⠔⡕⠔⡕⠔⡕⡍=`。
7.   当题目文件出现大量无特征、无规律字符时，考虑是不是字频统计。例题:[[GXYCTF2019]gakki](https://buuoj.cn/challenges#[GXYCTF2019]gakki)
8.   010Editor可以更改阅读文本文件时的编码。菜单栏->视图->字符集。
9.   福尔摩斯跳舞的小人密码。例题:[[SWPU2019]伟大的侦探](https://blog.csdn.net/mochu7777777/article/details/109387134)
10.  音符密码，形如`♭♯♪‖¶♬♭♭♪♭‖‖♭♭♬‖♫♪‖♩♬‖♬♬♭♭♫‖♩♫‖♬♪♭♭♭‖¶∮‖‖‖‖♩♬‖♬♪‖♩♫♭♭♭♭♭§‖♩♩♭♭♫♭♭♭‖♬♭‖¶§♭♭♯‖♫∮‖♬¶‖¶∮‖♬♫‖♫♬‖♫♫§=`。可在[此处](https://www.qqxiuzi.cn/bianma/wenbenjiami.php?s=yinyue)直接解密。
11.  AAEncode，特征是颜文字，是将js代码转换为颜文字的编码。可用[网站](http://www.atoolbox.net/Tool.php?Id=703)在线解码。例题:[[SUCTF2018]single dog](https://blog.csdn.net/mochu7777777/article/details/109481013)。
12.  敲击码。类似棋盘密码，只不过与平时的棋盘排版不同，C和K在一个格，形如下方展示，/表示分割。

```
..... ../... ./... ./... ../
  5,2     3,1    3,1    3,2
```

例题:[[SWPU2019]你有没有好好看网课?](https://blog.csdn.net/mochu7777777/article/details/109449494)

22. 不要忘记查看压缩包注释。不装软件的情况下似乎看不到，可以安装Bandzip工具。
23. 遇见docx文件时，粗略看一遍看不出来线索就改后缀名为rar后解压查看里面是否有东西，或者直接binwalk -e提取内容。
24. [lsb隐写工具](https://github.com/livz/cloacked-pixel)（不是stegsolve可以提取的那种lsb隐写，可以加密码的另外一种）
25. 视频题粗略看一遍后最好放慢来看有没有漏掉的信息，可用[Kinovea](https://www.kinovea.org/)。例题:[[RoarCTF2019]黄金6年](https://blog.csdn.net/mochu7777777/article/details/109461931)
26. 磁盘、映像题，比如iso文件，打开后注意勾选上“隐藏的项目”，这种藏文件的方法不能漏掉了。
27. pdf文件可以用photoshop等软件打开，能找到里面隐藏的图片等内容。
28. crc值爆破恢复文件内容。zip加密的文件内容不应过小，因为此时攻击者可以通过爆破crc值的形式恢复文件内容。例题:[crc](https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/4%E7%BA%A7/Misc/crc.md)。下方脚本可以通过crc值破解多个zip，并将zip的内容写入一个文件中。

```python
import zipfile
import string
import binascii

def CrackCrc(crc):
	for i in dic:
		for j in dic:
			for k in dic:
				for h in dic:
					s = i + j + k + h
					if crc == (binascii.crc32(s.encode())):
						f.write(s)
						return

def CrackZip():
	for i in range(0,68):
		file = 'out'+str(i)+'.zip'
		crc = zipfile.ZipFile(file,'r').getinfo('data.txt').CRC
		CrackCrc(crc)
		print('\r'+"loading：{:%}".format(float((i+1)/68)),end='')

dic = string.ascii_letters + string.digits + '+/='
f = open('out.txt','w')
print("\nCRC32begin")
CrackZip()
print("\nCRC32finished")
f.close()
```

29. 中文电码+五笔编码。例题:[信息化时代的步伐](../../CTF/BUUCTF/Crypto/信息化时代的步伐.md)
30. DTMF拨号音识别+手机键盘密码。DTMF拨号音就像平时座机拨号的声音，手机键盘密码就是9键。例题:[[WUSTCTF2020]girlfriend](https://blog.csdn.net/mochu7777777/article/details/105412940)，使用工具[dtmf2num](http://hl.altervista.org/split.php?http://aluigi.altervista.org/mytoolz/dtmf2num.zip)
31. mimikatz可分析dmp后缀文件并获取密码。例题：[[安洵杯 2019]Attack](../../CTF/BUUCTF/Misc/[安洵杯%202019]Attack.md)
32. 当一串base64解码后是`Salted__`，可能的密文格式为AES，3DES或者Rabbit。
33. usb流量包数据提取。例题:[usb](../../CTF/moectf/Misc/usb.md)
34. rar文件可以通过更改文件结构隐藏文件，效果是让rar里有的文件解压不出来。用010 Editor打开rar文件，注意用文件名的区域开头是否是74（在[RAR文件结构](https://www.freebuf.com/column/199854.html)中，文件块的位置应该是74并不是7A，74让文件可以被解压出来，7A则不能），如果不是要改成74让文件被解压出来。例题:[USB](https://blog.csdn.net/mochu7777777/article/details/109632626)
35. python3 单字节16进制异或结果写入文件。今天遇到一道题，文本文件里的内容需要需要单字节与5异或后转为16进制写入文件。不知道为啥大佬们的脚本我用不了，可能是版本的问题，故自己写了一个python3的简陋玩意。题目:[[GUET-CTF2019]虚假的压缩包](https://blog.csdn.net/mochu7777777/article/details/105367979)

```python
from Crypto.Util.number import *
original = open("亦真亦假",'r').read()
flag = open("ctf",'wb')
res=''
for i in original:
	tmp = int(i,16)^5
	res+=hex(tmp)[2:]
flag.write(long_to_bytes(int(res,16)))
```

36. ttl隐写脚本。例题:[[SWPU2019]Network](https://blog.csdn.net/mochu7777777/article/details/109633675)

```python
import binascii
with open('attachment.txt','r') as fp:
    a=fp.readlines()
    p=[]
    for x in range(len(a)):
       p.append(int(a[x])) 
    s=''
    for i in p:
        if(i==63):
            b='00'
        elif(i==127):
            b='01'
        elif(i==191):
            b='10'
        else:
            b='11'
        s +=b
flag = ''
for i in range(0,len(s),8):
    flag += chr(int(s[i:i+8],2))
flag = binascii.unhexlify(flag)
wp = open('ans','wb')
wp.write(flag)
wp.close()
```

37. logo编程语言，可用于绘画，形如：

```
cs pu lt 90 fd 500 rt 90 pd fd 100 rt 90 repeat 18[fd 5 rt 10] lt 135 fd 50 lt 135 pu bk 100 pd setcolor pick [ red orange yellow green blue violet ] repeat 18[fd 5 rt 10] rt 90 fd 60 rt 90 bk 30 rt 90 fd 60 pu lt 90 fd 100 pd rt 90 fd 50 bk 50 setcolor pick [ red orange yellow green blue violet ] lt 90 fd 50 rt 90 fd 50 pu fd 50 pd fd 25 bk 50 fd 25 rt 90 fd 50 pu setcolor pick [ red orange yellow green blue violet ] fd 100 rt 90 fd 30 rt 45 pd fd 50 bk 50 rt 90 fd 50 bk 100 fd 50 rt 45 pu fd 50 lt 90 pd fd 50 bk 50 rt 90 setcolor pick [ red orange yellow green blue violet ] fd 50 pu lt 90 fd 100 pd fd 50 rt 90 fd 25 bk 25 lt 90 bk 25 rt 90 fd 25 setcolor pick [ red orange yellow green blue violet ] pu fd 25 lt 90 bk 30 pd rt 90 fd 25 pu fd 25 lt 90 pd fd 50 bk 25 rt 90 fd 25 lt 90 fd 25 bk 50 pu bk 100 lt 90 setcolor pick [ red orange yellow green blue violet ] fd 100 pd rt 90 arc 360 20 pu rt 90 fd 50 pd arc 360 15 pu fd 15 setcolor pick [ red orange yellow green blue violet ] lt 90 pd bk 50 lt 90 fd 25 pu home bk 100 lt 90 fd 100 pd arc 360 20 pu home
```

[在线解释器](https://www.calormen.com/jslogo/)

38. [zip明文攻击](https://www.cnblogs.com/LEOGG321/p/14493327.html)，[原理](https://www.aloxaf.com/2019/04/zip_plaintext_attack/)。明文攻击可以用[archpr](https://blog.csdn.net/weixin_43778378/article/details/106077774)跑。archpr里面选好加密的zip文件后攻击类型选明文，然后点到明文，明文文件路径选择包含明文内容的zip（没错是zip，不是写有明文的txt，是装有明文的txt的zip）。例题:[[ACTF新生赛2020]明文攻击](https://blog.csdn.net/qq_46230755/article/details/112108707)
39. [零宽字符隐写](https://zhuanlan.zhihu.com/p/87919817)。[解密网站](http://330k.github.io/misc_tools/unicode_steganography.html)
40. 010Editor找到工具->十六进制运算->二进制异或，可以直接对整个文件异或。
41. gaps+montage工具自动拼图。例题:[[MRCTF2020]不眠之夜](https://blog.csdn.net/mochu7777777/article/details/109649446)
42. 汉信码，形如：

![hanxin_code](../images/hanxin_code.png)

可用[网站](https://tuzim.net/hxdecode/)解码。

43. [snow隐写](https://lazzzaro.github.io/2020/06/20/misc-%E6%96%87%E4%BB%B6%E9%9A%90%E5%86%99/)，有[网页版](http://fog.misty.com/perry/ccs/snow/snow/snow.html)和[exe版](https://darkside.com.au/snow/)。例题:[看雪看雪看雪](https://blog.csdn.net/qq_53105813/article/details/127896201)
44. 图片隐写工具[stegpy](https://github.com/dhsdshdhk/stegpy)。
45. ppt文档密码爆破工具。可用[Accent OFFICE Password Recovery](https://www.52pojie.cn/thread-82569-1-1.html)工具，也能用[ffice2john.py](https://fossies.org/linux/john/run/office2john.py)或者john。
46. 电动车钥匙信号PT224X解码。例题:[打开电动车](../../CTF/攻防世界/3级/Misc/打开电动车.md)。类似的还有PT226x。例题:[[HDCTF2019]信号分析](https://www.onctf.com/posts/d228f8e5.html#%E4%B8%80%E7%99%BE%E5%9B%9B%E5%8D%81%E5%85%AD%E3%80%81-HDCTF2019-%E4%BF%A1%E5%8F%B7%E5%88%86%E6%9E%90)
47. TSL协议需要私钥（RSA）解密才能追踪。例题:[[DDCTF2018]流量分析](https://blog.csdn.net/qq_45699846/article/details/123529342)
48. VoIP——基于IP的语音传输（英语：Voice over Internet Protocol，缩写为VoIP）是一种语音通话技术，经由网际协议（IP）来达成语音通话与多媒体会议，也就是经由互联网来进行通信。其他非正式的名称有IP电话（IP telephony）、互联网电话（Internet telephony）、宽带电话（broadband telephony）以及宽带电话服务（broadband phone service）。在wireshark中可以根据数据包还原语音。菜单栏->Telephony->VoIP Calls。
49. SSTV音频解码。例题:[[UTCTF2020]sstv](https://blog.csdn.net/mochu7777777/article/details/109882441)
50. 图片缺少IDAT标识时,在010 Editor中将缺少标识的chunk的union CTYPE type的位置补上IDAT十六进制标识49 44 41 54即可。例题:[[湖南省赛2019]Findme](https://blog.csdn.net/mochu7777777/article/details/107737687)
51. BPG图片可用[honeyview](https://en.bandisoft.com/honeyview/)打开。
52. 内存取证工具[Volatility](https://github.com/volatilityfoundation/volatility)。例题:[[HDCTF2019]你能发现什么蛛丝马迹吗](https://blog.csdn.net/mochu7777777/article/details/109853022)
53. 某些思路邪门的题里，图片的颜色十六进制号可能是flag的十六进制编码。
54. [GCode](https://baike.baidu.com/item/G%E4%BB%A3%E7%A0%81/2892251),形如：

```
M73 P0 R2
M201 X9000 Y9000 Z500 E10000
M203 X500 Y500 Z12 E120
M204 P2000 R1500 T2000
M205 X10.00 Y10.00 Z0.20 E2.50
M205 S0 T0
M107
M115 U3.1.0
M83
M204 S2000 T1500
M104 S215
M140 S60
M190 S60
M109 S215
G28 W
G80
G1 Y-3.0 F1000.0
G92 E0.0
G1 X60.0 E9.0  F1000.0
M73 P4 R1
G1 X100.0 E12.5  F1000.0
G92 E0.0
M900 K30
G21
G90
M83
G92 E0.0
G1 E-0.80000 F2100.00000
G1 Z0.600 F10800.000
G1 X89.987 Y95.416
G1 Z0.200
G1 E0.80000 F2100.00000
```

55. FAT文件可以使用[VeraCrypt](https://sourceforge.net/projects/veracrypt/)进行挂载
56. FAT文件在挂载输入密码的时候，不同的密码可以进入不同的文件系统
57. 遇见vmdk文件，可以试试使用7z这个压缩软件打开，里面可能藏着其他文件。
58. 邮件协议：POP、SMTP、IMAP
59. 火狐浏览器的登陆凭证文件可用[Firepwd](https://github.com/lclevy/firepwd)破解。
60. ext4文件系统可用[extundelete](https://extundelete.sourceforge.net/)恢复被删除的目录或文件。例题:[[XMAN2018排位赛]file](https://blog.csdn.net/mochu7777777/article/details/110004817)
61. 文件类型识别工具TrID（可识别Python Pickle序列号数据）。例题:[我爱Linux](https://blog.csdn.net/wangjin7356/article/details/122471475)
62. [TestDisk](https://www.cgsecurity.org/wiki/TestDisk_CN)磁盘恢复工具。例题:[[BSidesSF2019]diskimage](https://blog.csdn.net/mochu7777777/article/details/110079540)
63. usb数据提取+autokey爆破。例题:[[XMAN2018排位赛]AutoKey](https://ctf-wiki.org/en/misc/traffic/protocols/usb/#_2)
64. [toy加密](https://eprint.iacr.org/2020/301.pdf)。例题:[[羊城杯 2020]signin](https://www.cnblogs.com/vuclw/p/16424799.html)
65. ALPHUCK一种 Programming Language ,只由 a,c,e,i,j,o,p,s 这 8 个小写字母组成。
66. [三分密码](https://baike.baidu.com/item/%E4%B8%89%E5%88%86%E5%AF%86%E7%A0%81/2250183)+veracrypt挂载被加密磁盘。例题:[[GKCTF 2021]0.03](https://www.cnblogs.com/vuclw/p/16428558.html)
67. 条形码修复。例题:[[BSidesSF2020]barcoder](https://blog.csdn.net/zippo1234/article/details/109249593)
68. TLS协议需要解密才能追踪。菜单栏->Wireshark->Preferences->Protocols->TLS。有RSA私钥选RSA key list，有sslkey的log文件在下方log filename选择log文件。
69. TCP-IP数据报的Identification字段隐写。例题:[[羊城杯 2020]TCP_IP](https://blog.csdn.net/qq_45699846/article/details/123833160)
70. 小米手机的备份文件实际也是ANDROID BACKUP文件，去掉小米的header后即可使用[脚本](https://github.com/nelenkov/android-backup-extractor)解压。
71. rpg maker修改游戏。例题:[[*CTF2019]She](https://blog.csdn.net/qq_49354488/article/details/115655115)
72. ARCHPR无法爆破RAR5，可以用rar2john提取hash后利用hashcat爆破密码。例题:[[羊城杯 2020]image_rar](https://blog.csdn.net/mochu7777777/article/details/118422921)
73. 字符串经过brainfuck加密后应该是++++++++[开头的，所以遇见解出来是乱码的brainfuck可以看看开头是否正确。
74. 空格+tab隐写过滤脚本

[例题及来源](https://www.bilibili.com/read/cv14000314)

```python
import os
def get_file_list(dir_path):
    _file_list = os.listdir(dir_path)
    file_list = []
    for file_str in _file_list:
        new_dir_path = dir_path+'/'+file_str
        if os.path.isdir(new_dir_path):
            file_list.extend(get_file_list(new_dir_path))
        else:
            file_list.append(new_dir_path)
    return file_list
file_list = get_file_list(r'/Users/constellation/Desktop/source_code')
for file_str in file_list:
    f = open(file_str, 'r', encoding='utf-8')
    try:
        data = f.read()
        if ' \t \t' in data:
            print(file_str)
    except:
        pass
```

75. swf文件是flash文件，可用[JPEXS Free Flash Decompiler](https://github.com/jindrapetrik/jpexs-decompiler)反编译。例题:[[*CTF2019]babyflash](https://blog.csdn.net/mochu7777777/article/details/115833842)
76. 音频lsb提取。例题将一张bmp图片通过lsb的形式写入音频，需要知道正确的宽高才能恢复原来的图片。例题:[静静听这么好听的歌](https://blog.csdn.net/qq_45699846/article/details/123847848)
77. [TSPL/TSPL2 Programming Language](https://www.pos-shop.ru/upload/iblock/ebd/ebd9bed075d1b925be892b297590fc18.pdf)，用于打印机。例题:[[RCTF2019]printer](https://tobatu.gitee.io/blog/2020/10/06/BUUCTF-%E5%88%B7%E9%A2%98%E8%AE%B0%E5%BD%95-9/#RCTF2019-printer)
78. [北约音标字母](https://zh.wikipedia.org/wiki/%E5%8C%97%E7%BA%A6%E9%9F%B3%E6%A0%87%E5%AD%97%E6%AF%8D)，Alfa，Bravo之类的，其实就是每个单词的首字母。
79. pgp加密，使用[PGPTool](https://pgptool.github.io/)解密。例题:[[BSidesSF2019]bWF0cnlvc2hrYQ](https://blog.csdn.net/mochu7777777/article/details/115856882)
80. 镜像FTK挂载仿真，使用[AccessData FTK Imager](https://accessdata-ftk-imager.software.informer.com/3.1/)。例题:[[NPUCTF2020]回收站](https://shimo.im/docs/6hyIjGkLoRc43JRs)
81. 利用[dig](https://developer.aliyun.com/article/418787)命令分析dns shell。例题:[[UTCTF2020]dns-shell](https://meowmeowxw.gitlab.io/ctf/utctf-2020-do-not-stop/)
82. 乐高ev3机器人分析（蓝牙协议）。基本的4个协议为HCI、L2CAP、SDP、RFCOMM。对比于英特网五层结构来说：HCI相当于与物理层打交道的协议，L2CAP协议则是链路层相关协议，SDP和RFCOMM则是运输层相关协议，当然其上也有对应的应用层相关的一些协议。SDP用来发现周围蓝牙服务，然后由L2CAP来建立信道链接，然后传输由上层RFCOMM给予的数据分组。如果只是提取数据的话，只需要关心：RFCOMM协议。例题:[[HITCON2018]ev3basic](https://www.youncyb.cn/?p=493)
83. 使用[e2fsck](https://www.runoob.com/linux/linux-comm-e2fsck.html)命令修复超级块损坏的ext2文件。例题:[[BSidesSF2020]mpfrag](http://www.ga1axy.top/index.php/archives/17/)
84. 压感数位板usb协议分析+emoji aes密码。例题:[[RoarCTF2019]davinci_cipher](http://www.ga1axy.top/index.php/archives/43/)
85. [exiftool](https://www.rmnof.com/article/exiftool-introduction/)使用。当用exiftool发现有`ThumbnailImage	(Binary data 215571 bytes, use -b option to extract)`一项时，可以用`exiftool -b -ThumbnailImage attachment.jpg > flag.jpg`提取出缩略图。例题:[[BSidesSF2019]delta](https://www.shawroot.cc/142.html)，这题还有条形码分析。
86. Discord服务器link泄露。可用下方的代码插入一个iframe，强制加入服务器。

例题及来源:[discord l34k](https://github.com/uclaacm/lactf-archive/tree/main/2023/misc/discord-leak)

```html
<!DOCTYPE html>
<html>
    <body>
        <!-- 1. Copy Discord embed iframe template (visit any server Server Settings -> Widget -> Premade Widget). -->
        <!-- 2. Replace id with id from prompt. -->
        <!-- 3. Open this file up in a browser. -->
        <!-- 4. Click "Join Discord" to access the server. -->
        <iframe src="https://discord.com/widget?id=1060030874722259057&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
    </body>
</html>
```

87. 利用Google Sheets API获取被保护、隐藏的sheet内容。需要在[这里](https://www.google.com/script/start/)运行。

例题及来源:[hidden in plain sheets](https://github.com/uclaacm/lactf-archive/tree/main/2023/misc/hidden-in-plain-sheets)

```js
function myFunction() {
  const sheet = SpreadsheetApp.openById("1ULdm_KCOYCWuf6gqpg6tm0t-wnWySX_Bf3yUYOfZ2tw");
  const sheets = sheet.getSheets();
  const secret = sheets.find(x => x.getName() == "flag");
  console.log(secret.getDataRange().getValues().map(l => l.join("")).join("\n"));
}
```

88. 智能汽车协议分析+arm可执行文件逆向。例题:[[网鼎杯 2020 青龙组]Teslaaaaa](https://blog.csdn.net/Breeze_CAT/article/details/106156567)
89. 利用相位抵消分离特殊信号。例题:[[QCTF2018]Noise](https://blog.csdn.net/u011297466/article/details/81059248)
90. Wireshark菜单栏->Statistics->Conversations可以看到抓到的包的所有通信的ip和端口号，有时候是流量题找ip的捷径。