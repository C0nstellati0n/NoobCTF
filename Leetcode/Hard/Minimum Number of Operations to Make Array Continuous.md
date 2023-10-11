# [Minimum Number of Operations to Make Array Continuous](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous)

我觉得能被我一下看懂的都不算hard。《我能做出来的只是我懒得想》
```c#
//https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/editorial
//Approach 2: Sliding Window
class Solution {
    public int MinOperations(int[] nums) {
        int n = nums.Length;
        int ans = n;
        HashSet<int> unique = new(nums);
        int[] newNums = new int[unique.Count];
        int index = 0;
        foreach(int num in unique) {
            newNums[index++] = num;
        }
        Array.Sort(newNums);
        int j = 0;
        for (int i = 0; i < newNums.Length; i++) {
            while (j < newNums.Length && newNums[j] < newNums[i] + n) {
                j++;
            }
            int count = j - i;
            ans = Math.Min(ans, n - count);
        }
        return ans;
    }
}
```
首先需要更好地理解题目。题目对Continuous的定义乱七八糟一大堆，其实就一句话：包含从n到n+k的不重复元素的数列。题目要求用最少的步骤获取这样的数列。那我们总要先找个n吧？首先对nums从小到大排序，然后从最小的数开始，将其设为n，n+k为最大的数，这就是我们的数列。怎么知道该动什么数字？在数组里找那些不在n到n+k范围里的数的数量。这时排序就派上用场了，可以用binary search找到第一个超过n+k的数字的索引，剩下的都属于需要改动的范围。不过使用的binary search稍微改动了一下，不是找特定数字的索引，而是超过某个特定数字的最小索引。

那为什么又用上sliding window了？因为数组是排序好的，n+k只会越来越大，不可能跑到前面去。那直接linear遍历过去好了，window的右边（j）不需要动