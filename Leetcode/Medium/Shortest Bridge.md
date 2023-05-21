# Shortest Bridge

[题目](https://leetcode.com/problems/shortest-bridge/description/)

首先是大佬给出的最简单最好理解的一种解法。感觉和dfs和bfs关系不大，但也不懂这种算法的名字。有人在solution里提到洪水（flood fill），感觉挺形象的，不过不确定。

```c#
//https://leetcode.com/problems/shortest-bridge/solutions/189293/c-bfs-island-expansion-uf-bonus/
//强烈推荐去看解法里的图，一看就懂
public class Solution {
    int paint(int[][] A, int i, int j) {
        if (Math.Min(i, j) < 0 || Math.Max(i, j) == A.Length || A[i][j] != 1) //判断有没有越界或者是不是岛
            return 0;
        A[i][j] = 2; //是岛就标2
        return 1 + paint(A, i + 1, j) + paint(A, i - 1, j) + paint(A, i, j + 1) + paint(A, i, j - 1); //把整个岛全标上2
    }
    bool expand(int[][] A, int i, int j, int cl) {
        if (Math.Min(i, j) < 0 || Math.Max(i, j) == A.Length)
            return false;
        A[i][j] = A[i][j] == 0 ? cl + 1 : A[i][j]; //岛标上2，围着岛的一圈是3，再外一圈是4……一直延伸
        return A[i][j] == 1; //这样一直延伸，一定会延伸到另外一个岛。那个时候就能停下了，当前的cl-2就是层数，即题目要求的返回值
    }  
    public int ShortestBridge(int[][] A) {
        for (int i = 0, found = 0; found==0 && i < A.Length; ++i)
            for (int j = 0; found==0 && j < A[0].Length; ++j)
                found = paint(A, i, j); //题目指定了只有两个岛，这里把第一个岛标成2（哪个岛先遍历到哪个就是第一个岛）
        for (int cl = 2; ; ++cl) //这是个无限循环。知道有这种写法但我从来没写过
            for (int i = 0; i < A.Length; ++i)
                for (int j = 0; j < A.Length; ++j) 
                    if (A[i][j] == cl && ((expand(A, i - 1, j, cl) || expand(A, i, j - 1, cl) || //从刚刚标好的岛开始，向四方延伸
                        expand(A, i + 1, j, cl) || expand(A, i, j + 1, cl))))
                            return cl - 2;
    }
}
```
```
Runtime
125 ms
Beats
85.48%
Memory
50 MB
Beats
100%
```
相同的思路还能用list来实现。list那一部分就有点像下一个解法的bfs了。
```c#
public class Solution {
    int[] dir = {0, 1, 0, -1, 0};
    void paint(int[][] A, int i, int j, List<Tuple<int,int>> q) {
        if (Math.Min(i, j) >= 0 && Math.Max(i, j) < A.Length && A[i][j] == 1) {
            A[i][j] = 2;
            q.Add(new Tuple<int,int>(i, j));
            for (int d = 0; d < 4; ++d)
                paint(A, i + dir[d], j + dir[d + 1], q);
        }
    }
    public int ShortestBridge(int[][] A) {
        List<Tuple<int,int>> q=new();
        for (int i = 0; q.Count == 0 && i < A.Length; ++i)
            for (int j = 0; q.Count == 0 && j < A[0].Length; ++j)
                paint(A, i, j, q);
        while (q.Count!=0) {
            List<Tuple<int,int>> q1=new();
            foreach(var (i, j) in q) {
                for (int d = 0; d < 4; ++d) {
                    int x = i + dir[d], y = j + dir[d + 1];
                    if (Math.Min(x, y) >= 0 && Math.Max(x, y) < A.Length) {
                        if (A[x][y] == 1)
                            return A[i][j] - 2;
                        if (A[x][y] == 0) {
                            A[x][y] = A[i][j] + 1;
                            q1.Add(new Tuple<int,int>(x, y));
                        }
                    }
                }
            }
            swap(ref q, ref q1);
        }
        return 0;
    }
    void swap<T>(ref T a, ref T b)
    {
        T temp;
        temp = a;
        a = b;
        b = temp;
    }
}
```
```
Runtime
118 ms
Beats
93.55%
Memory
53.5 MB
Beats
64.52%
```
最后是dfs+multi-source bfs（多源bfs）。dfs用来找第一个岛，多源bfs用来找从第一个岛到第二个岛的最短路径。
```c#
public class Solution {
    public int ShortestBridge(int[][] grid) {
        int len = grid.Length;
        Queue<int[]> queue = new Queue<int[]>();
        int[,] dir = new int[,]{{1,0},{-1,0},{0,1},{0,-1}};
        bool[,] visited = new bool[len,len];
        int level = 0;

        for(int i = 0; i < len; i++){
            for(int j = 0; j < len; j++){
                if(grid[i][j] == 1 && queue.Count == 0){
                    dfs(i, j, grid, queue, dir, visited);
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
                    if(new_i<0 || new_i>=len || new_j<0 || new_j>=len || visited[new_i,new_j])
                        continue;
                    if(grid[new_i][new_j] == 1) //如果延伸到另一个岛了就返回延伸的层数
                        return level;

                    queue.Enqueue(new int[]{new_i, new_j}); //把接下来的node放入queue
                    visited[new_i, new_j] = true;
                }
            }
            level++; //一整个for循环遍历完代表一层
        }

        return level;
    }

    private void dfs(int row, int col, int[][] grid, Queue<int[]> queue, int[,] dir, bool[,] visited){
        queue.Enqueue(new int[]{row,col}); //把第一个岛所有的node放入queue，作为多源bfs的全部起点
        visited[row,col] = true;
        for(int k = 0; k < 4; k++){
            int new_i = row + dir[k,0];
            int new_j = col + dir[k,1];

            if(new_i<0 || new_i>=grid.Length || new_j<0 || new_j>=grid.Length || visited[new_i,new_j] == true || grid[new_i][new_j] == 0)
                continue;
            dfs(new_i, new_j, grid, queue, dir, visited);
        }
    }
}
```
```
Runtime
127 ms
Beats
83.87%
Memory
53.4 MB
Beats
64.52%
```
让chatgpt来告诉我什么是多源bfs。
```
Multi-source BFS is an algorithm to find the shortest path between multiple sources and a destination in an unweighted graph. Here are the steps to implement it:

Multi-source BFS works in the same way as regular BFS, but instead of starting with a single node, you would put all your sources in the queue at the beginning. That is, make a pass over the graph to find all sources and initialize your BFS queue with all of them at distance 0. Then proceed with BFS as normal.

First, initialize the queue with all the positions of the sources in the graph. Then, each time you pop a position at the front of the queue, push all the positions which can be reached by 1 step and hasn't been visited yet. The first time you visit the destination, you get the shortest path from all the sources to the destination.

An even better method is to use the Multisource BFS which is a modification of BFS. We will put all the source vertices in the queue at first rather than a single vertex. This way, Multisource BFS will first visit all the source vertices. After that, it will visit the vertices which are at a distance of 1 from all source vertices, then at a distance of 2 from all source vertices and so on and so forth.
```