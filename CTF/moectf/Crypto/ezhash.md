# ezhash

我已经对ez形成ptsd了，看见就头疼。

看源码。

```python
from hashlib import md5,sha256
from secret import flag
import socketserver
import random
import signal
import string 

msg = b'c4n_y0u_g1v3_m3_@_string_w1th_th3_same_h4sh_a5_th1s_m3ss4ge?1f_u_g1ve_m3_i_wi11_giv3_y$u_@_flag!'

def pad(m):
    return m + bytes([64-len(m)%64 for _ in range(64-len(m)%64)])

def F(x,y,z):#Don't get confused by magic bit operations! Take it easy!
    return (x * y * z) & 0xffffffffffffffffffffffffffffffff

def R(x,y,z,t):#wow, interesting!
    return (x ^ y ^ z ^ t ^ F(y,z,t) ^ F(z,t,x) ^ F(t,x,y)) & 0xffffffffffffffffffffffffffffffff

def hash(m:bytes) -> str:#Seems too complex? Take it easy!
    m = pad(m)
    H = b""
    for _ in range(len(m)//64):
        round_m = m[_*64:_*64+64]
        a,b,c,d =   int.from_bytes(round_m[:16],byteorder='little'),int.from_bytes(round_m[16:16*2],byteorder='little'),\
                    int.from_bytes(round_m[16*2:16*3],byteorder='little'),int.from_bytes(round_m[16*3:16*4],byteorder='little')
        tmpH = hex(R(a,b,c,d))[2:].rjust(8,'0').encode()
        H = md5(H + tmpH).hexdigest().encode()# Actually, How many iterations?
    return H.decode()

class Task(socketserver.BaseRequestHandler):
    #--------These are just the server's transceiver functions and are not important------
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b' '):
        self.send(prompt, newline=False)
        return self._recvall()
    #--------Above are just the server's transceiver functions and are not important------

    def proof_of_work(self):
        table = string.ascii_letters+string.digits
        proof = (''.join([random.choice(table)for _ in range(20)])).encode()
        sha = sha256(proof).hexdigest().encode()
        self.send(b"[+] sha256(XXXX+" + proof[4:] + b") == " + sha )
        XXXX = self.recv(prompt = b'[+] Plz Tell Me XXXX :')
        if len(XXXX) != 4 or sha256(XXXX + proof[4:]).hexdigest().encode() != sha:
            return False
        return True

    def handle(self):# main
        signal.alarm(300)#you have 300s to interactive

        self.send(b"Welcome to ezhash! You need to complete the Proof of work first!")
        proof = self.proof_of_work()
        if not proof:
            self.request.close()
        
        #get hash(msg1)
        Hash_nonce = hash(msg)
        self.send(b"Well done! Your challange is to find a collision of given hash.")
        self.send(b"message1 = "+msg)
        self.send(f"Hash(message1) = {Hash_nonce}".encode())

        #get hash(msg2)
        yourmsg=self.recv(b"Tell me message2 = ")
        your_hash=hash(yourmsg)
        self.send(f"Ok, Hash(message2) = {your_hash}".encode())

        if(msg!=yourmsg):#judge
            if(your_hash==Hash_nonce):
                self.send(f"Well done! your flag is {flag}".encode())
            else:
                self.send(b"Not Yet! Try again!")
        else:
            self.send(b"Same message! Try again!")


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10002
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    print(HOST, PORT)
    server.serve_forever()
```

服务器端代码就不用怎么分析了，只需要知道我们的任务有两个：sha256暴力破解和自制hash碰撞。sha256那个之前已经遇到过了，不说了，而这个哈希碰撞要死人的节奏。分析吧，怎么头疼也要看，已经好久没解出来一道题了。

```python
def hash(m:bytes) -> str:#Seems too complex? Take it easy!
    m = pad(m)
    H = b""
    for _ in range(len(m)//64):
        round_m = m[_*64:_*64+64]
        a,b,c,d =   int.from_bytes(round_m[:16],byteorder='little'),int.from_bytes(round_m[16:16*2],byteorder='little'),\
                    int.from_bytes(round_m[16*2:16*3],byteorder='little'),int.from_bytes(round_m[16*3:16*4],byteorder='little')
        tmpH = hex(R(a,b,c,d))[2:].rjust(8,'0').encode()
        H = md5(H + tmpH).hexdigest().encode()# Actually, How many iterations?
    return H.decode()
```

pad就是个填充函数,让m的长度是64的倍数。这个for循环的计数变量是_,从这点已经看出来与其他题的不同之处：阴间。看起来把m填充后每64个字符分成一组。

- ### int.from_bytes
  > 把bytes类型的参数转化为十进制整数

a,b,c,d每次循环的值都不同，但具体分别为m的前16位bytes转成的数字，m从16位到32位bytes转成的数字，m从32位到48位bytes转成的数字，m的后16位bytes转成的数字，都是小端。就是把m以64分割为两半后再把每一半以16作为分割都转成数字。

- ### rjust
  > 返回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串。
  - 语法：str.rjust(width[, fillchar])

比如一个字符串是'test'，'test'.rjust(10,'0')返回的结果就是'000000test'。那么tmpH的值就是R函数的返回值的16进制左边补0后转bytes的结果。H会在每次循环中累加，看了一下一共2次循环。继续。

```python
def R(x,y,z,t):#wow, interesting!
    return (x ^ y ^ z ^ t ^ F(y,z,t) ^ F(z,t,x) ^ F(t,x,y)) & 0xffffffffffffffffffffffffffffffff
```

一点也不interesting。按位与相同为1，不同为0。0xffffffffffffffffffffffffffffffff换成2进制就是一堆1，另一个操作数是1的还是1，是0的还是0，不会改变源操作数的值，除非源操作数转换成2进制后长度大于这串数字转成2进制的长度，才会改变源操作数，仅保留最后最多39位的数字。

这有啥分析的，不会，直接看F。

```python
def F(x,y,z):#Don't get confused by magic bit operations! Take it easy!
    return (x * y * z) & 0xffffffffffffffffffffffffffffffff
```

这根本不会像注释说的那样confused，唯一的问题是我怎么碰撞啊？这个函数x,y,z的顺序不重要，R函数x,y,z,t异或的顺序也不重要，唯一重要的是向F传的参数。我认为应该要在这两个函数上动手脚，使两个字符串经过这两个函数时的输出是一样的。否则后面调用md5就真的成了hash碰撞了，题目描述也告诉我们很难。

目前想到了两种思路。第一种让F函数的输出交换。比如原来字符串输出的是a,b,c，我们就让碰撞字符串经过F函数的输出错位对应，d的输出等于b，e的输出等于c，f的输出等于a，或者别的错位也行。第二种思路是让所有函数的结果最后39位相同，反正后面异或只会保留39位，更高位也没什么用。先看看第一种吧，第二种可能性超级小。

输出错位对应就要y,z,t值错位对应，比如碰撞字符d,e,f，e=y,f=z,d=t。让我想想怎么实验。

不对劲，我想错了，我以为x不会作为F的参数，没想到会。不是我怎么天天看错代码啊？而且我发现问题了，最多只能替换成功两个，无论怎么替换三个中一定有一个不符合。不会真要找什么高位吧？

这种级别的计算量肯定不是人类可以做到的。不过你还记得有道题教了我们怎么用z3吗？这不就是解个方程的事吗？所以隆重请出我们的z3！只需要把F和R函数作为约束条件，跑一会就可以出答案了。

```python
from z3 import *
def F(x,y,z):#Don't get confused by magic bit operations! Take it easy!
    return (x * y * z) & 0xffffffffffffffffffffffffffffffff
def R(x,y,z,t):#wow, interesting!
    return (x ^ y ^ z ^ t ^ F(y,z,t) ^ F(z,t,x) ^ F(t,x,y)) & 0xffffffffffffffffffffffffffffffff
x=126543685064601143072558889932495402083
y=138843953101822601405029160226257067840
z=154684798394979155560889998150189932339
t=156015016415975645921614901671550464360
to_x=BitVec("to_x",128)
to_y=BitVec("to_y",128)
to_z=BitVec("to_z",128)
to_t=BitVec("to_t",128)
sol=Solver()
sol.add(((x ^ y ^ z ^ t ^ F(y,z,t) ^ F(z,t,x) ^ F(t,x,y))& 0xffffffffffffffffffffffffffffffff)==((to_x ^ to_y ^ to_z ^ to_t ^ F(to_y,to_z,to_t) ^ F(to_z,to_t,to_x) ^ F(to_t,to_x,to_y))& 0xffffffffffffffffffffffffffffffff))
if sol.check():
    print(sol.model())
```

x,y,z,t是第一次循环中a,b,c,d的值，print一下就知道了。为什么只用算第一个循环呢？因为题目只要求字符串不能相同，没规定要有多不相同，所以只需要一半不相同就行了，后面不变的内容hash肯定不会变。也可以考虑前半部分一样后半部分不一样，这个我就没试过了，不知道行不行。使用BitVec是因为Int型在z3里不支持异或，只有这个可以。位数还是调试a,b,c,d得到，跟a,b,c,d一样位数就行了，我算的是128位（2进制）。

求出来的解转成byte可以得到下面这样的内容。

- b'\xfdA)~\xed\xa3\x13$\xe6\x8fkG\x0f\xde\x00\x02\xd1\x92\xbe?\xaf\xf5\x0f\x15\xb0\xc7W\x86\x16.L\x89\x84\xde"\xc7\x9c\x1e\x93\xcc\x1f\xe9\xdc\xa9\xd7\xa5C\x11\x9e\x10\xf3\xabXHgj\xad\xafp7\xfd\x88\xd7|_g1ve_m3_i_wi11_giv3_y$u_@_flag!'

要借助pwntools来发送byte。开始写exp。

```python
import itertools
import string
import hashlib
from pwn import *
def crack(key,sha256enc):
    code = ''
    strlist = itertools.product(string.ascii_letters + string.digits, repeat=4)
    for i in strlist:
        code = i[0] + i[1] + i[2]+i[3]
        temp=code+key
        encinfo = hashlib.sha256(temp.encode()).hexdigest().encode()
        if encinfo == sha256enc:
            return code

#这里是求出来的解
""" to_x = 2662959897027750434378848477463003645
to_z = 22948123502074977621032066796507815556
to_t = 165943393771503673761320420801734971550
to_y = 182499784759220575639686275323037389521 """

m=b'\xfdA)~\xed\xa3\x13$\xe6\x8fkG\x0f\xde\x00\x02\xd1\x92\xbe?\xaf\xf5\x0f\x15\xb0\xc7W\x86\x16.L\x89\x84\xde"\xc7\x9c\x1e\x93\xcc\x1f\xe9\xdc\xa9\xd7\xa5C\x11\x9e\x10\xf3\xabXHgj\xad\xafp7\xfd\x88\xd7|_g1ve_m3_i_wi11_giv3_y$u_@_flag!'
p=remote("polarnova.top",10002)
p.recvuntil(b'XXXX+')
d=p.recvline().split(b') == ')
key=str(d[0],encoding='utf-8')
sha256enc=d[1][:-1]
p.sendlineafter("[+] Plz Tell Me XXXX :",crack(key,sha256enc))
p.sendlineafter("Tell me message2 = ",m)
print(p.recvall())
```

运行一会即可得到flag。不过我看flag提到的ARX我根本就不知道，可能这道题出题人想的解法不是这个，被我误打误撞找到捷径了。

- ### Flag
  > moectf{w0w!U_f1nd_@_c0l1isi0n!U_2_th3_m4ster_of_ARX!}