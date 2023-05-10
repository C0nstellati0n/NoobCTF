# Spiral Matrix II

[题目](https://leetcode.com/problems/spiral-matrix-ii/description/)

昨天的没抄好，导致今天又没想出来。看着推荐题目还有同名题目的三和四，到时候再看看（总要做出来一个吧？）

```c#
public class Solution {
    public int[][] GenerateMatrix(int n) {
        // Declaration
        int[][] matrix = new int[n][];
        for(int i=0;i<n;i++){
            matrix[i]=new int[n];
        }
        // Edge Case
        if (n == 0) {
            return matrix;
        }
        
        // Normal Case
        int rowStart = 0;
        int rowEnd = n-1;
        int colStart = 0;
        int colEnd = n-1;
        int num = 1; //change
        
        while (rowStart <= rowEnd && colStart <= colEnd) {
            for (int i = colStart; i <= colEnd; i ++) {
                matrix[rowStart][i] = num ++; //change
            }
            rowStart ++;//昨天的解法是这些变量放到最后才自增，昨天的题也有像这样分开自增的。看来这种写法更广泛
            
            for (int i = rowStart; i <= rowEnd; i ++) { //这里少了一个判断
                matrix[i][colEnd] = num ++; //change
            }
            colEnd --;
            
            for (int i = colEnd; i >= colStart; i --) {
                if (rowStart <= rowEnd)  //其他地方基本一样，除了这里加了判断
                    matrix[rowEnd][i] = num ++; //change
            }
            rowEnd --;
            
            for (int i = rowEnd; i >= rowStart; i --) {
                if (colStart <= colEnd)
                    matrix[i][colStart] = num ++; //change
            }
            colStart ++;
        }
        
        return matrix;
    }
}
```

```
Runtime
92 ms
Beats
82.28%
Memory
36.6 MB
Beats
41.77%
```