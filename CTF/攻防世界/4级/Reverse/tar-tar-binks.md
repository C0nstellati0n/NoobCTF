# tar-tar-binks

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=4ec37492-cb8b-4ea1-b60f-003e286fb62c_2)

至此集齐所有常见操作系统。

附件给了个tar包，还有个……dylib文件？查了一下，原来是Mac OS X下二进制可执行文件的动态链接库。tar包解压不出来，但是file查看确实是tar包。cat文件，这是哪门子tar包？里面一堆16进制。ghidra尝试分析dylib文件，草入口点都没找到。学习[wp](https://blog.csdn.net/xiao__1bai/article/details/120990620)时间。

wp给了很好的思路啊。看flag文件，不明所以的16进制都是4个一组的，可以猜测打印时如果用了printf，format格式是%04X。果不其然找到了，这就是入手点，查找其引用就来到了一个函数。

```c
undefined4 _archive_write_client_write(long param_1,undefined8 param_2,ulong param_3)

{
  long lVar1;
  ulong *puVar2;
  char *pcVar3;
  size_t sVar4;
  long lVar5;
  ulong uVar6;
  ulong local_d8;
  ulong local_80;
  ulong local_78;
  uint local_6c;
  ulong local_48;
  void *local_30;
  
  lVar1 = *(long *)(param_1 + 8);
  puVar2 = *(ulong **)(param_1 + 0x40);
  local_30 = __stubs::_malloc((size_t)&DAT_00002710);
  __stubs::___memcpy_chk(local_30,param_2,param_3);
  if (0x200 < param_3) {
    _sub_1023457();
    pcVar3 = (char *)__stubs::_malloc((size_t)&DAT_00002710);
    __stubs::___memset_chk(local_30,0,&DAT_00002710,0xffffffffffffffff);
    __stubs::___memset_chk(pcVar3,0,&DAT_00002710);
    for (local_6c = 0; local_6c < _posi; local_6c = local_6c + 1) {
      sVar4 = __stubs::_strlen(pcVar3);
      __stubs::___sprintf_chk
                (pcVar3 + sVar4,0,0xffffffffffffffff,"%04X,",
                 *(undefined4 *)(&_sub_101 + (ulong)local_6c * 4));
    }
    __stubs::___memcpy_chk(local_30,pcVar3,param_3,0xffffffffffffffff);
  }
  local_48 = param_3;
  if (*puVar2 == 0) {
    for (; 0 < (long)local_48; local_48 = local_48 - lVar5) {
      lVar5 = (**(code **)(lVar1 + 0xd0))(lVar1,*(undefined8 *)(lVar1 + 0xe0),local_30,local_48);
      if (lVar5 < 1) {
        return 0xffffffe2;
      }
      local_30 = (void *)(lVar5 + (long)local_30);
    }
  }
  else {
    if (puVar2[1] < *puVar2) {
      local_d8 = param_3;
      if (puVar2[1] <= param_3 && param_3 != puVar2[1]) {
        local_d8 = puVar2[1];
      }
      __stubs::___memcpy_chk(puVar2[3],local_30,local_d8,0xffffffffffffffff);
      puVar2[3] = local_d8 + puVar2[3];
      puVar2[1] = puVar2[1] - local_d8;
      local_30 = (void *)(local_d8 + (long)local_30);
      local_48 = param_3 - local_d8;
      if (puVar2[1] == 0) {
        local_78 = puVar2[2];
        for (local_80 = *puVar2; local_80 != 0; local_80 = local_80 - uVar6) {
          uVar6 = (**(code **)(lVar1 + 0xd0))(lVar1,*(undefined8 *)(lVar1 + 0xe0),local_78,local_80)
          ;
          if ((long)uVar6 < 1) {
            return 0xffffffe2;
          }
          if (local_80 < uVar6) {
            _archive_set_error(lVar1,0xffffffff,"write overrun");
            return 0xffffffe2;
          }
          local_78 = uVar6 + local_78;
        }
        puVar2[3] = puVar2[2];
        puVar2[1] = *puVar2;
      }
    }
    for (; *puVar2 <= local_48; local_48 = local_48 - lVar5) {
      lVar5 = (**(code **)(lVar1 + 0xd0))(lVar1,*(undefined8 *)(lVar1 + 0xe0),local_30,*puVar2);
      if (lVar5 < 1) {
        return 0xffffffe2;
      }
      local_30 = (void *)(lVar5 + (long)local_30);
    }
    if (0 < (long)local_48) {
      __stubs::___memcpy_chk(puVar2[3],local_30,local_48,0xffffffffffffffff);
      puVar2[3] = local_48 + puVar2[3];
      puVar2[1] = puVar2[1] - local_48;
    }
  }
  return 0;
}
```

这个函数乱七八糟的，啥也分析不出来。不过既然用了格式化字符串，格式化的内容是什么？明显和_sub_101有关。此处ghidra玩家要注意，直接右键reference可能找不到引用，出现这种情况直接点进_sub_101然后划到右边的XREF，所有引用一目了然。

```c
void _sub_1023458(int *param_1)

{
  ulong uVar1;
  
  uVar1 = (ulong)_posi;
  _posi = _posi + 1;
  *(int *)(&_sub_101 + uVar1 * 4) = param_1[2] * 0x640 + param_1[1] * 0x28 + *param_1;
  return;
}
```

把param_1相关的内容赋值给_sub_101，那就要知道传进来的参数是什么。继续找XREF。

```c
void _sub_1023457(undefined8 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  int local_30;
  int local_2c;
  undefined4 local_1c [3];
  long local_10;
  
  local_10 = *(long *)__got::___stack_chk_guard;
  local_30 = 3;
  local_2c = param_2;
  while (iVar2 = local_2c + -1, local_2c != 0) {
    __pending = 1;
    while (local_2c = iVar2, __pending != 0) {
      uVar1 = _sub_1023456();
      local_30 = local_30 + -1;
      local_1c[local_30] = uVar1;
      if (local_30 == 0) {
        _sub_1023458();
        local_30 = 3;
      }
    }
  }
  if (local_30 != 3) {
    while (local_30 != -1) {
      local_30 = local_30 + -1;
      local_1c[local_30] = 0;
    }
    _sub_1023458(local_1c);
  }
  if (*(long *)__got::___stack_chk_guard != local_10) {
                    /* WARNING: Subroutine does not return */
    __stubs::___stack_chk_fail();
  }
  return;
}
```

我懵了。没传参数？第一个调用压根没写，只有第二个调用本分地写了参数。ida倒是好好的，又是渴望ida的一天。结合ida可以看出，传进_sub_1023458()的是local_1c，自然就要看_sub_1023456()了。

```c
int _sub_1023456(int param_1)

{
  int i;
  int local_10;
  int local_c;
  
  local_c = _sub_1023456.shifted;
  if (_sub_1023456.shifted == -1) {
    local_10 = param_1;
    if (param_1 == 0x7e) {
      local_10 = 0;
    }
    for (i = 0; i < 0x27; i = i + 1) {
      if ((char)(&_ctable)[i] == local_10) {
        __pending = 0;
        return i;
      }
      if (s_abcdefghijklmnopqrstuvwxyz012345_000d8841[(long)i + 0x26] == local_10) {
        _sub_1023456.shifted = i;
        __pending = 1;
        return 0x27;
      }
    }
    local_c = 0x25;
  }
  else {
    _sub_1023456.shifted = -1;
  }
  __pending = 0;
  return local_c;
}
```

_sub_1023456()你不是没有参数吗？怎么这里又写param_1？还是ghidra的锅，看ida就知道参数a1是外部的v5，v5=*v3，v3无法跟踪。来历不明的变量最有可能是用户输入了，于是猜测是我们的输入，也就是逆向目标。分析函数，把param_1赋值给local_10，然后走一个for循环，如果_ctable)[i]等于local_10就返回当前索引i；如果s_abcdefghijklmnopqrstuvwxyz012345_000d8841[(long)i + 0x26]等于local_10，将_sub_1023456.shifted设为i，返回0x27。注意local_c初始赋值为 _sub_1023456.shifted，因此下一次执行这个函数就会直接返回local_c即_sub_1023456.shifted，因为最开始的if语句以及最后的return语句。

不分析了，直接上脚本。

```python
last_ver=[0xF5D1,0x4D6B,0xED6A,0x08A6,0x38DD,0xF7FA,0x609E,0xEBC4,0xE55F,0xE6D1,0x7C89,0xED5B,0x0871,0x1A69,0x5D58,0x72DE,0x224B,0x3AA6,0x0845,0x7DD6,0x58FB,0xE9CC,0x0A2D,0x76B8,0xED60,0x251A,0x1F6B,0x32CC,0xE78D,0x12FA,0x201A,0xE889,0x2D25,0x922A,0x4BC5,0xF5FF,0xF8E5,0xC79B,0x3A77,0x4BDB,0xEA11,0x5941,0x58BD,0x3A95,0xF5C9,0xA225,0xAD40,0xF8BD,0x095D,0x70B6,0x458C,0xE7A9,0xEA68,0x252F,0x094B,0x5E41,0x0969,0x6015,0x5ED5,0xF6E5,0x59B9,0x7CAF,0x66DF,0x265B,0x7837,0x57B4,0x7CAF,0xAED9,0xF707,0x6A3C,0xF8E5,0xF509,0x7C8B,0x0915,0x2235,0x336F,0x33E9,0x2D14,0x7C91,0x5804,0x83E5,0xE78D,0xF4EA,0x0874,0xED6B,0x4B35,0xE839,0x57B4,0xE77C,0xEA68,0x2525,0xAD41,0xED6F,0x3A4A,0x4BCC,0x6015,0xF440,0x0858,0x3AA6,0x7809,0x671D,0x0874,0xEA77,0x63AF,0x2E91,0x5845,0xF6C4,0x086D,0x7795,0x3939,0x57B4,0x7C89,0x82DC,0x32ED,0xB994,0xC7AF,0x9135,0x0E65,0x1B66,0xED5B,0x3235,0x6577,0x5A80,0x3AD3,0xE776,0x1EE5,0xAD41,0xED59,0x864C,0x70B4,0x3876,0xED67,0x64D6,0xF8E5,0xF505,0xEAD9,0x7C9C,0x32ED,0xB994,0xB4EF,0x0C6C,0xF665,0xF5F5,0x9047,0x521A,0xE99E,0xEA68,0x252F,0x9D09,0x76B7,0xE776,0x1ED0,0x095D,0x0D4D,0x5D5A,0x087B,0x2005,0x1526,0x7E76,0x85AD,0x78B9,0xE8B6,0x782C,0x251C,0x32ED,0x7F68,0xEBE3,0xEA41,0x57FD,0xED59,0x846D,0x7A05,0xB994,0xBB78,0xED6A,0x08A6,0x38DD,0x3B5D,0x7E45,0xE839,0x738C,0xE9CC,0x0A2D,0x764A,0x609E,0xE8B6,0xEA68,0x2524,0xE6BB,0x7C9C,0x639F,0x3A95,0x0895,0xF40F,0x8328,0xEA69,0x7EE5,0xF8BD,0x7F7D,0x0D6D,0x70B6,0x458C,0xE8B6,0xEA68,0x251C,0x6065,0xB35F,0xC789,0x5845,0x7F7D,0x6D89,0x4C6E,0xA20E,0x60B5,0x7E45,0xED59,0xF707,0x69EF,0x922A,0x4BC5,0xF6EF,0x8635,0xF4B9,0x57B4,0x7CF8,0xED60,0x2510,0x095D,0x20AF,0x3545,0xF40F,0x8328,0xEA41,0x58A4,0x225D,0x7E7C,0x4BDB,0xF8BD,0x082C,0xEAE7,0x5D57,0x5D50,0x0914,0xE7C7,0x8624,0x7CF8,0xED60,0x2511,0x7C8E,0x7159,0x8416,0x7EF9,0xE7E5,0x774A,0x3895,0x1EC9,0x7C90,0x09B9,0x58BD,0x5FF5,0xE99E,0xEA68,0x250A,0x224C,0xEA3D,0x73F5,0x7C89,0x53A6,0x3190,0x3B5D,0x1526,0x7DD5,0x666A,0x0919,0x225F,0xCDEF,0x79E1,0x7E7B,0x7E6B,0x082C,0xA277,0xE885,0xE8BB,0xE775,0x5FF7,0xEA68,0x251B,0x7FDF,0x589D,0x7A05,0x779A,0x8A5A,0x7C91,0x5D5C,0x32ED,0xF628,0x2195,0xF49A,0x0C77,0xEAE1,0x59B9,0x58BD,0xE570,0xE99E,0xEA3D,0x73F9,0x13AD,0x2BF5,0x225D,0x7F7D,0x70B6,0x4A9C,0x337A,0x1EC9,0x4D05,0x7E75,0x2578,0xED59,0x38E5,0x1ECA,0xA210,0x3B5D,0x779A,0x8A6F,0xC790,0x2518,0x4B41,0x7C89,0x5D49,0x4D05,0x152D,0x73C5,0x79F9,0x4BED,0x913C,0x37C9,0x5D4D,0x53C8,0x0941,0x7C97,0x5D5B,0x346A,0x82D8,0x5F36,0x801F,0xC800]
t1=[]
t2=[]
flag=""
ctable = [0x00, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0x73,
0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x30, 0x31, 0x32,
0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x20, 0x0A, 0x00,
0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A,
0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54,
0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x28, 0x21, 0x40, 0x23,
0x2C, 0x2E, 0x3F, 0x2F, 0x2A, 0x29, 0x3C, 0x3E, 0x00]

for num in last_ver:  #abc cba逆序放回
    a=num%40
    b=(num//40)%40
    c=num//1600
    t1+=[c,b,a]

i=0
while i<len(t1):
    if t1[i]==39:    #合成位置
        t2+=[t1[i]+t1[i+1]]
        i+=2
    else :
        t2+=[t1[i]]
        i+=1

for i in t2:
    if ctable[i] != "\x00": #去掉最后填一堆的0
    	flag+=chr(ctable[i])
print(flag)
```

要知道_sub_1023458其实是一个三元一次方程，a = param[0] + param[1] * 0x28 + param[2] * 0x640，现在我们有a，怎么逆向？好像不太可能，就给个解让我们找到3个未知数？结果大佬告诉我们可以。只要a的值没有超过一定的值就可以用以下方法求param[0]、param[1]、param[2]:param[0]=a % 0x28;param[1]=(a // 0x28) % 0x28,param[3]=a // 0x640,这也是解题脚本第一个for语句的由来。逆序返回是因为_sub_1023457中赋值也是逆着来的，我们现在正在找里面local_1c的内容。

接下来的while循环逆向_sub_1023456函数。结果是一篇文章，它的md5值就是flag。可以用cyberchef，但是直接粘贴进去得到的md5值是不对的，还要再加个回车。

### Flag
- 2c8cd31daeba8753815851f13e6370b3