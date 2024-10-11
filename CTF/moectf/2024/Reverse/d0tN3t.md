# d0tN3t

```py
from string import printable
array=[173,
            146,
            161,
            174,
            132,
            179,
            187,
            234,
            231,
            244,
            177,
            161,
            65,
            13,
            18,
            12,
            166,
            247,
            229,
            207,
            125,
            109,
            67,
            180,
            230,
            156,
            125,
            127,
            182,
            236,
            105,
            21,
            215,
            148,
            92,
            18,
            199,
            137,
            124,
            38,
            228,
            55,
            62,
            164]
flag=''
for j in range(len(array)):
    for i in printable:
        if ((ord(i) + 114 ^ 114) ^ j * j)&0xff == array[j]:
            flag+=i
            break
print(flag)
```
重点是要按位与0xff(模仿java的char类型)，软件用dnSpy