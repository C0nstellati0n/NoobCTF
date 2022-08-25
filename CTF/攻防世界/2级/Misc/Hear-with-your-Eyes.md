# Hear-with-your-Eyes

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=b56536ac-f606-4c17-b05a-029db1d9e935_2)

这道题非常友好，不仅题目已经说出重点了，还在提示又说了一遍ᶘ ᵒᴥᵒᶅ。既然是用眼睛听，肯定要考虑一下频谱图。这里我找到了一个在线的[频谱图分析网站](https://audiotoolset.com/cn/spectral-analysis)

不过在开始查看频谱图之前，我们要先把音频找出来。附件是一个zip，但是解压后并没有直接得到wav波形文件，而是一个无后缀的未知文件。

[终端显示1]()

file命令查看一个文件的真实格式。可以看到显示为tar文件。那就可以用 tar -xvf 文件名 进行解压。

[终端显示2]()

tar命令的有关帮助：

[tar]()

其中-x为解压命令，-f为指定文件，-v则是显示文件名。

最后播放音频就可以在频谱图里看见flag了

[flag]()