# Keyword

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=32e0237d-b7fa-4910-ad6b-6774c94e4bbc_2)

python2似乎不应该被淘汰。

附件是张png，写着"keyword:lovekfc"。目前还不知道这个keyword在哪里用，zsteg看看。

- b1,rgb,msb,xy       .. text: "$~7MO8)|"
<br>b1,bgr,lsb,xy       .. <wbStego size=68, ext="\x00J\x84", data="\aO;\x12\xB6[\x18\x85l\xC0"..., even=false>
<br>b1,rgba,msb,xy      .. file: OpenPGP Public Key
<br>b1,abgr,msb,xy      .. file: OpenPGP Secret Key
<br>b2,b,lsb,xy         .. file: SoftQuad DESC or font file binary
<br>b2,b,msb,xy         .. file: VISX image file
<br>b2,bgr,msb,xy       .. text: "]]UUUUUU]wW]U"
<br>b2,abgr,msb,xy      .. text: "WWWWWWWWW_"
<br>b4,rgb,msb,xy       .. text: ["w" repeated 15 times]
<br>b4,bgr,msb,xy       .. text: ["w" repeated 13 times]
<br>b4,abgr,msb,xy      .. file: RDI Acoustic Doppler Current Profiler (ADCP)

我去我今天第一次知道zsteg前面还有这些东西。终端上看不到因为背景是黑色的，字体也是黑色的。lsb模式下有发现个不知道是什么的东西的file，stegsolve提取看看。

- 500000001a81119e7e06ed360e05696248454987c915ac1699c0c30d0633af9d9ff9c2c00d89040227708e5464c9b7e134d0be5e36c50d5fe127b7245abd247eecb2f21c943eb893d4f1e57d89ea5653e929bd81

有效的内容就这么多，剩下的全是f。这是什么？试了常见项都不是。没思路了。

看了wp又发现了个[新工具](https://github.com/livz/cloacked-pixel)。脚本小子之路越走越远。然后又是python2。虽然我有python2，但是里面的库在ython3才有。唉我也懒得把库迁移过去了，毕竟这种工具的使用很少见。如果运行了结果如下：

- PVSF{vVckHejqBOVX9C1c13GFfkHJrjIQeMwf}

有些wp说这是Nihilist密码。查了一下好像就是关键字密码，也有说是虚无主义密码的，似乎是一种东西。找个普通的关键字密码破解网站就行了。

- ### Flag
  > QCTF{cCgeLdnrIBCX9G1g13KFfeLNsnMRdOwf}