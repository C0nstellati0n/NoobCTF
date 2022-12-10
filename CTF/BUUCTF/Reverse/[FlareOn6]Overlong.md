# [FlareOn6]Overlong

[题目地址](https://buuoj.cn/challenges#[FlareOn6]Overlong)

出题人在玩一种很新的东西。

无壳，但是程序的函数少得可怜。

```c
int __stdcall start(int a1, int a2, int a3, int a4)
{
  CHAR Text[128]; // [esp+0h] [ebp-84h] BYREF
  unsigned int v6; // [esp+80h] [ebp-4h]

  v6 = sub_401160(Text, (int)&unk_402008, 28u);
  Text[v6] = 0;
  MessageBoxA(0, Text, Caption, 0);
  return 0;
}
```

这个函数仅仅是调用`sub_401160`处理一串字符串然后调出messagebox打印内容。`sub_401160`本身仅仅在调用另一个函数`sub_401000`，直接看另一个好了。

```c
int __cdecl sub_401000(_BYTE *a1, char *a2)
{
  int v3; // [esp+0h] [ebp-8h]
  char v4; // [esp+4h] [ebp-4h]

  if ( (int)(unsigned __int8)*a2 >> 3 == 30 )
  {
    v4 = a2[3] & 0x3F | ((a2[2] & 0x3F) << 6);
    v3 = 4;
  }
  else if ( (int)(unsigned __int8)*a2 >> 4 == 14 )
  {
    v4 = a2[2] & 0x3F | ((a2[1] & 0x3F) << 6);
    v3 = 3;
  }
  else if ( (int)(unsigned __int8)*a2 >> 5 == 6 )
  {
    v4 = a2[1] & 0x3F | ((*a2 & 0x1F) << 6);
    v3 = 2;
  }
  else
  {
    v4 = *a2;
    v3 = 1;
  }
  *a1 = v4;
  return v3;
}
```

有点复杂，感觉不好逆向。不对，我要逆向什么？程序根本就没要求输入啊？运行程序也是，弹出个对话框，没了。看一眼[wp](https://blog.csdn.net/ytj00/article/details/107734647)，原来是patch练习啊？

这题要点进`unk_402008`看看里面有什么。往下翻发现东西不少，肯定不止start函数里传的28个字符。计算一下会发现有175个，即0xAF个。查看start函数的汇编：

```
public start
start proc near

Text= byte ptr -84h
var_4= dword ptr -4

push    ebp
mov     ebp, esp
sub     esp, 84h
push    0FFFFFFAFh
push    offset unk_402008
lea     eax, [ebp+Text]
push    eax
call    sub_401160
add     esp, 0Ch
mov     [ebp+var_4], eax
mov     ecx, [ebp+var_4]
mov     [ebp+ecx+Text], 0
push    0               ; uType
push    offset Caption  ; "Output"
lea     edx, [ebp+Text]
push    edx             ; lpText
push    0               ; hWnd
call    ds:MessageBoxA
xor     eax, eax
mov     esp, ebp
pop     ebp
retn    10h
start endp
```

`push 1Ch`是相关的参数值，利用[ida patch](https://www.jianshu.com/p/cf751c7aec87)成af。把鼠标点到`push 1Ch`那一行，接着菜单栏->Edit->Patch program->Change byte，把1C改成AF，其他不动。确认后再次菜单栏->Edit->Patch program->Apply patches to input file。

现在原程序就被patch了，直接运行就能看见flag了。

## Flag
> flag{I_a_M_t_h_e_e_n_C_o_D_i_n_g@flare-on.com}