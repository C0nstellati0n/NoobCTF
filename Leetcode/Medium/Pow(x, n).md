# Pow(x, n)

[题目](https://leetcode.com/problems/powx-n/description/)

这题不是算法题，纯纯数学题啊！我用一分钟完成了这道题，50秒逛discussion，10秒写个`return Math.Pow(x,n)`。太作弊了，轮子要自己造才有意思哈。
```c#
//https://leetcode.com/problems/powx-n/editorial/
class Solution {
    private double binaryExp(double x, long n) {
        if (n == 0) {
            return 1;
        }

        // Handle case where, n < 0.
        if (n < 0) { //指数是负数就求倒数
            n = -1 * n;
            x = 1.0 / x;
        }

        // Perform Binary Exponentiation.
        double result = 1;
        while (n != 0) {
            // If 'n' is odd we multiply result with 'x' and reduce 'n' by '1'.
            if (n % 2 == 1) {
                result = result * x;
                n -= 1;
            }
            // We square 'x' and reduce 'n' by half, x^n => (x^2)^(n/2).
            x = x * x;
            n = n / 2;
        }
        return result;
    }

    public double MyPow(double x, int n) {
        return binaryExp(x, (long) n);
    }
}
```
```
Runtime
26 ms
Beats
70.64%
Memory
27.1 MB
Beats
26.59%
```
没有技巧，全是数学。指数是负数那里这么做是因为 $x^n=\frac{1}{x^{-n}}$ ,n < 0。然后基本算乘方的逻辑是：
- 若n为偶数， $(x^2)^{\frac{n}{2}}$
- 若n为奇数， $x*(x^2)^{(n-1)/2}$

好这就是全部了。吐槽一下，editorial连swift都有就是没有c#，我们大微软这么冷门吗？