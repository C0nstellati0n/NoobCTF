# EASYHOOK

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f88bf119-9935-494f-a774-99cdc439ce07_2)

如何让easyhook变得不easy呢？答案之一是用ghidra反编译exe。

```c
undefined4 Main(void)

{
  char cVar1;
  HANDLE hFile;
  void *this;
  int iVar2;
  char *pcVar3;
  DWORD local_24;
  char local_20 [32];
  
  FUN_00401370((byte *)s_Please_input_flag:_0040a0d0);
  FUN_00401437(this,&DAT_0040a0c8);
  iVar2 = -1;
  pcVar3 = local_20;
  do {
    if (iVar2 == 0) break;
    iVar2 = iVar2 + -1;
    cVar1 = *pcVar3;
    pcVar3 = pcVar3 + 1;
  } while (cVar1 != '\0');
  if (iVar2 != -0x15) {
    FUN_00401370((byte *)s_Wrong!_0040a0c0);
    FUN_004013a1((int)s_pause_0040a0b8);
    return 0;
  }
  FUN_00401220();
  hFile = CreateFileA(s_Your_input_0040a0ac,0x40000000,0,(LPSECURITY_ATTRIBUTES)0x0,2,0x80,
                      (HANDLE)0x0);
  WriteFile(hFile,local_20,0x13,&local_24,(LPOVERLAPPED)0x0);
  FUN_00401240(local_20,&local_24);
  if (local_24 == 1) {
    pcVar3 = s_Right!flag_is_your_input_0040a090;
  }
  else {
    pcVar3 = s_Wrong!_0040a0c0;
  }
  FUN_00401370((byte *)pcVar3);
  FUN_004013a1((int)s_pause_0040a0b8);
  return 0;
}
```

头皮发麻，万幸还能看见关键判断——local_24==1。往上看，发现local_24在FUN_00401240和WriteFile均有引用。WriteFile是系统函数，进不去，那只能看FUN_00401240了。

```c
void __cdecl FUN_00401240(char *param_1,undefined4 *param_2)

{
  char cVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  char *pcVar7;
  undefined4 local_18 [6];
  
  iVar2 = 0;
  puVar5 = (undefined4 *)s_This_is_not_the_flag_0040a078;
  puVar6 = local_18;
  for (iVar3 = 5; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = *puVar5;
    puVar5 = puVar5 + 1;
    puVar6 = puVar6 + 1;
  }
  *(undefined *)puVar6 = *(undefined *)puVar5;
  uVar4 = 0xffffffff;
  pcVar7 = param_1;
  do {
    if (uVar4 == 0) break;
    uVar4 = uVar4 - 1;
    cVar1 = *pcVar7;
    pcVar7 = pcVar7 + 1;
  } while (cVar1 != '\0');
  if (0 < (int)(~uVar4 - 1)) {
    do {
      if (param_1[iVar2] != *(char *)((int)local_18 + iVar2)) {
        return;
      }
      iVar2 = iVar2 + 1;
    } while (iVar2 < (int)(~uVar4 - 1));
    if (iVar2 == 0x15) {
      *param_2 = 1;
    }
  }
  return;
}
```

param_2对应了local_24，param_1对应了local_20。这里可能是主要加密函数，但是好乱啊，完全看不出来在干什么。唯一勉强看懂的是最后一个do-while循环，要求param_1[iVar2]等同于*(char *)((int)local_18 + iVar2)。local_18啥时候初始化的？param_1是啥？回到main函数，发现local_20也在WriteFile有出现。这就很可疑了啊，两个关键变量均有出现，这个函数不会有问题吧？可是系统函数还能骗人？

```c
void FUN_00401220(void)

{
  HMODULE hModule;
  DWORD dwProcessId;
  
  dwProcessId = GetCurrentProcessId();
  DAT_0040c9c8 = OpenProcess(0x1f0fff,0,dwProcessId);
  hModule = LoadLibraryA(s_kernel32.dll_0040a068);
  DAT_0040c9b0 = (undefined4 *)GetProcAddress(hModule,s_WriteFile_0040a05c);
  _DAT_0040c9c4 = DAT_0040c9b0;
  if (DAT_0040c9b0 == (undefined4 *)0x0) {
    FUN_00401370(&DAT_0040a044);
    return;
  }
  DAT_0040c9b4 = *DAT_0040c9b0;
  DAT_0040c9b8 = *(undefined *)(DAT_0040c9b0 + 1);
  DAT_0040c9bc = 0xe9;
  _DAT_0040c9bd = (int)&UNK_0040107b - (int)DAT_0040c9b0;
  FUN_004010d0();
  return;
}
```

确实，不要相信任何一个函数。在调用writeFile之前，还有一个函数，出现了WriteFile的地址。然后呢？

```c
void FUN_004010d0(void)

{
  DWORD local_8;
  DWORD local_4;
  
  local_8 = 0;
  VirtualProtectEx(DAT_0040c9c8,DAT_0040c9b0,5,4,&local_4);
  WriteProcessMemory(DAT_0040c9c8,DAT_0040c9b0,&DAT_0040c9bc,5,(SIZE_T *)0x0);
  VirtualProtectEx(DAT_0040c9c8,DAT_0040c9b0,5,local_4,&local_8);
  return;
}
```

[VirtualProtectEx](https://zhidao.baidu.com/question/472172741.html)这个函数可以修改内存的权限，此处修改DAT_0040c9b0地址中的5字节改成可读写，然后[WriteProcessMemory](https://www.cnblogs.com/HeroZearin/articles/2539090.html)修改DAT_0040c9b0中的5个字节为DAT_0040c9bc，之前赋值为0xe9，最后再执行一次VirtualProtectEx]把权限改回来。也就是说，邪恶的出题人把WriteFile的地址改了，很有可能改成了真正的加密函数。

0xe9机器码中代表jmp。然而跳去哪里我是真看不出来了。看[wp](https://blog.csdn.net/xiao__1bai/article/details/119920369)才知道跳去了真正的加密函数，在ghidra里看不出来，ida里可以直接发现真正的加密函数。关键ghidra里加密函数的地址还和ida里不一样。

```c
undefined4 __cdecl FUN_00401000(int param_1,int param_2)

{
  byte bVar1;
  int iVar2;
  char cVar3;
  uint uVar4;
  byte bVar5;
  uint uVar6;
  bool bVar7;
  
  bVar1 = 0;
  if (0 < param_2) {
    do {
      if (bVar1 == 18) {
        *(byte *)(param_1 + 0x12) = *(byte *)(param_1 + 0x12) ^ 0x13;
      }
      else {
        uVar4 = (uint)(char)bVar1;
        uVar6 = uVar4 & 0x80000001;
        bVar7 = uVar6 == 0;
        if ((int)uVar6 < 0) {
          bVar7 = (uVar6 - 1 | 0xfffffffe) == 0xffffffff;
        }
        if (bVar7) {
          bVar5 = *(byte *)(uVar4 + 2 + param_1);
        }
        else {
          bVar5 = *(char *)(uVar4 + param_1) - bVar1;
        }
        *(byte *)(uVar4 + param_1) = bVar5 ^ bVar1;
      }
      bVar1 = bVar1 + 1;
    } while ((char)bVar1 < param_2);
  }
  cVar3 = '\0';
  if (0 < param_2) {
    iVar2 = 0;
    do {
      if ((&DAT_0040a030)[iVar2] != *(char *)(iVar2 + param_1)) {
        return 0;
      }
      cVar3 = cVar3 + '\x01';
      iVar2 = (int)cVar3;
    } while (iVar2 < param_2);
  }
```

然而还是无限混乱。不要靠近ghidra，它会让你变得不幸。直接去ida里看吧，这个函数能看出来个什么东西？

```python
dst=[0x61, 0x6A, 0x79, 0x67, 0x6B, 0x46, 0x6D, 0x2E, 0x7F, 0x5F, 0x7E, 0x2D, 0x53, 0x56, 0x7B, 0x38, 0x6D, 0x4C, 0x6E]
flag=list("-------------------")
flag[-1]=chr(dst[18]^0x13)
for i in range(17,-1,-1):
    tmp=dst[i]^i
    if i%2==1:
        flag[i]=chr(tmp+i)
    else:
        flag[i+2]=chr(tmp)
print(''.join(flag))
```

- ### Flag
  > flag{Ho0k_w1th_Fun}