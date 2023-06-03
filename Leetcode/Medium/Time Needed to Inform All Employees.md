# Time Needed to Inform All Employees

[题目](https://leetcode.com/problems/time-needed-to-inform-all-employees/description/)

所以这题是树对吧？但是不是二叉树？而且考点是maximum root to leaf path sum？哦，那我不会了。

```c#
//https://leetcode.com/problems/time-needed-to-inform-all-employees/solutions/532560/java-c-python-dfs/
//top down dfs
public class Solution {
    public int NumOfMinutes(int n, int headID, int[] manager, int[] informTime) {
        Dictionary<int,List<int>> graph = new();
        int total = 0;
        for (int i = 0; i < manager.Length; i++) {
            int j = manager[i];
            if (!graph.ContainsKey(j))
                graph[j]=new();
            graph[j].Add(i); //根据题目给出的数据构建树
        }
        return dfs(graph, informTime, headID); //从树的根开始遍历
    }
    private int dfs(Dictionary<int,List<int>> graph, int[] informTime,int cur) {
        int max = 0;
        if (!graph.ContainsKey(cur))
            return max;
        for (int i = 0; i < graph[cur].Count; i++)
            max = Math.Max(max, dfs(graph, informTime, graph[cur][i])); //dfs遍历cur的所有下属，取出最大值
        return max + informTime[cur];
    }
}
```
```
Runtime
332 ms
Beats
62.96%
Memory
61.9 MB
Beats
37.4%
```
换一个方向dfs：bottom up。咱也不知道为啥简单了这么多。
```c#
//https://leetcode.com/problems/time-needed-to-inform-all-employees/solutions/532560/java-c-python-dfs/
public class Solution {
    public int NumOfMinutes(int n, int headID, int[] manager, int[] informTime) {
        int res = 0;
        for (int i = 0; i < n; ++i)
            res = Math.Max(res, dfs(i, manager, informTime));
        return res;
    }
    public int dfs(int i, int[] manager, int[] informTime) {
        if (manager[i] != -1) {
            informTime[i] += dfs(manager[i], manager, informTime);
            manager[i] = -1;
        }
        return informTime[i];
    }
}
```
```
Runtime
269 ms
Beats
96.30%
Memory
51.8 MB
Beats
91.36%
```
当然也能bfs。
```c#
//https://leetcode.com/problems/time-needed-to-inform-all-employees/solutions/533109/java-python-bfs-dfs-solutions-clean-code/
class Solution {
    public int NumOfMinutes(int n, int headID, int[] manager, int[] informTime) {
        List<int>[] graph = new List<int>[n];
        for (int i = 0; i < n; i++) graph[i] = new();
        for (int i = 0; i < n; i++) if (manager[i] != -1) graph[manager[i]].Add(i);
        Queue<int[]> q = new(); // Since it's a tree, we don't need `visited` array
        q.Enqueue(new int[]{headID, 0});
        int ans = 0;
        while (q.Count!=0) {
            int[] top = q.Dequeue();
            int u = top[0], w = top[1];
            ans = Math.Max(w, ans);
            foreach(int v in graph[u]) q.Enqueue(new int[]{v, w + informTime[u]});
        }
        return ans;
    }
}
```
```
Runtime
319 ms
Beats
71.60%
Memory
65.9 MB
Beats
13.58%
```