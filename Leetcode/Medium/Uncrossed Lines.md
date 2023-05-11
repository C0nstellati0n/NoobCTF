# Uncrossed Lines

[题目](https://leetcode.com/problems/uncrossed-lines/description/)

大家说和longest common sequence那题很像，然而我没做过那道题。我做过的题里面唯一和这个有点关系的是[Longest Palindromic Subsequence](./Longest%20Palindromic%20Subsequence.md),不过这题没那题复杂。

```c#
//https://leetcode.com/problems/uncrossed-lines/solutions/282842/java-c-python-dp-the-longest-common-subsequence/
public class Solution {
    public int MaxUncrossedLines(int[] A, int[] B) {
        int m = A.Length, n = B.Length;
        if (m < n) return MaxUncrossedLines(B, A); //保证A的长度一定大于B的。以前遇到这种情况我都是用if判断做两个分支，今天发现可以直接这样，原来这么简单
        int[] dp = new int[n+1]; //以短的为主。较长的那个序列多出来的数字不好连，基本是最差情况才会连
        for (int i = 0; i < m; i++) {
            for (int j = 0, prev = 0, cur; j < n; j++) {
                cur = dp[j+1];
                if (A[i] == B[j]) dp[j+1] = 1+prev;
                else dp[j+1] = Math.Max(dp[j+1], dp[j]);
                prev = cur;
            }
        }
        return dp[n];
    }
}
```

```
Runtime
86 ms
Beats
93.75%
Memory
38.8 MB
Beats
100%
```

另一个方向的dp。

```c#
//https://leetcode.com/problems/uncrossed-lines/solutions/3510440/why-use-dp-recursion-top-down-bottom-up/
public class Solution {
    public int MaxUncrossedLines(int[] A, int[] B) {
        int n1 = A.Length, n2 = B.Length;
        int[,] dp=new int[n1+1,n2+1]; //这种从后往前推+二维dp的就不用考虑谁大谁小，反正dp数组都记录了
        for (int nums1Start = n1 - 1; nums1Start >= 0; nums1Start--)
        {
            for (int nums2Start = n2 - 1; nums2Start >= 0; nums2Start--)
            {
                //======================================================================================
                int makeLineCount = 0, notMakeLineCount = 0;
                if (A[nums1Start] == B[nums2Start]) 
                    makeLineCount = 1 + dp[nums1Start + 1,nums2Start + 1]; 
                else
                {
                    int leaveFromNums1 = dp[nums1Start + 1,nums2Start];
                    int leaveFromNums2 = dp[nums1Start,nums2Start + 1];
                    notMakeLineCount = Math.Max(leaveFromNums1, leaveFromNums2);
                }
                //=======================================================================================
                dp[nums1Start,nums2Start] = Math.Max(makeLineCount, notMakeLineCount);
            }
        }
        int ans = dp[0,0];
        return ans;
    }
}
```

```
Runtime
83 ms
Beats
93.75%
Memory
40.9 MB
Beats
56.25%
```