# one-more-time-pad

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/crypto/one-more-time-pad)

chall.py is really simple.

```python
from itertools import cycle
pt = b"Long ago, the four nations lived together in harmony ..."

key = cycle(b"lactf{??????????????}")

ct = ""

for i in range(len(pt)):
    b = (pt[i] ^ next(key))
    ct += f'{b:02x}'
print("ct =", ct)

#ct = 200e0d13461a055b4e592b0054543902462d1000042b045f1c407f18581b56194c150c13030f0a5110593606111c3e1f5e305e174571431e
```

For exclusive or, if A ^ B=C, then C^B=A and C^A=B. Knowing this, the problem is easy to solve.

```python
from Crypto.Util.number import *
pt = b"Long ago, the four nations lived together in harmony ..."
ct = long_to_bytes(0x200e0d13461a055b4e592b0054543902462d1000042b045f1c407f18581b56194c150c13030f0a5110593606111c3e1f5e305e174571431e)
for i in range(len(ct)):
    print(chr(ct[i]^pt[i]),end='')
```

## Flag
> lactf{b4by_h1t_m3_0ne_m0r3_t1m3}