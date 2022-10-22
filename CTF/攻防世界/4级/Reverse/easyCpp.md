# easyCpp

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a36448b8-c929-42da-aaa0-2b2a7e6e0d6a_2)

不会吧，不会学到最后连c++也要会吧？

看到题目想了一下，cpp是什么东西？意识到是c++，c plus plus。这题各位看ida吧，ghidra里面编译得没有花指令胜似花指令，压根没反编译出来，强行编译的函数名都是乱七八糟的。放[wp](https://blog.csdn.net/weixin_45055269/article/details/105876587)。

这题用了c++的[stl](http://c.biancheng.net/view/6557.html)，标准模板库。出现了函数[push_back](https://blog.csdn.net/sjpz0124/article/details/45191095),在vector类中作用为在vector尾部加入一个数据。[transform](https://www.jianshu.com/p/cbe722ca4276)就是用来做转换的，本题转换用的是匿名函数。

```c++
__int64 __fastcall main::{lambda(int)#1}::operator() const(_DWORD **a1, int a2)
{
  return (unsigned int)(**a1 + a2);
}
```

[accumulate](https://blog.csdn.net/Jeanphorn/article/details/45114233)在这题的用法和c++的常见用法不一样，因为题目内部还有一个匿名函数，作用是把输入内容数组反向。加密流程其实挺简单的。

1. 接受16个数字输入
2. 计算斐波那契数列前16项
3. 把16个数字输入从第二个元素开始,都加上第一个元素
4. 将3的结果反向
5. 将4的结果和2的结果比较,完全相同则输入的是flag

关键点就这样，我在ghidra里啥也看不出来。大冤种一个。

### Flag
- flag{987-377-843-953-979-985}