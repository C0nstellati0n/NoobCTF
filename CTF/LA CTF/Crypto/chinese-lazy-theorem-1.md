# chinese-lazy-theorem-1

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/crypto/chinese-lazy-theorem-1)

```python
#!/usr/local/bin/python3

from Crypto.Util.number import getPrime
from Crypto.Random.random import randint

p = getPrime(512)
q = getPrime(512)
n = p*q

target = randint(1, n)

used_oracle = False

print(p)
print(q)

print("To quote Pete Bancini, \"I'm tired.\"")
print("I'll answer one modulus question, that's it.")
while True:
    print("What do you want?")
    print("1: Ask for a modulus")
    print("2: Guess my number")
    print("3: Exit")
    response = input(">> ")

    if response == "1":
        if used_oracle:
            print("too lazy")
            print()
        else:
            modulus = input("Type your modulus here: ")
            modulus = int(modulus)
            if modulus <= 0:
                print("something positive pls")
                print()
            else:
                used_oracle = True
                print(target%modulus)
                print()
    elif response == "2":
        guess = input("Type your guess here: ")
        if int(guess) == target:
            with open("flag.txt", "r") as f:
                print(f.readline())
        else:
            print("nope")
        exit()
    else:
        print("bye")
        exit()
```

The server will give us p and q, our goal is to guess a random number "target" that $1\geq target\leq n$ . We have three choices, 1 for getting a result of "target % modulus"; 2 for guessing numbers, 3 for quitting. It's not hard to see that if the modulus we input is greater than n, "target % modulus" will be the target itself.

```python
from pwn import *
p=remote("lac.tf",31110)
r=int(p.recvline(keepends=False))
q=int(p.recvline(keepends=False))
p.sendlineafter(">> ",'1')
p.sendlineafter("here: ",str(r*q))
target=int(p.recvline(keepends=False))
p.sendlineafter(">> ",'2')
p.sendlineafter("here: ",str(target))
print(p.recvline(keepends=False))
```

## Flag
> lactf{too_lazy_to_bound_the_modulus}