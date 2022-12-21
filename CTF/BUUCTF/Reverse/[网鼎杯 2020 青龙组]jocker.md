# [网鼎杯 2020 青龙组]jocker

[题目地址](https://buuoj.cn/challenges#[%E7%BD%91%E9%BC%8E%E6%9D%AF%202020%20%E9%9D%92%E9%BE%99%E7%BB%84]jocker)

第一次用ollydbg脱壳，下方展示的代码都是脱壳修正并重命名后的了。先看脱完壳的程序的逻辑，逆向出来flag后再记录如何脱的壳，参考[wp](https://blog.csdn.net/qq_32072825/article/details/121657090)。

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char input[50]; // [esp+22h] [ebp-96h] BYREF
  char Destination[80]; // [esp+54h] [ebp-64h] BYREF
  char v6[4]; // [esp+A4h] [ebp-14h] BYREF
  size_t v7; // [esp+A8h] [ebp-10h]
  int i; // [esp+ACh] [ebp-Ch]

  sub_4021B0();
  puts("please input you flag:");
  if ( !((int (__stdcall *)(int (__cdecl *)(int), int, int, char *))(&byte_406128 + 12))(encrypt, 200, 4, v6) )
    exit(1);
  scanf("%40s", input);
  v7 = strlen(input);
  if ( v7 != 24 )
  {
    puts("Wrong!");
    exit(0);
  }
  strcpy(Destination, input);
  wrong((int)input);
  omg((int)input);
  for ( i = 0; i <= 186; ++i )
    *((_BYTE *)encrypt + i) ^= 0x41u;
  if ( encrypt((int)Destination) )
    finally((int)Destination);
  return 0;
}
```

能明显地看到wrong和omg这两个函数。名字不是很吉利，进去看看再说。

```c
int __cdecl wrong(int a1)
{
  int result; // eax
  int i; // [esp+Ch] [ebp-4h]

  for ( i = 0; i <= 23; ++i )
  {
    result = i + a1;
    if ( (i & 1) != 0 )
      *(_BYTE *)(i + a1) -= i;
    else
      *(_BYTE *)(i + a1) ^= i;
  }
  return result;
}
```

一个非常简单的加密操作。接着看omg。

```c
int __cdecl omg(int a1)
{
  int result; // eax
  int v2[24]; // [esp+18h] [ebp-80h] BYREF
  int i; // [esp+78h] [ebp-20h]
  int v4; // [esp+7Ch] [ebp-1Ch]

  v4 = 1;
  qmemcpy(v2, &unk_4030C0, sizeof(v2));
  for ( i = 0; i <= 23; ++i )
  {
    if ( *(char *)(i + a1) != v2[i] )
      v4 = 0;
  }
  if ( v4 == 1 )
    result = puts("hahahaha_do_you_find_me?");
  else
    result = puts("wrong ~~ But seems a little program");
  return result;
}
```

是比较操作。把`unk_4030C0`提取出来根据wrong的加密方法逆向看看能得到什么。

```python
data='66 00 00 00 6B 00 00 00 63 00 00 00 64 00 00 00 7F 00 00 00 61 00 00 00 67 00 00 00 64 00 00 00 3B 00 00 00 56 00 00 00 6B 00 00 00 61 00 00 00 7B 00 00 00 26 00 00 00 3B 00 00 00 50 00 00 00 63 00 00 00 5F 00 00 00 4D 00 00 00 5A 00 00 00 71 00 00 00 0C 00 00 00 37 00 00 00 66 00 00 00 '.split(" 00 00 00 ")[:-1]
for i in range(23):
    if not i&1==0:
        print(chr(int(data[i],16)+i),end='')
    else:
        print(chr(int(data[i],16)^i),end='')
#flag{fak3_alw35_sp_me!!
```

不知道为啥少了最后的括号。这个flag亦真亦假的，提交去buu发现不是。这时候去到main函数，发现底下还有个encrypt。

```c
int __cdecl encrypt(int a1) 
{ 
    int v2[19]; // [esp+1Ch] [ebp-6Ch] BYREF 
    int v3; // [esp+68h] [ebp-20h] 
    int i; // [esp+6Ch] [ebp-1Ch] 
    v3 = 1; qmemcpy(v2, &unk_403040, sizeof(v2)); 
    for ( i = 0; i <= 18; ++i ) 
    { 
        if ( (char)(*(_BYTE *)(i + a1) ^ aHahahahaDoYouF[i]) != v2[i] ) 
        {
            puts("wrong ~"); 
            v3 = 0; 
            exit(0); 
        } 
    } 
    puts("come here"); 
    return v3; 
}
```

又是一个异或，简单逆向完事。

```python
hahaha = 'hahahaha_do_you_find_me?'
v2 = [0x0E, 0x0D, 0x9, 0x6, 0x13, 0x5, 0x58, 0x56, 0x3E, 0x6,
      0x0C, 0x3C, 0x1F, 0x57, 0x14, 0x6B, 0x57, 0x59, 0x0D]
true_flag = ''
for i in range(19):
    true_flag+=chr(v2[i] ^ ord(hahaha[i]))
print(true_flag)
# flag{d07abccf8a410c
```

你这flag不对吧，}去哪了？剩下的部分一定在finally函数里。

```c
int __cdecl finally(int a1)
{
  unsigned int v1; // eax
  int result; // eax
  char v3[9]; // [esp+13h] [ebp-15h] BYREF
  int v4; // [esp+1Ch] [ebp-Ch]

  strcpy(v3, "%tp&:");
  v1 = time(0);
  srand(v1);
  v4 = rand() % 100;
  if ( (v3[*(_DWORD *)&v3[5]] != *(_BYTE *)(*(_DWORD *)&v3[5] + a1)) == v4 )
    result = puts("Really??? Did you find it?OMG!!!");
  else
    result = puts("I hide the last part, you will not succeed!!!");
  return result;
}
```

出现了随机数。虽然是伪随机，但是我们也确实不知道出题时time(0)的值，故无法得知v4。不过函数里出现了`%tp&:`这串可疑的字符串，猜测和之前一样都是异或，那就要找key。把``:`和flag已知的部分异或得到异或值`0x47`，那就让剩下的都跟这个异或，确实是flag。

```python
s='%tp&:' 
for i in s: 
    print(chr(ord(i)^0x47),end='')
```

接下来才是重头戏ollydbg脱壳环节。在我用ida打开原程序时，没有和众多wp一样出不来main函数，需要改sp，我直接main函数里f5就出来伪代码了。不过encrypt和finally也是一样出不来。不知道大家有没有注意到，main函数末尾有个for循环把encrypt函数异或0x41，异或完成后才调用的encrypt。如果encrypt本身是好的，这样异或肯定会出问题，说明encrypt在静态分析下就是坏的，或者说加了一层壳，for循环是在脱壳。wp记录的od脱壳步骤已经很详细了，再补充一点我自己踩的坑。

od加载程序后，根据ida里看到的指令地址，找到for循环结束的地址0x40182D下断点（右键0x40182D地址处，选择Breakpoint->Toggle)，如果已经下了也可以用相同的方法取消断点。然后F9（Run program），这时程序会弹出一个窗口让我们输入flag。注意输入的flag一定要是24位的，程序在最开始有逻辑`if ( v7 != 24 )`，如果不等于24就会直接退出，就没法走到断点那了。如果输入的flag长度正确，程序会在断点处停下，按几次F7（Step into），直到程序转到0x401500处。这里就是脱壳后的encrypt函数，菜单栏->Plugins->OllyDump->脱壳当前正在调试的进程。设置什么的都不用改，保存后的程序拖入ida就是上面我展示的那样了。不过符号表全部乱了，需要自己重命名函数。

如果没有装插件是找不到Plugins栏的。建议下载吾爱破解ollydbg这个版本，很多插件都安排好了。

## Flag
> flag{d07abccf8a410cb37a}