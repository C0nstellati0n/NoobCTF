# Course Schedule

[题目](https://leetcode.com/problems/course-schedule/description/)

这 道 题 我 用 了 不 到 十 分 钟 一 次 过！！！主要还是因为这题是拓扑排序的基础题，没有任何坑，且[昨天](./Find%20Eventual%20Safe%20States.md)做的就是拓扑排序。于是我直接一套，诶，成了！
```c#
public class Solution {
    public bool CanFinish(int numCourses, int[][] prerequisites) {
        int[] indegrees = new int[numCourses];
        List<List<int>> graph = new();
        for (int i = 0; i < numCourses; i++) {
            graph.Add(new());
        }
        foreach(int[] prerequisite in prerequisites) {
            graph[prerequisite[0]].Add(prerequisite[1]);
            indegrees[prerequisite[1]]++;
        }
        Queue<int> zeroIndegree = new();
        for (int i = 0; i < numCourses; i++) {
            if (indegrees[i] == 0) {
                zeroIndegree.Enqueue(i);
            }
        }
        int count=0;
        while (zeroIndegree.Any()) {
            int course = zeroIndegree.Dequeue();
            count++;
            foreach(int neighbor in graph[course]) {
                indegrees[neighbor]--;
                if (indegrees[neighbor] == 0) {
                    zeroIndegree.Enqueue(neighbor);
                }
            }
        }
        return count==numCourses;
    }
}
```
```
Runtime
111 ms
Beats
85.77%
Memory
44.5 MB
Beats
79.44%
```
[editorial](https://leetcode.com/problems/course-schedule/editorial/)有dfs的做法，确实和昨天差不多。