# APK逆向-2

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=674f06fb-be6e-4635-b657-fee1cbbd2107_2&task_category_id=6)

jadx反编译apk，函数不多，好事。但是看了一会有点怀疑人生，我要干啥啊？整个程序没有任何地方涉及到判断，没有判断我就不知道从哪入手。看了看wp，原来是AndroidManifest.xml的活。

apk逆向题做的不多，养成了上来就猛冲MainActivity的坏习惯。虽然很多时候都没啥问题，但现在就是出问题的时候。但凡我去看一下AndroidManifest.xml，就能立刻意识到有问题，因为那个文件是空的，正常的apk不可能是空的。这道题考的是AndroidManifest.xml的修复。翻出之前做的题，把其中3个的AndroidManifest.xml搞出来放进010Editor分析；同时把这道题的搞出来放进去对比。

能在3个好的文件里发现共性：

1. 第一行8-B范围内的字节固定为01 00 1C 00
2. 第3行2处的字节都是00

根据共性修改这道题的AndroidManifest.xml文件。我们把原apk后缀改为zip拿出的AndroidManifest.xml文件，然而不能把zip改为apk来重新打包，需要利用例如Android Studio等工具[打包](https://blog.csdn.net/woaichimahua/article/details/54427528)。打包完成后放入jadx反编译，查看AndroidManifest.xml，发现有一个android:name字段内容较为奇怪，正常后面应该跟着包名，但是这里却是一串16进制。这就是flag。

## Flag
> 8d6efd232c63b7d2