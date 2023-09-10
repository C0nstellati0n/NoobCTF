# Count All Valid Pickup and Delivery Options

[题目](https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options)

数学题。排列组合。忘了。寄。
```c#
//https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/solutions/4024280/99-57-dp-math-recursion
public class Solution {
    int MOD = 1000000007;
    public int CountOrders(int n) {
        long count = 1; //base case。当包裹只有1个时，唯一可能的操作是P D
        for (int i = 2; i <= n; i++) {
            count = (count * (2 * i - 1) * i) % MOD; //把pick记为P，delivery记为D。P和D的操作数量总和等于包裹的数量i*2。对于P，2*i个操作空间里在哪都行（除了最后一个），因此为2*i-1
            //D的话则有现限制，要在P后面。所以只有i个操作空间。每个包裹共有(2 * i - 1) * i种方式，乘上之前的即可
        }
        return (int) count;
    }
}
```
```
Runtime
19 ms
Beats
100%
Memory
26.6 MB
Beats
100%
```