# Easy-one

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4dbda34c-13fc-49da-b65f-9500b56c5e34_2)

我不再读错题的那天就是我突破瓶颈之日。

附件给了4个文件，一组明文和密文，一个要破解的密文，一个源代码。

```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
	if (argc != 3) {
		printf("USAGE: %s INPUT OUTPUT\n", argv[0]);
		return 0;
	}
	FILE* input  = fopen(argv[1], "rb");
	FILE* output = fopen(argv[2], "wb");
	if (!input || !output) {
		printf("Error\n");
		return 0;
	}
	char k[] = "CENSORED";
	char c, p, t = 0;
	int i = 0;
	while ((p = fgetc(input)) != EOF) {
		c = (p + (k[i % strlen(k)] ^ t) + i*i) & 0xff;
		t = p;
		i++;
		fputc(c, output);
	}
	return 0;
}
```

天真且不读题的我懵了好一会。看起来是异或，key也给了，那给我msg001和msg001.enc干啥呢？尝试直接用key逆向逻辑解密，无果。查了才知道key不是CENSORED，这表示出题人把key隐藏掉了的意思。没办法英文不好来做ctf就是这个结果。

这种情况下msg001就有用了。已知明文和其对应的密文，我们可以直接爆破key。逆向逻辑有一个法则：能逆就逆，不逆拉倒。意思就是明显有逆运算的符号逆过来，比如+逆成-，*逆成//等。像&，赋值这类操作暂时看不出来可以先保留，如果无脑逆向不行再分析加密过程调整逆向的方法。比如这里+明显可以逆成-号，先逆了。至于%，遍历文件内容，t=p这类一下子看不出来是啥的就先不管。于是你就可以发现这次我们运气很好，直接秒杀逆向逻辑。

```python
from string import ascii_letters
with open("./msg001",'rb') as f:
    msg=f.read()
with open("./msg001.enc",'rb') as f:
    cipher=f.read()
with open("./msg002.enc",'rb') as f:
    flag_cipher=f.read()
def encrypt(char,t,k):
    return (char + (k ^ t) + i*i) & 0xff
def decrypt(cipher,t,k):
    return (cipher - (ord(k[i % len(k)]) ^ t) - i*i) & 0xff
letters=ascii_letters
t=0
key=''
for i in range(len(msg)):
    char=msg[i]
    c=cipher[i]
    for letter in letters:
        temp=encrypt(char,t,ord(letter))
        if temp==c:
            key+=letter
            t=char
            break
t=0
key=key[:-2]
for i in range(len(flag_cipher)):
    result=decrypt(flag_cipher[i],t,key)
    t=result
    print(chr(result),end='')
```

key=key[:-2]是因为爆破出来的key最后两位和前面重复了。另外代码很垃圾不要介意，我也不知道我怎么写出来这个鬼东西的。

- ### Flag
  > CTF{6d5eba48508efb13dc87220879306619}