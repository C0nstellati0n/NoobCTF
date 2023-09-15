# Reconstruct Itinerary

[题目](https://leetcode.com/problems/reconstruct-itinerary)

没见过的图论新知识。这题是[Semi-Eulerian Graph](http://mathonline.wikidot.com/eulerian-graphs-and-semi-eulerian-graphs)(链接里也有Eulerian Graph的介绍，一起学了吧)。Eulerian Graph指的是那些node全部连接在一起且存在一条无重复edge的路径经过所有node的graph。也就是说，从一个vertex开始，把每条edge不重复地走一次，经过所有vertex后还能回到起点。倒也不用看这么长的定义，只需要知道：A graph is Eulerian if and only if each vertex has an even degree. 而Semi-Eulerian Graph顾名思义，Eulerian Graph的一半。走不重复edge时不用回到起点vertex。A graph is semi-Eulerian if and only if there is one pair of vertices with odd degree（pair所以是两个）。这题的要求等同于找Semi-Eulerian Graph里的[Eulerian path](https://en.wikipedia.org/wiki/Eulerian_path)。你问我什么是Eulerian path？Eulerian trail (or Eulerian path) is a trail in a finite graph that visits every edge exactly once (allowing for revisiting vertices).
```c#
//https://leetcode.com/problems/reconstruct-itinerary/solutions/4041944/95-76-dfs-recursive-iterative/
//也可以看看 https://leetcode.com/problems/reconstruct-itinerary/solutions/4042004/beats-99-17-dfs-recursive-iterative-euler-path-intuition-commented-code/
public class Solution {
    public IList<string> FindItinerary(IList<IList<string>> tickets) {
        var graph = new Dictionary<string, List<string>>();
        foreach (var ticket in tickets) { //build graph
            if (!graph.ContainsKey(ticket[0])) {
                graph[ticket[0]] = new List<string>();
            }
            graph[ticket[0]].Add(ticket[1]);
        }
        foreach (var key in graph.Keys) {
            graph[key].Sort((a, b) => b.CompareTo(a)); //按照lexical order倒序排序
        }
        var stack = new Stack<string>();
        stack.Push("JFK");
        var itinerary = new List<string>();
        while (stack.Count > 0) { //dfs
            string curr = stack.Peek();
            if (graph.ContainsKey(curr) && graph[curr].Count > 0) {
                var next = graph[curr].Last();
                graph[curr].RemoveAt(graph[curr].Count - 1);
                stack.Push(next);
            } else {
                itinerary.Add(stack.Pop());
            }
        }
        itinerary.Reverse();
        return itinerary;
    }
}
```
```
Runtime
157 ms
Beats
91.91%
Memory
57.8 MB
Beats
68.38%
```
我打算自己演算一遍dfs到底是怎么运行的。拿example2的`[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]`。
- JFK进栈，进入if语句。curr=JFK,next=SFO,移除并push进栈。目前stack:JFK,SFO
- curr=SFO,进入if语句。next=ATL,移除并push进栈。目前stack:JFK,SFO,ATL
- curr=ATL,进入if语句。next=SFO,移除并push进栈。目前stack:JFK,SFO,ATL,SFO
- curr=SFO,进入else语句。itinerary添加SFO,stack pop SFO.目前itinerary:SFO.目前stack:JFK,SFO,ATL
- curr=ATL,进入if语句。next=JFK,移除并push进栈。目前stack:JFK,SFO,ATL,JFK
- curr=JFK,进入if语句。next=ATL,移除并push进栈。目前stack:JFK,SFO,ATL,JFK,ATL
- curr=ATL,进入else语句。itinerary添加ATL,stack pop ATL.目前itinerary:SFO,ATL.目前stack:JFK,SFO,ATL,JFK
- curr=JFK,进入else语句。itinerary添加JFK,stack pop JFK.目前itinerary:SFO,ATL,JFK.目前stack:JFK,SFO,ATL
- curr=ATL,进入else语句。itinerary添加ATL,stack pop ATL.目前itinerary:SFO,ATL,JFK,ATL.目前stack:JFK,SFO
- curr=SFO,进入else语句。itinerary添加SFO,stack pop SFO.目前itinerary:SFO,ATL,JFK,ATL,SFO.目前stack:JFK
- curr=JFK,进入else语句。itinerary添加JFK,stack pop JFK.目前itinerary:SFO,ATL,JFK,ATL,SFO,JFK.目前stack为空
- 返回结果itinerary.Reverse():JFK,SFO,ATL,JFK,ATL,SFO

完成。虽然不懂什么原理。