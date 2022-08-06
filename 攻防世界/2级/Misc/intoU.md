# intoU

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=1d35d813-3ce5-48f0-994d-788f1ad986e7_2)

音频题，看来需要Audacity这类软件了。但是我没有，难道就不做了？在我的高强度冲浪下，我找到了个能用的在线[Audacity](https://www.offidocs.com/index.php/desktop-online-video-audio-apps/audacity-audio-editor-online)。

把文件上传并导入后可以看到下面的场景：

![audacity](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/audacity.png)

波形图翻了一会没啥东西，那么就看看频谱图。

![spectrum](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/spectrum.png)

感觉好像隐隐约约有点字藏在下面。这时候就可以考虑改一下采样率，看看会不会出现什么别的东西。

![sample](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/sample.png)

把采样率调成900就能在末尾看见flag了。

- #### Flag
- > RCTF{bmp_file_in_wav}