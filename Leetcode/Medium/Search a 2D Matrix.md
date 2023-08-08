# Search a 2D Matrix

[题目](https://leetcode.com/problems/search-a-2d-matrix/description/)

discussion的提示直接让这题变成笨蛋binary search题。
```c#
public class Solution {
    public bool SearchMatrix(int[][] matrix, int target) {
        int rowLength=matrix[0].Length;
        int start = 0;
        int end = matrix.Length*rowLength-1;
        while (start <= end) {
            int mid = start + (end-start)/2;
            if (matrix[mid/rowLength][mid%rowLength] == target) return true; //将2d矩阵看成一个排序的数组，关键在于mid/rowLength和mid%rowLength
            //参考discussionCodahhhhhh的评论
            else if (matrix[mid/rowLength][mid%rowLength] > target) end = mid-1;
            else start = mid + 1;
        }
        return false;
    }
}
```
```
Runtime
83 ms
Beats
97.90%
Memory
40.9 MB
Beats
35.43%
```
还能稍微变化下。
```c#
public class Solution {
    public bool SearchMatrix(int[][] matrix, int target) {
        var rows = matrix.Length-1;
        var cols = matrix[0].Length-1;
        if (target < matrix[0][0] || target > matrix[rows][cols]) return false;
        while(matrix[rows][0] > target) rows--;
        while(cols >= 0){
            if (matrix[rows][cols] == target) return true; //这块linear search就够了
            cols--;
        }
        return false;
    }
}
```
```
Runtime
78 ms
Beats
99.63%
Memory
40.7 MB
Beats
86.54%
```