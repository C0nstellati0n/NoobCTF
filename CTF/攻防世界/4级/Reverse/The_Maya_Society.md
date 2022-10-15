# The_Maya_Society

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=601464fa-1e39-4f8d-bc33-a003c847dad7_2)

这题给了个逆向新思路，猜初始内容。

附件是网页的源码，最开始没看出来逆向什么，然后发现一个无后缀的launcher文件，放进ghidra看看。

```c
undefined8 Main(void)

{
  size_t sVar1;
  size_t sVar2;
  undefined8 uVar3;
  time_t time;
  undefined8 str1;
  undefined8 str2;
  undefined local_118;
  char local_108 [32];
  char format_time [104];
  undefined8 local_80;
  char local_74 [9];
  char local_6b [9];
  char local_62 [9];
  char local_59 [9];
  code *local_50;
  long local_48;
  char *local_40;
  char *local_38;
  undefined1 *local_30;
  size_t local_28;
  tm *local_time;
  
  str1 = 0x6e696678756c662e;
  str2 = 0x74656e2e73726567;
  local_118 = 0;
  time = ::time((time_t *)0x0);
  local_time = localtime(&time);
  strftime(format_time,99,"%Y-%m-%d",local_time);
  local_28 = strlen(format_time);
  uVar3 = 0x101ab5;
  Md5(format_time,local_28);
  local_30 = &DAT_003030b8;
  snprintf(local_59,9,"%02x%02x%02x%02x",(ulong)DAT_003030b8,(ulong)DAT_003030b9,(ulong)DAT_003030ba
           ,(ulong)DAT_003030bb,uVar3);
  local_30 = &DAT_003030c0;
  snprintf(local_62,9,"%02x%02x%02x%02x",(ulong)DAT_003030c0,(ulong)DAT_003030c1,(ulong)DAT_003030c2
           ,(ulong)DAT_003030c3);
  local_30 = &DAT_003030b4;
  snprintf(local_6b,9,"%02x%02x%02x%02x",(ulong)DAT_003030b4,(ulong)DAT_003030b5,(ulong)DAT_003030b6
           ,(ulong)DAT_003030b7);
  local_30 = &DAT_003030bc;
  snprintf(local_74,9,"%02x%02x%02x%02x",(ulong)DAT_003030bc,(ulong)DAT_003030bd,(ulong)DAT_003030be
           ,(ulong)DAT_003030bf);
  snprintf(local_108,0x21,"%s%s%s%s",local_59,local_62,local_6b,local_74);
  sVar1 = strlen(local_108);
  sVar2 = strlen((char *)&str1);
  local_38 = (char *)malloc(sVar2 + sVar1 + 1);
  if (local_38 == (char *)0x0) {
    uVar3 = 1;
  }
  else {
    *local_38 = '\0';
    strcat(local_38,local_108);
    strcat(local_38,(char *)&str1);
    local_40 = (char *)FUN_001018a4(local_38);
    if (local_40 == (char *)0x0) {
      uVar3 = 1;
    }
    else {
      sVar1 = strlen(local_40);
      local_48 = FUN_001015e0(local_40,sVar1,&local_80);
      sVar1 = strlen(local_40);
      local_50 = (code *)FUN_001015e0(local_40,sVar1,&local_80);
      if (local_48 == 0) {
        uVar3 = 1;
      }
      else {
        FUN_00101858(local_48,local_80,local_50);
        (*local_50)();
        uVar3 = 0;
      }
    }
  }
  return uVar3;
}
```

之前一直习惯那种给flag判断对不对的程序的逆向，所以这次找关键if语句时啥也没找到。查看字符串，也没啥东西。好吧直接分析。

开始的str1和str2换端序并转hex得到.fluxfingers.net。然后time得到时间戳，[local_time](https://www.runoob.com/cprogramming/c-function-localtime.html)转当前时间，[strftime](https://www.runoob.com/cprogramming/c-function-strftime.html)格式化时间。Md5函数内部很复杂，不可能分析得出来，通过识别md5加密的[特征](https://blog.csdn.net/weixin_44767965/article/details/122305570)猜测是md5函数。在ida里可以清楚地看到最开始有初始化了4个变量，这就是特征。

接下来一堆snprintf不知道是什么东西，查很多[wp](https://www.cnblogs.com/Mayfly-nymph/p/11594407.html)也没找到答案。跟着wp走，说是把md5的结果和.fluxfingers.net做拼接（我在ghidra里根本就没看见str2的引用，local_108也是）。接着经过FUN_001018a4做一堆看不懂的处理，不放了后面会知道根本不用逆。FUN_001015e0是base64解密，以后在函数内部发现base64编码表的很大概率是base64编码，解码还是编码需要进一步判断。

```c
void FUN_00101858(long param_1,ulong param_2,long param_3)

{
  ulong i;
  
  for (i = 0; i < param_2; i = i + 1) {
    *(byte *)(i + param_3) = *(byte *)(i + param_1) ^ 0x25;
  }
  return;
}
```

这个函数就是简单异或。分析完后发现根本就没有逆向入手点，所以这题有点脑洞题的意思。说到玛雅文明你会想到什么？那个著名的预言？程序内部调用了当前时间，那我们就把当前时间[修改](https://blog.csdn.net/modi000/article/details/119352867)为2012-12-21，运行就能得到flag了。嗯就是这么草率。

- ### Flag
  > flag{e3a03c6f3fe91b40eaa8e71b41f0db12}