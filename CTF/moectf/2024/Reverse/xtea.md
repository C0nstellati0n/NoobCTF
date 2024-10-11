# xtea

```c++
#include <stdio.h>
#include <stdint.h>
void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], delta=0xccffbbbb;
    uint32_t sum=(delta*num_rounds);
    for (i=0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[((sum >> 0xb) & 3)]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[(sum & 3)]);
    }
    v[0]=v0; v[1]=v1;
}
int main()
{
    uint32_t v[]={ 0x3d0b78bd,0x6228a59d};
    uint32_t const k[4]={2,0,2,4};
    unsigned int r=32;
    decipher(r,v,k);
    printf("%x\n",v[1]);
    v[1]=v[0];
    v[0]=0x269669a3;
    decipher(r,v,k);
    printf("%x\n",v[0]);
    printf("%x\n",v[1]);
    return 0;
}
```
警惕反编译器用类型来骗人。拿ghidra举例，反编译出来的xtea是这样的：
```c
void xtea(uint round,uint *value,longlong key)
{
  uint i;
  uint v0;
  uint v1;
  uint sum;
  __CheckForDebuggerJustMyCode(&DAT_140028066);
  v0 = *value;
  v1 = value[1];
  sum = 0;
  for (i = 0; i < round; i = i + 1) {
    v0 = v0 + ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + *(int *)(key + (ulonglong)(sum & 3) * 4));
    sum = sum + 0xccffbbbb;
    v1 = v1 + ((v0 * 0x10 ^ v0 >> 5) + v0 ^ sum + *(int *)(key + (ulonglong)(sum >> 0xb & 3) * 4));
  }
  *value = v0;
  value[1] = v1;
  return;
}
```
会发现有个莫名其妙的`*4`。因为这里把key识别成longlong了，所以必须乘四才取得到值……