# chinese-lazy-theorem-2

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/crypto/chinese-lazy-theorem-2)

```python
#!/usr/local/bin/python3

from Crypto.Util.number import getPrime
from Crypto.Random.random import randint

p = getPrime(512)
q = getPrime(512)
n = p*q*2*3*5

target = randint(1, n)

oracle_uses = 0

print(p)
print(q)

print("This time I'll answer 2 modulus questions and give you 30 guesses.")
while True:
    print("What do you want?")
    print("1: Ask for a modulus")
    print("2: Guess my number")
    print("3: Exit")
    response = input(">> ")

    if response == "1":
        if oracle_uses == 2:
            print("too lazy")
            print()
        else:
            modulus = input("Type your modulus here: ")
            modulus = int(modulus)
            if modulus <= 0:
                print("something positive pls")
                print()
            elif modulus > max(p, q):
                print("something smaller pls")
                print()
            else:
                oracle_uses += 1
                print(target%modulus)
                print()
    elif response == "2":
        for _ in range(30):
            guess = input("Type your guess here: ")
            if int(guess) == target:
                with open("flag.txt", "r") as f:
                    print(f.readline())
                    exit()
            else:
                print("nope")
        exit()
    else:
        print("bye")
        exit()
```

We need to guess the target number agian. This time, $1\geq target\leq n$ , which n = p\*q\*2\*3\*5. We can only input a modulus that is less or equal to max(p,q). It means we can't just get the target like `chinese-lazy-theorem-2`. We now have the system of simultaneous congruences like this:

$res_1=target\bmod m_1$<br>
$res_2=target\bmod m_2$

The [CRT](http://ramanujan.math.trinity.edu/rdaileda/teach/s18/m3341/CRT.pdf) can solve this easily when $gcd(m_1,m_2)=1$ . The module sympy has the crt function; we can just use it easily.

```python
from sympy.ntheory.modular import crt
from pwn import *
context.log_level='debug'
p=remote("lac.tf",31111)
r=int(p.recvline()[:-1])
q=int(p.recvline()[:-1])
n=r*q*2*3*5
p.sendlineafter(">>",'1')
p.sendlineafter("here:",str(r))
mr=int(p.recvuntil('\n',drop=True))
p.sendlineafter(">>",'1')
p.sendlineafter("here:",str(q))
mq=int(p.recvuntil('\n',drop=True))
res=crt([r,q],[mr,mq])[0] #For function crt, the first parameter is a list that contains all the modules, and the second parameter is a list that contains all the residues that correspond to the modules.
temp=res
p.sendlineafter(">>",'2')
isChanged=False
for i in range(30):
    #res is one possible solution of target; the target may not be res. If we get one solution of the system of simultaneous congruences, solution+k*qr or solution-k*qr can also be a solution.
	p.sendlineafter("here:",str(temp))
	if temp+q*r<n and not isChanged:
		temp+=q*r
	elif temp+q*r>=n:
		temp=res
		isChanged=True
	if isChanged:
		temp-=q*r
```

## Flag
> lactf{n0t_$o_l@a@AzY_aNYm0Re}