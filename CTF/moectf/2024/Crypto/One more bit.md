# One more bit

```py
from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot
def continuedFra(x, y):
    cF = []
    while y:
        cF += [x // y]
        x, y = y, x % y
    return cF
def Simplify(ctnf):
    numerator = 0
    denominator = 1
    for x in ctnf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return (numerator, denominator)
def calculateFrac(x, y):
    cF = continuedFra(x, y)
    cF = list(map(Simplify, (cF[0:i] for i in range(1, len(cF)))))
    return cF
def wienerAttack(e, n,real_n,ciphertext):
    for (d, k) in calculateFrac(e, n):
        if k==0:
            continue
        if (e*d-1)%k==0:
            if b"moectf" in long_to_bytes(pow(ciphertext,d,real_n)):
                print(long_to_bytes(pow(ciphertext,d,real_n)))
pk = (134133840507194879124722303971806829214527933948661780641814514330769296658351734941972795427559665538634298343171712895678689928571804399278111582425131730887340959438180029645070353394212857682708370490223871309129948337487286534021548834043845658248447393803949524601871557448883163646364233913283438778267, 83710839781828547042000099822479827455150839630087752081720660846682103437904198705287610613170124755238284685618099812447852915349294538670732128599161636818193216409714024856708796982283165572768164303554014943361769803463110874733906162673305654979036416246224609509772196787570627778347908006266889151871)
ciphertext = 73228838248853753695300650089851103866994923279710500065528688046732360241259421633583786512765328703209553157156700672911490451923782130514110796280837233714066799071157393374064802513078944766577262159955593050786044845920732282816349811296561340376541162788570190578690333343882441362690328344037119622750
n,e=pk
wienerAttack(e, n+1-2*iroot(n,2)[0],n,ciphertext)
```
wiener attack有个要求，就是d必须小于关于n的特定bit数。这里正好差了一bit还是两bit左右，直接跑wiener attack确实出不来。冥思苦想得不到解决办法，想着说“差这么1bit就不能支棱起来吗，有没有增强版wiener attack啊”？遂浏览器搜索“enhanced wiener attack”，出来了这个玩意： https://onlinelibrary.wiley.com/doi/10.1155/2014/650537 。论文我是不看的，一股脑往下翻，看到了`2.3. Verheul and van Tilborg’s Extension`。内容也是看不懂的，但是为我指明了方向，继续搜索“wiener attack verheul and van tilborg’s extension”，找到了这个： https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=158dd0abfe27fdf2ceba24c3d168df93743af569 。还是那句话：论文是不会看的，原理是不明白的，结论是要偷的。第7页有个式子，标了个`(7)`。有点像普通wiener attack的展开式啊，套！然后成功了。哇，运气最好的一集