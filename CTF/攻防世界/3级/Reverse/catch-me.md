# catch-me

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=9b71a8c3-63dd-440c-84a4-73efc7fa70f6_2)

我裂开了，每次做reverse我都要说一遍。

给的附件很奇怪啊，两层压缩包，第一个还没有后缀。导入ghidra时提示后才知道。给文件价格后缀xz就能直接gzip解了。然后里面还有个tar，解了。最后才是个elf。

```c
undefined8 Main(void)

{
  undefined auVar1 [13];
  undefined auVar2 [16];
  undefined auVar3 [16];
  undefined8 uVar4;
  uint uVar5;
  char *pcVar6;
  uint *puVar7;
  long lVar8;
  undefined4 *puVar9;
  uint uVar10;
  uint5 uVar11;
  byte bVar15;
  uint uVar16;
  uint uVar17;
  uint uVar18;
  ushort uVar22;
  ushort uVar23;
  byte bVar24;
  uint uVar25;
  ushort uVar31;
  unkuint10 Var28;
  unkuint10 Var29;
  undefined auVar26 [16];
  unkuint10 Var30;
  unkuint10 Var32;
  ulong uVar12;
  undefined auVar13 [12];
  undefined auVar14 [14];
  uint5 uVar19;
  undefined auVar20 [12];
  undefined auVar21 [15];
  undefined auVar27 [13];
  
  uVar5 = FUN_00400820(DAT_006012b4);
  DAT_006012a8 = (undefined)(uVar5 >> 0x18);
  DAT_006012a9 = (byte)(uVar5 >> 0x10) & 0xfd;
  DAT_006012aa = (byte)(uVar5 >> 8) & 0xdf;
  DAT_006012ab = (byte)uVar5 & 0xbf;
  pcVar6 = getenv("ASIS");
  if (pcVar6 != (char *)0x0) {
    puVar7 = (uint *)getenv("CTF");
    if ((uVar5 ^ *puVar7) == 0xfeebfeeb) {
      puVar9 = (undefined4 *)getenv("ASIS");
      _DAT_006012ac = *puVar9;
    }
  }
  lVar8 = 0;
  do {
    flag[lVar8] = flag[lVar8] ^ (&DAT_006012a8)[(uint)lVar8 & 7];
    lVar8 = lVar8 + 1;
  } while (lVar8 != 0x21);
  uVar4 = CONCAT44(flag._4_4_,flag._0_4_);
  auVar13 = CONCAT48(flag._8_4_,uVar4);
  auVar3 = CONCAT97((unkuint9)
                    (SUB158(CONCAT78(SUB157(CONCAT69(SUB156(CONCAT510(SUB155(CONCAT411(SUB154(
                                                  CONCAT312(SUB153(CONCAT213(SUB152(CONCAT114((char)
                                                  ((uint)flag._4_4_ >> 0x18),
                                                  ZEXT1314(SUB1613(CONCAT412(flag._12_4_,auVar13),0)
                                                          )) >> 0x68,0),
                                                  CONCAT112((char)((uint)flag._4_4_ >> 0x10),auVar13
                                                           )) >> 0x60,0),auVar13) >> 0x58,0),
                                                  CONCAT110((char)((uint)flag._4_4_ >> 8),
                                                            SUB1210(auVar13,0))) >> 0x50,0),
                                                  (unkuint10)SUB129(auVar13,0)) >> 0x48,0),
                                                  CONCAT18((char)flag._4_4_,uVar4)) >> 0x40,0),uVar4
                                    ) >> 0x38,0) & 0xff) &
                    SUB169((undefined  [16])0xffffffffffffffff >> 0x38,0),
                    ((uint7)uVar4 >> 0x18) << 0x30) & (undefined  [16])0xffff000000000000;
  auVar26 = CONCAT115(SUB1611(auVar3 >> 0x28,0),((uint5)uVar4 >> 0x10) << 0x20) &
            (undefined  [16])0xffffffff00000000;
  auVar2 = CONCAT142(SUB1614(CONCAT133(SUB1613(auVar26 >> 0x18,0),((uint3)flag._0_4_ >> 8) << 0x10)
                             >> 0x10,0),(short)flag._0_4_) & (undefined  [16])0xffffffffffff00ff;
  uVar5 = (uint)CONCAT12((char)((uint)flag._8_4_ >> 8),(ushort)(byte)flag._8_4_);
  uVar11 = CONCAT14((char)((uint)flag._8_4_ >> 0x10),uVar5);
  uVar12 = (ulong)CONCAT16((char)((uint)flag._8_4_ >> 0x18),(uint6)uVar11);
  auVar13 = ZEXT1112(CONCAT110((char)((uint)flag._12_4_ >> 8),
                               (unkuint10)CONCAT18((char)flag._12_4_,uVar12)));
  auVar14 = ZEXT1314(CONCAT112((char)((uint)flag._12_4_ >> 0x10),auVar13));
  bVar15 = (byte)((uint)flag._12_4_ >> 0x18);
  uVar16 = (uint)SUB162(auVar3 >> 0x40,0);
  auVar20 = ZEXT1012(CONCAT28(SUB162(auVar3 >> 0x60,0),
                              (ulong)CONCAT24(SUB162(auVar3 >> 0x50,0),uVar16)));
  uVar23 = SUB162(auVar3 >> 0x70,0);
  Var28 = (unkuint10)
          SUB148(CONCAT68(SUB146(CONCAT410(SUB144(CONCAT212(SUB162(auVar3 >> 0x30,0),
                                                            SUB1612(auVar2,0)) >> 0x50,0),
                                           CONCAT28(SUB162(auVar26 >> 0x20,0),SUB168(auVar2,0))) >>
                                 0x40,0),SUB168(auVar2,0)) >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0);
  uVar10 = (uint)SUB142(auVar14 >> 0x40,0);
  auVar1 = CONCAT112(bVar15,ZEXT1012(CONCAT28(SUB162(ZEXT1516(CONCAT114(bVar15,auVar14)) >> 0x60,0),
                                              (ulong)CONCAT24(SUB162(ZEXT1516(CONCAT114(bVar15,
                                                  auVar14)) >> 0x50,0),uVar10))));
  Var29 = (unkuint10)
          SUB148(CONCAT68(SUB146(CONCAT410(SUB144(CONCAT212(SUB142(auVar14 >> 0x30,0),auVar13) >>
                                                  0x50,0),CONCAT28(SUB122(auVar13 >> 0x20,0),uVar12)
                                          ) >> 0x40,0),uVar12) >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0);
  uVar4 = CONCAT44(flag._20_4_,flag._16_4_);
  auVar26 = CONCAT88(flag._24_8_,uVar4);
  uVar17 = (uint)CONCAT12((char)((ulong)flag._24_8_ >> 8),(ushort)(byte)flag._24_8_);
  uVar19 = CONCAT14((char)((ulong)flag._24_8_ >> 0x10),uVar17);
  uVar12 = (ulong)CONCAT16((char)((ulong)flag._24_8_ >> 0x18),(uint6)uVar19);
  auVar13 = ZEXT1112(CONCAT110((char)((ulong)flag._24_8_ >> 0x28),
                               (unkuint10)CONCAT18((char)((ulong)flag._24_8_ >> 0x20),uVar12)));
  auVar14 = ZEXT1314(CONCAT112((char)((ulong)flag._24_8_ >> 0x30),auVar13));
  bVar24 = (byte)((ulong)flag._24_8_ >> 0x38);
  auVar21 = CONCAT114(bVar24,auVar14);
  auVar27 = SUB1613(CONCAT124(SUB1612(CONCAT115(SUB1611(CONCAT106(SUB1610(CONCAT97((unkuint9)
                                                                                   SUB158(CONCAT78(
                                                  SUB157(CONCAT69(SUB156(CONCAT510(SUB155(CONCAT411(
                                                  SUB154(CONCAT312(SUB153(CONCAT213(SUB152(CONCAT114
                                                  ((char)((uint)flag._20_4_ >> 0x18),
                                                   SUB1614(auVar26,0)) >> 0x68,0),
                                                  CONCAT112((char)((uint)flag._20_4_ >> 0x10),
                                                            SUB1612(auVar26,0))) >> 0x60,0),
                                                  SUB1612(auVar26,0)) >> 0x58,0),
                                                  CONCAT110((char)((uint)flag._20_4_ >> 8),
                                                            SUB1610(auVar26,0))) >> 0x50,0),
                                                  SUB1610(auVar26,0)) >> 0x48,0),
                                                  CONCAT18((char)flag._20_4_,uVar4)) >> 0x40,0),
                                                  uVar4) >> 0x38,0) &
                                                  SUB169((undefined  [16])0xffffffffffffffff >> 0x38
                                                         ,0) &
                                                  SUB169((undefined  [16])0xffffffffffffffff >> 0x38
                                                         ,0) &
                                                  SUB169((undefined  [16])0xffffffffffffffff >> 0x38
                                                         ,0) &
                                                  SUB169((undefined  [16])0xffffffffffffffff >> 0x38
                                                         ,0),((uint7)uVar4 >> 0x18) << 0x30) >> 0x30
                                                  ,0),(int6)uVar4) >> 0x28,0) &
                                                SUB1611((undefined  [16])0xffff00ffffffffff >> 0x28,
                                                        0),((uint5)uVar4 >> 0x10) << 0x20) >> 0x20,0
                                     ),flag._16_4_) >> 0x18,0) &
            SUB1613((undefined  [16])0xffffffff00ffffff >> 0x18,0);
  auVar26 = CONCAT142(SUB1614(CONCAT133(auVar27,((uint3)flag._16_4_ >> 8) << 0x10) >> 0x10,0),
                      (short)flag._16_4_) & (undefined  [16])0xffffffffffff00ff;
  uVar25 = (uint)SUB132(auVar27 >> 0x28,0);
  uVar31 = SUB132(auVar27 >> 0x48,0);
  Var32 = (unkuint10)
          SUB148(CONCAT68(SUB146(CONCAT410(SUB144(CONCAT212(SUB162(auVar26 >> 0x30,0),
                                                            SUB1612(auVar26,0)) >> 0x50,0),
                                           CONCAT28(SUB162(auVar26 >> 0x20,0),SUB168(auVar26,0))) >>
                                 0x40,0),SUB168(auVar26,0)) >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0);
  uVar18 = (uint)SUB142(auVar14 >> 0x40,0);
  uVar22 = (ushort)((unkuint10)SUB159(auVar21 >> 0x30,0) >> 0x30);
  Var30 = (unkuint10)
          SUB148(CONCAT68(SUB146(CONCAT410(SUB144(CONCAT212(SUB142(auVar14 >> 0x30,0),auVar13) >>
                                                  0x50,0),CONCAT28(SUB122(auVar13 >> 0x20,0),uVar12)
                                          ) >> 0x40,0),uVar12) >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0) &
          SUB1610((undefined  [16])0xffffffffffffffff >> 0x30,0);
  if (uVar10 + uVar16 + (SUB164(auVar2,0) & 0xffff) + (uVar5 & 0xffff) +
      (SUB164(auVar26,0) & 0xffff) + uVar25 + (uVar17 & 0xffff) + uVar18 +
      SUB124(ZEXT912(SUB139(auVar1 >> 0x20,0)) >> 0x20,0) +
      SUB164(ZEXT1416(CONCAT212(uVar23,auVar20)) >> 0x40,0) + (int)(Var28 >> 0x10) +
      (int)(Var29 >> 0x10) + (int)(Var32 >> 0x10) + (uint)uVar31 + (int)(Var30 >> 0x10) +
      (uint)uVar22 +
      SUB164(ZEXT1316(auVar1) >> 0x20,0) +
      SUB124(auVar20 >> 0x20,0) +
      SUB164(CONCAT106(Var28,(SUB166(auVar2,0) >> 0x10) << 0x20) >> 0x20,0) +
      SUB164(CONCAT106(Var29,(uint6)(uVar11 >> 0x10) << 0x20) >> 0x20,0) +
      SUB164(CONCAT106(Var32,(SUB166(auVar26,0) >> 0x10) << 0x20) >> 0x20,0) +
      SUB124(ZEXT1012(CONCAT28(uVar31,(ulong)CONCAT24(SUB132(auVar27 >> 0x38,0),uVar25))) >> 0x20,0)
      + SUB164(CONCAT106(Var30,(uint6)(uVar19 >> 0x10) << 0x20) >> 0x20,0) +
      SUB124(ZEXT1012(CONCAT28(uVar22,(ulong)CONCAT24(SUB142(ZEXT1314(SUB1513(auVar21 >> 0x10,0)) >>
                                                             0x40,0),uVar18))) >> 0x20,0) +
      (uint)bVar15 + (uint)uVar23 + (int)(Var28 >> 0x30) + (int)(Var29 >> 0x30) +
      (int)(Var32 >> 0x30) + (uint)SUB132(auVar27 >> 0x58,0) + (int)(Var30 >> 0x30) + (uint)bVar24
      != 0x954) {
    flag._0_4_ = 0x5f646162;
    flag._4_4_ = 0x5f646162;
    flag._8_4_ = 0x5f646162;
    flag._12_4_ = 0x5f646162;
    flag._16_4_ = 0x5f646162;
    flag._20_4_ = 0x646162;
  }
  printf("Flag: ASIS{%s}\n",flag);
  pcVar6 = strstr(flag,"bad_");
  if (pcVar6 != (char *)0x0) {
    puts("this flag is absolutely fake ");
  }
  return 0;
}
```

……一时间不知道说啥。不过发现末尾的flag还是很简单的。此处积累了ghidra中做数组的方法。这里本来flag是几个不同名字的数据但是物理相邻，flag本身肯定不止1个字节这么长，推测全部数据都是flag。选中你觉得是连续数据的数据，右键后选择Data->Create Array。这样flag在函数内的调用就清晰很多了。不过这个方法仅适用于栈上数据，在当前函数栈帧的变量不行。

主要逻辑看不出来是什么玩意。函数本身没有发现任何输入函数，看来需要动态调试。这里就是ghidra和ida天差地别的地方了。在ida中可以看见中途没动过flag，但是ghidra中间乱七八糟的函数疯狂引用flag。还好开头最重要的逻辑没有乱。getenv("ASIS")不能为0，getenv("CTF")异或uVar5的值要等于0xfeebfeeb，uVar5的值可以调试得到，那我们就能知道CTF应该有的值。ASIS不知道了，理论上应该爆破，但我看[wp](https://blog.csdn.net/xiao__1bai/article/details/120518638)是猜的。啊，这也可以吗，关键还猜对了，两个环境变量的值一样。那设置一下。

```bash
export ASIS="$(printf "\x0a\xda\xf2\x4f")"
export CTF="$(printf "\x0a\xda\xf2\x4f")"
```

[export](https://www.runoob.com/linux/linux-comm-export.html)设置环境变量，就喝python里赋值一样一样的。[$](https://www.yisu.com/zixun/132163.html)在linux中有大用途，这里用来命令替换，执行括号或者反引号中的命令。里面是printf，通过printf可以导入16进制整数类型。然后运行脚本就直接出来了。

也可以自己写脚本逆向，个人感觉不是很有必要，不过做补充练习逆向能力还是不错的。

### Flag
- ASIS{600d_j0b_y0u_4r3_63771n6_574r73d}