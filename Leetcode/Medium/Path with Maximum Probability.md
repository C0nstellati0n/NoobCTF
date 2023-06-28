# Path with Maximum Probability

[题目](https://leetcode.com/problems/path-with-maximum-probability/description/)

java改c#从来没有这么恼火过。为啥c#的priorityQueue老是报错“double不能转int”啊？我哪里写int了？不过另一种[Bellman-Ford算法](https://zhuanlan.zhihu.com/p/352724346)的改写还算成功。
```c#
//https://leetcode.com/problems/path-with-maximum-probability/solutions/731767/java-python-3-2-codes-bellman-ford-and-dijkstra-s-algorithm-w-brief-explanation-and-analysis/
//然后我发现同一种方法 https://leetcode.com/problems/path-with-maximum-probability/editorial/ 讲得更好。虽然这其实是Shortest Path Faster Algorithm，不过也算Bellman-Ford算法的改进算法
public class Solution {
    public double MaxProbability(int n, int[][] edges, double[] succProb, int start, int end) {
        Dictionary<int, List<int[]>> g = new();
        for (int i = 0; i < edges.Length; ++i) {
            int a = edges[i][0], b = edges[i][1];
            if(!g.ContainsKey(a)){
                g[a]=new();
            }
            g[a].Add(new int[]{b, i}); //构造邻接表，不过同时记录索引，方便下面获取succProb
            if(!g.ContainsKey(b)){
                g[b]=new();
            }
            g[b].Add(new int[]{a, i});
        }
        double[] p = new double[n]; //记录从start开始到i处的成功率
        p[start] = 1d;
        Queue<int> q = new();
        q.Enqueue(start);
        while (q.Count!=0) {
            int cur = q.Dequeue();
            if(g.ContainsKey(cur)){
                foreach(int[] a in g[cur]) { //和bfs很像，从start开始遍历所有邻居
                    int neighbor = a[0], index = a[1];
                    if (p[cur] * succProb[index] > p[neighbor]) {
                        p[neighbor] = p[cur] * succProb[index]; //若成功率比之前记录的还高，说明找到了另一条路（或者单纯第一条路，毕竟初始值为0）
                        q.Enqueue(neighbor); //与普通bfs的不同点在于，仅当几率更高时才Enqueue
                    }
                }
            }
        }
        return p[end];
    }
}
```
```
Runtime
235 ms
Beats
95.12%
Memory
55.6 MB
Beats
73.17%
```
Bellman-Ford算法是一种处理存在负权边的单元最短路问题的算法。虽然这题要求找的是最大几率而且没有负权边，不过这玩意没有负权其实也能用，最小和最大也只不过是反过来的关系。这题的重头戏应该是Dijkstra's Algorithm，然而我真改不出来，就不放了。