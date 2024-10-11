# xor(大嘘)

动调发现在xor加密函数的ret处没有正常返回，而是继续往下走了。ghidra里如果点击这段汇编，会出现一个灰色的伪代码，不太好懂但至少比汇编好。binary ninja更厉害，直接就出来了全部内容（好像稍微有点偏差，关于delta的值和类型什么的）。能看出是个tea加上别的一些xor内容。因此整个加密流程是xor+tea+xor
```c
#include <stdio.h>
#include <stdint.h>
void encrypt(uint32_t* v, uint32_t* k) {
    uint32_t v0 = v[0], v1 = v[1], sum = 0, i;
    uint32_t delta = 0x9e3779b9;
    uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];
    for (i = 0; i < 32; i++) {
        sum += delta;
        v1 += ((v0 << 4) + k0) ^ (v0 + sum) ^ ((v0 >> 5) + k1); //这块和普通tea的实现反过来了
        v0 += ((v1 << 4) + k2) ^ (v1 + sum) ^ ((v1 >> 5) + k3);
    }
    v[0] = v0; v[1] = v1;
}
void decrypt(uint32_t* v, uint32_t* k) {
    uint32_t delta = 0x9e3779b9;
    uint32_t v0 = v[0], v1 = v[1], sum = delta*32, i;
    uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];
    for (i = 0; i < 32; i++) {
        v0 -= ((v1 << 4) + k2) ^ (v1 + sum) ^ ((v1 >> 5) + k3);
        v1 -= ((v0 << 4) + k0) ^ (v0 + sum) ^ ((v0 >> 5) + k1);
        sum -= delta;
    }
    v[0] = v0; v[1] = v1;
}

int main()
{
    int32_t k[4] = {0x6c6c6568,0x6f6d5f6f,0x66746365,0x34323032}; //注意端序。我直接手动转了
    uint32_t cipher[8] = {0x9a831a78,0x5e87ff17,0x00c52f51,0x56c8707a,0xc7c31e09,0x08bc7393,0xddcf1d26,0xb1efa477};
    uint32_t v[2]={0,0};
    for(int i=0;i<8;i+=2){
        v[i%2]=cipher[i];
        v[i%2+1]=cipher[i+1];
        decrypt(v,k);
        printf("%x\n%x\n\n",v[0],v[1]);
    }
    return 0;
}
```
偷懒拿cyberchef做异或： https://gchq.github.io/CyberChef/#recipe=From_Hex('None')Swap_endianness('Raw',4,true)XOR(%7B'option':'UTF8','string':'hello_moectf2024'%7D,'Standard',false)&input=MGYwOTBhMDUwNzE2MzkxYjA3MmIxNDBhNTU1NzZmNWMwNjMzMWMxYjMwMDYzMTFhMzkxMDBkMDQ0OTUzNTU0Ng
