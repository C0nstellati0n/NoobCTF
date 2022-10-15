# neo

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c6610b63-b203-4961-99b2-e0430120af48_2)

攻防世界根本就没配置好环境，只给了个nc，完全不知道要干啥。所以这篇将会是[wp](https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/neo)的简短翻译。

这题原版给了个网页进行交互，同时展示了base64编码后的一些内容。有解码选项会给出80字节的内容。每过几秒数据都会改变，合理猜测跟时间戳有关。如果我们自己提供base64内容会显示aes解码失败。种种迹象表明这是Padding Oracle Attack——这种方法可以让我们解码cbc模式下的块密码中的n-1个块。

cbc模式下明文与前一个块的密文进行异或。这意味着密文中任意字节的改变会让后续密文块中对应位置的字节解密不成功，毕竟它们没有和正确的值进行异或。我们想要了解解密过程中是如何处理填充的。在PKCS7中，解密后的数据的最后一个字节定义了填充。最后一个字节是一个数字，说明了有多少填充字节以及填充字节的值。举个例子，如果一个16字节的块有3字节填充，值为XXXXXXXXXXXXX0x30x030x3。

如果填充没有正确形成，我们会收到解密错误，因为原来的数据被篡改了。我们可以利用攻击尝试将明文字节转换为填充。

假设我们有2块密文。如果我们改变第一个块的最后一个字节，这个值会与第二个块的最后一个字节进行异或。既然我们改变了，自然不会得到正确的值，那么填充也会损坏，除非值为0x1，也就是正确的填充。如果值是0x1，意味着 我们改变的byte ^ 明文byte=0x1，转换得到明文byte=我们的改变的byte ^ 0x1。

所以当我们发现某一个值不会得到解密错误时，我们可以成功得到明文的最后一个byte。

接下来就能扩展到更多字节的情况了。尝试恢复k-1的byte，我们需要将最后一个byte改成0x2。如果没有出现错误，意味着异或的值也是0x2。

这个方法肯定不能让我们恢复第一个块，不过无伤大雅。有些情况加密时确实会把IV放在第一块明文前，如果是这种情况，我们同样可以把IV恢复。现在的情况时我们完全不知道IV是如何处理的，也不知道IV有没有用。猜测不需要IV，事实证明我们是对的。

脚本借助[模版](https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py)。

```python
import base64
import re
import urllib
import urllib2
import sys
from binascii import hexlify, unhexlify
from itertools import cycle

# most of the code comes from https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py
'''
    Padding Oracle Attack implementation of this article https://not.burntout.org/blog/Padding_Oracle_Attack/
    Check the readme for a full cryptographic explanation
    Author: mpgn <martial.puygrenier@gmail.com>
    Date: 2016
'''


def oracle(data):
    url = "http://crypto.chal.csaw.io:8001/"
    bytes_data = long_to_bytes(int(data, 16))
    values = {'matrix-id': base64.b64encode(bytes_data)}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    if "exception" in the_page:
        return False
    else:
        return True


def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


''' create custom block for the byte we search'''


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split('0x')[1]
    return "00" * (size_block - (i + 1)) + ("0" if len(hex_char) % 2 != 0 else '') + hex_char + ''.join(l)


''' create custom block for the padding'''


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(("0" if len(hex(i + 1).split('0x')[1]) % 2 != 0 else '') + (hex(i + 1).split('0x')[1]))
    return "00" * (size_block - (i + 1)) + ''.join(l)


def hex_xor(s1, s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1), cycle(unhexlify(s2)))))


def run(ciphertext, size_block):
    ciphertext = ciphertext.upper()
    found = False
    valid_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(ciphertext, len_block)
    if len(cipher_block) == 1:
        print "[-] Abort there is only one block"
        sys.exit()
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print "[-] Abort length block doesn't match the size_block"
            break
        print "[+] Search value block : ", block, "\n"
        for i in range(0, size_block):
            for ct_pos in range(0, 256):
                if ct_pos != i + 1 or (
                                len(valid_value) > 0 and int(valid_value[len(valid_value) - 1], 16) == ct_pos):
                    bk = block_search_byte(size_block, i, ct_pos, valid_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)
                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()
                    up_cipher = cb + cipher_block[block]
                    response = oracle(up_cipher)
                    exe = re.findall('..', cb)
                    discover = ''.join(exe[size_block - i:size_block])
                    current = ''.join(exe[size_block - i - 1:size_block - i])
                    find_me = ''.join(exe[:-i - 1])
                    sys.stdout.write(
                        "\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m" % (
                            ct_pos, block, find_me, current, discover))
                    sys.stdout.flush()
                    if response:
                        found = True
                        value = re.findall('..', bk)
                        valid_value.insert(0, value[size_block - (i + 1)])
                        print ''
                        print "[+] Block M_Byte : %s" % bk
                        print "[+] Block C_{i-1}: %s" % bp
                        print "[+] Block Padding: %s" % bc
                        print ''
                        bytes_found = ''.join(valid_value)
                        print '\033[36m' + '\033[1m' + "[+]" + '\033[0m' + " Found", i + 1, "bytes :", bytes_found
                        print ''
                        break
            if not found:
                print "\n[-] Error decryption failed"
                result.insert(0, ''.join(valid_value))
                hex_r = ''.join(result)
                print "[+] Partial Decrypted value (HEX):", hex_r.upper()
                padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
                print "[+] Partial Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")
                sys.exit()
            found = False
        result.insert(0, ''.join(valid_value))
        valid_value = []
    print ''
    hex_r = ''.join(result)
    print "[+] Decrypted value (HEX):", hex_r.upper()
    padding = int(hex_r[len(hex_r) - 2:len(hex_r)], 16)
    print "[+] Decrypted value (ASCII):", hex_r[0:-(padding * 2)].decode("hex")


def long_to_bytes(flag):
    flag = str(hex(flag))[2:-1]
    return "".join([chr(int(flag[i:i + 2], 16)) for i in range(0, len(flag), 2)])


def bytes_to_long(data):
    return int(data.encode('hex'), 16)


ct = base64.b64decode(
    "9aMTHPS1oP9VQA9Hxz5mGSIRuOVSspcQrGJlBYUoZIUhmur9X1B8hJJFeR48trScLtToNPCeWZiSz4Qit3KvsHlv0Xqy8rHREJUvYNbff1I=")
hexlified = bytes_to_long(ct)
run(hex(hexlified)[2:-1], 16)
```

补充学习时找到了一个讲的很好的博客，看这里没懂再来[这里](https://goodapple.top/archives/217)看绝对就懂了。

- ### Flag
  > flag{what_if_i_told_you_you_solved_the_challenge}