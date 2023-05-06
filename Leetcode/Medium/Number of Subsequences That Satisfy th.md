# Number of Subsequences That Satisfy the Given Sum Condition

[题目](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/description/)

这个subsequence怎么算啊？题目提示用two pointers找到满足条件的最大的i和j，找到后就能在里面数subsequence。道理我都懂，可是怎么数啊？

```c#
//https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/solutions/3491280/image-explanation-binary-exponentiation-two-pointers-pre-computation-c-java-python/
class Solution {
    public int NumSubseq(int[] nums, int target) {
        int res = 0, mod = 1000000007, l = 0, r = nums.Length - 1;
        List<int> pre = new();
        pre.Add(1);
        for (int i = 1; i <= nums.Length; ++i) {
            pre.Add((pre[i - 1] << 1) % mod);//2的n次方
        }

        Array.Sort(nums);

        while (l <= r) {
            if (nums[l] + nums[r] > target) {
                r--;
            } else {
                res = (res + pre[r - l++]) % mod; //这里是我懵了的地方。最开始以为l到r的subsequence数量只跟l和r有关，想了一下发现不对，但也想不出公式。看来是固定r后把l索引出的数量全部加起来
            }
        }

        return res;
    }
}
```

```
Runtime
201 ms
Beats
100%
Memory
51.8 MB
Beats
100%
```