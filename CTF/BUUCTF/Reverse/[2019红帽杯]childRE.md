# [2019红帽杯]childRE

[题目地址](https://buuoj.cn/challenges#[2019%E7%BA%A2%E5%B8%BD%E6%9D%AF]childRE)

为什么我动调不了？

这题就是动调的活，再难的逻辑一个动调搞定。但是我的电脑不知道咋了，运行不了程序，自然就无法动调了。找了个[wp](https://blog.csdn.net/qq_41858371/article/details/103111366)，云做题。

```c++
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  _QWORD *v4; // rax
  const CHAR *v5; // r11
  __int64 v6; // r10
  int v7; // er9
  const CHAR *v8; // r10
  __int64 v9; // rcx
  __int64 v10; // rax
  int result; // eax
  unsigned int v12; // ecx
  __int64 v13; // r9
  __int128 v14[2]; // [rsp+20h] [rbp-38h] BYREF

  v14[0] = 0i64;
  v14[1] = 0i64;
  scanf("%s", v14);
  v3 = -1i64;
  do
    ++v3;
  while ( *((_BYTE *)v14 + v3) );               // 计算v14的长度，结果为v3
  if ( v3 != 31 )                               // 要求输入的长度是31
  {
    while ( 1 )
      Sleep(0x3E8u);
  }
  v4 = sub_7FF6EEF61280(v14);                   // 这个意义不明的函数卡了我好久，后面才知道压根就没用，不用逆向
  v5 = name;
  if ( v4 )
  {
    binary_tree((unsigned __int8 *)v4[1]);      // 构建二叉树，其实完全可以看作将输入有规律地打乱顺序，那么就可以通过动调获取打乱的对应关系
    binary_tree(*(unsigned __int8 **)(v6 + 16));
    v7 = dword_7FF6EEF657E0;
    v5[dword_7FF6EEF657E0] = *v8;
    dword_7FF6EEF657E0 = v7 + 1;
  }
  UnDecorateSymbolName(v5, outputString, 0x100u, 0);// c++函数名反修饰
  v9 = -1i64;
  do
    ++v9;
  while ( outputString[v9] );
  if ( v9 == 62 )
  {
    v12 = 0;
    v13 = 0i64;
    do
    {
      if ( a1234567890Qwer[outputString[v13] % 23] != *(_BYTE *)(v13 + 0x7FF6EEF63478i64) )// 看到这种统一动调看到底是什么
        _exit(v12);
      if ( a1234567890Qwer[outputString[v13] / 23] != *(_BYTE *)(v13 + 0x7FF6EEF63438i64) )
        _exit(v12 * v12);
      ++v12;
      ++v13;
    }
    while ( v12 < 0x3E );
    sub_7FF6EEF61020("flag{MD5(your input)}\n");
    result = 0;
  }
  else
  {
    v10 = sub_7FF6EEF618A0(std::cout);
    std::ostream::operator<<(v10, sub_7FF6EEF61A60);
    result = -1;
  }
  return result;
}
```

c++有个[函数名修饰规则](https://blog.csdn.net/wenqiang1208/article/details/53163788)，这里就是判断反修饰处理后的函数名是否等于指定字符，可通过调试找到是什么字符，或者直接打开strings窗口，两个一看就有问题的都试一下也行。这个比较可以直接爆破，得到是`private: char * __thiscall R0Pxx::My_Aut0_PWN(unsigned char *)`。这是反修饰后的结果，我们还要将其还原为修饰的状态。可以照着刚刚给的链接自己写，或者利用这个办法自动获取修饰结果：

```c++
#include<iostream>
using namespace std;
 
class ROPxx {
public:
	ROPxx(){
		unsigned char a;
		My_Aut0_PWN(&a);
	}
 
private:
	char My_Aut0_PWN(unsigned char*) {
		printf("%s", __FUNCDNAME__);
		return '0';
	}
};
int main() {
	new ROPxx();
	getchar();
	return 0;
}
```

获得修饰结果为`?My_Aut0_PWN@R0Pxx@@AAEPADPAE@Z`。这个就是输入经过二叉树变换的结果。像普通的二叉树变换题根本不需要费劲计算出二叉树，只需要最开始按顺序输入`ABCD...`31个字符，（不同程序可能要输入的不一样，不过都是按顺序的，如果有长度限制的题就把长度限制那里patch掉），断点下在二叉树变换完成那里，查看结果是什么。这个结果就是不同字符的变换对照结果，照着算索引就好了。以下解题脚本来自[此处](https://blog.csdn.net/weixin_52640415/article/details/124669121)。

```python
a1 = b'(_@4620!08!6_0*0442!@186%%0@3=66!!974*3234=&0^3&1@=&0908!6_0*&'
a2 = b'55565653255552225565565555243466334653663544426565555525555222'
a3 = b'1234567890-=!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;\'ASDFGHJKL:"ZXCVBNM<>?zxcvbnm,./'
tmp = ''
for i in range(62):
    for j in range(256):
        if a3[j%23] == a1[i] and a3[j//23] == a2[i]: #爆破获取反修饰结果
            tmp +=chr(j)
            break 
 
print(tmp)
#UnDecorateSymbolName C++反修饰，手工改回
#private: char * __thiscall R0Pxx::My_Aut0_PWN(unsigned char *)
#?My_Aut0_PWN@R0Pxx@@AAEPADPAE@Z
#? + func + @ + class + @@ + private + char * + unsigned char * + @Z 
#A-Z[\]
#交换顺序的加密，动调得到加密顺序表, 在 UnDecorateSymbolName(v5, outputString, 0x100u, 0); 下断点，输入字符31个，得到rcx的值
#'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_
print(bytes([i for i in range(0x41, 0x41+31)]))
#1: rcx 000000013FDB57C0 "PQHRSIDTUJVWKEBXYLZ[MF\\]N^_OGCA"
tab = b"PQHRSIDTUJVWKEBXYLZ[MF\\]N^_OGCA" #动调得到的加密顺序表
c = b'?My_Aut0_PWN@R0Pxx@@AAEPADPAE@Z' #修饰结果
m = [0]*31
for i in range(31):
    m[tab[i]-0x41] = c[i] #转换索引
print(bytes(m))
 
from hashlib import md5
print('flag{'+md5(bytes(m)).hexdigest()+'}')
#flag{63b148e750fed3a33419168ac58083f5}
```

## Flag
> flag{63b148e750fed3a33419168ac58083f5}