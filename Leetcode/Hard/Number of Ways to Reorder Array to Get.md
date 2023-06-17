# Number of Ways to Reorder Array to Get Same BST

[题目](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/)

这是个数学+语文题。不仅题目描述比较难懂，解法还要用杨辉三角算permutation的数量。
```c#
//https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/solutions/819725/java-clean-code-uses-yang-hui-s-pascal-s-triangle-with-explanation/
class Solution {
    private static long MOD = 1000000007;
    public int NumOfWays(int[] nums) { //题目给定nums数组，nums[0]固定为root，剩下的数字要是小于root就去左子树，大于root就去右子树。所以存在将root后面的数字打乱后，构造的BST还跟没打乱时构造的一样的情况。函数范围这种情况的数量
        int len = nums.Length;
        List<int> arr = new();
        foreach(int n in nums) {
            arr.Add(n);
        }
        return (int)getCombs(arr, getTriangle(len + 1)) - 1;
    }
    
    private long getCombs(List<int> nums, long[][] combs) {
        if (nums.Count <= 2) {
            return 1;
        }
        int root = nums[0];
        List<int> left = new();
        List<int> right = new();
        foreach(int n in nums) {
            if (n < root) {
                left.Add(n);
            } else if (n > root) {
                right.Add(n);
            }
        }
        // mod every number to avoid overflow
        return (combs[left.Count + right.Count][left.Count] * (getCombs(left, combs) % MOD) % MOD) * getCombs(right, combs) % MOD;
    }
    
    private long[][] getTriangle(int n) {
        // Yang Hui (Pascle) triangle
        // 4C2 = triangle[4][2] = 6
        long[][] triangle = new long[n][];
        for(int j=0;j<n;j++){
            triangle[j]=new long[n];
        }
        for (int i = 0; i < n; i++) {
            triangle[i][0] = triangle[i][i] = 1;
        }
        for (int i = 2; i < n; i++) {
            for (int j = 1; j < i; j++) {
                triangle[i][j] = (triangle[i - 1][j] + triangle[i - 1][j - 1]) % MOD;
            }
        }
        return triangle;
    }
}
```
```
Runtime
257 ms
Beats
100%
Memory
78.9 MB
Beats
50%
```