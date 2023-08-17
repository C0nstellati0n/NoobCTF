# 01 Matrix

[题目](https://leetcode.com/problems/01-matrix/description/)

代码很好，除了内存炸了而已。
```c#
public class Solution {
    public int[][] UpdateMatrix(int[][] mat) {
        int xlen = mat.Length;
        int ylen=mat[0].Length;
        Queue<int[]> queue = new Queue<int[]>();
        int[,] dir = new int[,]{{1,0},{-1,0},{0,1},{0,-1}};
        bool[,] visited = new bool[xlen,ylen];
        int level = 1;
        int[][] ans=new int[xlen][];
        for(int i = 0; i < xlen; i++){
            ans[i]=new int[ylen];
            for(int j = 0; j < ylen; j++){
                if(mat[i][j] == 0){
                    queue.Enqueue(new int[]{i,j});
                    ans[i][j]=0;
                    visited[i,j]=true;
                }
            }
        }
        while(queue.Count>0){
            int size = queue.Count();
            for(int i = 0; i < size; i++){ //遍历当前queue中所有的起点node
                int[] cell = queue.Dequeue();
                for(int k = 0; k < 4; k++){
                    int new_i = cell[0] + dir[k, 0];
                    int new_j = cell[1] + dir[k, 1];
                    if(new_i<0 || new_i>=xlen || new_j<0 || new_j>=ylen || visited[new_i,new_j])
                        continue;
                    if(mat[new_i][new_j] == 1) //如果延伸到另一个岛了就返回延伸的层数
                        ans[new_i][new_j]=level;
                    queue.Enqueue(new int[]{new_i, new_j}); //把接下来的node放入queue
                    visited[new_i, new_j] = true;
                }
            }
            level++; //一整个for循环遍历完代表一层
        }
        return ans;
    }
}
```
```
Runtime
178 ms
Beats
98.61%
Memory
81 MB
Beats
6.2%
```
这种找路径长度的推荐多源bfs。我这题的代码都是从[Shortest Bridge](./Shortest%20Bridge.md)的代码改过来的。

O(1)内存多源bfs/dp解法：https://leetcode.com/problems/01-matrix/solutions/1369741/c-java-python-bfs-dp-solutions-with-picture-clean-concise-o-1-space/ 。这个做法把题目给的mat当visited和结果数组，这波内存省了可不是一点半点。以及dp解法，从两个方向遍历也是我没见过的。好理解但是我想不出来。