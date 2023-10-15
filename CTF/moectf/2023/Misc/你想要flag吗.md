# 你想要flag吗

音频文件audacity打开，看频谱图，有:
```
key:Bulbasaur
passwd:youseeme
```
字样。然后用steghide(linux安装steghide：`apt install steghide`)对音频进行提取，密码就是youseeme
```sh
steghide extract -sf 1.WAV -xf out
```
出来的out：
```sh
file out 
out: openssl enc'd data with salted password, base64 encoded
```
cat一下，发现开头是U2F。想到去年的rabbit，那就去个在线网站即可： https://www.sojson.com/encrypt_rabbit.html ，密码是Bulbasaur