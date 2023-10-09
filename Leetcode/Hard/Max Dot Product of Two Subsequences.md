# [Max Dot Product of Two Subsequences](https://leetcode.com/problems/max-dot-product-of-two-subsequences)

做了这么多dp，虽然我每次都懒得自己写，但是理解越来越得心应手了
```c#
//https://leetcode.com/problems/max-dot-product-of-two-subsequences/editorial
//Approach 3，也是最佳解法
class Solution {    
    public int MaxDotProduct(int[] nums1, int[] nums2) {
        int firstMax = Int32.MinValue; //这些min和max是为了防止当nums1全是负数，nums2全是正数（反过来也是）时，无论怎么操作值都会越来越小。所以直接提前计算并返回
        int secondMax = Int32.MinValue;
        int firstMin = Int32.MaxValue;
        int secondMin = Int32.MaxValue;
        foreach(int num in nums1) {
            firstMax = Math.Max(firstMax, num);
            firstMin = Math.Min(firstMin, num);
        }
        foreach(int num in nums2) {
            secondMax = Math.Max(secondMax, num);
            secondMin = Math.Min(secondMin, num);
        }
        if (firstMax < 0 && secondMin > 0) {
            return firstMax * secondMin;
        }
        if (firstMin > 0 && secondMax < 0) {
            return firstMin * secondMax;
        }
        //下面才是dp
        int m = nums2.Length + 1;
        int[] dp = new int[m]; //dp[i,j]表示当nums1的索引为i，nums2的索引为j，其后面（suffix）的数组的subsequence所能构成的最大点积。只有一维是因为每次计算最多只依赖dp[i+1,j+1]
        int[] prevDp = new int[m]; //用prevDp记录dp[i+1]即可
        for (int i = nums1.Length - 1; i >= 0; i--) { //这里dp的方向是倒着来的，因为dp的定义就是suffix，取也是往i+1，j+1的地方取，需要从后面开始才能累加起来
            dp = new int[m];
            for (int j = nums2.Length - 1; j >= 0; j--) {
                int use = nums1[i] * nums2[j] + prevDp[j + 1]; //情况一，取i和j，则此处的结果为nums1[i] * nums2[j]，然后再加上后面的积dp(i + 1, j + 1)。prevDp是dp[i+1]
                dp[j] = Math.Max(use, Math.Max(prevDp[j], dp[j + 1])); //情况二和三，只取j所以i向后移，或者只取i所以j向后移。这些情况此处就没有结果，直接拿dp的值
            }
            prevDp = dp;
        }
        return dp[0];
    }
}
```