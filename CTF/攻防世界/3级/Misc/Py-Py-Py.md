# Py-Py-Py

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=8faa99ad-c064-4af0-8954-29647c8d1f1e_2)

长见识，但是脚本小子。

附件是个pyc，直接反编译。结果又是python2，有点烦人。

```python
import sys, os, hashlib, time, base64
fllag = '9474yeUMWODKruX7OFzD9oekO28+EqYCZHrUjWNm92NSU+eYXOPsRPEFrNMs7J+4qautoqOrvq28pLU='
def crypto(string, op='encode', public_key='ddd', expirytime=0):
    ckey_lenth = 4
    public_key = public_key and public_key or ''
    key = hashlib.md5(public_key).hexdigest()
    keya = hashlib.md5(key[0:16]).hexdigest()
    keyb = hashlib.md5(key[16:32]).hexdigest()
    keyc = ckey_lenth and (op == 'decode' and string[0:ckey_lenth] or hashlib.md5(str(time.time())).hexdigest()[32 - ckey_lenth:32]) or ''
    cryptkey = keya + hashlib.md5(keya + keyc).hexdigest()
    key_lenth = len(cryptkey)
    string = op == 'decode' and base64.b64decode(string[4:]) or '0000000000' + hashlib.md5(string + keyb).hexdigest()[0:16] + string
    string_lenth = len(string)
    result = ''
    box = list(range(256))
    randkey = []
    for i in xrange(255):
        randkey.append(ord(cryptkey[(i % key_lenth)]))

    for i in xrange(255):
        j = 0
        j = (j + box[i] + randkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp
    for i in xrange(string_lenth):
        a = j = 0
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result += chr(ord(string[i]) ^ box[((box[a] + box[j]) % 256)])
    if op == 'decode':
        if result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0:
            if result[10:26] == hashlib.md5(result[26:] + keyb).hexdigest()[0:16]:
                pass
            return result[26:]
        else:
            return
    else:
        return keyc + base64.b64encode(result)
if __name__ == '__main__':
    while True:
        flag = raw_input('Please input your flag:')
        if flag == crypto(fllag, 'decode'):
            print('Success')
            break
        else:
            continue
```

看到xrange就能判断是python2了。还好我本机有残留的2.7环境，[网上](https://c.runoob.com/compile/6/)也可以在线运行。

运行出来提示“这是个隐写题”，又到了我的知识盲区。查阅发现pyc也有隐写，可以用[stegosaurus](https://github.com/AngelKitty/stegosaurus)来提取payload。注意虽然这个工具要求3.6版本及以上，但是我3.10是没办法运行的。3.6环境下一行命令搞定。

- python3 stegosaurus.py -x py_py_py.pyc

- ### Flag
  > Flag{HiD3_Pal0ad_1n_Python}