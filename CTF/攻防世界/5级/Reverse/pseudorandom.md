# pseudorandom

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=33d8561c-3b2d-43e0-befe-71283539ea07_2)

逆向真的越来越难了，对环境的要求也高了。唉至今连ida都没有。

```c
undefined4 Main(undefined4 param_1,undefined8 param_2)

{
  byte bVar1;
  uint uVar2;
  int iVar3;
  size_t sVar4;
  byte flag [48];
  char md5_result [48];
  byte sha_result [32];
  byte md5_temp [28];
  int i;
  SHA_CTX local_178;
  MD5_CTX local_118;
  char local_b8 [140];
  uint local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  uint input;
  undefined8 local_18;
  undefined4 local_10;
  undefined4 local_c;
  
  local_c = 0;
  local_20 = 0;
  local_2c = 0;
  local_18 = param_2;
  local_10 = param_1;
  printf("I will generate some random numbers.\n");
  printf("If you can give me those numbers, you will be $$rewarded$$\n");
  printf("hmm..thinking...");
  fflush(stdout);
  uVar2 = rand();
  sleep(uVar2);
  input = rand();
  printf("OK. I am Ready. Enter Numbers.\n");
  local_20 = 0;
  local_2c = FUN_00400c30(input);
  bVar1 = FUN_00400b40(input);
  local_28 = (1 << (bVar1 & 0x1f)) - 1;
  MD5_Init(&local_118);
  SHA1_Init(&local_178);
  while (local_20 != input) {
    __isoc99_scanf();
    iVar3 = FUN_00400ea0();
    if (iVar3 == 0) {
      Fail();
    }
    else {
      local_28 = local_28 + local_24;
      sprintf(local_b8,"%d",(ulong)local_24);
      sVar4 = strlen(local_b8);
      MD5_Update(&local_118,local_b8,sVar4);
      sVar4 = strlen(local_b8);
      SHA1_Update(&local_178,local_b8,sVar4);
    }
    while ((local_28 ^ 0xffffffff | local_2c ^ 0xffffffff) != 0xffffffff) {
      local_20 = local_20 & local_2c | local_20 ^ local_2c;
      local_28 = (local_28 ^ local_2c) & local_28;
      local_2c = FUN_00400c30();
    }
  }
  MD5_Final(md5_temp,&local_118);
  for (i = 0; i < 0x10; i = i + 1) {
    sprintf(md5_result + (i << 1),"%02x",(ulong)md5_temp[i]);
  }
  iVar3 = strcmp(md5_result,"15b74b4db57d0afdfe98eb5dbc3b542b");
  if (iVar3 != 0) {
    Fail();
  }
  printf("Good Job!!\n");
  printf("Wait till I fetch your reward...");
  fflush(stdout);
  uVar2 = rand();
  sleep(uVar2);
  SHA1_Final(sha_result,&local_178);
  for (i = 0; i < 0x14; i = i + 1) {
    sprintf((char *)(flag + (i << 1)),"%02x",(ulong)sha_result[i]);
  }
  printf("OK. Here it is\n");
  for (i = 0; i < 0x28; i = i + 1) {
    flag[i] = ((flag[i] ^ 0xff) & 0xb5 | flag[i] & 0x4a) ^
              (((byte)*(undefined4 *)(&DAT_006020d0 + (long)i * 4) ^ 0xff) & 0xb5 |
              (byte)*(undefined4 *)(&DAT_006020d0 + (long)i * 4) & 0x4a);
  }
  printf("The flag is:nullcon{%s}\n",flag);
  return local_c;
}
```

md5和sha这类函数似乎不是c语言自带的，网上搜不到。ghidra很草的一点是上方的__isoc99_scanf没有参数……对照着[wp](https://blog.csdn.net/weixin_52640415/article/details/123748108)才勉强重命名了一下。可以看出来flag跟DAT_006020d0有关，这个直接在ghidra里找得到，一点一点往上推flag哪里来的。从sprintf看见flag是local_178的sha加密结果，然而我再往上看发现local_178和输入似乎没关系。嗯，那从输入入手也行。如果iVar3等于0就会Fail，那FUN_00400ea0必定是检查函数。

```c
uint FUN_00400ea0(uint param_1,int param_2)

{
  uint uVar1;
  int iVar2;
  int local_20;
  uint local_10;
  
  local_20 = -0x57121c23;
  do {
    while( true ) {
      while (local_20 < -0x33161e00) {
        if ((local_20 == -0x57121c23) && (local_20 = 0xd0706b8, param_2 != 0)) {
          local_20 = 0x1f711b5c;
        }
      }
      if (local_20 < 0xd0706b8) break;
      if (local_20 == 0xd0706b8) {
        Fail();
        local_10 = 0;
        local_20 = -0x33161e00;
      }
      else if (local_20 == 0x1cde6c41) {
        uVar1 = FUN_00400c30(param_1);
        uVar1 = (param_1 ^ uVar1) & param_1;
        iVar2 = FUN_00400c30();
        local_10 = (uint)((uVar1 & iVar2 << 1 | uVar1 ^ iVar2 << 1) == param_2 + param_1);
        local_20 = -0x33161e00;
      }
      else if ((local_20 == 0x1f711b5c) && (local_20 = 0xd0706b8, param_1 != 0)) {
        local_20 = 0x1cde6c41;
      }
    }
  } while (local_20 != -0x33161e00);
  return local_10;
}
```

ghidra每次反编译和md5有关的题就是这种情况，我永远不知道这些数字是干啥的。而且明明有参数的函数为什么main函数里调用看不到呢？要是是64位我直接看寄存器了，然而是32位，我也不知道该如何用gdb调试，看它在调用函数前压入了什么东西吗？根据大佬得到的结果，verify 的第一个参数最初由程序内部运算后给出，第二个参数是我们的输入。当第一个输入的数通过验证后，verify 的第一个参数会加上输入的数。因此自然想到可以逐次地对输入的数进行爆破。通过动态调试，知道第一次 verify 的第一个参数为 0xffff，接下来就能爆破了。有很大一部分[wp](https://blog.csdn.net/qq_43547885/article/details/113831507)使用[angr](http://hacky.ren/2018/08/27/%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7angr%E4%BD%BF%E7%94%A8%E7%AC%94%E8%AE%B0/),像下面这个。

```python
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import angr
# %%
# 导入项目
proj=angr.Project("./pseudorandom")
# 初始 state 为 verify 函数的地址
state=proj.factory.blank_state(addr=0x400EA0)
# BVS 可以理解为符号的意思，也就是为输入->输出的映射指定一个自变量。一般来说这就是我们要求解的值
arg2=state.solver.BVS('arg2',32)
# 通过动调知道 verify 的第一个参数为 0xffff
state.regs.edi=0xffff
state.regs.esi=arg2
# 初始化 simulation_manager
simgr=proj.factory.simulation_manager(state)
# 找到一条 0x400ea0 -> 0x401039 的路径
simgr.explore(find=0x401039)
# %%
# 获得 found 的 state
found=simgr.found[0]
# 增加限制条件，即存放返回值的内存单元为 True
found.add_constraints(found.memory.load(found.regs.rbp-8,4)!=0)
# 对输入进行求解
value=found.solver.eval(arg2)
print(hex(value))
```

下方的大佬提供了pwn做法。

```python
from pwn import *
from hashlib import md5,sha1
 
dword_6020D0 = [0x0D,0x52,0x67,0x53,0x44,0x40,0x16, 0x8,
                0x51,0x67, 0x6,0x0B,0x52, 0x3, 0x0, 0x0,
                0x5F, 0x1,0x0B,0x6F,0x53,0x55,0x43,0x6A,
                0x53,0x50,0x5B, 0x5,0x51, 0x4,0x10,0x3A,
                0x1, 0x54,0x5C, 0x7,0x4E,0x41,0x9, 0x46]
 
v18 = [0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 0x200000, 0x400000, 0x800000, 0x1000000, 0x2000000, 0x4000000, 0x8000000, 0x10000000, #14
       0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 0x200000, 0x400000, 0x800000, 0x1000000, 0x2000000, 0x4000000, 0x8000000,  #14
       0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 0x200000, 0x400000, 0x800000, 0x1000000, #12
       0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 0x200000, #10
       0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000, 
       0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 
       0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000, 0x40000, 
       0x100, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, 0x10000, #9
       0x80, 0x100, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000, #9
       0x40, 0x80, 0x100, 0x200, 0x400, 0x800, 0x1000, #7
       0x20, 0x40, 0x80, 0x100,  #4
       0x10, 0x20, 0x40, 0x80,
       0x8, 0x10, 0x20, 0x40,
       0x4, 0x8, 0x10, 0x20,
       2, #1
       1]
 
 
p = process('./pseudorandom')
p.recv()
context(log_level='debug')
a = ''
for i in v18:
    print(i, hex(i))
    #p.sendline(str(i).encode())
    a +=str(i)
 
#p.recv()   
print(md5(a.encode()).hexdigest())
print(sha1(a.encode()).hexdigest())
 
'''
  for ( i = 0; i < 40; ++i )
    v8[i] = (dword_6020D0[i] & 0x4A | ~LOBYTE(dword_6020D0[i]) & 0xB5) ^ (v8[i] & 0x4A | ~v8[i] & 0xB5);
'''
 
 
v8 = sha1(a.encode()).hexdigest()
v8 = [ord(i) for i in v8]
for i in range(40):
    v8[i] = (dword_6020D0[i] & 0x4A | ~dword_6020D0[i] & 0xB5) ^ (v8[i] & 0x4A | ~v8[i] & 0xB5)
print(b'nullcon{' + bytes(v8) + b'}')
```

还可以用gdb。我们知道返回值会被存在eax里，在ret处下个断点，根据eax里的值进行爆破。可能会有点痛苦，毕竟数字有点大，还好是有一点规律的。致命的问题在于这题太老了，用的动态链接库我没有。

## Flag
> nullcon{50_5tup1d_ch4113ng3_f0r_e1i73er_71k3-y0u}