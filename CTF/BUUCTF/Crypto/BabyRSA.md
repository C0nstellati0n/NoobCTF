# BabyRSA

[题目地址](https://buuoj.cn/challenges#[GUET-CTF2019]BabyRSA)

从数学废物进化成数学马后炮。

附件给了e，d，c，p+q和(p+1)(q+1)。做rsa题第一步一定要看有什么条件，缺了什么条件，这是帮助判断属于什么题型的关键步骤。根据rsa的解密过程，现在我们只少了n。看来要用e，p+q，(p+1)(q+1)中的东西构造出n。看了眼[wp](https://blog.csdn.net/qq_61774705/article/details/124674479)，我瞬间悟了。

(p+1)(q+1)=pq+p+q+1<br>
(p-1)(q-1)=pq-p-q+1<Br>
n=pq=(p+1)(q+1)+(p-1)(q-1)=[2(p+q+1)]/2-1

问题在于怎么找到(p-1)(q-1)。简单啊，(p-1)(q-1)=pq+p+q+1-2(p+q)=(p+1)(q+1)-2(p+q)。原理真的很简单，就是难以构造。不过对于打数竟的大佬们来说构造这玩意简直有手就行。以后遇到这种题多因式分解，多联想，比如从(p+1)(q+1)的因式分解结果联想到(p-1)(q-1)来构造n。

```python
from Crypto.Util.number import *
p_plus_q=0x1232fecb92adead91613e7d9ae5e36fe6bb765317d6ed38ad890b4073539a6231a6620584cea5730b5af83a3e80cf30141282c97be4400e33307573af6b25e2ea
p_plus_1_times_q_plus_1=0x5248becef1d925d45705a7302700d6a0ffe5877fddf9451a9c1181c4d82365806085fd86fbaab08b6fc66a967b2566d743c626547203b34ea3fdb1bc06dd3bb765fd8b919e3bd2cb15bc175c9498f9d9a0e216c2dde64d81255fa4c05a1ee619fc1fc505285a239e7bc655ec6605d9693078b800ee80931a7a0c84f33c851740
e = 0xe6b1bee47bd63f615c7d0a43c529d219
d =0x2dde7fbaed477f6d62838d55b0d0964868cf6efb2c282a5f13e6008ce7317a24cb57aec49ef0d738919f47cdcd9677cd52ac2293ec5938aa198f962678b5cd0da344453f521a69b2ac03647cdd8339f4e38cec452d54e60698833d67f9315c02ddaa4c79ebaa902c605d7bda32ce970541b2d9a17d62b52df813b2fb0c5ab1a5
c=0x50ae00623211ba6089ddfae21e204ab616f6c9d294e913550af3d66e85d0c0693ed53ed55c46d8cca1d7c2ad44839030df26b70f22a8567171a759b76fe5f07b3c5a6ec89117ed0a36c0950956b9cde880c575737f779143f921d745ac3bb0e379c05d9a3cc6bf0bea8aa91e4d5e752c7eb46b2e023edbc07d24a7c460a34a9a
phi=p_plus_1_times_q_plus_1-2*p_plus_q
n=(phi+p_plus_1_times_q_plus_1)//2-1
m=pow(c,d,n)
print(long_to_bytes(m))
```

### Flag
> flag{cc7490e-78ab-11e9-b422-8ba97e5da1fd}