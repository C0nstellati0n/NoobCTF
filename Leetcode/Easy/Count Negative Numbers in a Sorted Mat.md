# Count Negative Numbers in a Sorted Matrix

[题目](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/description/)

很难有一道题把我整无语的，这题做到了。主要是它有一个简单到不能再简单的解法。
```c#
public class Solution {
    public int CountNegatives(int[][] grid) {
        int count=0;
        foreach(int[] g in grid){
            foreach(int num in g){
                if(num<0){
                    count++;
                }
            }
        }
        return count;
    }
}
```
```
Runtime
89 ms
Beats
97.70%
Memory
42.6 MB
Beats
91.71%
```
或者用点至少比这个高级的做法，比如two pointers
```c#
//https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/solutions/510249/java-python-3-2-similar-o-m-n-codes-w-brief-explanation-and-analysis/
public class Solution {
    public int CountNegatives(int[][] grid) {
        int m = grid.Length, n = grid[0].Length, r = m - 1, c = 0, cnt = 0;
        while (r >= 0 && c < n) {
            if (grid[r][c] < 0) {
                --r;
                cnt += n - c; // there are n - c negative numbers in current row.
            }else {
                ++c;
            }
        }
        return cnt;
    }
}
```
```
Runtime
97 ms
Beats
80.65%
Memory
42.8 MB
Beats
68.20%
```
比如binary search
```c#
//https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/solutions/512165/java-binary-search-beats-100-explained/
public class Solution {
    public int CountNegatives(int[][] grid) {
        int rows = grid.Length, cols = grid[0].Length; 
        int res = 0, lastNeg = cols - 1;
        for (int row = 0; row < rows; row++) {
            //check edge cases - if first element is < 0 - all elements in row are negative
            if (grid[row][0] < 0) {
                res+=cols;
                continue;
            }
            //if last element is positive - it means there are no negative numbers in a row
            if (grid[row][cols - 1] > 0)
                continue;
            //there is a mix of negative and positive ones, need to find the border. starting
            //binary search
            int l = 0, r = lastNeg;
            while (l <= r) {
                int m = l + (r - l)/2;
                if (grid[row][m] < 0) {
                    r = m - 1;
                } else
                    l = m + 1;
            }
            //l points to the first negative element, which means cols - l is a number of
            //such elements
            res += (cols - l); lastNeg = l;
        }
        return res;
    }
}
```
```
Runtime
94 ms
Beats
89.86%
Memory
42.5 MB
Beats
96.31%
```