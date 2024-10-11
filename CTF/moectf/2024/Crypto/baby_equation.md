# baby_equation

wolframalpha分解方程得到`(a + 1)^2 (b - 1)^2 - 4 k = 0`，见`https://www.wolframalpha.com/input?i=((a**2+%2B+1)*(b**2+%2B+1)+-+2*(a+-+b)*(a*b+-+1))+-+4*(k+%2B+a*b)%3D0`

4k是两个完全平方数的乘积，所以4k肯定也是完全平方数。4k开方后是`(a+1)(b-1)`，可以把4k放进factordb即可看见分解结果。将其所有质因数按照爆破的方式组装起来，可以得到`a+1`或者`b-1`

末尾两个质因数较大，必然不可能在一起。可以剔除掉一个加快爆破速度
```py
from itertools import permutations
from math import prod
from Crypto.Util.number import *
num=64889106213996537255229963986303510188999911
candidates=[2,2,2,2,3,3,31,61,223,4013,281317,4151351,339386329,370523737,5404604441993,26798471753993]
prod_all=prod(candidates)*num*25866088332911027256931479223
for group in permutations(candidates,7):
    temp=prod(group)*num
    if b'moectf' in long_to_bytes(temp) or b'moectf' in long_to_bytes(prod_all//temp):
        print(long_to_bytes(temp+1))
        print(long_to_bytes(prod_all//temp-1))
        break
```