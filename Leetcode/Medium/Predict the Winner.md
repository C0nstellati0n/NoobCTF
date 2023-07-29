# Predict the Winner

[题目](https://leetcode.com/problems/predict-the-winner/description/)

我发现我有个毛病，脑子想不清楚的题就一定不会做，连试都不试一下。问题是这类dp/递归题基本一环套一环，疯狂套娃，人脑肯定是没法演算出全部运行过程的。所以递归题要来点base case返回避免无限递归，dp要想各项之间的关系。好，我的大脑说：“什么这题竟然算不明白？不试了”。到最后已经变化成：“什么？这题是dp？跑了不想了”。
```c#
//在采样区看见了这个解法，似乎属于editorial里的递归做法，不过加了cache，速度更快了
//solution有个类似的考虑四种情况的： https://leetcode.com/problems/predict-the-winner/solutions/155217/from-brute-force-to-top-down-dp/ ，不过也不完全相同
public class Solution {
    int[] nums;
    int n;
    public bool PredictTheWinner(int[] nums) {
        this.nums = nums;
        n = nums.Count();
        cache = new Dictionary<(int left, int right, int player1Sum, int player2Sum), bool>();
        return Recurse(0,n-1,0,0);
    }
    Dictionary<(int left, int right, int player1Sum, int player2Sum), bool> cache;
    bool Recurse(int left, int right, int player1Sum, int player2Sum) {
        if(left == right) {
            // only one number remaining
            return player1Sum + nums[left] >= player2Sum;
        }
        if(left > right) {
            // no numbers remaining
            return player1Sum >= player2Sum;
        }
        if(cache.ContainsKey((left,right,player1Sum,player2Sum)) == false) {
            cache[(left,right,player1Sum,player2Sum)] = 
                Recurse(left+2, right, player1Sum+nums[left], player2Sum+nums[left+1]) && // both players taking from left side
                Recurse(left+1, right-1, player1Sum+nums[left], player2Sum+nums[right]) || // player1 from left player2 from right
                Recurse(left, right-2, player1Sum+nums[right], player2Sum+nums[right-1]) && // both players taking from right side
                Recurse(left+1, right-1, player1Sum+nums[right], player2Sum+nums[left]); // player1 from right player2 from left
        }
        return cache[(left,right,player1Sum,player2Sum)];
    }
}
```
```
Runtime
83 ms
Beats
100%
Memory
41.6 MB
Beats
18.18%
```
代码挺好懂的，就是不好想。另外有个优化内存的dp。
```c#
//本质上是Approach 3，把那个看懂了这个就懂了
class Solution {
    public bool PredictTheWinner(int[] nums) {
        int n = nums.Length;
        int[] dp = nums[..]; //拷贝一个nums数组。editorial里说dp的更新方式是斜着的，所以越更新到最后就越小，只剩下一个的时候就是解（参考editorial的图）
        
        for (int diff = 1; diff < n; ++diff) {
            for (int left = 0; left < n - diff; ++left) {
                int right = left + diff;
                dp[left] = Math.Max(nums[left] - dp[left + 1], nums[right] - dp[left]);
            }
        }
        
        return dp[0] >= 0;
    }
}   
```
```
Runtime
75 ms
Beats
100%
Memory
40.1 MB
Beats
54.55%
```