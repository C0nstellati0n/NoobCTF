# Maximum Value at a Given Index in a Bounded Array

[题目](https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/description/)

难点竟然是算数列和……

```c#
//https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/solutions/1119801/java-c-python-binary-search/
public class Solution {
    public int MaxValue(int n, int index, int maxSum) {
        maxSum -= n;
        int left = 0, right = maxSum, mid;
        while (left < right) {
            mid = (left + right + 1) / 2;
            if (test(n, index, mid) <= maxSum)
                left = mid;
            else
                right = mid - 1;
        }
        return left + 1;
    }
    
    private long test(int n, int index, int a) {
        int b = Math.Max(a - index, 0);
        long res = (long)(a + b) * (a - b + 1) / 2;
        b = Math.Max(a - ((n - 1) - index), 0);
        res += (long)(a + b) * (a - b + 1) / 2;
        return res - a;
    }
}
```
```
Runtime
22 ms
Beats
100%
Memory
26.6 MB
Beats
58.33%
```

计算差值为1的数列和的公式：1 + 2 + ... + n = n * (n+1) / 2 （末项*(项数+1)/2）。懂这个公式基本这题就不难了，不过还要注意binary search的边界问题(`while (left < right)`)。换个two pointers写法。
```c#
//https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/solutions/1121538/easy-java-solution-without-using-binary-search-using-greedy-approach-with-explanation/
public class Solution {
    public int MaxValue(int n, int index, int maxSum) {
        int sum = n;
        int l = index, r = index;
        int res = 1;  //intial height

        while(sum + (r-l+1) <= maxSum) {
            sum += r-l+1;
            
            // ensuring l doesn't go below 0 && r doesn't go beyond n-1
            l = l == 0 ? 0 : l-1;
            r = r == n-1 ? r : r+1;
            res++;   

            //optimizing once l == 0 and r == n-1 as we need to add n in each step
            if(l == 0 && r == n-1) {
                int steps = 0;
                steps += (maxSum - sum)/n;
                sum += (steps * n);
                res += steps;
            }
        }

        return res;
    }
}
```
```
Runtime
22 ms
Beats
100%
Memory
26.6 MB
Beats
58.33%
```