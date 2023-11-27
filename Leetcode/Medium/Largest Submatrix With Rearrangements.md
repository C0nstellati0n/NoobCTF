# [Largest Submatrix With Rearrangements](https://leetcode.com/problems/largest-submatrix-with-rearrangements)

看到大家说这题偏难我就跑了，没犹豫一秒
```c++
//采样区去掉开头的提速魔法，太作弊了。但就算是这样也比editorial提供的做法快
//但是editorial的解析非常详细
class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int m = matrix.size();
        int n = matrix[0].size();
        for (int i = 1; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 1) {
                    matrix[i][j] += matrix[i - 1][j]; //column记录连续“1”的数量。所以从原来的1 1 1 1（应该是竖着的，这里凑合看吧）变成1 2 3 4
                }
            }
        }
        int res = 0;
        for (int i = 0; i < m; i++) {
            sort(matrix[i].begin(), matrix[i].end()); //matrix[i]是当前row，排序其实相当于把每个column的第i个元素进行排序。这里的排序就是题目说的Rearrangements
            for (int j = 0; j < n; j++) {
                res = max(res, matrix[i][j] * (n - j)); //子矩阵的形状等于矩形，按照高*底的方式进行计算
            }
        }
        return res;
    }
};
```
让column记录连续1的数量，然后排序。大概长这个样：
```
1
2 1
3 2 1
4 3 2 1
```
这里的高就是matrix[i][j]，分别取所有可能的数字；底为(n - j)。总算知道为啥比editorial快乐，因为同样思路editorial的更好理解，这个应该是优化过的