# crackMe

[题目地址](https://buuoj.cn/challenges#crackMe)

```c
int __usercall wmain@<eax>(int a1@<ebx>)
{
  FILE *v1; // eax
  FILE *v2; // eax
  char v4; // [esp+3h] [ebp-405h]
  char v5; // [esp+4h] [ebp-404h] BYREF
  char v6[255]; // [esp+5h] [ebp-403h] BYREF
  char Format; // [esp+104h] [ebp-304h] BYREF
  char v8[255]; // [esp+105h] [ebp-303h] BYREF
  char v9; // [esp+204h] [ebp-204h] BYREF
  char v10[255]; // [esp+205h] [ebp-203h] BYREF
  char v11; // [esp+304h] [ebp-104h] BYREF
  char v12[255]; // [esp+305h] [ebp-103h] BYREF

  printf("Come one! Crack Me~~~\n");
  v11 = 0;
  memset(v12, 0, sizeof(v12));
  v9 = 0;
  memset(v10, 0, sizeof(v10));
  while ( 1 )
  {
    do
    {
      do
      {
        printf("user(6-16 letters or numbers):");
        scanf("%s", &v11);
        v1 = (FILE *)sub_4024BE();
        fflush(v1);
      }
      while ( !sub_401000(&v11) );
      printf("password(6-16 letters or numbers):");
      scanf("%s", &v9);
      v2 = (FILE *)sub_4024BE();
      fflush(v2);
    }
    while ( !sub_401000(&v9) );
    sub_401090(&v11);
    Format = 0;
    memset(v8, 0, sizeof(v8));
    v5 = 0;
    memset(v6, 0, sizeof(v6));
    v4 = ((int (__cdecl *)(char *, char *))loc_4011A0)(&Format, &v5);
    if ( sub_401830(a1, (int)&v11, &v9) )
    {
      if ( v4 )
        break;
    }
    printf(&v5);
  }
  printf(&Format);
  return 0;
}
```

我都不用分析就知道事情不简单。运行程序随便输入账号密码，错误时会弹出Please try again。然而ida的字符串窗口却找不到这样一个字符串。挑出几个有用的函数看一下。

```c
_BYTE *__cdecl sub_401090(_BYTE *a1)
{
  _BYTE *result; // eax
  int v2; // [esp+Ch] [ebp-18h]
  int v3; // [esp+10h] [ebp-14h]
  _BYTE *v4; // [esp+14h] [ebp-10h]
  int i; // [esp+18h] [ebp-Ch]
  char v7; // [esp+20h] [ebp-4h]
  char v8; // [esp+22h] [ebp-2h]
  unsigned __int8 v9; // [esp+23h] [ebp-1h]

  for ( i = 0; i < 256; ++i )
    byte_416050[i] = i;                         // 无输入点，无需逆向，直接动调就能得到byte_416050数组的值
  v2 = 0;
  v9 = 0;
  v3 = 0;
  result = a1;
  v4 = a1;
  do
    LOBYTE(result) = *v4;
  while ( *v4++ );
  while ( v2 < 256 )
  {
    v8 = byte_416050[v2];
    v9 += v8 + a1[v3];
    v7 = byte_416050[v9];
    ++v3;
    byte_416050[v9] = v8;
    byte_416050[v2] = v7;
    result = (_BYTE *)v3;
    if ( v3 >= v4 - (a1 + 1) )
      v3 = 0;
    ++v2;
  }
  return result;
}
```

这个函数生成byte_416050数组。逻辑不用细看，反正到时候也是动调的。继续看别的函数。下面还有个loc_4011A0，划拉几下感觉是一个函数的逻辑，还能找到刚才提到的Please try again，甚至有congratulations。根据[wp](https://blog.csdn.net/A951860555/article/details/118667242)所说，0x004011EA出了问题（ida里出现的问题都有红色字体标注出来），patch成nop就行了（0x90）。我试了一下，确实没有报错了，但是还是出不来伪代码。跑去看ghidra，果然ghidra默认就反编译出来了，这点ghidra一直比ida好。

```c
undefined4 __cdecl FUN_004011a0(undefined *param_1,undefined *param_2)

{
  int iVar1;
  
  *param_1 = 0x43;
  param_1[1] = 0x6f;
  param_1[2] = 0x6e;
  param_1[3] = 0x67;
  param_1[4] = 0x72;
  param_1[5] = 0x61;
  param_1[6] = 0x74;
  param_1[7] = 0x75;
  param_1[8] = 0x6c;
  param_1[9] = 0x61;
  param_1[10] = 0x74;
  param_1[0xb] = 0x69;
  param_1[0xc] = 0x6f;
  param_1[0xd] = 0x6e;
  param_1[0xe] = 0x73;
  param_1[0xf] = 0x3a;
  param_1[0x10] = 0x29;
  param_1[0x11] = 0xd;
  param_1[0x12] = 10;
  param_1[0x13] = 0;
  *param_2 = 0x50;
  param_2[1] = 0x6c;
  param_2[2] = 0x65;
  param_2[3] = 0x61;
  param_2[4] = 0x73;
  param_2[5] = 0x65;
  param_2[6] = 0x20;
  param_2[7] = 0x74;
  param_2[8] = 0x72;
  param_2[9] = 0x79;
  param_2[10] = 0x20;
  param_2[0xb] = 0x61;
  param_2[0xc] = 0x67;
  iVar1 = 0;
  if (param_2 != (undefined *)0x0) {
    for (; ((uint)param_2 >> iVar1 & 1) == 0; iVar1 = iVar1 + 1) {
    }
  }
  param_2[0xd] = 0x61;
  param_2[0xe] = 0x69;
  param_2[0xf] = 0x6e;
  rdtsc();
  param_2[0x10] = 0xd;
  param_2[0x11] = 10;
  rdtsc();
  param_2[0x12] = 0;
  return 1;
}
```

没有什么重要的逻辑。看别的函数。

```c
bool __usercall sub_401830@<al>(int ebx0@<ebx>, int a1, const char *a2)
{
  int v4; // [esp+18h] [ebp-22Ch]
  signed int v5; // [esp+1Ch] [ebp-228h]
  signed int v6; // [esp+28h] [ebp-21Ch]
  unsigned int v7; // [esp+30h] [ebp-214h]
  char v8; // [esp+36h] [ebp-20Eh]
  char v9; // [esp+37h] [ebp-20Dh]
  char v10; // [esp+38h] [ebp-20Ch]
  unsigned __int8 v11; // [esp+39h] [ebp-20Bh]
  unsigned __int8 v12; // [esp+3Ah] [ebp-20Ah]
  char v13; // [esp+3Bh] [ebp-209h]
  int v14; // [esp+3Ch] [ebp-208h] BYREF
  char v15; // [esp+40h] [ebp-204h] BYREF
  char v16[255]; // [esp+41h] [ebp-203h] BYREF
  char v17; // [esp+140h] [ebp-104h] BYREF
  char v18[255]; // [esp+141h] [ebp-103h] BYREF

  v5 = 0;
  v6 = 0;
  v12 = 0;
  v11 = 0;
  v17 = 0;
  memset(v18, 0, sizeof(v18));
  v15 = 0;
  memset(v16, 0, sizeof(v16));
  v10 = 0;
  v7 = 0;
  v4 = 0;
  while ( v7 < strlen(a2) )
  {
    if ( isdigit(a2[v7]) )
    {
      v9 = a2[v7] - 48;                         // 将字符0-9转换为数字0-9
    }
    else if ( isxdigit(a2[v7]) )
    {
      if ( *((_DWORD *)NtCurrentPeb()->SubSystemData + 3) != 2 )
        a2[v7] = 34;
      v9 = (a2[v7] | 0x20) - 87;                // 如果输入有16进制字符（a-f），就将其转换为真正的16进制数字存储
    }
    else
    {
      v9 = ((a2[v7] | 0x20) - 97) % 6 + 10;     // 把其他不在16进制范围内的字符也转换到16进制范围内。比如i的结果就是12
    }
    __rdtsc();
    __rdtsc();
    v10 = v9 + 16 * v10;                        // v9是这一次循环取到的用户输入，v10可以看成是上一次的。假设这是第一次运行，v10初始值为0，那么v10就等于v9的值，if进不去。然后第二次运行，v9是当前值，v10取出上一次的值后乘上16。这里乘上16是因为上一次的值应该是高位。比如，当我们知道高位是a，低位是b，16进制里它们的值是什么？就是a*16+b，即这里的逻辑
    if ( !((int)(v7 + 1) % 2) )                 // if语句仅当v7是奇数时才会进入
    {
      *(&v15 + v4++) = v10;                     // v4是v15数组的索引
      ebx0 = v4;
      v10 = 0;
    }
    ++v7;                                       // 从v10=xxx那里开始到这里的逻辑是把输入分成2位一组存入v15数组
  }
  while ( v6 < 8 )
  {
    v11 += byte_416050[++v12];                  // 一些关于byte_416050的操作。后期动调，这里也不用多看
    v13 = byte_416050[v12];
    v8 = byte_416050[v11];
    byte_416050[v11] = v13;
    byte_416050[v12] = v8;
    if ( ((int)NtCurrentPeb()->UnicodeCaseTableData & 0x70) != 0 )
      v13 = v11 + v12;
    *(&v17 + v6) = byte_416050[(unsigned __int8)(v8 + v13)] ^ *(&v15 + v5);// 这里注意下，因为v17关乎到输入对不对，所以是逆向重点。同时v17的值下方可以推出来
    if ( (unsigned __int8)*(_DWORD *)&NtCurrentPeb()->BeingDebugged )
    {
      v11 = -83;
      v12 = 43;
    }
    sub_401710((int)&v17, (const char *)a1, v6++);
    v5 = v6;
    if ( v6 >= (unsigned int)(&v15 + strlen(&v15) + 1 - v16) )
      v5 = 0;
  }
  v14 = 0;
  sub_401470(ebx0, &v17, &v14);
  return v14 == 0xAB94;                         // 从这句可以知道上面v14的返回值必须是0xAB94
}
```

`sub_401830`是最重要的函数，负责检查输入是否正确。里面的函数`sub_401710`如下：

```c
const char *__cdecl sub_401710(int a1, const char *a2, signed int a3)
{
  const char *result; // eax
  signed int v4; // [esp+4h] [ebp-58h]
  struct _STARTUPINFOW StartupInfo; // [esp+14h] [ebp-48h] BYREF

  memset(&StartupInfo, 0, sizeof(StartupInfo));
  StartupInfo.cb = 68;
  GetStartupInfoW(&StartupInfo);
  v4 = strlen(a2);
  if ( StartupInfo.dwX
    || StartupInfo.dwY
    || StartupInfo.dwXCountChars
    || StartupInfo.dwYCountChars
    || StartupInfo.dwFillAttribute
    || StartupInfo.dwXSize
    || StartupInfo.dwYSize )                    // 判断是否是调试状态，正常运行不会进入
  {
    if ( a3 <= v4 )
      result = &a2[a3];
    else
      result = &a2[v4];
  }
  else if ( a3 <= v4 )
  {
    result = (const char *)(a2[a3] ^ *(unsigned __int8 *)(a3 + a1));// 会执行这里，一直往上分析就会知道a2是用户名
    *(_BYTE *)(a3 + a1) = (_BYTE)result;        // 结果直接给到a3也就是外面的v17
  }
  else
  {
    result = (const char *)(a3 + a1);
    *(_BYTE *)(a3 + a1) += byte_416050[v4 + a3] & a2[v4];
  }
  return result;
}
```

最后是`sub_401470`。根据结果慢慢看就知道a2应该是dbappsec了。（注意a2[5]有两个判断，第二个才是对的）。

```c
_DWORD *__usercall sub_401470@<eax>(int a1@<ebx>, _BYTE *a2, _DWORD *a3)
{
  char v5; // al
  _DWORD *result; // eax

  if ( *a2 != 0x64 )
    *a3 ^= 3u;
  else
    *a3 |= 4u;
  if ( a2[1] != 0x62 )
  {
    *a3 &= 0x61u;
    _EAX = (_DWORD *)*a3;
  }
  else
  {
    _EAX = a3;
    *a3 |= 0x14u;
  }
  __asm { aam }
  if ( a2[2] != 0x61 )
    *a3 &= 0xAu;
  else
    *a3 |= 0x84u;
  if ( a2[3] != 0x70 )
    *a3 >>= 7;
  else
    *a3 |= 0x114u;
  if ( a2[4] != 0x70 )
    *a3 *= 2;
  else
    *a3 |= 0x380u;
  if ( *((_DWORD *)NtCurrentPeb()->SubSystemData + 3) != 2 )
  {
    if ( a2[5] != 'f' )
      *a3 |= 0x21u;
    else
      *a3 |= 0x2DCu;
  }
  if ( a2[5] != 's' )
  {
    v5 = (char)a3;
    *a3 ^= 0x1ADu;
  }
  else
  {
    *a3 |= 0xA04u;
    v5 = (char)a3;
  }
  _AL = v5 - (~(a1 >> 5) - 1);
  __asm { daa }
  if ( a2[6] != 'e' )
    *a3 |= 0x4Au;
  else
    *a3 |= 0x2310u;
  if ( a2[7] != 'c' )
  {
    *a3 &= 0x3A3u;
    result = (_DWORD *)*a3;
  }
  else
  {
    result = a3;
    *a3 |= 0x8A10u;
  }
  return result;                                // 那么对照一下外面的期望值，加出来预期值就好了
}
```

直接抄wp了，绕但不完全绕。

```python
v16_2 = "dbappsec"
user = "welcomebeijing"

v16 = []
for i in range(8):
    temp = ord(v16_2[i])^ord(user[i])
    v16.append(temp)
print(v16)

passwd = ""
byte_416050 = [0x2a, 0xd7, 0x92, 0xe9, 0x53, 0xe2, 0xc4, 0xcd]
for i in range(8):
	# 网上大部分的wp答案
	# passwd += hex(byte_416050[i]^ord(v16_2[i]))[2:] # 4eb5f3992391a1ae
    passwd += hex(byte_416050[i]^v16[i])[2:]

print(passwd)
# 39d09ffa4cfcc4cc
```

关键加密逻辑发生在`sub_401830`的这一段：

```c
//第一个变化：v15是密码按2位分割后的结果，那么这里就是数组异或密码，具体怎么异或先不看，捋清楚逻辑最重要
*(&v17 + v6) = byte_416050[(unsigned __int8)(v8 + v13)] ^ *(&v15 + v5);// 这里注意下，因为v17关乎到输入对不对，所以是逆向重点。同时v17的值下方可以推出来
    if ( (unsigned __int8)*(_DWORD *)&NtCurrentPeb()->BeingDebugged )
    {
      v11 = -83;
      v12 = 43;
    }
    //第二个变化：v17是刚刚的异或结果，sub_401710内部是v17与用户名异或
    sub_401710((int)&v17, (const char *)a1, v6++);
    v5 = v6;
    if ( v6 >= (unsigned int)(&v15 + strlen(&v15) + 1 - v16) )
      v5 = 0;
  v14 = 0;
  //比对v17的结果，要求生成结果dbappsec。那么dbappsec就是v17
  sub_401470(ebx0, &v17, &v14);
  //总结：密码异或数组->（密码异或数组）异或用户名->得到期望结果。逆向就反着来：期望结果异或用户名->密码异或数组->(密码异或数组)异或数组->密码。这就是解密脚本的整体逻辑
```

根据大佬所说，这样出来的答案不对，注释那里才是对的，即不执行sub_401710直接逆向的结果。这我就不知道了，求大佬指教。

## Flag
> flag{d2be2981b84f2a905669995873d6a36c}