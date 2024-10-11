# SMCProMax

手动解码smc：
```py
with open("SMCProMax.exe",'rb') as f:
    start=f.read(0x45e)
    smc=list(f.read(0x827-0x45e))
    rest=f.read()
for i in range(len(smc)):
    smc[i]^=0x90
with open("recoverd.exe",'wb') as f:
    f.write(start+bytes(smc)+rest)
```
然后四个字符四个字符地爆破：
```c++
#include <stdio.h>
#include <stdint.h>
#include <string>
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
vector<uint32_t> chars{48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,64,33,95,63,125};
bool check(uint32_t c1,uint32_t c2,uint32_t c3,uint32_t c4,int target){
    int local_c = (c1<<24)|(c2<<16)|(c3<<8)|c4;
    uint32_t puVar2;
    for (int j = 0; j < 0x20; j = j + 1) {
        if (local_c < 0) {
            puVar2 = local_c << 1;
            local_c = puVar2 ^ 0xc4f3b4b3;
        }
        else {
            local_c = local_c << 1;
        }
    }
    return local_c==target;
}
int main()
{
    //moectf{y0u_mu5t_know_vvZAt_1s__SMC__n0w}
    //注意求出的结果的第23个字符要异或0x12，对应那个Z
    int target=0xcecdd9c3;
    for(uint32_t c1:chars){
        for(uint32_t c2:chars){
            for(uint32_t c3:chars){
                for(uint32_t c4:chars){
                    if(check(c1,c2,c3,c4,target)){
                        printf("%x%x%x%x",c4,c3,c2,c1);
                        break;
                    }
                }
            }
        }
    }
    return 0;
}
```