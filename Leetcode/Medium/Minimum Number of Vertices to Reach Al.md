# Minimum Number of Vertices to Reach All Nodes

[题目](https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/description/)

这题只要看了提示就能知道，实际考的是返回入度为0的node。要是啥也不考虑的话，解法我一分钟就能出来。

```c#
public class Solution {
    public IList<int> FindSmallestSetOfVertices(int n, IList<IList<int>> edges) {
        List<int> numberList = Enumerable.Range(0,n).ToList();
        foreach(var edge in edges){
            if(numberList.Contains(edge[1]))
                numberList.Remove(edge[1]);
        }
        return numberList;
    }
}
```
```
Runtime
3230 ms
Beats
6.67%
Memory
69.1 MB
Beats
61.67%
```

或者按照普通的计算入度的方式做。

```c#
//https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/solutions/805685/java-c-python-nodes-with-no-in-degree/
public class Solution {
    public IList<int> FindSmallestSetOfVertices(int n, IList<IList<int>> edges) {
        List<int> res = new();
        int[] seen = new int[n];
        foreach(List<int> e in edges)
            seen[e[1]] = 1;
        for (int i = 0; i < n; ++i)
            if (seen[i] == 0)
                res.Add(i);
        return res;
    }
}
```
```
Runtime
478 ms
Beats
48.33%
Memory
69.4 MB
Beats
38.33%
```

稍微复杂一点，用union find。
```c#
//https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/solutions/805697/java-union-find/
class Solution {
    public int findParent(int[] parent, int i) {
        if(parent[i] == i) return i;
        return parent[i] = findParent(parent, parent[i]);
    }
    public IList<int> FindSmallestSetOfVertices(int n, IList<IList<int>> edges) {
        int[] parent = new int[n];
        bool[] visited = new bool[n];
        for(int i = 0; i < n; i++) parent[i] = i;
        for(int i = 0; i < edges.Count; i++) {
            var curr = edges[i];
            int sv = curr[0];
            int ev = curr[1];
            if(visited[ev]) continue;
            int p1 = findParent(parent, sv);
            int p2 = findParent(parent, ev);
            parent[p2] = p1; 
            visited[ev] = true;
        }
        List<int> ans = new();
        for(int i = 0; i < n; i++) if(parent[i] == i) ans.Add(i);
        return ans;
    }
}
```
```
Runtime
475 ms
Beats
51.67%
Memory
69.6 MB
Beats
28.33%
```
整那么多复杂的表现也就那样，不如就用第一种最容易理解的计算入度的办法，然后在数据结构上做文章。
```c#
public class Solution 
{
	public IList<int> FindSmallestSetOfVertices(int n, IList<IList<int>> edges) 
	{
		var result = new List<int>();
		var set = new HashSet<int>();
		
		for(int i = 0; i < edges.Count; i ++)
			set.Add(edges[i][1]);
		
		for(int i = 0; i < n; i ++)
			if(!set.Contains(i))
				result.Add(i);
				
		return result;
	}
}
```
```
Runtime
442 ms
Beats
100%
Memory
67.7 MB
Beats
86.67%
```