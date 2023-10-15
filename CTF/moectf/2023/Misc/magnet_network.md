# magnet_network

装torrent文件的challenge.zip不是zip，是zstd。`zstd -d challenge.zst`解压

torrent文件在 https://chocobo1.github.io/bencode_online/ 可以查看其结构

然后 https://en.wikipedia.org/wiki/Torrent_file 有torrent的文件结构解释。重要的是pieces，表示文件每一部分的SHA1值（然后拼接在一起）。文件每一部分的长度在piece length里，为16384。

comment提示flag除去moectf{}，中间长度为24。查看info里的files，发现一个文件小一个文件大，长度刚好是16384.猜测要4位4位地爆破flag。但是那个大的长度16380的文件不知道就没法爆破。查了一下发现是qBittorrent的pad文件，用于将文件长度pad成piece length。不过没有查到pad文件的内容，那就猜。空格，p（因为里面有个`"attr": "p"...`,开脑洞可惜是错的）都不是，最后发现是`\x00`

注意最后一段4个字符的flag不需要ljust(16384,b'\x00')。仔细看torrent的json文件就能看到后面没有pad文件了。
```py
from itertools import product
import hashlib
letters="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@!_?"
h="3ACAD96EE53545F8AD3C419C5B1965BEA234CC6AB339E2547E1BB5C1E56C2ACEAB1F7CF5AF93D13D65131DBA750FDCB715E3235107041DE9C79671AED3BA653B9D29544B623902AA07074492793C7AD44DD6E892D925A7411CB1677B8B5D8FEC6D9308ACCC83047E9AE392E02B5044283C89F16DC26F328E"
def crack(h):
    for comb in product(letters,repeat=4):
        code = ''.join(comb)
        encinfo = hashlib.sha1(code.encode().ljust(16384,b'\x00')).hexdigest()
        if encinfo == h:
            return code
flag=''
#用来爆后4个字符的
for comb in product(letters,repeat=4):
        code = ''.join(comb)
        encinfo = hashlib.sha1(code.encode()).hexdigest()
        if encinfo == h[-40:].lower():
            flag+=code
            break
print(flag)
#前20个字符直接爆
""" for i in range(40*5,len(h)-40,40):
    flag+=crack(h[i:i+40].lower())
    print(flag) """
```
然后出来的flag的字符顺序不对。我也不知道去哪里看正确的顺序（以为是path的数字，但是好像出不来？可能我搞错了）。所以我手动把它调好的
```
p2p_ nter ng_2 iS_i WPIB eSti

p2p_iS_intereSting_2WPIB
moectf{p2p_iS_intereSting_2WPIB}

sha256(b'moectf{p2p_iS_intereSting_2WPIB}').hexdigest()==de5d94f22a9b8eab09779102a0fcc9c566880f7807d359da6f27723f3b881584
```