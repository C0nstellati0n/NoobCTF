# testre

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4dc22d15-0a1c-4c8e-924c-1ac70b62d6c3_2)

这才在密密麻麻的代码缝中挤出字来：这都不会？

reverse区很难受，exe的都几乎逆不了，只能挑一些简单的elf做做——然后还是不会。

```c
undefined Main(char *param_1,ulong *param_2,long param_3,ulong param_4)
{
  byte bVar1;
  long lVar2;
  void *__s;
  char *pcVar3;
  ulong uVar4;
  size_t sVar5;
  int iVar6;
  undefined8 uStack208;
  undefined auStack200 [8];
  int local_c0;
  byte local_b9;
  undefined4 local_b8;
  undefined local_b1;
  undefined *local_b0;
  byte local_a1;
  uint local_a0;
  ulong i;
  size_t local_90;
  ulong local_88;
  ulong local_80;
  ulong j;
  size_t local_70;
  uint local_64;
  ulong local_60;
  int local_54;
  undefined *local_50;
  long copyOfInput;
  void *local_40;
  int local_34;
  ulong local_30;
  long input;
  ulong *local_20;
  char *local_18;
  undefined local_9;
  local_34 = -0x21524111;
  uStack208 = 0x400732;
  local_30 = param_4;
  input = param_3;
  local_20 = param_2;
  local_18 = param_1;
  local_40 = malloc(0x100);
  copyOfInput = input;
  local_50 = auStack200;
  local_60 = 0;
  local_88 = 0;
  for (i = 0; i < local_30; i = i + 1) {
    local_a0 = (uint)*(byte *)(input + i);
    *(byte *)((long)local_40 + i) = *(byte *)(input + i) ^ "fake_secret_makes_you_annoyed"[i % 29];
    *(char *)((long)local_40 + i) = *(char *)((long)local_40 + i) + *(char *)(input + i);
  }
  while( true ) {
    local_a1 = 0;
    if (local_88 < local_30) {
      local_a1 = *(char *)(input + local_88) != '\0' ^ 0xff;
    }
    if ((local_a1 & 1) == 0) break;
    local_88 = local_88 + 1;
  }
  uVar4 = ((local_30 - local_88) * 0x8a >> 2) / 0x19;
  sVar5 = uVar4 + 1;
  local_90 = sVar5;
  local_54 = (int)(((local_30 + local_88) * 0x40) / 0x30) + -1;
  lVar2 = -(uVar4 + 0x10 & 0xfffffffffffffff0);
  local_b0 = auStack200 + lVar2;
  *(undefined8 *)(auStack200 + lVar2 + -8) = 0x4008e5;
  memset(auStack200 + lVar2,0,sVar5);
  pcVar3 = local_18;
  sVar5 = local_88;
  local_70 = local_88;
  local_80 = local_90 - 1;
  do {
    if (local_30 <= local_70) {
      j = 0;
      while( true ) {
        local_b9 = 0;
        if (j < local_90) {
          local_b9 = local_b0[j] != '\0' ^ 0xff;
        }
        if ((local_b9 & 1) == 0) break;
        j = j + 1;
      }
      if ((local_88 + local_90) - j < *local_20) {
        if (local_88 != 0) {
          local_c0 = 0x3d;
          *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400b09;
          memset(pcVar3,0x31,sVar5);
          __s = local_40;
          sVar5 = local_88;
          iVar6 = local_c0;
          *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400b1c;
          memset(__s,iVar6,sVar5);
        }
        pcVar3 = local_18;
        local_70 = local_88;
        for (; j < local_90; j = j + 1) {
          local_18[local_70] =
               "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[(byte)local_b0[j]];
          *(char *)((long)local_40 + local_70) =
               "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[(byte)local_b0[j]]
          ;
          local_70 = local_70 + 1;
        }
        local_18[local_70] = '\0';
        *local_20 = local_70 + 1;
        *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400bca;
        iVar6 = strncmp(pcVar3,"D9",2);
        if (iVar6 == 0) {
          pcVar3 = local_18 + 20;
          *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400bf4;
          iVar6 = strncmp(pcVar3,"Mp",2);
          if (iVar6 == 0) {
            pcVar3 = local_18 + 18;
            *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400c1e;
            iVar6 = strncmp(pcVar3,"MR",2);
            if (iVar6 == 0) {
              pcVar3 = local_18 + 2;
              *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400c48;
              iVar6 = strncmp(pcVar3,"cS9N",4);
              if (iVar6 == 0) {
                pcVar3 = local_18 + 6;
                *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400c72;
                iVar6 = strncmp(pcVar3,"9iHjM",5);
                if (iVar6 == 0) {
                  pcVar3 = local_18 + 11;
                  *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400c9c;
                  iVar6 = strncmp(pcVar3,"LTdA8YS",7);
                  if (iVar6 == 0) {
                    *(undefined8 *)(auStack200 + lVar2 + -8) = 0x400cb4;
                    puts("correct!");
                  }
                }
              }
            }
          }
        }
        local_9 = 1;
      }
      else {
        *local_20 = ((local_88 + local_90) - j) + 1;
        local_9 = 0;
      }
      return local_9;
    }
    local_64 = (uint)*(byte *)(copyOfInput + local_70);
    j = local_90;
    do {
      j = j - 1;
      local_b1 = true;
      if (j <= local_80) {
        local_b1 = local_64 != 0;
      }
      if ((bool)local_b1 == false) break;
      bVar1 = local_b0[j];
      iVar6 = (uint)(byte)local_b0[j] * 0x100 + local_64;
      local_b8 = 0x40;
      local_b0[j] = (char)((long)iVar6 % 58);
      *(undefined *)((long)local_40 + j) = 0;
      local_60 = (ulong)(long)(int)((uint)bVar1 << 6) >> 6;
      local_64 = iVar6 / 58;
      local_34 = local_34 / 0x40;
    } while (j != 0);
    local_70 = local_70 + 1;
    local_80 = j;
  } while( true );
}
```

密密麻麻的，ghidra把全部加密逻辑都放在main函数里了。照例从关键比较部分倒着看。iVar6 = strncmp(pcVar3,"D9",2);这行代码说明期望输入为pcVar3（或者看成local_18)，iVar6可能是我们的输入经过加密后的结果。一堆if语句里的字符看起来像base家族，往上看看是什么base。

发现两个很明显的编码字母表，第一眼想到了base64，数了较短的那个发现是base58。暂时不知道是怎么加密的，但是提到local_18的只有base58那个。先不看base64的，就是赌你不用。

于是我就陷入了深深的疑惑中。我完全看不出来上面一串代码究竟在干啥，只能知道搞了一堆乱七八糟可能和flag没关系的东西。另外还有很坑的一点是，对input进行base58编码的逻辑在比较逻辑的下面，属实是没想到。识别编码是因为出现了58这个关键数字和copyOfInput，并不是因为我看得懂。

编码的是copyOfInput，最上面进行异或加密的却是input，且input之后也没有再出现，猜测input和异或是混淆项。中间还有很多变量，粗略过一遍会发现似乎没有出现在比较逻辑中。此时就出现了问题：是按部就班把整个逻辑看一遍并理解，还是直接去看比较逻辑中期望的base58编码然后尝试直接解密？事实证明应该选第二种，因为第二种耗时短，如果直接成功了就不用管那些鬼都不知道在干啥的逻辑了。

注意判断逻辑不是按顺序的，local_18是指针，这里看成基指针。由于使用strncmp指定字节进行比较，所以每比较n个就把基指针加n个字节。第一个for语句，也就是基地址处，比较了D9两个字节，所以下一次应该是local_18 + 2。找到local_18 + 2的for语句，这次往后比较了4个字节，所以下次是local_18 + 6，以此类推。最后拼出正确的base58编码串。

- D9cS9N9iHjMLTdA8YSMRMp

cyberchef解密得到flag。

- ### Flag
  > flag{base58_is_boring}