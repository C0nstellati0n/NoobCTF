# reverse-for-the-holy-grail-350

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=341d0c26-1acb-4dd8-9c38-830610a1d40d_2)

这题倒是没有什么特殊的知识点，但是我看ghidra真的看不懂啊。

```c++
undefined8 main(void)

{
  int result;
  basic_ostream *pbVar1;
  undefined *local_78 [2];
  undefined auStack104 [16];
  undefined *password [2];
  undefined auStack72 [16];
  undefined *name;
  undefined8 local_30;
  undefined local_28 [24];
  
  name = local_28;
  local_30 = 0;
  local_28[0] = 0;
                    /* try { // try from 00400f5c to 004010f0 has its CatchHandler @ 0040110e */
  std::__ostream_insert<char,std::char_traits<char>>
            ((basic_ostream *)std::cout,"What... is your name?",0x15);
  std::endl<char,std::char_traits<char>>((basic_ostream *)std::cout);
  std::operator>>((basic_istream *)std::cin,(basic_string *)&name);
  std::__ostream_insert<char,std::char_traits<char>>
            ((basic_ostream *)std::cout,"What... is your quest?",0x16);
  std::endl<char,std::char_traits<char>>((basic_ostream *)std::cout);
  std::basic_istream<char,std::char_traits<char>>::ignore();
  std::getline<char,std::char_traits<char>,std::allocator<char>>
            ((basic_istream *)std::cin,(basic_string *)&name);
  std::__ostream_insert<char,std::char_traits<char>>
            ((basic_ostream *)std::cout,"What...  is the secret password?",0x20);
  std::endl<char,std::char_traits<char>>((basic_ostream *)std::cout);
  std::operator>>((basic_istream *)std::cin,(basic_string *)userIn[abi:cxx11]);
  local_78[0] = auStack104;
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::_M_construct<char*>
            ((char *)local_78,userIn[abi:cxx11]._0_8_,
             (int)userIn[abi:cxx11]._0_8_ + (int)userIn[abi:cxx11]._8_8_);
  result = validChars((basic_string)local_78);
  if (local_78[0] != auStack104) {
    operator.delete(local_78[0]);
  }
  if (-1 < result) {
    password[0] = auStack72;
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
    _M_construct<char*>((char *)password,userIn[abi:cxx11]._0_8_,
                        (int)userIn[abi:cxx11]._0_8_ + (int)userIn[abi:cxx11]._8_8_);
    result = stringMod((basic_string)password);
    if (password[0] != auStack72) {
      operator.delete(password[0]);
    }
    if (-1 < result) {
      std::__ostream_insert<char,std::char_traits<char>>
                ((basic_ostream *)std::cout,"Go on. Off you go. tuctf{",0x19);
      pbVar1 = std::__ostream_insert<char,std::char_traits<char>>
                         ((basic_ostream *)std::cout,userIn[abi:cxx11]._0_8_,userIn[abi:cxx11]._8_8_
                         );
      std::__ostream_insert<char,std::char_traits<char>>(pbVar1,"}",1);
      std::endl<char,std::char_traits<char>>(pbVar1);
      goto LAB_004010f1;
    }
  }
  std::__ostream_insert<char,std::char_traits<char>>((basic_ostream *)std::cout,"Auuuuuuuugh",0xb);
  std::endl<char,std::char_traits<char>>((basic_ostream *)std::cout);
LAB_004010f1:
  if (name != local_28) {
    operator.delete(name);
  }
  return 0;
}
```

好吧又是c++。直接看下面，要求result大于-1。稍微往上看一点，result = stringMod((basic_string)password);，也和我们的输入有关系，那关键函数就是stringMod了。

```c++
int stringMod(basic_string param_1)

{
  ulong uVar1;
  long lVar2;
  ulong uVar3;
  uint return_value2;
  int iVar4;
  int iVar5;
  undefined8 *puVar6;
  undefined4 in_register_0000003c;
  undefined8 *puVar7;
  int return_value1;
  int iVar8;
  undefined8 local_60 [9];
  undefined8 local_18;
  
  puVar7 = local_60;
  for (lVar2 = 9; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar7 = 0;
    puVar7 = puVar7 + 1;
  }
  uVar1 = ((long *)CONCAT44(in_register_0000003c,param_1))[1];
  if (uVar1 == 0) {
    return_value1 = 0;
  }
  else {
    lVar2 = *(long *)CONCAT44(in_register_0000003c,param_1);
    uVar3 = 0;
    return_value1 = 0;
    do {
      iVar4 = (int)*(char *)(lVar2 + uVar3);
      *(int *)((long)local_60 + uVar3 * 4) = iVar4;
      if (((int)((uVar3 & 0xffffffff) / 3) * 3 == (int)uVar3) &&
         (iVar4 != *(int *)(firstchar + ((uVar3 & 0xffffffff) / 3) * 4))) {
        return_value1 = -1;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 != uVar1);
  }
  puVar7 = local_60;
  return_value2 = 0x29a;
  puVar6 = puVar7;
  do {
    *(uint *)puVar6 = *(byte *)puVar6 ^ return_value2;
    return_value2 = return_value2 * 2 + ((int)return_value2 / 5) * -5;
    puVar6 = (undefined8 *)((long)puVar6 + 4);
  } while (&local_18 != puVar6);
  iVar8 = 1;
  iVar4 = 0;
  uVar1 = 1;
  iVar5 = 0;
  do {
    if (iVar5 == 2) {
      if (*(uint *)puVar7 != *(uint *)(thirdchar + (long)iVar4 * 4)) {
        return_value1 = -1;
      }
      if ((int)(uVar1 % (ulong)*(uint *)puVar7) != *(int *)(masterArray + (long)iVar4 * 4)) {
        return_value1 = -1;
      }
      iVar4 = iVar4 + 1;
      uVar1 = 1;
      iVar5 = 0;
    }
    else {
      uVar1 = (ulong)((int)uVar1 * *(uint *)puVar7);
      iVar5 = iVar5 + 1;
      if (iVar5 == 3) {
        iVar5 = 0;
      }
    }
    iVar8 = iVar8 + 1;
    puVar7 = (undefined8 *)((long)puVar7 + 4);
  } while (iVar8 != 0x13);
  return return_value1 * return_value2;
}
```

又来。看返回值，return_value1和return_value2之间不能有一个为负数，用这点来切入。查找两个return_value，在第一个do-while循环中发现了它们的身影。

```c
do {
      iVar4 = (int)*(char *)(lVar2 + uVar3);
      *(int *)((long)local_60 + uVar3 * 4) = iVar4;
      if (((int)((uVar3 & 0xffffffff) / 3) * 3 == (int)uVar3) &&
         (iVar4 != *(int *)(firstchar + ((uVar3 & 0xffffffff) / 3) * 4))) {
        return_value1 = -1;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 != uVar1);
```

虽然看不出来iVar4是干啥的，但是可以猜测是输入。逆向题做的越多，越感觉猜是很重要的能力。uVar3应该是索引，因为查看firstchar是一个数组，ghidra把取索引对地址进行相加见怪不怪了。基本可以忽略& 0xffffffff，取低几位，不过uVar3又能有多大呢。然后的判断有点奇怪，要求uVar3/3\*3=uVar3。可以这么想，如果uVar3不能被3整除的话，除以3再乘2因为小数肯定会丢精度，就不等于原来的数字了。跟uVar3%3==0一样。if语句的第二个条件就是简单的比较，如果uVar3被3整除，用uVar3作为索引在firstchar里取值。\*4是因为ghidra里数组的数据隔了4个\x00，ida里看直接就是连着的，不是大问题。

第二个do-while循环虽然也涉及到了return_value，但是没有if这种判断，不是我们能够控制的，不用看。

```c
do {
    if (iVar5 == 2) {
      if (*(uint *)puVar7 != *(uint *)(thirdchar + (long)iVar4 * 4)) {
        return_value1 = -1;
      }
      if ((int)(uVar1 % (ulong)*(uint *)puVar7) != *(int *)(masterArray + (long)iVar4 * 4)) {
        return_value1 = -1;
      }
      iVar4 = iVar4 + 1;
      uVar1 = 1;
      iVar5 = 0;
    }
    else {
      uVar1 = (ulong)((int)uVar1 * *(uint *)puVar7);
      iVar5 = iVar5 + 1;
      if (iVar5 == 3) {
        iVar5 = 0;
      }
    }
    iVar8 = iVar8 + 1;
    puVar7 = (undefined8 *)((long)puVar7 + 4);
  } while (iVar8 != 0x13);
```

这里涉及了两个数组。咱也不知道为什么这次比的又是puVar7了，全靠信念逆向。iVar5初始值是0，第一次会走到else分支。每次iVar5自增1并更新uVar1的值，当iVar5为2时执行if语句里的内容，相信大家都看得懂。大概就是这样，抄[脚本](https://www.cnblogs.com/Auuu/p/14415330.html)。

```python
firstchar = [65, 105, 110, 69, 111, 97]
thirdchar = [751, 708, 732, 711, 734, 764]
masterArray = [471, 12, 580, 606, 147, 108]
flag = [0] * 18
tem = [0] * 18
v7 = 666
for i in range(18):
    tem[i] = v7  # 参与异或的数组
    v7 += v7 % 5
# 第一组
index = 0
for i in range(0, 18, 3):
    flag[i] = firstchar[index]
    index += 1
# 第三组
index = 0
for i in range(2, 18, 3):
    flag[i] = thirdchar[index] ^ tem[i]
    index += 1
# 爆破第二组
index = 0
for i in range(1, 18, 3):
    for j in range(32, 126):
        if (flag[i - 1] ^ tem[i - 1]) * (j ^ tem[i]) % (flag[i + 1] ^ tem[i + 1]) == masterArray[index]:
            flag[i] = j
            index += 1
            break
print('tuctf{', end='')
for i in range(len(flag)):
    print(chr(flag[i]), end='')
print('}', end='')
```

- ### Flag
  > tuctf{AfricanOrEuropean?}