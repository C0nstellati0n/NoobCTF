# Jail Level 1-4 & Leak Level 1-2

## Jail Level 1

`breakpoint()`

## Jail Level 2

参考 https://zhuanlan.zhihu.com/p/578986988 。由于开启了socat，直接help()函数后在控制台打!sh即可getshell

## Jail Level 3

快乐非ascii字符通杀：`ｂｒｅａｋｐｏｉｎｔ()`（可以绕过过滤但是可以正常执行）

## Jail Level 4

记得题目是个python2，python 2.7的input相当于python3的eval(input())。`open('flag').read()`

## Leak Level 0 & Leak Level 2

`hｅlp()`。用特殊字体（看我就说通杀）绕过滤。然后`__main__`获取真正的admin key

## Leak Level 1

`vars()`