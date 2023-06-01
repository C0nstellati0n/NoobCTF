# Shortest Path in Binary Matrix

[题目](https://leetcode.com/problems/shortest-path-in-binary-matrix/description/)

Yet another BFS. 类似的“找最短路径”之前做过([Shortest Bridge](./Shortest%20Bridge.md),多源bfs)，于是不久答案就出来了。
```c#
public class Solution {
    public int ShortestPathBinaryMatrix(int[][] grid) {
        int len = grid.Length;
        if(grid[0][0]!=0||grid[len-1][len-1]!=0){
            return -1;
        }
        if(len==1){
            return 1;
        }
        Queue<int[]> queue = new Queue<int[]>();
        int[,] dir = new int[,]{{1,0},{-1,0},{0,1},{0,-1},{-1,-1},{1,-1},{-1,1},{1,1}};
        bool[,] visited = new bool[len,len];
        int level = 1;
        queue.Enqueue(new int[]{0,0});
        while(queue.Count>0){
            int size = queue.Count();
            for(int i = 0; i < size; i++){
                int[] cell = queue.Dequeue();
                for(int k = 0; k < 8; k++){
                    int new_i = cell[0] + dir[k, 0];
                    int new_j = cell[1] + dir[k, 1];
                    if(new_i<0 || new_i>=len || new_j<0 || new_j>=len || visited[new_i,new_j]||grid[new_i][new_j]!=0)
                        continue;
                    if(new_i==len-1&&new_j == len-1)
                        return level+1;

                    queue.Enqueue(new int[]{new_i, new_j});
                    visited[new_i, new_j] = true;
                }
            }
            level++;
        }
        return -1;
    }
}
```
```
Runtime
130 ms
Beats
95.93%
Memory
55.8 MB
Beats
51.22%
```
还发现了A*（A star寻路算法）做法。
```c#
//https://leetcode.com/problems/shortest-path-in-binary-matrix/solutions/313347/a-search-in-python/
public class Solution {
    // eight directions sorted in clockwise order
    public static int[,] DIRECTIONS = new int[,]{{0, -1}, {1, -1}, {1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}, {-1, -1}};
    public int ShortestPathBinaryMatrix(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        int endX = m - 1, endY = n - 1;
        
        if (grid[endX][endY] == 1) return -1; // early exit
        
        // Initialize the open list -> which node we expand next?
        Queue<Node> pq = new();
        
        // Initialize the closed list -> which nodes we've already visited? What is the minimum g from start node to this?
        int[] closed = new int[m * n];
        Array.Fill(closed, Int32.MaxValue);
        
        // put the starting node on the open list
        pq.Enqueue(new Node(0, 0, 1, Math.Max(m, n)));
        
        // while the open list is not empty
        while (pq.Count!=0) {
            
            // retrive the node with the least f on the open list, call it "node"
            Node node = pq.Dequeue();
            
            int x = node.x;
            int y = node.y;
            
            // skip disallowed area
            if (x < 0 || x >= m || y < 0 || y >= n || grid[x][y] == 1) continue;
            
            // if node is the goal, stop search
            if (x == endX && y == endY) return node.g;
            
            // if a node with the same position is in the closed list
            // which has a lower or equals g than this, skip this expansion
            if (closed[x * m + y] <= node.g) continue;
            
            // push node on the closed list
            closed[x * m + y] = node.g;
            
            // generate 8 successors to node
            for(int i=0;i<8;i++) {
                // for each successor
                // successor.g = node.g + distance between successor and node (equals to 1)
                // successor.h = estimate distance from successor to goal
                int g = node.g + 1;
                
                // h(node) is a heuristic function that 
                // estimates the cost of the cheapest path from node to the goal
                
                // Here we use **Diagonal Distance** as heuristic function, 
                // because we can and only can move in eight directions
                int h = Math.Max(Math.Abs(endX - x), Math.Abs(endY - y));
                
                // push the successor on the open list
                pq.Enqueue(new Node(x + DIRECTIONS[i,0], y + DIRECTIONS[i,1], g, h));
            }
        }
        
        return -1;
    }
}
public class Node:IComparable{
    // coordinate
    public int x;
    public int y;
    
    // g(node) is the cost of the path from the start node to node
    public int g;
    // f(node) = g(node) + h(node)
    public int f;
    
    public Node(int x, int y, int g, int h) {
        this.x = x;
        this.y = y;
        this.g = g;
        this.f = g + h;
    }
    
    public int CompareTo(Object node) {

        return this.f - (node as Node).f;
    }
}
```
```
Runtime
169 ms
Beats
43.9%
Memory
57 MB
Beats
32.52%
```
最后再提供一个c++的多种解法：https://leetcode.com/problems/shortest-path-in-binary-matrix/solutions/1063734/c-optimised-bfs-vs-dfs-fastest-solution-to-date-100-time-35ms-99-space-18-3mb/ 。我与c++势不两立，这玩意真的好难改啊，很多引用的传参放到c#里不知道怎么搞，用ref吗？