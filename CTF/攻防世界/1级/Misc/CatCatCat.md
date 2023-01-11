# CatCatCat

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e395fd1e-8d98-11ed-ab28-000c29bc20bf&task_category_id=1)

拿到一张图片和一个txt。发现txt里面以U2F开头，结合txt名称“我养了一只叫兔子的91岁的猫猫”，判断是rabbit加密。去[网站](https://www.woodmanzhang.com/webkit/rabbitencrypt/index.html)尝试无密码解密，没成功。看看图片，binwalk命令等无果，倒是strings发现了东西：

- strings èè.jpg | grep flag
> passwordis..catflag..]

有了密码再去解密，得到下面的内容（截取一小部分）：

```
]DW35W/HqUYt3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_ow"3P_o6cTf=[BBo!9/qB>ie50F%*6Y@Flxax*L.IzI9g1RLRX~PjWi8of+s)d[8y|u5.cL]DW35W/HqUYt3P_ow"3P_ow"3P_o6cTf=[BBo!9/DC>ie5HE%*6YPIlxaxeQ.IzI9g1RLRf%PjWi8of+s){{9y|u5.cL]D)=9W/Hr%Rt3P_ow"3P_o%"3P_o6cTf=
```

本人基础很拉胯，但是隐隐约约感觉末尾的等于号有点像base家族。结合txt文件名，好像有个base91？继续找个[网站](https://www.dcode.fr/base-91-encoding)解密,得到下面的内容：

```
cat. cat. cat. cat. cat. cat. cat. cat. cat. cat. cat. cat. cat. cat. cat.
cat. cat! cat? cat! cat! cat. cat? cat. cat. cat. cat. cat. cat. cat. cat.
cat. cat. cat. cat. cat. cat. cat. cat. cat? cat. cat? cat! cat. cat? cat.
cat. cat. cat. cat. cat. cat! cat. cat! cat! cat! cat! cat! cat. cat? cat.
```

txt名都告诉我们两个考点了，我就下意识以为有个cat密码之类的，结果搜了发现没有。倒是内容的格式很像Ook!语言。把全部cat替换为Ook，来[这里](https://www.dcode.fr/ook-language)解密，得到flag。注意flag的格式为CatCTF{}。

## Flag
> CatCTF{Th1s_V3ry_cute_catcat!!!}