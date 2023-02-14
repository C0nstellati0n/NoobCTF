# ravin-cryptosystem

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/crypto/ravin-cryptosystem)

The rabin.py file looks like just a normal [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), but with a small n.

```python
from Crypto.Util import number

def fastpow(b, p, mod):
    # idk this is like repeated squaring or something i heard it makes pow faster
    a = 1
    while p:
        p >>= 1
        b = (b*b)%mod
        if p&1:
            a = (a*b)%mod
    return a

p = number.getPrime(100)
q = number.getPrime(100)
n = p*q
e = 65537
m = int.from_bytes(open("flag.txt", "r").readline().strip().encode(), 'big')
assert(m < n)
c = fastpow(m, e, n)

print("n =", n)
print("e =", e)
print("c =", c)
```

output.txt gives us n, e, and c.

```
n = 996905207436360486995498787817606430974884117659908727125853
e = 65537
c = 375444934674551374382922129125976726571564022585495344128269
```

Go to [factordb](http://www.factordb.com/index.php?query=996905207436360486995498787817606430974884117659908727125853). We get the p and q. Are we done? No. Look carefully at the "fastpow" function used by the author; it seems like something is wrong? Search for the right implementation for fastpow.

```python
def right_fastpow(b,p,mod):
    a = 1
    while p:
        if p&1:
            a = (a*b)%mod
        b = (b*b)%mod
        p >>= 1
    return a
def fastpow(b, p, mod):
    # idk this is like repeated squaring or something i heard it makes pow faster
    a = 1
    while p:
        p >>= 1
        b = (b*b)%mod
        if p&1:
            a = (a*b)%mod
    return a
```

What's their difference? Well, it should be "if statement" -> "change the value of b" -> "bit shift", but now it's backwards. What will happen? Look at my test codes.

```python
def fastpow(b, p, mod):
    index=1
    # idk this is like repeated squaring or something i heard it makes pow faster
    a = 1
    while p:
        p >>= 1
        b = (b*b)%mod
        print(bin(p))
        if p&1:
            a = (a*b)%mod
            print('yes')
        index+=1
        print(f"fastpow_a:{a}")
        print(f"fastpow_b:{b}")
    return a
def test(b,p,mod):
    a = 1
    index=1
    print(bin(p))
    while p:
        if p&1:
            a = (a*b)%mod
            print("yes")
        b = (b*b)%mod
        p >>= 1
        index+=1
        print(f"test_a:{a}")
        print(f"test_b:{b}")
    return a
p=861346721469213227608792923571
q=1157379696919172022755244871343
n=p*q
res1=fastpow(239843894,65537,n)
res2=test(239843894,65537,n)
print(res1,res2)
```

The test function is the right implementation of "fastpow". During the process of calculation, it enters the if statement twice, but the fastpow function that the author uses only enters once. That's because the fastpow function performs a bit shift at the beginning, before the if statement. So it just loses one bit; it's actually powing 32768(0b1000000000000000).

We change the power of the test function to 32768. It still doesn't produce the same result as fastpow. Maybe we should think more about the algorithm itself. I found an [explaination](https://www.youtube.com/watch?v=ne0gHR57qUU&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=15) of the fastpow. I will show an example to demonstrate it briefly. If we want to calculate $2^{13}$ ,we can do the following:

```
x  13       2    * (2 to the power of 1)
   6        4      (2 to the power of 2)
x  3       16    * (2 to the power of 4)
x  1      256    * (2 to the power of 8)
   0    2*16*256=8192
```

We divide 13 by 2 every time, which is a way to write 13 as a binary. Mark every place where "1" lies, and multiply all the numbers that are marked, then we get the result. If we want to do a pow mod, just mod every power with the modulus.

Get back to the function. We can see the if statement as "marking 1", b is the power. Now we see the key point. Let's say the first bit of e is marked, so we want to multiply a by b. Since it's the first bit, b should be the base number itself, but the fastpow function has already multiplied b itself. Current b value doesn't correspond to current bit; instead it corresponds to next bit.

We know the fastpow function only enters the if statement once, the last bit. The b value it multiplies doesn't correspond to the last bit, but the next bit of the last bit. Modify e as the following:

```python
def fastpow(b, p, mod):
    index=1
    # idk this is like repeated squaring or something i heard it makes pow faster
    a = 1
    while p:
        p >>= 1
        b = (b*b)%mod
        print(bin(p))
        if p&1:
            a = (a*b)%mod
            print('yes')
        index+=1
        print(f"fastpow_a:{a}")
        print(f"fastpow_b:{b}")
    return a
def test(b,p,mod):
    a = 1
    index=1
    print(bin(p))
    while p:
        if p&1:
            a = (a*b)%mod
            print("yes")
        b = (b*b)%mod
        p >>= 1
        index+=1
        print(f"test_a:{a}")
        print(f"test_b:{b}")
    return a
p=861346721469213227608792923571
q=1157379696919172022755244871343
n=p*q
res1=fastpow(239843894,65537,n)
res2=test(239843894,0b10000000000000000,n)
print(res1,res2)
print(bin(65537))
print(bin(0b10000000000000000))
```

Now we get the same result. So the e-exponent is actually 65536(0b10000000000000000), rather than 65537. Here comes the next problem: when we do "GCD(e,(p-1)*(q-1))" , it gives us 4. They are not co-prime! If e and phi of n are not co-prime, we can't decrypt it easily. I searched for "ravin-cryptosystem" to see if there's actually such a cryptosystem. There's not, but I find this: [Rabin_cryptosystem](https://en.wikipedia.org/wiki/Rabin_cryptosystem).

It says "Choose two large distinct prime numbers p and q such that $p\equiv 3\bmod {4}$ and $q\equiv 3\bmod {4}$ ". Check our p and q, they do satisfy this. But the e-exponent in Rabin_cryptosystem is 2. We have 65536.

Wait, 65536 is the multiple of 2, right? We can write the following formula:

$c\equiv m^{e}\bmod {n}$

Divide e by 2:

$c\equiv (m^{e//2})^2\bmod {n}$

If we see $m^{e//2}$ as the plaintext, we can apply Rabin_cryptosystem to solve for it. After we get the result, e//2 can still divide by 2. Repeat doing this, in the end we can get the real m.

```python
from Crypto.Util.number import *
p=861346721469213227608792923571
q=1157379696919172022755244871343
n = 996905207436360486995498787817606430974884117659908727125853
e = 65537
c = 375444934674551374382922129125976726571564022585495344128269
def decrypt(c,p,q,n):
    c_p = pow(c,(p+1)//4,p)
    c_q = pow(c,(q+1)//4,q)
    a = inverse(p,q)
    b = inverse(q,p)
    x = (b*q*c_p+a*p*c_q)%n
    y = (b*q*c_p-a*p*c_q)%n
    res1=x%n
    res2=(-x)%n
    res3=y%n
    res4=(-y)%n
    res=[res1,res2,res3,res4]
    for i in res:
        if b'lactf' in long_to_bytes(i):
            print(long_to_bytes(i))
            return
        decrypt(i,p,q,n)
decrypt(c,p,q,n)
```

It will give us a Traceback, but it doesn't matter, we get the flag.

## Flag
> lactf{g@rbl3d_r6v1ng5}