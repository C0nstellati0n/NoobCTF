# Bulb Switcher

[题目](https://leetcode.com/problems/bulb-switcher/description/)

数学题，搞明白后它的解法将是你看过最简单的。

```c#
class Solution {
    public int BulbSwitch(int n) {
        return (int)Math.Sqrt(n);
    }
}
```

```
Runtime
24 ms
Beats
69.57%
Memory
26.7 MB
Beats
60.87%
```

数据这么差是因为大家基本都是这么写的，到底数据怎样与案例密切相关。现在的问题是，为啥？

```
The light bulb at postion k must be toggled in odd number to stay on, e.g. 'On, Off, On' including the initial toggle. What triggers k-th bulb be toggled? Number k must be an exact multiple of each toggling. For example, when k=4, the bulb will be triggered by the 1st (On), 2nd (Off) and 4th (On) operation. What is the exact number of multiple of a nature number k? All of its factors !

So the k-th bulb 'ON' is corresponding to the number of factors of k being odd. You can certainly develop a program to count. However, the number math tells us only perfect square numbers have odd number of factors, which is what needed for the bulb to stay on.

Great! Now to solve the problem is to find out how many perfect square number between 1 and n. The math kicks in again, and that number is the square root of n (more preceisly the floor of sqaure root of n).
```

我们要找出只有单数个因子的数字，那些数字对应处的灯泡是两者的。完全平方数正好可以满足这一点。对于其他数，我们把它的因子两两一对写出来，因子数肯定是偶数。但是到完全平方数身上，最后一对将是某个平方根，虽然也成对，但是是同一个。https://math.stackexchange.com/questions/525935/why-perfect-square-has-odd-number-of-factors

那么怎么计算有多少个？计算num1与num2之间的完全平方数的公式为`floor(sqrt(num2)) - ceil(sqrt(num1)) + 1`。这道题我们的num1是1，直接前半部分就行了。不知道怎么证明，但是想一下，假设num2是1000，开方会得到31多。说明1-31的数的平方都不会超过1000，但是32会。那不直接就是31个了吗？