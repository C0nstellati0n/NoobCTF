# arrdeepee

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e34d7c55-7e58-4436-8d34-05ad78361240_2&task_category_id=1)

流量分析一生之敌。

拿到pcap，一堆tcp，追踪起来只有1个流，搜flag关键字自然也搜不到东西。看下协议分级，原来还有udp，然而同样只有一个流，找不到什么有用的东西。不懂了，这就是我的全部水平，看[wp](https://blog.csdn.net/weixin_39934520/article/details/122014291)。

这些tcp大有玄机，右键点击一条tcp流，选择Decode As会弹出一个窗口，点击Curren下的none会弹出一个选择框，一直往下划找到TPKT，选择后点击ok，就能看见tpkt流了。此时再看协议分级，会发现有2个rdp包。它们在这里绝不是偶然，考虑到rdp是远程桌面，怀疑可能和flag密切相关。

再仔细看看跟踪的udp流，会发现一段可疑的地方（我真的菜，眼睛还不好）：

```
T.S.S.e.c.K.e.y.S.e.t.10].	+.....7..1P.N.M.i.c.r.o.s.o.f.t. .S.t.r.o.n.g. .C.r.y.p.t.o.g.r.a.p.h.i.c. .P.r.o.v.i.d.e.r
```

udp只有这一个流，保存下来，binwalk会发现里面藏着证书和私钥，那就提取出来。

```
$ binwalk -e extracted_data.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
30            0x1E            Certificate in DER format (x509 v3), header length: 4, sequence length: 2376
57            0x39            Certificate in DER format (x509 v3), header length: 4, sequence length: 1466
1546          0x60A           Private key in DER format (PKCS header length: 4, sequence length: 860
```

但是这证书有点问题，直接用openssl读不出来是什么东西。那就用openssl读取其ASN.1来看看到底藏着什么。

```
$ openssl asn1parse -inform DER -in extracted_data.bin
    0:d=0  hl=4 l=2467 cons: SEQUENCE
    4:d=1  hl=2 l=   1 prim: INTEGER           :03
    7:d=1  hl=4 l=2399 cons: SEQUENCE
   11:d=2  hl=2 l=   9 prim: OBJECT            :pkcs7-data
   22:d=2  hl=4 l=2384 cons: cont [ 0 ]
   26:d=3  hl=4 l=2380 prim: OCTET STRING      [HEX DUMP]:省略
 2410:d=1  hl=2 l=  59 cons: SEQUENCE
 2412:d=2  hl=2 l=  31 cons: SEQUENCE
 2414:d=3  hl=2 l=   7 cons: SEQUENCE
 2416:d=4  hl=2 l=   5 prim: OBJECT            :sha1
 2423:d=3  hl=2 l=  20 prim: OCTET STRING      [HEX DUMP]:C6636BA1DC7A4063D2AD49F7DBB800AD92260253
 2445:d=2  hl=2 l=  20 prim: OCTET STRING      [HEX DUMP]:9BADF56CE6069E1EB9339E0E9FCD096ACD0DBC5B
 2467:d=2  hl=2 l=   2 prim: INTEGER           :07D0
```

省略掉一部分内容是有原因的，因为实在太长了，说明里面有东西。openssl刚好可以读取嵌套类型。

```
$ openssl asn1parse -inform DER -in extracted_data.bin -strparse 26
    0:d=0  hl=4 l=2376 cons: SEQUENCE
    4:d=1  hl=4 l=1489 cons: SEQUENCE
    8:d=2  hl=2 l=   9 prim: OBJECT            :pkcs7-data
   19:d=2  hl=4 l=1474 cons: cont [ 0 ]
   23:d=3  hl=4 l=1470 prim: OCTET STRING      [HEX DUMP]:省略
 1497:d=1  hl=4 l= 879 cons: SEQUENCE
 1501:d=2  hl=2 l=   9 prim: OBJECT            :pkcs7-encryptedData
 1512:d=2  hl=4 l= 864 cons: cont [ 0 ]
 1516:d=3  hl=4 l= 860 cons: SEQUENCE
 1520:d=4  hl=2 l=   1 prim: INTEGER           :00
 1523:d=4  hl=4 l= 853 cons: SEQUENCE
 1527:d=5  hl=2 l=   9 prim: OBJECT            :pkcs7-data
 1538:d=5  hl=2 l=  28 cons: SEQUENCE
 1540:d=6  hl=2 l=  10 prim: OBJECT            :pbeWithSHA1And40BitRC2-CBC
 1552:d=6  hl=2 l=  14 cons: SEQUENCE
 1554:d=7  hl=2 l=   8 prim: OCTET STRING      [HEX DUMP]:135DB999CA2CD6B1
 1564:d=7  hl=2 l=   2 prim: INTEGER           :07D0
 1568:d=5  hl=4 l= 808 prim: cont [ 0 ]
```

继续套娃，再来。

```
$ openssl asn1parse -inform DER -in extracted_data.bin -strparse 26 -strparse 23
    0:d=0  hl=4 l=1466 cons: SEQUENCE
    4:d=1  hl=4 l=1462 cons: SEQUENCE
    8:d=2  hl=2 l=  11 prim: OBJECT            :pkcs8ShroudedKeyBag
   21:d=2  hl=4 l=1270 cons: cont [ 0 ]
   25:d=3  hl=4 l=1266 cons: SEQUENCE
   29:d=4  hl=2 l=  28 cons: SEQUENCE
   31:d=5  hl=2 l=  10 prim: OBJECT            :pbeWithSHA1And3-KeyTripleDES-CBC
   43:d=5  hl=2 l=  14 cons: SEQUENCE
   45:d=6  hl=2 l=   8 prim: OCTET STRING      [HEX DUMP]:66AFD4385D4302C4
   55:d=6  hl=2 l=   2 prim: INTEGER           :07D0
   59:d=4  hl=4 l=1232 prim: OCTET STRING      [HEX DUMP]:省略
 1295:d=2  hl=3 l= 172 cons: SET
 1298:d=3  hl=2 l=  13 cons: SEQUENCE
 1300:d=4  hl=2 l=   9 prim: OBJECT            :Microsoft Local Key set
 1311:d=4  hl=2 l=   0 cons: SET
 1313:d=3  hl=2 l=  19 cons: SEQUENCE
 1315:d=4  hl=2 l=   9 prim: OBJECT            :localKeyID
 1326:d=4  hl=2 l=   6 cons: SET
 1328:d=5  hl=2 l=   4 prim: OCTET STRING      [HEX DUMP]:01000000
 1334:d=3  hl=2 l=  39 cons: SEQUENCE
 1336:d=4  hl=2 l=   9 prim: OBJECT            :friendlyName
 1347:d=4  hl=2 l=  26 cons: SET
 1349:d=5  hl=2 l=  24 prim: BMPSTRING
 1375:d=3  hl=2 l=  93 cons: SEQUENCE
 1377:d=4  hl=2 l=   9 prim: OBJECT            :Microsoft CSP Name
 1388:d=4  hl=2 l=  80 cons: SET
 1390:d=5  hl=2 l=  78 prim: BMPSTRING
```

这次省略的内容像一个PKCS12文件（我不知道怎么看出来的），一个带有证书和私钥的文件。还是openssl提取出来。

```
$ openssl pkcs12 -in extracted_data.bin -nocerts -nodes -out private.key
Enter Import Password: mimikatz
MAC verified OK
```

密码猜的，不过题目描述也给了。拿到私钥后就能用[RDP-Replay](https://github.com/ctxis/RDP-Replay)来重放rdp了。

- rdp_replay -r ../e8e2ceb9-b77f-4b26-b09a-fcec86e27497.pcap  -o recording.avi -p ./private.key --save_clipboard --show_keys > output

根据得到的视频，出题人把flag压缩后再输入一串密码加密，把压缩包进行了base64编码再拷贝到剪切板。`rdp_replay`可以保留剪切板以及键盘输入，上面的命令已经指定参数了。查看键盘输入的记录结果：

```
RDP SSL MODE Requested by server!!
SSL private key found.
1024x756x8
REALLY DELICIOUS PANCAKES<Tab>REALLY DELICIOUS PANCAKES
```

查看剪切板：

```
N3q8ryccAATjAlOVMAAAAAAAAABqAAAAAAAAACmoQ4fA1DQXZvCzJGIg/8cxnh8QXnWoDkwNxjGL
37P7rvVC2SMn8+wquEv/A5HBL9djQewBBAYAAQkwAAcLAQACJAbxBwEKUweBdxD1DDirkCEhAQAB
AAwrJwAICgGwcALcAAAFARkJAAAAAAAAAAAAERMAZgBsAGEAZwAuAHQAeAB0AAAAGQAUCgEAAFNu
lssb0wEVBgEAIAAAAAAA
```

最后就是flag时间了！把base64解密后得到的压缩包用密码解压。

```
$ cat ../clip-00000000-down | base64 -d -i > flag.7z
$ 7z x flag.7z

7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
p7zip Version 9.20 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,2 CPUs)

Processing archive: flag.7z


Enter password (will not be echoed) :
Extracting  flag.txt

Everything is Ok

Size:       39
Compressed: 186
$ cat flag.txt
HITB{44519a67ffc654e40febc09e20e8e745}
```

## Flag
> HITB{44519a67ffc654e40febc09e20e8e745}