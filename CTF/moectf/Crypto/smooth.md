# smooth

看题目我就想到了之前做过的一道有关平滑数的题，当时使用pollard n-1分解法强行把n分解出来了。我们先看看脚本，是不是真的符合平滑数的定义。

```python
from Crypto.Util.number import sieve_base,isPrime,getPrime
import random
from secret import flag

def get_vulnerable_prime():
    p=2
    while True:
        for i in range(136):
            smallp=random.choice(sieve_base)
            p*=smallp
        if isPrime(p+1):
            return p+1

P=get_vulnerable_prime()
Q=getPrime(2048)
N=P*Q
e=0x10001

for i in range(1,P-1729):
    flag=flag*i%P

c=pow(flag,e,N)
print("c=",hex(c))
print("N=",hex(N))
```

c和N一会再放，有亿点大。看下get_vulnerable_prime的定义。首先p等于2，为正整数中最小的素数。然后无限循环，从前10000个素数（sieve_base是包含前10000个素数的列表）中随机选择一个乘上p，然后赋值给p。如果p+1是素数，则跳出循环返回p+1，否则继续循环。完全符合[光滑数](https://zh.m.wikipedia.org/zh-cn/%E5%85%89%E6%BB%91%E6%95%B8)的定义，这也是有关rsa的题型之一：p-1为光滑数。

用上面提到的[pollard n-1](https://upwikizh.top/wiki/Pollard%27s_p_%E2%88%92_1_algorithm)可以直接分解出p和q。

```python
import gmpy2
from Crypto.Util.number import inverse
def factor_smooth_p(N):
    a = 2
    n = 2
    for n in range(2, N):
        a = gmpy2.powmod(a, n, N)
        res = gmpy2.gcd(a - 1, N)
        if res != 1 and res != N:
            q = N // res
            p = N // q
            return p, q
c= 0x3cc51d09c48948e2485820f6758fb10c7693c236acc527ad563ba8369c50a0bc3f650f39a871ee7ef127950ed916c5f4dc69894e11caf9d178cd7e8f9bf9af77e1c69384cc5444da64022b45636eeb5b7a221792880dd242be2bb99be3ed02c430c2b77d4912bec1619d664e066680910317c2bb0c87fafdf25f0a2400103278f557b8eca51d3b67d61098f1ab68da072bb2810596180afbc81a840cd24efef4d4113235160e725a5af4824dc716d758b3bc792f2458e979398e001b27e44d21682e2ef80ae94e21cd09a12e522ca2e569df72f012fa40341645445c6e68c6233a8a39e5b91eb14b1ccfa61c9bad25e8e3285a22da27cd506ddd63f207517a4e8ede00b104d8806ff4c0e3162c3de69169d7e584952655272b96d39d242bb83019c7eab1ceb0b4b287591e1e0a5b6378e70340a82d3430c5925d215f31fda6d9d0bccea240591b22a3d0f6b5bf4ddf1243d71aca0fd53045c352c8c5497ebcdbd7ac11083d63aba7c053604fda2430c317a4e04702b5ad539e110f101165b21dcd9fdb5ba7324acdba6a506244ce7c911197dfe067441fe7488d164c050f45ef6476aaf399cedde1793cceb8c21d88ec8ecf5e17df27586713d7dd9566ec5023cfef75422b73e2d5a932c661b3cfdf9c4bda12b64380d2be1aa957c3e1416e068937bafe79b8cf303296792388e9c197702e11e7ded6088ae992d352b23a4a27
N= 0xdc77f076092cbe81c44789ccfc1b2ca55eabae65f44cf34382799e8bbb42d4d6c032bd897c21df1da401929d82deb56264823a757f6cacf63e0037146026cbab32ab9e4abc783dcabaac2b7ccc439937be3ab0fbf149524ff29ef0fe6f27e45215d74b40597c70e8207159dc7f542c2a6828500016480053dfc2d8dbf8fcdf6700640184c8f3318f7aab2e17e116edf680592f5eae951159bb8c20cfbd0cbab8b4b95925b5068038d0377a55a4d346ebbf53a1c2943b7c17e1b9d4a1b77916da2e15140b05b96655906942a07d04b7e25fa7521b3b7ae26eda68375a8b8ef2d5b4704a28168b236de97f24a663f0d0a3aeab47767dfe75a21662f5f25ef7f7d4b25c90fd7bcdd7137c23f03b6ea4209f8fb9b4628355e6ad62e6467d26666d3d1b0e6f078c5f3866413a6fcd3c1dc2ff3a5ab286e339d5c72f4d2f0473a4faddcba6b031bb6ec226fd4b319834b5029f09ea0ffeb5b6ed182d5a13675571b6708c38299118043390343e2f79edebd2ae0e0a765a3aebf776f54ca983cdae8547547cfc8430f7222aefa77301d7cc7c03b1451b6603028b21fea869d35138a9c83919985a91b3fdfa934f25a442cc10349b0ed6f2ee3955d40249e8b3fb9f1955534ee06cee41a3ad2d6ff7dbdb0f01e47b9e4d04f65232f5579135ae035e8ba2d1fe6465a730dcc8b9ba3a558ab38f040ea510757d25e92f886c50c24ad967f1
e=65537
p,q=factor_smooth_p(N)
toitent=(p-1)*(q-1)
d=inverse(e,toitent)
plaintext=hex(pow(c,d,N))[2:]
print(f"p值为: {p}\nq值为: {q}")
print(f"明文为: {plaintext}")
#p=45130782138821231634664822924606644347274161463663927387578931639175223286413378324882645031302403289842551326638702711998962760517679897418281467484531163375644705075213662848721478455926415639437965574871053673938130437463383431907231224801316309790287364751279984404056565040242248326224648040650860211493169850992812996172453840449200075853777085801648416876006333273306936825124410389797307488083056497244608773881660250930270420195391832629035158125925203262309579280388854014294622011159984832956422300816768157089660974628522818677622546453173413252374696944407138466146678080076210538578674319834619518810099
#q=19929480903966971877741359978214832777067673186776101767607985415984872967131783702304729626331577711025830876686674170433788564223656884574965375895417512648538448454114165043668565344845361735967533803734325629433944151906019295203849389937041766109566748588937702389000280859653264841778232075227804461734481644568063879619171473653153879467534960561551793532641987408308262590477344407917566949561595540828562062207376467975716207562802834742657134267225310067273840884699549038482335638587159643505585791895934244621169372816478043004416985427985158346066496193091020702283948166437350554644511384320505926737291
#明文=0x3c1f23837cb4b3c6c08917e762184110fbdeb6b85a7552df0581ddb644671d820f77871b8082b67a588677dbeeb9b065c8be1b1bde1dd84751b045d4ba3104fcea4132b9d8009ab6a2f49f219ebb49388275d70318b6165d584f55fa75b075d5e5f4dcd87d1edd11047a157f9efa6d33235944b3c7ee8b8481e63789ad91821c73e3e59c54f906f46a39d860a9947a4ef44e5075cc994e62e997bad74468c9cf28cb4c724543266d07c34c2b404bacb174f200f8b699002b0dff07f050da89815e838b6c8a114d9ac2fe8c61b0bcc24c83f27d6f303b0be4506d2067696470ba342ba2436f06cff651fa7365eb6805414494b8fa9b267152fe33c5fae4c2e1d0
```

此明文非彼明文。注意题目有一个for循环了P-1729（或者P-1730？不重要，都很大就对了）次，每次flag=flag*i%P。现在的任务是找到最开始的flag。我的眼睛表示很简单，我的脑子表示自己的容量只有米粒大小。所以我又要瞎推算了。

把flag\*i看作一个整体，那么第n+1次的flag是第n次flag除以p的余数。众所周知在除法的世界里，a=qb+r，其中a是被除数，b是除数，q是商，r是余数。在此处的上下文中，被除数是第n次flag\*i，flag*i//P是商，P是除数，余数是第n+1次flag。有没有一点感觉了？管他的直接开始写脚本，错了就错了。

不对，我怎么找到qb的值？商不知道啊。不过这还能表达成同余的方式。$a\equiv r(\mod qb)$，必有整数k满足$a-r=mk$。假如我们找到mk了就可以mk+r求出a。但是mk也找不到啊？我还有一个，同余也等价于$m|(a-r)$，即m整除于a-r。a应该是要比r大的，所以试一下。

试个鬼，m整除于a-r但是整除于多少倍的a-r？刚刚看了下明文，比p小了一位。因为都是余数，所以除了最初的flag长度不确定外，剩下几次循环的flag长度都在1到p-1之间。我还特地看了一下for循环（python基础开始拉了），for循环的i值最大只会取到P-1730。先看看两个极值：如果余数flag为1，最后一次循环乘上了p-1730，模p的余数还是p-1730。假如余数flag为p-1，乘上p-1730再模p等于$((p-1)(p-1730))(\mod p)=p^2-1731p+1730(\mod p),p^2\equiv 0(\mod p),-1731p\equiv 0(\mod p),1730\equiv 1730(\mod p),(p^2-1731p+1730)\equiv 0+0+1730(\mod p)$。所以余数应该是1730，但我们是这一串乱七八糟的数字，因此上一次循环的余数肯定不是p-1。

不对吧，虽然能这么算出来，但我们要倒着推p-1730次？疯了吗？就算用计算机暴力破解，每个循环都有很多种可能性，每个可能性又能爆炸增长可能性，算到电脑报废都算不出来。

所有的余数都能被表达为p-n的形式，每次的i都能被表达为p-j的形式。$(p-n)*(p-j)=p^2-pj-np+nj=p^2-p(j+n)+nj$。$p^2$和p(j+n)怎么着都整除于p，所以余数仅仅取决于nj。这是否意味着只有一种情况？

结果不对。我就知道。应该是有什么漏了。还记得余数等于1那个情况吗？按照我们的推算，这种情况就是$(p-(p-1))*(p-j)=p^2-pj-p(p-1)+j(p-1)=p^2-pj-p^2+p+jp-j=p-j,p-j\equiv 0-j\equiv -1730(\mod p)$。同余里面是可以同余负数的，但是转成python后\%的结果肯定没有负数，故要再加个p，把结果还原成整数。这个式子的nj是什么？$j(p-1)=jp-j\equiv -j\equiv p-j(\mod p)$。别说一下子还真没看出来什么规律，或许是我脚本写错了？我自己乱搞搞试试。

还没法实验，随便找个数字经过那么多次for循环后结果直接是0，可能因为我用的不是质数吧。我也不敢用求出来的p，太大了根本没法跑。

找了质数就有最后的余数了。可是我求不出来。确实是nj，不过还要%p。

找到了一个好像可以的办法，开始算了。怎么说呢，我已经算了10分钟了，还没有出来。最多算20分钟，再长电脑就炸了。已经开始烫了，而且我不敢保证一次能出。要是不行还要再来一次。难道是我太菜了没找到捷径吗？怎么要这么久？

出题人是什么魔鬼，怎么想出来那个for循环的？要不我试一下拿c语言会不会更快。

我忘了c语言会溢出。啊！！！我觉得我方法错了，这样几乎要算p的二次方次，比赛结束了都算不出来。再说一次出题人真的狠人，硬生生循环了将近P次。我的方法应该是没错了，就是运行时间跑不起啊。而且我把可能的值都放到了字典里做了比对，重复项很少，也找不到明显的规律。p更大的情况肯定更多可能。这题的难度不在smooth，而是还原flag？

没招了。flag=flag\*i%P说明n+1次的flag是flag\*i模p的余数，因此第n次的flag\*i-第n+1次的flag整除于p。找p的各个倍数然后加上n+1次的flag，结果如果能整除i就是flag。没少多少次，当p=9973的时候倍数最大能大于9000p。还能推吗？

$flag*i\equiv rFlag(\mod p),flag\equiv rFlag//i(\mod p)$。flag最小等于p+rFlag。但是不一定最小，搞了半天还是不行，同余这个条件真的太难搞了。

几个星期过去了，我问大佬了大佬没回。仔细看了一下，不是这不就是普通的一次同余方程吗，难怪大佬没回，被我整无语了。一次同余方程形如$ax\equiv b\mod n$，当gcd(a,n)=1时可以在方程两边同乘a模n的逆元，构成$a*a^{-1}*x\equiv b*a^{-1}$。我们知道a对n逆元的定义是$a*a^{-1}\equiv 1\mod n$，所以方程就被转换成了$x\equiv b*a^{-1}\mod n$，只需要把b和逆元相乘就是x的一个解了。更详细的内容参考[这](https://www.expii.com/t/solving-linear-congruence-ax-b-mod-n-3389#:~:text=To%20solve%20a%20linear%20congruence,solutions%20for%20x%20mod%20N.)。

回到我们当下的情况。i一定小于p，且一定与p互质，等于直接找i对p的逆元，然后乘上当前的flag值就能一直往前推了。得到的结果记得模p，否则会变得超级大。举个例子，当前i为978，p为9973，flag为2561（这个情况随便举的不一定有解，看个过程就行了）。所以现在的方程是$978x\equiv 2561\mod 9973$。找到978对9973的模逆元，方程两边乘上这个逆元，978被消掉，答案为$x\equiv 2561*x^{-1}\mod 9973$。因为上次的结果肯定小于p，故再把得到的x模p就是答案。

但是这样还是要循环p-1729次。想不出来别的方法了，出题人电脑是真的好啊。我没跑出来，放弃了，查了python的for循环速度，我这个跑一周能出来都悬。

官方wp出来了，我离flag只差了个威尔逊定理。唉数论没学到那。定理本身很简单：p是素数，则 $(p-1)!\equiv -1\mod p$。至于1729，没啥意义，是出题人的彩蛋。草。知道这个，脚本就很简单了，因为p是质数，题目已经把阶乘算到了p-1729，那我们从这里开始，继续求阶乘，完整后取负数模p就是了。

```python
import gmpy2
from Crypto.Util.number import *
def factor_smooth_p(N):
    a = 2
    n = 2
    for n in range(2, N):
        a = gmpy2.powmod(a, n, N)
        res = gmpy2.gcd(a - 1, N)
        if res != 1 and res != N:
            q = N // res
            p = N // q
            return p, q
c= 0x3cc51d09c48948e2485820f6758fb10c7693c236acc527ad563ba8369c50a0bc3f650f39a871ee7ef127950ed916c5f4dc69894e11caf9d178cd7e8f9bf9af77e1c69384cc5444da64022b45636eeb5b7a221792880dd242be2bb99be3ed02c430c2b77d4912bec1619d664e066680910317c2bb0c87fafdf25f0a2400103278f557b8eca51d3b67d61098f1ab68da072bb2810596180afbc81a840cd24efef4d4113235160e725a5af4824dc716d758b3bc792f2458e979398e001b27e44d21682e2ef80ae94e21cd09a12e522ca2e569df72f012fa40341645445c6e68c6233a8a39e5b91eb14b1ccfa61c9bad25e8e3285a22da27cd506ddd63f207517a4e8ede00b104d8806ff4c0e3162c3de69169d7e584952655272b96d39d242bb83019c7eab1ceb0b4b287591e1e0a5b6378e70340a82d3430c5925d215f31fda6d9d0bccea240591b22a3d0f6b5bf4ddf1243d71aca0fd53045c352c8c5497ebcdbd7ac11083d63aba7c053604fda2430c317a4e04702b5ad539e110f101165b21dcd9fdb5ba7324acdba6a506244ce7c911197dfe067441fe7488d164c050f45ef6476aaf399cedde1793cceb8c21d88ec8ecf5e17df27586713d7dd9566ec5023cfef75422b73e2d5a932c661b3cfdf9c4bda12b64380d2be1aa957c3e1416e068937bafe79b8cf303296792388e9c197702e11e7ded6088ae992d352b23a4a27
N= 0xdc77f076092cbe81c44789ccfc1b2ca55eabae65f44cf34382799e8bbb42d4d6c032bd897c21df1da401929d82deb56264823a757f6cacf63e0037146026cbab32ab9e4abc783dcabaac2b7ccc439937be3ab0fbf149524ff29ef0fe6f27e45215d74b40597c70e8207159dc7f542c2a6828500016480053dfc2d8dbf8fcdf6700640184c8f3318f7aab2e17e116edf680592f5eae951159bb8c20cfbd0cbab8b4b95925b5068038d0377a55a4d346ebbf53a1c2943b7c17e1b9d4a1b77916da2e15140b05b96655906942a07d04b7e25fa7521b3b7ae26eda68375a8b8ef2d5b4704a28168b236de97f24a663f0d0a3aeab47767dfe75a21662f5f25ef7f7d4b25c90fd7bcdd7137c23f03b6ea4209f8fb9b4628355e6ad62e6467d26666d3d1b0e6f078c5f3866413a6fcd3c1dc2ff3a5ab286e339d5c72f4d2f0473a4faddcba6b031bb6ec226fd4b319834b5029f09ea0ffeb5b6ed182d5a13675571b6708c38299118043390343e2f79edebd2ae0e0a765a3aebf776f54ca983cdae8547547cfc8430f7222aefa77301d7cc7c03b1451b6603028b21fea869d35138a9c83919985a91b3fdfa934f25a442cc10349b0ed6f2ee3955d40249e8b3fb9f1955534ee06cee41a3ad2d6ff7dbdb0f01e47b9e4d04f65232f5579135ae035e8ba2d1fe6465a730dcc8b9ba3a558ab38f040ea510757d25e92f886c50c24ad967f1
e=65537
#p,q=factor_smooth_p(N)
#toitent=(p-1)*(q-1)
#d=inverse(e,toitent)
#m=hex(pow(c,d,N))[2:]
p=45130782138821231634664822924606644347274161463663927387578931639175223286413378324882645031302403289842551326638702711998962760517679897418281467484531163375644705075213662848721478455926415639437965574871053673938130437463383431907231224801316309790287364751279984404056565040242248326224648040650860211493169850992812996172453840449200075853777085801648416876006333273306936825124410389797307488083056497244608773881660250930270420195391832629035158125925203262309579280388854014294622011159984832956422300816768157089660974628522818677622546453173413252374696944407138466146678080076210538578674319834619518810099
q=19929480903966971877741359978214832777067673186776101767607985415984872967131783702304729626331577711025830876686674170433788564223656884574965375895417512648538448454114165043668565344845361735967533803734325629433944151906019295203849389937041766109566748588937702389000280859653264841778232075227804461734481644568063879619171473653153879467534960561551793532641987408308262590477344407917566949561595540828562062207376467975716207562802834742657134267225310067273840884699549038482335638587159643505585791895934244621169372816478043004416985427985158346066496193091020702283948166437350554644511384320505926737291
m=0x3c1f23837cb4b3c6c08917e762184110fbdeb6b85a7552df0581ddb644671d820f77871b8082b67a588677dbeeb9b065c8be1b1bde1dd84751b045d4ba3104fcea4132b9d8009ab6a2f49f219ebb49388275d70318b6165d584f55fa75b075d5e5f4dcd87d1edd11047a157f9efa6d33235944b3c7ee8b8481e63789ad91821c73e3e59c54f906f46a39d860a9947a4ef44e5075cc994e62e997bad74468c9cf28cb4c724543266d07c34c2b404bacb174f200f8b699002b0dff07f050da89815e838b6c8a114d9ac2fe8c61b0bcc24c83f27d6f303b0be4506d2067696470ba342ba2436f06cff651fa7365eb6805414494b8fa9b267152fe33c5fae4c2e1d0
for i in range(p-1729,p):
    m=m*i%p
m=(-m)%p
print(long_to_bytes(m))
```

## Flag
> moectf{Charming_primes!_But_Sm0oth_p-1_1s_vu1nerab1e!}