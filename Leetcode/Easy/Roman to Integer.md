# Roman to Integer

[题目地址](https://leetcode.com/problems/roman-to-integer/)

这题就看出我思路的死板了。罗马数字每个符号对应一个值，但是有例外：

- I can be placed before V (5) and X (10) to make 4 and 9. 
- X can be placed before L (50) and C (100) to make 40 and 90. 
- C can be placed before D (500) and M (1000) to make 400 and 900.

想着我在字典里加上IV，IX等，但是字符串怎么读取呢？卡了，后来发现可以倒着读取，因为这些组合数字都有一个特征——前面的符号值比后面的小。正常情况下从左到右，符号的值都是递减的。如果发现不符合这个规律的，就把当前读取的值减掉，否则加上。这样就不用考虑怎么截取字符串的问题了，字典也能少点值。

```c#
public class Solution {
    public int RomanToInt(string s) {
        Dictionary<char,int> table=new Dictionary<char,int>{
            {'I',1},
            {'V',5}, 
            {'X',10}, 
            {'L',50}, 
            {'C',100}, 
            {'D',500}, 
            {'M',1000},
        };
        int value=table[s[^1]];
        for(int i=s.Length-2;i>=0;i--){
            if(table[s[i]]<table[s[i+1]]){
                value-=table[s[i]];
            }
            else{
                value+=table[s[i]];
            }
        }
        return value;
    }
}
```

能过，但是无论运行时间还是内存都差强人意。去看了讨论区，似乎用switch-case会更快。于是实验了一下。

```c#
public class Solution {
    public int RomanToInt(string s) {
        int value=0;
        int number=0;
        int prev=0;
        for(int i=s.Length-1;i>=0;i--){
            switch(s[i]){
                case 'I':number=1;break;
                case 'V':number=5;break;
                case 'X':number=10;break;
                case 'L':number=50;break;
                case 'C':number=100;break;
                case 'D':number=500;break;
                case 'M':number=1000;break;
            }
            if(number<prev){
                value-=number;
            }
            else{
                value+=number;
            }
            prev=number;
        }
        return value;
    }
}
```

运行速度直接超越98%，内存超越63%。好家伙，没想到switch-case这么快啊？