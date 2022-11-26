# [NCTF2019]babyRSA

[题目地址](https://buuoj.cn/challenges#[NCTF2019]babyRSA)

咱也不知道rsa到底还能怎么变形。

这题特殊的地方只有p和q是相邻的素数，其他的都是正常rsa操作。然而给的条件非常奇怪，d和c。n呢？我的n呢？不懂，看[wp](https://blog.csdn.net/weixin_45441024/article/details/110351394)吧。

其实也不难，关键在于写出e和d关系的式子。

$∵e*d=1\mod(p-1)(q-1)$<br>
$∴e*d-1=k(p-1)(q-1)$

p和q都是1024位，所以他们的乘积会是2048位的。e*d的乘积是2064位的，所以k最多是一个16位的数字（不可能超过16位）。我们可以爆破k，条件就是ed-1%k==0。这种情况下，(ed-1)//k=(p-1)(q-1)，和n差不多了，然而不是n。此时我们将其开方，得到的数必定大于其中一个质数（因为p和q肯定不能一样大，而直接开方相当于将两个数看作一样大，自然会得到一个界于两个质数中间的数）。然后利用sympy.prevprime得到前一个质数，sympy.nextprime得到刚才得到的质数的下一个质数，解决n的问题。

```python
e = 0x10001
d = 19275778946037899718035455438175509175723911466127462154506916564101519923603308900331427601983476886255849200332374081996442976307058597390881168155862238533018621944733299208108185814179466844504468163200369996564265921022888670062554504758512453217434777820468049494313818291727050400752551716550403647148197148884408264686846693842118387217753516963449753809860354047619256787869400297858568139700396567519469825398575103885487624463424429913017729585620877168171603444111464692841379661112075123399343270610272287865200880398193573260848268633461983435015031227070217852728240847398084414687146397303110709214913
c = 5382723168073828110696168558294206681757991149022777821127563301413483223874527233300721180839298617076705685041174247415826157096583055069337393987892262764211225227035880754417457056723909135525244957935906902665679777101130111392780237502928656225705262431431953003520093932924375902111280077255205118217436744112064069429678632923259898627997145803892753989255615273140300021040654505901442787810653626524305706316663169341797205752938755590056568986738227803487467274114398257187962140796551136220532809687606867385639367743705527511680719955380746377631156468689844150878381460560990755652899449340045313521804
import sympy.crypto
import gmpy2
ed1=e*d-1
p=0
q=0
for k in range(pow(2,15),pow(2,16)):
    if ed1%k==0:
        p=sympy.prevprime(gmpy2.iroot(ed1//k,2)[0])
        q=sympy.nextprime(p)
        if (p-1)*(q-1)*k==ed1:
            break
n=p*q
print(n)
m=gmpy2.powmod(c,d,n)
print(m)
import binascii
print(binascii.unhexlify(hex(m)[2:]))
```

## Flag
> flag{70u2_nn47h_14_v3ry_gOO0000000d}