# [Parallel Courses III](https://leetcode.com/problems/parallel-courses-iii)

读题——发现题是以前做过的知识点——哇这题不难，应该能做——翻出笔记抄上答案——修改跑testcase发现报错——debug——啊好难我要死在debug了——发现之前忽略的细节，修改——没bug了！给的几个testcase都过了——去找新的testcase——wrong answer——仔细阅读错的testcase——发现之前忽略的非常重要的细节+难点——靠不会做了好难——看答案——什么原来这么简单吗

主打的就是一个过山车式的心肌梗塞
```c#
//https://leetcode.com/problems/parallel-courses-iii/editorial
//Topological Sort, Kahn's Algorithm
//还有个dfs（dp）做法
class Solution {
    public int MinimumTime(int n, int[][] relations, int[] time) {
        Dictionary<int, List<int>> graph = new();
        for (int i = 0; i < n; i++) {
            graph[i]=new();
        }
        int[] indegree = new int[n];
        foreach(int[] edge in relations) {
            int x = edge[0] - 1;
            int y = edge[1] - 1;
            graph[x].Add(y);
            indegree[y]++;
        }
        Queue<int> queue = new();
        int[] maxTime = new int[n];
        for (int node = 0; node < n; node++) {
            if (indegree[node] == 0) {
                queue.Enqueue(node);
                maxTime[node] = time[node];
            }
        }
        //前面都是Kahn's Algorithm的常规设置（除了maxTime）
        while (queue.Any()) {
            int node = queue.Dequeue();
            foreach(int neighbor in graph[node]) {
                maxTime[neighbor] = Math.Max(maxTime[neighbor], maxTime[node] + time[neighbor]); //自己做的时候卡在这里，没想到用个数组记时间
                indegree[neighbor]--;
                if (indegree[neighbor] == 0) {
                    queue.Enqueue(neighbor);
                }
            }
        }
        int ans = 0;
        for (int node = 0; node < n; node++) {
            ans = Math.Max(ans, maxTime[node]); //因为要完成所有课程并且可以同时进行多门课程，所以最终用时就是耗时最久的node
        }
        return ans;
    } 
}
```
但是表现没有采样区的好。估计是因为采样区最后计算ans时直接在遍历图表时顺便算了，就不用后面的for循环了
```c#
public class Solution {
    public int MinimumTime(int n, int[][] relations, int[] time) {
    //> graph
    //> start at all no input nodes
    //> when move to next nodes, check count of completed inputs, and set max
    //> if no next, set max=max(max,final val)
        List<int>[] adjList = new List<int>[n + 1];
        for (int node = 1; node <= n; node++)
            adjList[node] = new();
        int[] countInputs = new int[n + 1];
        foreach (var relation in relations)
        {
            adjList[relation[0]].Add(relation[1]);
            countInputs[relation[1]]++;
        }
        Stack<int> visitings = new(); //以及这里用的是stack。感觉有点dfs了，因为stack后进先出，后续push neighbour然后pop时先出来的是后面push进的node
        for (int node = 1; node <= n; node++)
            if (countInputs[node] == 0)
                visitings.Push(node);
        int max = 0;
        int[] preMaxTimes = new int[n + 1];
        while (visitings.Count > 0)
        {
            var node = visitings.Pop();
            var curTime = preMaxTimes[node] + time[node - 1];
            var nexts = adjList[node];
            if (nexts.Count == 0)
            {
                max = Math.Max(max, curTime); //当一个node没有任何邻居时，可以计算max了。不难理解max一定出现在这些最后面的node
                continue;
            }
            foreach (var next in nexts)
            {
                preMaxTimes[next] = Math.Max(preMaxTimes[next], curTime);
                countInputs[next]--;
                if (countInputs[next] == 0)
                    visitings.Push(next);
            }
        }
        return max;
    }
}
```