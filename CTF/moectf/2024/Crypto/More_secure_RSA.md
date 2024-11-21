# More_secure_RSA

笑死我了，三年了，仍然不知道这道题的原理是什么……想了很久没头绪，3个质数的rsa就给我其中一个质数没用啊。但注意到每个质数都有1024位，题目里flag看起来又很短，于是想到了前年的题： https://github.com/C0nstellati0n/NoobCTF/blob/main/CTF/moectf/2022/Crypto/signin.md 。成了。想了好几天都没想出来，今天看游戏实况，看着看着就灵光一闪。太抽象了

```py
from Crypto.Util.number import *
from sympy.ntheory.residue_ntheory import nthroot_mod
e = 0x10001
n = 16760451201391024696418913179234861888113832949815649025201341186309388740780898642590379902259593220641452627925947802309781199156988046583854929589247527084026680464342103254634748964055033978328252761138909542146887482496813497896976832003216423447393810177016885992747522928136591835072195940398326424124029565251687167288485208146954678847038593953469848332815562187712001459140478020493313651426887636649268670397448218362549694265319848881027371779537447178555467759075683890711378208297971106626715743420508210599451447691532788685271412002723151323393995544873109062325826624960729007816102008198301645376867
C = 1227033973455439811038965425016278272592822512256148222404772464092642222302372689559402052996223110030680007093325025949747279355588869610656002059632685923872583886766517117583919384724629204452792737574445503481745695471566288752636639781636328540996436873887919128841538555313423836184797745537334236330889208413647074397092468650216303253820651869085588312638684722811238160039030594617522353067149762052873350299600889103069287265886917090425220904041840138118263873905802974197870859876987498993203027783705816687972808545961406313020500064095748870911561417904189058228917692021384088878397661756664374001122513267695267328164638124063984860445614300596622724681078873949436838102653185753255893379061574117715898417467680511056057317389854185497208849779847977169612242457941087161796645858881075586042016211743804958051233958262543770583176092221108309442538853893897999632683991081144231262128099816782478630830512
N = 1582486998399823540384313363363200260039711250093373548450892400684356890467422451159815746483347199068277830442685312502502514973605405506156013209395631708510855837597653498237290013890476973370263029834010665311042146273467094659451409034794827522542915103958741659248650774670557720668659089460310790788084368196624348469099001192897822358856214600885522908210687134137858300443670196386746010492684253036113022895437366747816728740885167967611021884779088402351311559013670949736441410139393856449468509407623330301946032314939458008738468741010360957434872591481558393042769373898724673597908686260890901656655294366875485821714239821243979564573095617073080807533166477233759321906588148907331569823186970816432053078415316559827307902239918504432915818595223579467402557885923581022810437311450172587275470923899187494633883841322542969792396699601487817033616266657366148353065324836976610554682254923012474470450197
r=N//n
print(long_to_bytes(nthroot_mod(C,e,r)))
```
好像不是预期解？预期解见 https://github.com/XDSEC/MoeCTF_2024/blob/main/Official_Writeup/Crypto/MoeCTF2024%20Crypto%20Writeup.md