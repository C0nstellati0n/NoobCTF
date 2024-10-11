# babe-z3

关键是第一个条件期望值为false：`(v7 & v8 ^ (v6 | ~(v8 + v6)) & s & v7) == 0xD81AC01FBBA91837` ，可以从 `&& !(_DWORD)v4` 看出
```py
from z3 import *
from Crypto.Util.number import *
solver = Solver()
s=BitVec("s",64)
v6=BitVec("v6",64)
v7=BitVec("v7",64)
v8=BitVec("v8",64)
solver.add((v7 & v8 ^ (v6 | ~(v8 + v6)) & s & v7) != 0xD81AC01FBBA91837)
solver.add((v7 & s & v8 | (~(v6 | s) | v6 & v7) & v6 & s) == 0x2024243035302131)
solver.add((v6 ^ (v7 & (s + v7) | v8 & ~(v7 & s) | v6 & (v6 + v8) & ~s)) == 0x7071001344417B54)
solver.add(((v7 - v8) ^ (s - v6)) == 0x3FE01013130FFD3)
solver.add((s + v7 - v8 + v6) * (v8 + s + v6 - v7) == 0x1989A41A9049C5C9)
solver.add((v7 + v6 + s + v8) % 0x1BF52 == 21761)
solver.add(v8 * v7 * v6 * s % 0x1D4B42 == 827118)
if solver.check() == sat:
    print(solver.model())
print(long_to_bytes(7161907797182931769)[::-1]+long_to_bytes(7233453028217741666)[::-1]+long_to_bytes(3546362812256302905)[::-1]+long_to_bytes(3762587284301691189)[::-1])
```