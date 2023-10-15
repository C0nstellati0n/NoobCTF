# flag_exchange

题目的加密形式是diffie_hellman。由于p可自由选择，选择smooth prime即可用sagemath discrete_log算出private key（smooth prime算离散对数比较快，普通质数则非常慢。这也是diffie_hellman安全性的前提）
```py
#g^x = s mod p, find x
#在sagemath里运行
g=7
s= #alice_pub_key 
p = #和下面同样的smooth prime
Fp = IntegerModRing(p) 
g_modp = Fp(g) 
s_modp = Fp(s)
x = discrete_log(s_modp, g_modp)
print(x)

#拿到离散对数后再运行：
from Crypto.Util.number import *
from gmpy2 import *
import os
def get_prime(state, bits):
    return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))
#https://ctftime.org/writeup/32914
def get_smooth_prime(state, bits, smoothness=16):
    p = mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor
    bitcnt = (bits - p.bit_length()) // 2
    while True:
        prime1 = get_prime(state, bitcnt)
        prime2 = get_prime(state, bitcnt)
        tmpp = p * prime1 * prime2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if is_prime(tmpp + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p = tmpp + 1
            break
    p_factors.sort()
    return (p, p_factors)
SEED  = bytes_to_long(os.urandom(32))
STATE = random_state(SEED)
print(get_smooth_prime(STATE, 1024, 16)) #在这里拿到smooth prime然后提交给服务器
alice_privKey= #这就是上面sagemath拿到的离散对数x
p = #生成的smooth prime
#下面都是服务器给的
alice_pub_key=
bob_pubKey=
Ciphertext=
superkey = pow(bob_pubKey, alice_privKey, p)
d=inverse(superkey,p)
print(long_to_bytes((Ciphertext*d)%p))
```