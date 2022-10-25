# ezTea

看起来确实不难，问题在于我不会c语言啊，而且是那种模模糊糊的读完全不能写的不会。

```c
#include <stdio.h>
#include <stdint.h>

void encrypt (uint32_t* v, uint32_t* k) {                       // 主要加密函数，试着搞定它
    uint32_t v0 = v[0], v1 = v[1], sum = 0;
    uint32_t delta = 0xd33b470;
    for (int i = 0; i < 32; i++) {
        sum += delta;
        v0 += ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]);
        v1 += ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]);
    }
    v[0] = v0;
    v[1] = v1;
}
int main() {
    uint32_t k[4] = {1, 2, 3, 4};
    int8_t input[33] = {0};
    scanf("%32s", input);
    for (int i = 0; i < 32; i+=8) {
        uint32_t v[2] = {*(uint32_t *)&input[i], *(uint32_t *)&input[i+4]};
        encrypt(v, k);
        for (int j = 0; j < 2; j++) {                           // 这一段主要是把 v 按单字节输出，另外可以了解一下 “大小端序” 在这题是如何体现的
            for (int k = 0; k < 4; k++) {
                printf("%#x, ", v[j] & 0xff);
                v[j] >>= 8;
            }
        }
    }
    return 0;
}
```

TEA算法确实很容易搜到，解密脚本也是。关键我很容易理解了解密脚本，main函数的操作反而看了几个小时看不懂。随便拉个网上的脚本过来。

```c
void decrypt (uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up; sum is 32*delta */
    uint32_t delta=0x9E3779B9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}
```

肯定要先读懂加密函数才能读懂解密函数。

```c
void encrypt (uint32_t* v, uint32_t* k) {                       // 主要加密函数，试着搞定它
    uint32_t v0 = v[0], v1 = v[1], sum = 0;
    uint32_t delta = 0xd33b470;
    for (int i = 0; i < 32; i++) {
        sum += delta;
        v0 += ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]);
        v1 += ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]);
    }
    v[0] = v0;
    v[1] = v1;
}
```

其实挺直白的，v0和v1分别为参数v数组的第一个和第二个元素，循环32次，sum从0开始，每次循环加上0xd33b470。v0 += ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]) 这段有点绕，不过逆向可以将其分成两部分来看：v0+=x，其中x是那一串指令。所以逆向这段根本不用考虑什么位移异或等小操作的逆向，直接整体相减就得了。注意v0的加密依靠明文的v1，但v1的加密需要密文的v0，因此逆向需要先解密v1，再v0，正好符合加密时的操作。sum也从32次循环后的和开始，每次减去delta。

理论上只要找出传入的参数，然后用相同的步骤应该就能解密了。问题在于我读不懂uint32_t v[2] = {\*(uint32_t \*)&input[i], \*(uint32_t \*)&input[i+4]}这段代码，(uint32_t \*)&input[i]是找到input在i索引位置的值并取地址，转换为(uint32_t \*)也不会有什么变化。可是\*(uint32_t \*)&input[i]的结果是uint32_t我就摸不着头脑了，调试发现也和地址没关系。我本来想着那就直接用main函数吧，就把scanf注释掉然后把input换成描述里的cipher。但是当我把decrypt里面的sum换成0xd33b470的32倍后，它整形溢出了！我忘了这是c语言，不像python一样怎么造都不会溢出。

难道必须自己用python写出解密脚本？我肯定不会，问下大佬，得知了main函数是如何运行的。

```c
int main() {
    uint32_t k[4] = {1, 2, 3, 4};
    int8_t input[33] = {0};
    scanf("%32s", input);
    for (int i = 0; i < 32; i+=8) {
        uint32_t v[2] = {*(uint32_t *)&input[i], *(uint32_t *)&input[i+4]};
        encrypt(v, k);
        for (int j = 0; j < 2; j++) {                           // 这一段主要是把 v 按单字节输出，另外可以了解一下 “大小端序” 在这题是如何体现的
            for (int k = 0; k < 4; k++) {
                printf("%#x, ", v[j] & 0xff);
                v[j] >>= 8;
            }
        }
    }
    return 0;
}
```

前面不用多说，从第一个for循环开始。\*(uint32_t \*)&input[i] 取input[i]元素所在的地址，强制转换为(uint32_t \*)类型指针，然后\*符号取这个指针指向的值。我在[这篇文章](https://blog.csdn.net/nvd11/article/details/8749388)里懂了这段代码的逻辑。首先，(uint32_t \*)类型的指针指向的是uint32_t类型的值，但不代表(uint32_t \*)长度等同于uint32_t。所有类型的指针长度都是一样的，都只能放一个地址，也就是其指向存储块的首地址，然后根据指针的类型决定从这个首地址往后取多长。比如这里uint32_t类型占8个字节，那么(uint32_t \*)指针会指向存储uint32_t类型的连续存储单元的第一个字节，取值就是往后取8个。因此\*(uint32_t \*)&input[i]取的实际上是4个字符。比如input[4]={1,2,3,4}，那么这一串内容取到的值就是0x04030201(在我本机上实验是这样，我应该是小端)。

encrypt懂了直接跳过。第二个for循环遍历v数组的每一个元素，第三个for循环对于每一个元素分别取字节，可以看[这里](https://blog.csdn.net/zhengnianli/article/details/111189379)。&0xff获取后8位，>>8就是从第9位重复以上步骤。

搞笑的事情发生了：似乎我已经完全理解整个程序，但是我仍然无法写出解密脚本，借鉴了网上现成的python tea解密脚本也不行。问题就在于我不知道如何逆向给出的输出结果：

- 0x17, 0x65, 0x54, 0x89, 0xed, 0x65, 0x46, 0x32, 0x3d，0x58, 0xa9, 0xfd, 0xe2, 0x5e,
0x61, 0x97, 0xe4, 0x60, 0xf1, 0x91, 0x73, 0xe9, 0xe9, 0xa2, 0x59, 0xcb, 0x9a, 0x99,
0xec, 0xb1, 0xe1, 0x7d

用简单一点的情景模拟一下过程。input[9]={1,2,3,4,5,6,7,8,0}，v[2]={0x04030201,0x08070605},encrypt过程跳过，假设就按照原文输出。那么for循环输出内容应该是0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8。与明文两两对应，尝试把加密放进去试试。不过把原加密算法的delta改小一点，方便下一步模拟解密过程。相同数据加密后得到0xdc, 0x1e, 0xc0, 0x63, 0x70, 0x49, 0xa8, 0x94。尝试解密。

注意到解密需要的数据端序不一样。比如需要的第一个密文数据为0x63c01edc。不是我之前也是这么想的为什么不行？难道是因为我用脚本帮我拼数据然后莫名其妙就不行了？得那我这次自己手动改端序。

啊哈，这次成了。敢情这道题的难点在于换端序(･･;)

```python
"""void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up */
    uint32_t delta=0x9e3779b9;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}"""
from ctypes import *
def decrypt(v, k):
    v0, v1 = c_uint32(v[0]), c_uint32(v[1])
    delta = 0xd33b470
    k0, k1, k2, k3 = k[0], k[1], k[2], k[3]
    total = c_uint32(delta * 32)
    for i in range(32):                       
        v1.value -= ((v0.value<<4) + k2) ^ (v0.value + total.value) ^ ((v0.value>>5) + k3) 
        v0.value -= ((v1.value<<4) + k0) ^ (v1.value + total.value) ^ ((v1.value>>5) + k1)  
        total.value -= delta
    return [v0.value, v1.value]   
k=[1,2,3,4]
cipher=[[0x89546517,0x324665ed],[0xfda9583d,0x97615ee2],[0x91f160e4,0xa2e9e973],[0x999acb59,0x7de1b1ec]]
for i in range(len(cipher)):
    res=decrypt(cipher[i],k)
    for j in range(2):
        for z in range(4):
            print(chr(res[j]&0xff),end='')
            res[j]>>=8
```

恭喜这个菜狗在python水平垃圾,c语言连水平都没有的情况下靠着大佬的脚本和自己的苦力完成这道题。

- ### Flag
  > moectf{Th3_TEA_!S_s0_t4s7y~~!!!}