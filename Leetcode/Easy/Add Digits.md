# Add Digits

[题目](https://leetcode.com/problems/add-digits/description/)

数学真是个好东西。有人指出：
```
We can find regular pattern by enumerate following case:
1=1; 2=2; 3=3; 4=4; 5=5; 6=6; 7=7; 8=8; 9=9;
10=1; 11=2; 12=3; 13=4; 14=5; 15=6; 16=7; 17=8; 18=9;
19=1; 20=2; 21=3; 22=4; 23=5; 24=6; 25=7; 26=8; 27=9;
... ...
so, we supposed that the rule is a cycle per 9 number.
the math formulation:
(num - 1) % 9 + 1

note: num - 1 is to avoid k*9%9 = 0
```

把公式抄上去就好了。

```c#
public class Solution {
    public int AddDigits(int num) {
        while(num>9){
            num=(num-1)%9+1;
        }
        return num;
    }
}
```

```
Runtime
16 ms
Beats
97.45%
Memory
26.5 MB
Beats
62.42%
```

结果发现我是个笨蛋，我理解错公式了。那个公式是直接算出答案的，不需要while循环。

```c#
//https://leetcode.com/problems/add-digits/solutions/1754049/easy-o-1-explanation-with-example/
public class Solution {
    public int AddDigits(int num) {
        return 1 + (num - 1) % 9;
    }
}
```

```
Runtime
20 ms
Beats
90.13%
Memory
26.8 MB
Beats
19.11%
```