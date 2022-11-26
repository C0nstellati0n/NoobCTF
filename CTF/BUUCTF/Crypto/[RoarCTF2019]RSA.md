# [RoarCTF2019]RSA

[题目地址](https://buuoj.cn/challenges#[RoarCTF2019]RSA)

打ctf的同时还能做数学题，不得给参赛者乐疯了？

```
A=(((y%x)**5)%(x%y))**2019+y**316+(y+1)/x
p=next_prime(z*x*y)
q=next_prime(z)
A =  2683349182678714524247469512793476009861014781004924905484127480308161377768192868061561886577048646432382128960881487463427414176114486885830693959404989743229103516924432512724195654425703453612710310587164417035878308390676612592848750287387318129424195208623440294647817367740878211949147526287091298307480502897462279102572556822231669438279317474828479089719046386411971105448723910594710418093977044179949800373224354729179833393219827789389078869290217569511230868967647963089430594258815146362187250855166897553056073744582946148472068334167445499314471518357535261186318756327890016183228412253724
n =  117930806043507374325982291823027285148807239117987369609583515353889814856088099671454394340816761242974462268435911765045576377767711593100416932019831889059333166946263184861287975722954992219766493089630810876984781113645362450398009234556085330943125568377741065242183073882558834603430862598066786475299918395341014877416901185392905676043795425126968745185649565106322336954427505104906770493155723995382318346714944184577894150229037758434597242564815299174950147754426950251419204917376517360505024549691723683358170823416757973059354784142601436519500811159036795034676360028928301979780528294114933347127
c =  41971850275428383625653350824107291609587853887037624239544762751558838294718672159979929266922528917912189124713273673948051464226519605803745171340724343705832198554680196798623263806617998072496026019940476324971696928551159371970207365741517064295956376809297272541800647747885170905737868568000101029143923792003486793278197051326716680212726111099439262589341050943913401067673851885114314709706016622157285023272496793595281054074260451116213815934843317894898883215362289599366101018081513215120728297131352439066930452281829446586562062242527329672575620261776042653626411730955819001674118193293313612128

```

分析一下，看来是要从A中找出z，x和y。立刻放弃，看了[wp](https://aidaip.github.io/ctf/2019/10/13/RoarCTF2019-Writeup.html)后再次体会到数学的神奇。知道答案后也不难，然而不看答案前就是不会（看了也只能会一半）。

根据A的位数可以知道，A小于 $2^{2019}$ 。那么A表达式前面那一堆就能去除了，因为A本身小于2019，`(((y%x)**5)%(x%y))**2019`这堆东西中的`(((y%x)**5)%(x%y))`只能小于2。大佬说就是1，虽然我不知道怎么看出来的。把前面去掉后还剩下`y**316+(y+1)/x`。根据这个式子可以得到，如果A减去`(y+1)/x+1`，统称某个数i，就可以开316次方了。i大不到哪里去，爆破得到i值，同时就能得到a和b了。

```python
import gmpy2
for i in range(0xfffff):
	if i % 100000 == 0:
		print(i)
	if gmpy2.iroot(A-i,316)[1]==True:
		print(i)
		print(gmpy2.iroot(A-i,316)[0])
		break
```

ab为166，然后是z。根据sympy的next_prime实现，有next_prime(z)-z<10000。所以p<10000+166z,q<10000+z。让p=a+166z,q=b+z，n=pq=(a+166z)(b+z)。那么a和b都在10000以内，爆破a和b,当有整数解时解出z。

```python
for a in range(0,10000):
	if a % 1000 == 0:
		print(a)
	for b in range(0,10000):
		fuck = (166*b+a)**2 - 4*166*(a*b-n)
		if gmpy2.iroot(fuck,2)[1]==True:
			x = gmpy2.iroot(fuck,2)[0]-(166*b+a)
			print(gmpy2.gcd(x,166))
			if x%(166*2) == 0:
				print(gmpy2.iroot(fuck,2))
				print(a,b)
				print(x//(166*2))
```

说实话我完全没看懂怎么做的。我跟不上大佬的思路。最后解密出flag。不过这题其实有更简单的做法，直接factordb分解n就出来p和q了，估计是谁比赛后把分解结果传上去了。

## Flag
> flag{wm-l1l1ll1l1l1l111ll}