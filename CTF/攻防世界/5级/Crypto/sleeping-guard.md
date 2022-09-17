# sleeping-guard

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=46f3e1cc-921f-426b-b418-6d810f06a548_2&task_category_id=5)

这题少附件了，只有经验丰富的大佬才能在少附件的情况下做出来。这不巧了吗，我不是。

少的附件可以当作一种提示。

```python
import base64
from twisted.internet import reactor, protocol
import os
 
PORT = 9013
 
import struct
def get_bytes_from_file(filename):  
    return open(filename, "rb").read()  
    
KEY = "[CENSORED]"
 
def length_encryption_key():
    return len(KEY)
 
def get_magic_png():
    image = get_bytes_from_file("./sleeping.png")
    encoded_string = base64.b64encode(image)
    key_len = length_encryption_key()
    print 'Sending magic....'
    if key_len != 12:
        return ''
    return encoded_string 
    
 
class MyServer(protocol.Protocol):
    def connectionMade(self):
        resp = get_magic_png()
        self.transport.write(resp)
 
class MyServerFactory(protocol.Factory):
    protocol = MyServer
 
factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
```

图片的加密和key有关。虽然题目中并没有明确指出到底用的是什么类型的加密，但是在只给了加密的png的情况下最容易联想到什么？异或加密，就算png再怎么变化文件头都不会变化，那么知道密文且知道其对应的明文不就是经典异或破解key的操作了吗？且key长度只有12，png文件头的长度足够复原全部的key。

连接nc，我去怎么这么多。我懒得在shell中复制了，直接用pwntools接收输入然后存到文件中。

```python
from pwn import *
p=remote("61.147.171.105",55054)
content=p.recvall(timeout=1)
with open("ctf.txt",'wb') as f:
    f.write(content)
```

recvall默认会一直接收到p被关闭，但是实测nc在不干扰的情况下不会自动关闭，所以设置个timeout，1秒内没有新的输出就自动关闭，接收已有的内容。然后用标准png文件头89504e470d0a1a0a0000000d49484452异或base64解码后的图片前几个字符，得到key。后面就简单了，直接把图片与key异或得到正确图片，写入文件后打开。全部内容合在一个脚本后如下。

```python
from pwn import *
p=remote("61.147.171.105",55054)
content=p.recvall(timeout=1)
with open("ctf.txt",'wb') as f:
    f.write(content)
from base64 import b64decode
from Crypto.Util.strxor import strxor
from binascii import unhexlify
png_head=unhexlify('89504e470d0a1a0a0000000d49484452')
with open("ctf.txt",'rb') as f:
    png=b64decode(f.read())
key=strxor(png_head,png[:len(png_head)])[:-4]
flag=''
for i in range(len(png)-len(key)):
    key+=chr(key[i%len(key)]).encode()
flag=strxor(png,key)
with open("flag.png",'wb') as f:
    f.write(flag)
```

借助了Crypto库的strxor完成。strxor要求两个参数长度相同，但我们的key肯定没有png长，所以异或之前先补全长度。[:-4]是因为key长度只有12，但文件头长度有16，所以后面4个字符是重复的，不需要。

- ### Flag
  > flag{l4zy_H4CK3rs_d0nt_g3T_MAg1C_FlaG5}