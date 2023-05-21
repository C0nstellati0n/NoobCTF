# Evaluate Division

[题目](https://leetcode.com/problems/evaluate-division/description/)

费劲心思改写了几种做法，还有几种真改不出来。

```c#
//随便在solution里翻到的一个原生c#解法。让我发现了原来c#也有zip函数
public class Solution
{
    public double[] CalcEquation(IList<IList<string>> eq, double[] vals, IList<IList<string>> q)
    {
        Dictionary<string, Dictionary<string, double>> map = new();
        HashSet<string> visited = new();

        foreach (var (num, den, val) in eq.Zip(vals, (e, v) => (e[0], e[1], v)))
        {
            if (!map.ContainsKey(num)) map[num] = new();
            if (!map.ContainsKey(den)) map[den] = new();

            map[num][den] = 1 / val;
            map[den][num] = val;
        }

        return q.Select(s => FindResult(s[1], s[0])).ToArray();
        //函数里原来也能定义函数
        double FindResult(string s, string t)
        {
            if (!map.ContainsKey(s)) return -1;
            if (s == t) return 1;
            
            double cur = -1;
            visited.Add(s);
            
            foreach (var k in map[s].Keys)
            {
                if (visited.Contains(k)) continue;
                cur = FindResult(k, t);
                if (cur != -1)
                {
                    cur *= map[s][k];
                    break;
                }
            }

            visited.Remove(s);
            return cur;
        }
    }
}
```
```
Runtime
159 ms
Beats
26.88%
Memory
43.2 MB
Beats
32.26%
```
怎么也没想到这题竟然也是图表题。图表题怎么能少得了dfs呢？
```c#
//https://leetcode.com/problems/evaluate-division/solutions/171649/1ms-dfs-with-explanations/
public class Solution
{
        public double[] CalcEquation(IList<IList<string>> eq, double[] vals, IList<IList<string>> q) {
        
        /* Build graph. */
        Dictionary<string, Dictionary<string, double>> graph = buildGraph(eq, vals);
        double[] result = new double[q.Count];
        
        for (int i = 0; i < q.Count; i++) {
            result[i] = getPathWeight(q[i][0], q[i][1], new HashSet<string>(), graph);
        }  
        
        return result;
    }
    
    private double getPathWeight(string start, string end, HashSet<string> visited, Dictionary<string, Dictionary<string, double>> graph) {
        
        /* Rejection case. */
        if (!graph.ContainsKey(start)) 
            return -1.0;
        
        /* Accepting case. */
        if (graph[start].ContainsKey(end))
            return graph[start][end];
        
        visited.Add(start);
        foreach(KeyValuePair<string, double> entry in graph[start]) {
            if (!visited.Contains(entry.Key)) {
                double productWeight = getPathWeight(entry.Key, end, visited, graph);
                if (productWeight != -1.0)
                    return entry.Value * productWeight;
            }
        }
        
        return -1.0;
    }
    
    private Dictionary<string, Dictionary<string, double>> buildGraph(IList<IList<string>> eq, double[] vals) {
        Dictionary<string, Dictionary<string, double>> graph = new();
        string u, v;
        
        for (int i = 0; i < eq.Count; i++) {
            u = eq[i][0];
            v = eq[i][1];
            graph.TryAdd(u, new());
            graph[u][v]=vals[i];
            graph.TryAdd(v, new());
            graph[v][u]=1 / vals[i];
        }
        
        return graph;
    }
}
```
```
Runtime
141 ms
Beats
95.70%
Memory
43.4 MB
Beats
6.45%
```
以及union find。
```c#
//https://leetcode.com/problems/evaluate-division/solutions/278276/java-union-find-and-dfs-query-o-1/
public class Solution {
    Dictionary<string, string> parents = new();
    Dictionary<string, double> vals = new();

    public double[] CalcEquation(IList<IList<string>> equations, double[] values, IList<IList<string>> queries) {
        double[] res = new double[queries.Count];
        for (int i = 0; i < values.Length ; ++i )
            union(equations[i][0], equations[i][1], values[i]);
        for (int i = 0; i < queries.Count; ++i) {
            string x = queries[i][0], y = queries[i][1];
            res[i] = (parents.ContainsKey(x) && parents.ContainsKey(y) && find(x) == find(y)) ? vals[x] / vals[y] : -1.0;
        }
        return res;
    }

    public void add(string x) {
        if (parents.ContainsKey(x)) return;
        parents[x]=x;
        vals[x]=1.0;
    }

    public string find(string x) {
        string p = parents.GetValueOrDefault(x, x);
        if (x != p) {
            string pp = find(p);
            vals[x]=vals[x] * vals[p];
            parents[x]=pp;
        }
        return parents.GetValueOrDefault(x, x);
    }

    public void union(string x, string y, double v) {
        add(x); 
        add(y);
        string px = find(x), py = find(y);
        parents[px]=py;
        vals[px]=v * vals[y] / vals[x];
    }
}
```
```
Runtime
148 ms
Beats
86.2%
Memory
43.2 MB
Beats
13.98%
```
[bfs](https://leetcode.com/problems/evaluate-division/solutions/88275/python-fast-bfs-solution-with-detailed-explantion/)和[Floyd Warshall](https://leetcode.com/problems/evaluate-division/solutions/88175/9-lines-floyd-u2013warshall-in-python/).这两个都太难改了（python用起来是真方便，改成其他语言也是真麻烦）。