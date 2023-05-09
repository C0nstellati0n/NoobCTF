# Spiral Matrix

[题目](https://leetcode.com/problems/spiral-matrix/description/)

这题如果我多想一会的话，应该是能做出来的。毕竟没有涉及什么新的编程思想（天塌下来都有我的嘴顶着）。

```c#
//https://leetcode.com/problems/spiral-matrix/solutions/20599/super-simple-and-easy-to-understand-solution/?orderBy=most_votes
public class Solution {
    public IList<int> SpiralOrder(int[][] matrix) {
        List<int> res = new(); 
        if (matrix == null || matrix.Length == 0) return res;
        int n = matrix.Length, m = matrix[0].Length;
        int up = 0,  down = n - 1;
        int left = 0, right = m - 1;
        while (res.Count < n * m) {
            for (int j = left; j <= right && res.Count < n * m; j++)
                res.Add(matrix[up][j]);
            
            for (int i = up + 1; i <= down - 1 && res.Count < n * m; i++)
                res.Add(matrix[i][right]);
                     
            for (int j = right; j >= left && res.Count < n * m; j--)
                res.Add(matrix[down][j]);
                        
            for (int i = down - 1; i >= up + 1 && res.Count < n * m; i--) 
                res.Add(matrix[i][left]);
                
            left++; right--; up++; down--; 
        }
        return res;
    }
}
```

```
Runtime
141 ms
Beats
53.47%
Memory
42.6 MB
Beats
7.10%
```

或者看起来更短一点的。

```c#
//https://leetcode.com/problems/spiral-matrix/solutions/20573/a-concise-c-implementation-based-on-directions/?orderBy=most_votes
public class Solution {
    public IList<int> SpiralOrder(int[][] matrix) {
        int[,] dirs=new int[4,2] {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        List<int> res=new();
        int nr = matrix.Length;     if (nr == 0) return res;
        int nc = matrix[0].Length;  if (nc == 0) return res;
        
        List<int> nSteps=new List<int>{nc, nr-1};
        
        int iDir = 0;   // index of direction.
        int ir = 0, ic = -1;    // initial position
        while (nSteps[iDir%2]!=0) {
            for (int i = 0; i < nSteps[iDir%2]; ++i) {
                ir += dirs[iDir,0]; ic += dirs[iDir,1];
                res.Add(matrix[ir][ic]);
            }
            nSteps[iDir%2]--;
            iDir = (iDir + 1) % 4;
        }
        return res;
    }
}
```

```
Runtime
138 ms
Beats
67.82%
Memory
42.2 MB
Beats
38.45%
```