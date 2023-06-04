# Number of Provinces

[题目](https://leetcode.com/problems/number-of-provinces/description/)

我感觉力量回来了！

```c#
public class Solution {
    public int FindCircleNum(int[][] isConnected) {
        bool[] visited=new bool[isConnected.Length];
        int count=0;
        for(int i=0;i<isConnected.Length;i++){
            if(!visited[i]){
                dfs(isConnected,visited,i);
                count++;
            }
        }
        return count;
    }
    public void dfs(int[][] grid,bool[] visited,int node) {
        if(visited[node]){
            return;
        }
        visited[node]=true;
        for(int i=0;i<grid[node].Length;i++){
            if(grid[node][i]!=0){
                dfs(grid,visited,i);
            }
        }
    }
}
```
```
Runtime
98 ms
Beats
97.35%
Memory
45.4 MB
Beats
30.88%
```
无所谓，union find会出手。
```c#
//https://leetcode.com/problems/number-of-provinces/solutions/101336/java-solution-union-find/
public class Solution {
    class UnionFind {
        private int count = 0;
        private int[] parent, rank;
        
        public UnionFind(int n) { //初始都不是连在一起的，于是有n个node，count就是n
            count = n;
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
            }
        }
        
        public int find(int p) {
        	while (p != parent[p]) {
                parent[p] = parent[parent[p]];    // path compression by halving
                p = parent[p];
            }
            return p;
        }
        
        public void union(int p, int q) {
            int rootP = find(p);
            int rootQ = find(q);
            if (rootP == rootQ) return;
            if (rank[rootQ] > rank[rootP]) {
                parent[rootP] = rootQ;
            }
            else {
                parent[rootQ] = rootP;
                if (rank[rootP] == rank[rootQ]) {
                    rank[rootP]++;
                }
            }
            count--; //每次union count--，两个node->一个node
        }
        
        public int Count() {
            return count;
        }
    }
    
    public int FindCircleNum(int[][] M) {
        int n = M.Length;
        UnionFind uf = new UnionFind(n);
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (M[i][j] == 1) uf.union(i, j); //连接方式不会重复
            }
        }
        return uf.Count();
    }
}
```
```
Runtime
97 ms
Beats
97.94%
Memory
45 MB
Beats
58.24%
```