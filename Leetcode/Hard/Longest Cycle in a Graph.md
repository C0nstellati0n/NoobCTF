# Longest Cycle in a Graph

[题目](https://leetcode.com/problems/longest-cycle-in-a-graph/description/)

图表题，大佬们的解基本集中在变异dfs上，除了几个用[Floyd Cycle Detection Algorithm](https://medium.com/@orionssl/%E6%8E%A2%E7%B4%A2-floyd-cycle-detection-algorithm-934cdd05beb9)(Floyd判圈算法,龟兔赛跑算法,Tortoise and Hare Algorithm)。

```c#
//https://leetcode.com/problems/longest-cycle-in-a-graph/solutions/3341780/clean-codes-full-explanation-d-f-s-c-java-python3/
//dfs变种
class Solution {
  public int LongestCycle(int[] edges) {
    int ans = -1; // Initialize the answer to -1
    int time = 1; // Initialize the current time step to 1。time变量最后肯定会达到edges的长度，且不会超出于它。
    int[] timeVisited = new int[edges.Length]; // Initialize an array to store the time at which each node was first visited

    // Iterate through each node in the graph
    for (int i = 0; i < edges.Length; ++i) {
      if (timeVisited[i] > 0) // If the node has already been visited, skip it
        continue;
      int startTime = time; // Record the start time of the current traversal
      int u = i; // Initialize the current node to the ith node
      // Traverse the graph until the end of the path is reached or a visited node is encountered
      while (u != -1 && timeVisited[u] == 0) {
        timeVisited[u] = time++; // Record the current time step and increment time。注意自增顺序，先赋值再自增
        u = edges[u]; // Move to the next node in the path
      }
      // If a cycle is found that includes the current node, update the answer
      if (u != -1 && timeVisited[u] >= startTime)//因为timeVisited[u] = time++;，只要进到while循环里面了，timeVisited[u]就不可能小于startTime
        ans = Math.Max(ans, time - timeVisited[u]);
    }

    return ans; // Return the Length of the longest cycle found
  }
}
```

```
Runtime
229 ms
Beats
100%
Memory
53 MB
Beats
72.73%
```

这个方法一直看得我云里雾里的。人工在测试用例上运行了一遍倒是知道答案怎么来的了，不过仅此而已。没找到这里面的通用名（例如有些思想叫dfs/bfs，这种思想叫什么我还真不知道），看看以后有没有类似的题吧。

```c#
//https://leetcode.com/problems/longest-cycle-in-a-graph/solutions/3342721/image-explanation-complete-intuition-dfs-c-java-python/
//dfs
class Solution {
    int answer = -1;

    public void dfs(int node, int[] edges, Dictionary<int, int> dist, bool[] visit) {
        visit[node] = true;
        int neighbor = edges[node];

        if (neighbor != -1 && !visit[neighbor]) {
            dist.Add(neighbor, dist[node] + 1);
            dfs(neighbor, edges, dist, visit);
        } else if (neighbor != -1 && dist.ContainsKey(neighbor)) {
            answer = Math.Max(answer, dist[node] - dist[neighbor] + 1);
        }
    }

    public int LongestCycle(int[] edges) {
        int n = edges.Length;
        bool[] visit = new bool[n];

        for (int i = 0; i < n; i++) {
            if (!visit[i]) {
                Dictionary<int, int> dist = new();
                dist.Add(i, 1);
                dfs(i, edges, dist, visit);
            }
        }
        return answer;
    }
}
```

```
Runtime
415 ms
Beats
27.27%
Memory
75.7 MB
Beats
45.45%
```

这种至少能看出来dfs的影子，再用一个字典记录各个node的距离。总之就是跟着一个node走下去，要是走回原来的node了就用公式算出结果。

```c#
//https://leetcode.com/problems/longest-cycle-in-a-graph/solutions/3341780/clean-codes-full-explanation-d-f-s-c-java-python3/
//Floyd Cycle Detection Algorithm
class Solution {
  public int LongestCycle(int[] edges) {
    int maxLength = -1;
    int n = edges.Length;
    int[] dp=new int[n];
    Array.Fill(dp,-1);
    for(int i=0;i<n;i++){
        if(edges[i] != -1){
            int fast = i;
            int slow = i;
            while(fast != -1 && edges[fast] != -1){
                fast = edges[edges[fast]];
                slow = edges[slow];
                if(fast == slow){
                    int cnt = 1;
                    slow = edges[slow];
                    while(slow != fast){
                        slow = edges[slow];
                        cnt++;
                    }
                    maxLength = Math.Max(maxLength,cnt);
                    dp[i] = maxLength;
                    break;
                }
                if(dp[slow] != -1){
                    dp[i] = dp[slow];
                    break;
                }
            }
        }
    }
    return maxLength;
    }
}
```

```
Runtime
302 ms
Beats
63.64%
Memory
52.7 MB
Beats
72.73%
```

这个算法主要就是用两个指针，一个slow每次走一步，另一个fast每次走两步。如果图表中有一个循环，fast一定能走一圈回来后追上slow，和其相等。如果它们相等，那就让slow沿着走一圈，记录一圈的node数量。dp的作用是优化运行速度，省略之前已记录过的node长度，不走重复路。不加会有`Time Limit Exceeded`。