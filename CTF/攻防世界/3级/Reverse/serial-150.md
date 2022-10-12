# serial-150

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f20b3534-d15a-43d1-acd7-b450cf4049d0_2&task_category_id=4)

曾经参加比赛的时候做过一道很简单的花指令题，发现ghidra无需去除花指令就能反汇编出逻辑。当时以为是因为花指令太简单了，没想到这题也是这样的，那就给ghidra玩家们提供一个捷径吧。

进入main函数，什么玩意看起来不太对劲。

```c++
undefined8 main(void)

{
  long lVar1;
  char unaff_BH;
  char *pcVar2;
  undefined8 *puVar3;
  undefined1 *puVar4;
  char local_208;
  char cStack519;
  char cStack518;
  char cStack517;
  char cStack516;
  char cStack515;
  char cStack514;
  char cStack513;
  char cStack512;
  char cStack511;
  char cStack510;
  char cStack509;
  char cStack508;
  char cStack507;
  char cStack506;
  char cStack505;
  undefined8 local_108 [32];
  
  puVar3 = (undefined8 *)&local_208;
  for (lVar1 = 0x20; lVar1 != 0; lVar1 = lVar1 + -1) {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  }
  puVar3 = local_108;
  for (lVar1 = 0x20; lVar1 != 0; lVar1 = lVar1 + -1) {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  }
  pcVar2 = "Please Enter the valid key!\n";
  puVar4 = std::cout;
  func_0x404db6a6();
  ((basic_ostream *)puVar4)[0x6013e0] =
       (basic_ostream)((char)((basic_ostream *)puVar4)[0x6013e0] + unaff_BH);
                    /* try { // try from 004009ee to 00400c92 has its CatchHandler @ 00400ca3 */
  std::operator<<((basic_ostream *)puVar4,pcVar2);
                    /* WARNING: Bad instruction - Truncating control flow here */
  func_0x00400860(std::cin);
                    /* WARNING: Bad instruction - Truncating control flow here */
  lVar1 = func_0x00400850();
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
  if (((((((lVar1 == 0x10) && (local_208 == 'E')) && (cStack505 == 'V')) &&
        ((cStack519 == 'Z' && (cStack506 == 'A')))) &&
       ((cStack518 == '9' && ((cStack507 == 'b' && (cStack517 == 'd')))))) && (cStack508 == '7')) &&
     ((((cStack516 == 'm' && (cStack509 == 'G')) && (cStack515 == 'q')) &&
      (((cStack510 == '9' && (cStack514 == '4')) &&
       ((cStack511 == 'g' && ((cStack513 == 'c' && (cStack512 == '8')))))))))) {
    std::operator<<((basic_ostream *)std::cout,"Serial number is valid :)\n");
  }
  else {
    pcVar2 = "Serial number is not valid!\n";
    puVar4 = std::cout;
    func_0x404df146();
    ((basic_ostream *)puVar4)[0x6013e0] =
         (basic_ostream)((char)((basic_ostream *)puVar4)[0x6013e0] + unaff_BH);
    std::operator<<((basic_ostream *)puVar4,pcVar2);
  }
  return 0;
}
```

这么多warning你说没事我都不信。应该不是壳的原因，因为加了壳的程序不脱壳反编译出来比这还糟，字符串查看不了，更不可能有下面的逻辑。查看程序内定义的字符串，发现“Serial number is valid :) ”，却没找到引用。程序里函数倒是很少，猜测也在main函数中，只是因为某些原因没出来。在main函数的栈上划拉划拉，一堆看起来像数据的东西挤满了栈。但这是不可能的，记住函数栈帧上绝对不会有数据（至少我做了一些题发现是这样的），只可能有关于数据的引用。那么这些数据一定是未反编译出来的指令。ghidra里直接选中这些问号数据，右键选择disassemble，就能把原本的指令反编译出来了。完全反编译后选中main函数。

```c++
undefined8 main(void)

{
  size_t sVar1;
  long lVar2;
  char unaff_BH;
  char *pcVar3;
  undefined8 *puVar4;
  undefined1 *puVar5;
  undefined8 local_208;
  char cStack512;
  char cStack511;
  char cStack510;
  char cStack509;
  char cStack508;
  char cStack507;
  char cStack506;
  char cStack505;
  undefined8 local_108 [32];
  
  puVar4 = &local_208;
  for (lVar2 = 0x20; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  }
  puVar4 = local_108;
  for (lVar2 = 0x20; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  }
  pcVar3 = "Please Enter the valid key!\n";
  puVar5 = std::cout;
  func_0x404db6a6();
  ((basic_ostream *)puVar5)[0x6013e0] =
       (basic_ostream)((char)((basic_ostream *)puVar5)[0x6013e0] + unaff_BH);
                    /* try { // try from 004009ee to 00400c92 has its CatchHandler @ 00400ca3 */
  std::operator<<((basic_ostream *)puVar5,pcVar3);
                    /* WARNING: Bad instruction - Truncating control flow here */
  std::operator>>((basic_istream *)std::cin,(char *)&local_208);
                    /* WARNING: Bad instruction - Truncating control flow here */
  sVar1 = strlen((char *)&local_208);
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
                    /* WARNING: Bad instruction - Truncating control flow here */
  if (((((((sVar1 == 0x10) && ((char)local_208 == 'E')) && (cStack505 == 'V')) &&
        ((local_208._1_1_ == 'Z' && (cStack506 == 'A')))) &&
       ((local_208._2_1_ == '9' && ((cStack507 == 'b' && (local_208._3_1_ == 'd')))))) &&
      (cStack508 == '7')) &&
     ((((local_208._4_1_ == 'm' && (cStack509 == 'G')) && (local_208._5_1_ == 'q')) &&
      (((cStack510 == '9' && (local_208._6_1_ == '4')) &&
       ((cStack511 == 'g' && ((local_208._7_1_ == 'c' && (cStack512 == '8')))))))))) {
    std::operator<<((basic_ostream *)std::cout,"Serial number is valid :)\n");
  }
  else {
    pcVar3 = "Serial number is not valid!\n";
    puVar5 = std::cout;
    func_0x404df146();
    ((basic_ostream *)puVar5)[0x6013e0] =
         (basic_ostream)((char)((basic_ostream *)puVar5)[0x6013e0] + unaff_BH);
    std::operator<<((basic_ostream *)puVar5,pcVar3);
  }
  return 0;
}
```

虽然warning还是有，但是Serial number is valid :)出现了，那么这个字符串所在的if语句就是我们的目标，看一下，不难知道是简单到不能再简单的单字符比对。std::operator>>((basic_istream *)std::cin,(char *)&local_208); 是获取输入，cin是c++中获取输入的函数，那么local_208对应我们的输入。在if语句里关注local_208，能恢复一半的serial number：EZ9dmq4c。

剩下半部分没有那么明显，比对的是cStack512到cStack505。好像和输入没关系，但是我们能发现这些内容在栈上和输入是挨着的，且根据sVar1 = strlen((char *)&local_208); 可以知道sVar1是正确serial number的长度，应该是0x10，可local_208明显没有那么长，意味着会往下溢出。按溢出顺序看正好是cStack512到cStack505，那我们就看看这些变量的值是什么，由此恢复剩下半部分serial number。

- ### Flag
  > EZ9dmq4c8g9G7bAV 