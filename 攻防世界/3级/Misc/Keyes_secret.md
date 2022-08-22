# Keyes_secret

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=417d0728-13d9-42e6-a4f3-a0a7b2123b7b_2)

这题思路跟上了，脑洞没有。

附件txt，啥也不是，字频，凯撒，栅栏等都试过了，全部错。直到我仔细看里面的内容发现了QWERTY这个组合。我可太熟了，这不经典弱密码吗？立刻把注意力放到键盘上，此时感觉像是个键盘密码。

我之前做过一道键盘密码，是四个四个分开的，好圈出明文。但是这里根本没分割，一个一个跟着键走也不知道在干啥，有时候连在一起有时候又跳来跳去的。

看了wp才发现此键盘密码非彼键盘密码，是在键盘上画画……要自己感受在哪里分割和画的是什么字母。在密文里可以搜索到大括号，括号前面一部分的内容和包着的内容如下。

- TRFVG F
<br>WSXCV L
<br>GRDXCVB A
<br>CVGRED G
<br>{WSX I
<br>IUYHNBV S/Z
<br>TRFVB C
<br>TRFVB C
<br>QWERTY _
<br>QAZSCE K
<br>WSXCDE E
<br>EFVT Y
<br>YHNMKJ b
<br>TGBNMJUY O
<br>GRDXCVB A
<br>MNBVCDRTGHU R
<br>WSXCFE D
<br>QWERTY _
<br>TRFVB C
<br>WSX I
<br>NBVCXSWERF P
<br>RFVGYHN H
<br>WSXCDE E
<br>MNBVCDRTGHU} R

逐渐离谱。脑洞题我还能说什么呢？你需要——想——象——力——

- ### Flag
  > FLAG{ISCC-KEYBOARD-CIPHER}