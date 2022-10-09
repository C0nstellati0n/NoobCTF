# crazy

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=96151fca-0a20-4436-859a-2c1da1dfca5e_2&task_category_id=4)

竟然还有C++，我去这是第几种语言了？

```c++
undefined8 main(void)

{
  int iVar1;
  basic_ostream *pbVar2;
  long in_FS_OFFSET;
  basic_string input [8];
  basic_string local_118 [8];
  basic_string<char,std::char_traits<char>,std::allocator<char>> local_f8 [32];
  basic_string<char,std::char_traits<char>,std::allocator<char>> local_d8 [32];
  basic_string local_b8 [8];
  HighTemplar local_98 [120];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string();
                    /* try { // try from 004014c4 to 004015a5 has its CatchHandler @ 004017d7 */
  std::operator>>((basic_istream *)std::cin,input);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"-------------------------------------------")
  ;
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"Quote from people\'s champ");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"-------------------------------------------")
  ;
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,
                           "*My goal was never to be the loudest or the craziest. It was to be the m ost entertaining."
                          );
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"*Wrestling was like stand-up comedy for me.")
  ;
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,
                           "*I like to use the hard times in the past to motivate me today.");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"-------------------------------------------")
  ;
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  HighTemplar::HighTemplar(local_98,input);
  pbVar2 = std::operator<<((basic_ostream *)std::cout,"Checking....");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
             std::endl<char,std::char_traits<char>>);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            (local_118);
  func1((basic_string)local_f8);
  func2((basic_string)local_d8);
  func3((basic_string)local_d8,0);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
            (local_d8);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
            (local_f8);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
            ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)local_118);
  HighTemplar::calculate(local_98);
  iVar1 = HighTemplar::getSerial(local_98);
  if (iVar1 == 0) {
    pbVar2 = std::operator<<((basic_ostream *)std::cout,"/////////////////////////////////");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
               std::endl<char,std::char_traits<char>>);
    pbVar2 = std::operator<<((basic_ostream *)std::cout,"Do not be angry. Happy Hacking :)");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
               std::endl<char,std::char_traits<char>>);
    pbVar2 = std::operator<<((basic_ostream *)std::cout,"/////////////////////////////////");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
               std::endl<char,std::char_traits<char>>);
    HighTemplar::getFlag[abi:cxx11]((HighTemplar *)local_b8);
    pbVar2 = std::operator<<((basic_ostream *)std::cout,"flag{");
    pbVar2 = std::operator<<(pbVar2,local_b8);
    pbVar2 = std::operator<<(pbVar2,"}");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar2,
               std::endl<char,std::char_traits<char>>);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
              ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)local_b8);
  }
  HighTemplar::~HighTemplar(local_98);
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
            ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)input);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

这就是C++吗，我看不懂但我大受震撼。从运行结果入手，先输入flag，再打印一些内容，然后checking，然后too short or too long。说明接收输入在打印之前。不过靠猜不能完全确定，查了一下，[cin](https://blog.csdn.net/qq_38193597/article/details/70158564)果然是C++中的一种接收输入函数。正好都查一下，[cout](https://www.runoob.com/cplusplus/cpp-basic-input-output.html)是输出流。在main中搜索，发现了checking，但是没有too short or too long，全局搜索，在calculate函数中发现了想要的字符串。

```c++
void __thiscall HighTemplar::calculate(HighTemplar *this)

{
  long lVar1;
  basic_ostream *this_00;
  ulong uVar2;
  char *pcVar3;
  byte *pbVar4;
  int local_20;
  int local_1c;
  
  lVar1 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
  if (lVar1 != 0x20) {
    this_00 = std::operator<<((basic_ostream *)std::cout,"Too short or too long");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)this_00,
               std::endl<char,std::char_traits<char>>);
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  local_20 = 0;
  while( true ) {
    uVar2 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
    if (uVar2 < (ulong)(long)local_20) break;
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    pbVar4 = (byte *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    *pcVar3 = (*pbVar4 ^ 0x50) + 0x17;
    local_20 = local_20 + 1;
  }
  local_1c = 0;
  while( true ) {
    uVar2 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
    if (uVar2 < (ulong)(long)local_1c) break;
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    pbVar4 = (byte *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    *pcVar3 = (*pbVar4 ^ 0x13) + 0xb;
    local_1c = local_1c + 1;
  }
  return;
}
```

在main函数if判断前还有最后一个函数。

```c++
undefined4 __thiscall HighTemplar::getSerial(HighTemplar *this)

{
  char cVar1;
  ulong uVar2;
  char *pcVar3;
  basic_ostream *pbVar4;
  basic_ostream<char,std::char_traits<char>> *pbVar5;
  int local_1c;
  
  local_1c = 0;
  do {
    uVar2 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
    if (uVar2 <= (ulong)(long)local_1c) {
LAB_00401b83:
      return *(undefined4 *)(this + 0xc);
    }
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x50));
    cVar1 = *pcVar3;
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    if (cVar1 != *pcVar3) {
      pbVar4 = std::operator<<((basic_ostream *)std::cout,"You did not pass ");
      pbVar5 = (basic_ostream<char,std::char_traits<char>> *)
               std::basic_ostream<char,std::char_traits<char>>::operator<<
                         ((basic_ostream<char,std::char_traits<char>> *)pbVar4,local_1c);
      std::basic_ostream<char,std::char_traits<char>>::operator<<
                (pbVar5,std::endl<char,std::char_traits<char>>);
      *(undefined4 *)(this + 0xc) = 1;
      goto LAB_00401b83;
    }
    pbVar4 = std::operator<<((basic_ostream *)std::cout,"Pass ");
    pbVar5 = (basic_ostream<char,std::char_traits<char>> *)
             std::basic_ostream<char,std::char_traits<char>>::operator<<
                       ((basic_ostream<char,std::char_traits<char>> *)pbVar4,local_1c);
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              (pbVar5,std::endl<char,std::char_traits<char>>);
    local_1c = local_1c + 1;
  } while( true );
}
```

这个函数应该是比较函数，比较cVar1和pcVar3两处的值。然而，这两个引用都不是直接引用，我们要找到this + 0x50和this + 0x10到底是什么东西。可以猜测一个跟输入有关，一个是期望值。那先找找input在别的函数中的引用。

```c++
void __thiscall HighTemplar::HighTemplar(HighTemplar *this,basic_string *param_1)

{
  long in_FS_OFFSET;
  allocator<char> local_21;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  DarkTemplar::DarkTemplar((DarkTemplar *)this);
  *(undefined ***)this = &PTR_getSerial_00401ea0;
  *(undefined4 *)(this + 0xc) = 0;
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            ((basic_string *)(this + 0x10));
                    /* try { // try from 004018da to 004018de has its CatchHandler @ 00401946 */
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            ((basic_string *)(this + 0x30));
  std::allocator<char>::allocator();
                    /* try { // try from 00401902 to 00401906 has its CatchHandler @ 00401925 */
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            ((char *)(this + 0x50),(allocator *)"327a6c4304ad5938eaf0efb6cc3e53dc");
  std::allocator<char>::~allocator(&local_21);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

出现了this + 0x50和this + 0x10。this+0x50是"327a6c4304ad5938eaf0efb6cc3e53dc"，但this+0x10是什么没有明确发现（其实就是输入，ida里可以看见）。根据之前的推断，猜测是输入。那calcualte函数里就知道在干什么了，是主要加密函数。但是我真的完全看不懂c++啊，连最基本的异或加密都不懂怎么逆向。看了老半天才意识到这两个while循环是把input加密放成两次做。

```c++
while( true ) {
    uVar2 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
    if (uVar2 < (ulong)(long)local_20) break;
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    pbVar4 = (byte *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    *pcVar3 = (*pbVar4 ^ 0x50) + 0x17;
    local_20 = local_20 + 1;
  }
  local_1c = 0;
  while( true ) {
    uVar2 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length();
    if (uVar2 < (ulong)(long)local_1c) break;
    pcVar3 = (char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    pbVar4 = (byte *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
                     operator[]((ulong)(this + 0x10));
    *pcVar3 = (*pbVar4 ^ 0x13) + 0xb;
    local_1c = local_1c + 1;
  }
```

pcVar3和pbVar4都是input的指针，每次更改其中一个另一个的值在下次循环也会变。举个例子，\*pcVar3 = (\*pbVar4 ^ 0x50) + 0x17;这行代码表示将input中的一个字符异或0x50再加上0x17，然后赋值给自己，相当于flag[i]=ord(flag[i])^0x50+0x17。两个for循环就是把类似的内容来了两遍。逆向时倒过来做就好了。

```python
data="327a6c4304ad5938eaf0efb6cc3e53dc"
flag=''
for i in data:
    flag+=chr((((ord(i)-0xb)^0x13)-0x17)^0x50)
print(flag)
```

这个flag长的可真奇怪。

- ### Flag
  > flag{tMx~qdstOs~crvtwb~aOba}qddtbrtcd}