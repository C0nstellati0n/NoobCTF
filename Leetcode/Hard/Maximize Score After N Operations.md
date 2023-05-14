# Maximize Score After N Operations

[题目](https://leetcode.com/problems/maximize-score-after-n-operations/description/)

bitmask dp又是个什么玩意啊？

```c#
//https://leetcode.com/problems/maximize-score-after-n-operations/solutions/1118778/c-java-python-bitmask-dp/
public class Solution {
    int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
    int dfs(int[] n, int[,] dp, int i, int mask) {
        if (i > n.Length / 2)
            return 0;
        if (dp[i,mask] == 0)
            for (int j = 0; j < n.Length; ++j)
                for (int k = j + 1; k < n.Length; ++k) {
                    int new_mask = (1 << j) + (1 << k);
                    if ((mask & new_mask) == 0)
                        dp[i,mask] = Math.Max(dp[i,mask], i * gcd(n[j], n[k]) + dfs(n, dp, i + 1, mask + new_mask));
                }
        return dp[i,mask];
    }
    public int MaxScore(int[] n) {
        return dfs(n, new int[n.Length / 2 + 1,1 << n.Length], 1, 0);
    }
}
```

```
Runtime
310 ms
Beats
33.33%
Memory
41 MB
Beats
100%
```

上面那个做法省空间，也可以用空间换时间，将gcd的结果存起来。

```c#
//https://leetcode.com/problems/maximize-score-after-n-operations/solutions/1118778/c-java-python-bitmask-dp/
public class Solution {
    int[,] gcdMemo = new int[14,14];
    int[] memo = new int[1 << 14];
    int m, n;
    public int MaxScore(int[] nums) {
        m = nums.Length;
        n = m / 2;
        return dp(nums, 1, 0);
    }
    int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
    int dp(int[] nums, int op, int mask) {
        if (op > n) return 0; // Reach to n operations
        if (memo[mask] != 0) return memo[mask];

        for (int i = 0; i < m; ++i) {
            if (((mask >> i) & 1)!=0) continue; // If nums[i] is used -> Skip
            for (int j = i + 1; j < m; ++j) {
                if (((mask >> j) & 1)!=0) continue; // If nums[i] is used -> Skip
                int newMask = (1 << i) | (1 << j) | mask; // Mark nums[i] and nums[i] as used!
                int score = op * cache_gcd(nums, i, j) + dp(nums, op + 1, newMask);
                memo[mask] = Math.Max(memo[mask], score);
            }
        }
        return memo[mask];
    }
    int cache_gcd(int[] nums, int i, int j) { // gcd with cache
        if (gcdMemo[i,j] != 0) return gcdMemo[i,j];
        return gcdMemo[i,j] = gcd(nums[i], nums[j]);
    }
}
```

```
Runtime
129 ms
Beats
100%
Memory
43.2 MB
Beats
66.67%
```

或者在开始计算前统一算好gcd，其实跟上种差不多。

```c#
//https://leetcode.com/problems/maximize-score-after-n-operations/solutions/3521675/image-explanation-fastest-complete-intuition-c-java-python/
class Solution {
    public int func(int[] nums, int op, int mask, int[] dp, int[,] gcd) {
        int m = nums.Length, n = nums.Length/2;

        if(op > n) return 0;
        if(dp[mask] != -1) return dp[mask];

        for(int i=0; i<m; i++) {
            if( (mask & (1<<i)) != 0 ) continue;
            for(int j=i+1; j<m; j++) {
                if( (mask & (1<<j)) != 0 ) continue;

                int newMask = (1<<i) | (1<<j) | mask;
                int score = op * gcd[i,j] + func(nums, op+1, newMask, dp, gcd);
                dp[mask] = Math.Max(dp[mask], score);
            }
        }

        return dp[mask];
    }

    public int MaxScore(int[] nums) {
        int[] dp = new int[1<<14];
        Array.Fill(dp, -1);

        int m = nums.Length, n = nums.Length/2;
        int[,] gcd = new int[m,m];
        for(int i=0; i<m; i++) {
            for(int j=0; j<m; j++) {
                gcd[i,j] = _gcd(nums[i], nums[j]);
            }
        }

        return func(nums, 1, 0, dp, gcd);
    }

    private int _gcd(int a, int b) {
        return b == 0 ? a : _gcd(b, a % b);
    }
}
```

```
Runtime
137 ms
Beats
100%
Memory
43.5 MB
Beats
66.67%
```

搜了一下啥是bitmask dp。

```
Bitmask DP is a technique that uses the binary representation of numbers to represent the state of a problem. It is used to solve problems that involve subsets, combinations, or permutations of a given set of elements. In bitmask DP, we use a binary number to represent the state of the problem, where each bit of the binary number represents the presence or absence of an element in the current subset, combination, or permutation being considered. The technique is particularly useful when the number of elements in the set is small, typically less than 20, and the number of subsets, combinations, or permutations is large.

The idea behind Bitmask DP is to use a binary number to represent the state of the problem. We can use the binary number to represent the presence or absence of an element in the current subset, combination, or permutation being considered. For example, if we have a set of three elements, {A, B, C}, we can represent the subset {A, C} as the binary number 101. Here, the first and third bits are set to 1, indicating that the first and third elements are present in the subset.

One of the main advantages of Bitmask DP is that it can be used to solve problems involving subsets, combinations, or permutations of a set of elements in O(3^n) time, where n is the size of the set. This is because there are 2^n possible subsets, and for each subset, we need to iterate over all its elements, which gives us a total time complexity of O(3^n). However, by using memoization, we can reduce the time complexity to O(n*2^n), which is much faster.

There are several ways to implement Bitmask DP, but the most common approach is to use memoization. In this approach, we use a two-dimensional array to store the values of subproblems that have already been solved. The first dimension of the array represents the state of the problem (i.e., the binary number), and the second dimension represents the element being considered.

One of the most popular examples of Bitmask DP is the problem of counting the number of ways to assign unique caps to a group of people. In this problem, there are n people and m types of caps, and we need to find the number of ways to assign caps to the people such that no two people wear the same type of cap. The solution involves using a bitmask to represent the state of the problem and memoization to store the values of subproblems that have already been solved.

To solve this problem, we can use a bitmask to represent the state of the problem. In this case, we can use an integer variable as a bitmask to store which person is wearing a cap and which is not. Let i be the current cap number (caps from 1 to i-1 are already processed). If the i'th bit is set in the mask, then the i'th person is wearing a cap; otherwise, they are not.

The solution involves using memoization to store the values of subproblems that have already been solved. We can use a two-dimensional array to store the values of subproblems, where the first dimension represents the state of the problem (i.e., the bitmask), and the second dimension represents the cap being considered. We can also use an array of vectors, capList, to store the list of people that can wear a given cap.

The time complexity of this solution is O(n*2^m), where n is the number of people and m is the number of types of caps. This is because we need to iterate over all possible masks (i.e., all possible subsets of the set of people) and all possible caps. However, by using memoization, we can reduce the time complexity to O(2^m), which is much faster.

In conclusion, Bitmask DP is a powerful technique for solving problems that involve subsets, combinations, or permutations of a given set of elements. It involves using a binary number to represent the state of the problem and memoization to store the values of subproblems that have already been solved. Although it has a high time complexity, it can be optimized using memoization to achieve much faster performance.
```