# Integer Break

[题目](https://leetcode.com/problems/integer-break)

高等数学再就业。
```c#
//将n分成2和3是最优解法。有3就分3，4除外，不用分，因为2*2>1*3
//https://leetcode.com/problems/integer-break/editorial 有证明，用了微积分。“你永远不知道会在什么地方遇见微积分”
public class Solution {
    public int IntegerBreak(int n) {
        if (n == 2 || n == 3) return (n-1);
        int res = 1;
        while (n > 4)
        {
            n -= 3;
            res *= 3;
        }
        return (n * res);
    }
}
```
```
Runtime
17 ms
Beats
93.75%
Memory
26.5 MB
Beats
72.92%
```
editorial还有个极速解法.
```c#
class Solution {
    public int IntegerBreak(int n) {
        if (n <= 3) {
            return n - 1;
        }
        if (n % 3 == 0) { //整除于3就全拆成3
            return (int) Math.Pow(3, n / 3);
        }
        if (n % 3 == 1) { //余1就在全拆成3的基础上匀出一个3给1，凑成4和其他的3
            return (int) Math.Pow(3, (n / 3 - 1)) * 4;
        }
        return (int) Math.Pow(3, n / 3) * 2; //余2就全拆成3后留下那个2不拆
    }
}
```
```
Runtime
16 ms
Beats
95.83%
Memory
26.6 MB
Beats
64.58%
```