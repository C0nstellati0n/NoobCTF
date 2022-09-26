# xor_game

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=84142ef9-e8db-4e10-82d5-b0deb0b57f0f_2)

单纯记录一下脚本，因为这题在别的地方也出现过类似的。

```python
from Crypto.Util.strxor import strxor
import base64
import random


def enc(data, key):
    key = (key * (len(data) / len(key) + 1))[:len(data)]
    return strxor(data, key)


poem = open('poem.txt', 'r').read()
flag = "hctf{xxxxxxxxxxx}"

with open('cipher.txt', 'w') as f:
    f.write(base64.b64encode(enc(poem, flag[5:-1])))
    f.close()
```

异或，key为flag，完全未知。但是从enc函数中能看出来key是被重用的，且与data等长。没有别的办法，只能爆破。原理[在这](https://www.cnblogs.com/coming1890/p/13571982.html)。然后我发现官方的脚本好像更棒。

```python
import base64
import string


def bxor(a, b):     # xor two byte strings of different lengths
    if len(a) > len(b):
        return bytes([x ^ y for x, y in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for x, y in zip(a, b[:len(a)])])


def hamming_distance(b1, b2):
    differing_bits = 0
    for byte in bxor(b1, b2):
        differing_bits += bin(byte).count("1")
    return differing_bits


def break_single_key_xor(text):
    key = 0
    possible_space = 0
    max_possible = 0
    letters = string.ascii_letters.encode('ascii')
    for a in range(0, len(text)):
        maxpossible = 0
        for b in range(0, len(text)):
            if(a == b):
                continue
            c = text[a] ^ text[b]
            if c not in letters and c != 0:
                continue
            maxpossible += 1
        if maxpossible > max_possible:
            max_possible = maxpossible
            possible_space = a
    key = text[possible_space] ^ 0x20
    return chr(key)


text = ''
with open('cipher.txt', 'r') as f:
    for line in f:
        text += line
b = base64.b64decode(text)


normalized_distances = []

for KEYSIZE in range(2, 40):
    b1 = b[: KEYSIZE]
    b2 = b[KEYSIZE: KEYSIZE * 2]
    b3 = b[KEYSIZE * 2: KEYSIZE * 3]
    b4 = b[KEYSIZE * 3: KEYSIZE * 4]
    b5 = b[KEYSIZE * 4: KEYSIZE * 5]
    b6 = b[KEYSIZE * 5: KEYSIZE * 6]

    normalized_distance = float(
        hamming_distance(b1, b2) +
        hamming_distance(b2, b3) +
        hamming_distance(b3, b4) +
        hamming_distance(b4, b5) +
        hamming_distance(b5, b6)
    ) / (KEYSIZE * 5)
    normalized_distances.append(
        (KEYSIZE, normalized_distance)
    )
normalized_distances = sorted(normalized_distances, key=lambda x: x[1])


for KEYSIZE, _ in normalized_distances[:5]:
    block_bytes = [[] for _ in range(KEYSIZE)]
    for i, byte in enumerate(b):
        block_bytes[i % KEYSIZE].append(byte)
    keys = ''
    try:
        for bbytes in block_bytes:
            keys += break_single_key_xor(bbytes)
        key = bytearray(keys * len(b), "utf-8")
        plaintext = bxor(b, key)
        print("keysize:", KEYSIZE)
        print("key is:", keys, "n")
        s = bytes.decode(plaintext)
        print(s)
    except Exception:
        continue
```

但是我完全看不出来原理。就当积累脚本了。

- ### Flag
  > hctf{xor_is_interesting!@#}