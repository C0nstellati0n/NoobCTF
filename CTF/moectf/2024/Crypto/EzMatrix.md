# EzMatrix

```py
# https://www.ruanx.net/babylfsr/
import itertools
def bitAnd(a, b):
    assert len(a) == len(b)
    return list(map(lambda x,y: int(x)&int(y), a, b))
def test(padding):
    s = [int(x) for x in '11111110011011010000110110100011110110110101111000101011001010110011110011000011110001101011001100000011011101110000111001100111011100010111001100111101010011000110110101011101100001010101011011101000110001111110100000011110010011010010100100000000110'] + padding
    M = matrix(GF(2), 128, 128)
    T = vector(GF(2), 128)
    for i in range(len(s) - 128):
        M[i] = s[i : i + 128]
        T[i] = s[i+128]
    try:
        mask = M.inverse() * T
        print(''.join(map(str, (mask))))
    except:
        return
    suf = []
    for i in range(128):
        if bitAnd([0] + suf + s[0:127 - i], mask).count(1) % 2 == s[127 - i]:
            suf = [0] + suf
        else:
            suf = [1] + suf
    print(suf)
for x in itertools.product([0, 1], repeat = 5):
    test(list(x))
```
真正的mask只有几个bit是1(去年还是前年有类似的题，三周目中登经验之谈)。根据这个线索可以找到正确的输出
```py
from Crypto.Util.number import *
cipher=[0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1]
cipher=''.join(map(str,cipher[1:]))
print(long_to_bytes(int(cipher,2)))
```