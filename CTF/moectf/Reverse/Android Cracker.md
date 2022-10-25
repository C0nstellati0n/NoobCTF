# Android Cracker

这么简单的一道题搞得我那叫一个难受啊……

之前没有用ghidra逆向apk的经验，本来想在电脑上安装ida pro的，结果搞了两个小时都没搞好。浪费我的时间，我打算直接ghidra硬上，感谢这篇[文章](https://infosecwriteups.com/how-to-use-ghidra-to-reverse-engineer-mobile-application-c2c89dc5b9aa)。

进入ghidra，点击菜单上的import file，选中要逆向的apk。重点来了，它会提示里面似乎有多个文件，要你选择导入方式。选择batch，深度多加几层，防止漏文件。batch完成后会在项目文件夹中出现batch出来的文件，直接菜单file->open就能看见3个dex后缀的class文件了。坑来了：第一个和第二个文件都没用，非常大，无法分析完成，只有第三个classes3.dex能逆向出来，flag也在里面。

- ### Flag
  > moectf{Andr01d_1s_so00oo_e@sy_t0_cr4ck!!!}