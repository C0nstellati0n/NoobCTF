# Youngter-drive

[题目地址](https://buuoj.cn/challenges#Youngter-drive)

```c
undefined8 Main(void)

{
  int iVar1;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  undefined4 extraout_EDX_04;
  undefined4 *puVar2;
  undefined8 uVar3;
  undefined4 local_dc [49];
  HANDLE local_18;
  HANDLE local_c;
  undefined4 uStack8;
  
  puVar2 = local_dc;
  for (iVar1 = 0x36; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  Menu(); //打印菜单及获取输入
  CreateMutexW((LPSECURITY_ATTRIBUTES)0x0,0,(LPCWSTR)0x0); //创建一个互斥锁
  uVar3 = __RTC_CheckEsp(extraout_ECX,extraout_EDX);
  DAT_004181b0 = (HANDLE)uVar3;
  strcpy(&DAT_00418148,&result);
  CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&LAB_004110a0,(LPVOID)0x0,0, //创建一个线程
               (LPDWORD)0x0);
  uVar3 = __RTC_CheckEsp(extraout_ECX_00,extraout_EDX_00);
  local_c = (HANDLE)uVar3;
  CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&LAB_0041119f,(LPVOID)0x0,0,//创建另一个线程
               (LPDWORD)0x0);
  uVar3 = __RTC_CheckEsp(extraout_ECX_01,extraout_EDX_01);
  local_18 = (HANDLE)uVar3;
  CloseHandle(local_c);
  __RTC_CheckEsp(extraout_ECX_02,extraout_EDX_02);
  CloseHandle(local_18);
  __RTC_CheckEsp(extraout_ECX_03,extraout_EDX_03);
  do {
  } while (index != -1);
  GetFlag(); //检查输入是否正确
  CloseHandle(DAT_004181b0);
  uVar3 = __RTC_CheckEsp(extraout_ECX_04,extraout_EDX_04);
  uStack8 = 0x411d6f;
  uVar3 = __RTC_CheckEsp(extraout_ECX_05,(int)((ulonglong)uVar3 >> 0x20));
  return uVar3;
}
```

ghidra找交叉引用没ida好，看着[wp](https://blog.csdn.net/weixin_45701079/article/details/109402704)才找到main在哪。[CreateThread](https://blog.csdn.net/u012877472/article/details/49721653)明显的创建线程函数，根据定义，第三个参数是线程要执行的函数。点进去看看，里面有个套娃，真正的代码如下：

```c
undefined8 __fastcall Encrypt1(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 *puVar2;
  undefined4 local_c4 [48];
  
  puVar2 = local_c4;
  for (iVar1 = 0x30; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  do {
    WaitForSingleObject(DAT_004181b0,0xffffffff);
    __RTC_CheckEsp(extraout_ECX,extraout_EDX);
    if (-1 < index) {
      MainEncrypt((int)&result,index); //内部真正的加密函数
      index = index + -1;
      Sleep(100);
      __RTC_CheckEsp(extraout_ECX_00,extraout_EDX_00);
    }
    ReleaseMutex(DAT_004181b0); //释放互斥锁，两个线程不会互相干扰
    __RTC_CheckEsp(extraout_ECX_01,extraout_EDX_01);
  } while( true );
}
```

MainEncrypt里面是个替换加密。

```c
undefined8 __cdecl MainEncrypt(int param_1,int param_2)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined8 uVar4;
  undefined4 local_d0 [49];
  char local_9;
  
  puVar3 = local_d0;
  for (iVar1 = 0x33; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_9 = *(char *)(param_1 + param_2);
  if (((local_9 < 'a') || ('z' < local_9)) && ((local_9 < 'A' || ('Z' < local_9)))) {
                    /* WARNING: Subroutine does not return */
    exit(0); //如果输入不是字母就退出，说明flag没有除字母以外的内容
  }
  if ((local_9 < 'a') || ('z' < local_9)) {   //感觉是判断大写字母，因为上面已经排除非字母输入了，这里又排除小写字母
    uVar2 = CONCAT31((undefined3)(*(char *)(param_1 + param_2) >> 7),
                     PTR_s_QWERTYUIOPASDFGHJKLZXCVBNMqwerty_00418000
                     [*(char *)(param_1 + param_2) + -38]);  //不要理这里，我也搞不懂这是在干啥，ghidra特色
    *(undefined *)(param_1 + param_2) =
         PTR_s_QWERTYUIOPASDFGHJKLZXCVBNMqwerty_00418000[*(char *)(param_1 + param_2) + -38];  //param_1是输入，param_2是index，取输入的每一个字符的ord值-38得到索引，然后去一串字符串里取值
  }
  else {
    uVar2 = CONCAT31((undefined3)(*(char *)(param_1 + param_2) >> 7),
                     PTR_s_QWERTYUIOPASDFGHJKLZXCVBNMqwerty_00418000
                     [*(char *)(param_1 + param_2) + -96]);
    *(undefined *)(param_1 + param_2) =
         PTR_s_QWERTYUIOPASDFGHJKLZXCVBNMqwerty_00418000[*(char *)(param_1 + param_2) + -96];  //同理，只不过小写字母减去96
  }
  uVar4 = __RTC_CheckEsp(uVar2,param_1 + param_2);
  return uVar4;
}
```

还有个Encrypt2。

```c
undefined8 __fastcall Encrypt2(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 *puVar2;
  undefined4 local_c4 [48];
  
  puVar2 = local_c4;
  for (iVar1 = 0x30; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  do {
    WaitForSingleObject(DAT_004181b0,0xffffffff);
    __RTC_CheckEsp(extraout_ECX,extraout_EDX);
    if (-1 < index) {
      Sleep(100);
      __RTC_CheckEsp(extraout_ECX_00,extraout_EDX_00);
      index = index + -1;
    }
    ReleaseMutex(DAT_004181b0);
    __RTC_CheckEsp(extraout_ECX_01,extraout_EDX_01);
  } while( true );
}
```

Encrypt1和2极其相似，只是Encrypt2里没有调用MainEncrypt，单纯将index-1。虽然开了互斥锁，但是这个互斥锁并不表示这个线程改的index不会影响另一个线程。互斥锁的作用在于不让多个线程访问同一个资源时混乱。比如线程2已经把index减去1了，线程1获取到的index就是减去1后的，而不是原本的。由于index影响到MainEncrypt里取值，那么只会有大概一半的字符会进入MainEncrypt里被加密。谁先谁后决定哪一半被加密，毕竟它们是交替进行的。后面发现是奇数位被加密。

```c
undefined8 GetFlag(void)

{
  int iVar1;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_EDX;
  undefined4 *puVar2;
  undefined8 uVar3;
  undefined4 local_d0 [49];
  int local_c;
  undefined4 uStack8;
  
  puVar2 = local_d0;
  for (iVar1 = 0x33; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  while( true ) {
    if (0x1c < local_c) {
      printf("\nflag{%s}\n\n",&DAT_00418148);
      uVar3 = __RTC_CheckEsp(extraout_ECX,extraout_EDX);
      uStack8 = 0x41190f;
      uVar3 = __RTC_CheckEsp(extraout_ECX_00,(int)((ulonglong)uVar3 >> 0x20));
      return uVar3;
    }
    if ((&result)[local_c] != PTR_s_TOiZiZtOrYaToUwPnToBsOaOapsyS_00418004[local_c]) break;
    local_c = local_c + 1;
  }
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

检查输入环节简单验证加密后的输入是否等于期望字符串。写出脚本：

```python
str="0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#大写字母加密那里-38的含义，为了取到当前字符在字符集内的索引
print(ord('A')-str.index('A'))
#小写字母同理
print(ord('a')-str.index('a'))
text1='TOiZiZtOrYaToUwPnToBsOaOapsyS'
text2='QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
flag=''
s=0
for i in range(len(text1)):
    if(i%2==0):
        flag+=text1[i] #没加密直接拼上flag
    else:
        s=text2.index(text1[i]) #如果加密了，就找到期望输入在text2的索引，然后就能根据索引找回flag了
        flag+=str[s]
print(flag)
```

最后少了一位，根据flag内容推断是E。

## Flag
> flag{ThisisthreadofwindowshahaIsESE}