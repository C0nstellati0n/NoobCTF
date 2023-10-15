# ezchain

瞄了一眼题就想到了去年的[ez_cbc](../../2022/Crypto/ez_cbc.md)。但是我没看懂我tm写的是什么鬼东西，直接抄后面的脚本然后改一下即可。
```py
from Crypto.Util.number import *
IV = 3735927943
cipher=[8490961288, 122685644196, 349851982069, 319462619019, 74697733110, 43107579733, 465430019828, 178715374673, 425695308534, 164022852989, 435966065649, 222907886694, 420391941825, 173833246025, 329708930734]
flag=[5329712293]
key=flag[0]^IV^cipher[0]
for i in range(1,len(cipher)):
    flag_part=cipher[i]^key^cipher[i-1]
    flag.append(flag_part)
flag_digit=0
for i in flag:
    flag_digit*=461430682735
    flag_digit+=i
print(long_to_bytes(flag_digit))
```
今年的创新点在于flag的进制转换。如果之前有了解过的可以直接写个转回去的脚本，或者逆向那个函数。我属于卡在中间的那一类，之前见过类似的但是忘的差不多了，就记得反正是乘一下加一下，摆弄了一下顺序就得到了结果。总之这类进制转换的逻辑都是这么写的，无论进制是什么base都行