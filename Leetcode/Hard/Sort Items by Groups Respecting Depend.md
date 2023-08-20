# Sort Items by Groups Respecting Dependencies

[题目](https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/description/)

题没看懂……我感觉leetcode的题目描述可以做个阅读理解。
```c#
//https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/editorial/
public class Solution {
    public int[] SortItems(int n, int m, int[] group, IList<IList<int>> beforeItems) {
       int groupId = m;
       //给没在任何group里的item也分配个id（所以这个id对应的group里只有这一个item），方便后面对group进行拓扑排序
        for (int i = 0; i < n; i++) {
            if (group[i] == -1) {
                group[i] = groupId;
                groupId++;
            }
        }
        //分别做item和group的dependencies
        Dictionary<int, List<int>> itemGraph = new Dictionary<int, List<int>>();
        int[] itemIndegree = new int[n];
        for (int i = 0; i < n; ++i) {
            itemGraph[i] = new List<int>();
        }
        Dictionary<int, List<int>> groupGraph = new Dictionary<int, List<int>>();
        int[] groupIndegree = new int[groupId];
        for (int i = 0; i < groupId; ++i) {
            groupGraph[i] = new List<int>();
        }
        for (int curr = 0; curr < n; curr++) {
            foreach (int prev in beforeItems[curr]) {
                //beforeItems[curr]中存储着应该被放在curr物品前的所有物品。写成graph就是 prev->curr
                itemGraph[prev].Add(curr); //有向graph
                itemIndegree[curr]++; //curr的入度即为prev的数量
                //group[i]表示元素i所在的group id
                if (group[curr] != group[prev]) { //若两个item不是同一个group id（不在一个group）
                    groupGraph[group[prev]].Add(group[curr]); //必须先放prev item再到curr item，因此prev所在的group要优先于curr所在的group。 prev group->curr group
                    groupIndegree[group[curr]]++; //同理增加curr group的入度
                }
            }
        }
        List<int> itemOrder = TopologicalSort(itemGraph, itemIndegree); //不考虑group，仅对item做拓扑
        List<int> groupOrder = TopologicalSort(groupGraph, groupIndegree); //不考虑item，仅对group做拓扑
        if (itemOrder.Count == 0 || groupOrder.Count == 0) { //若其中有一个排序不存在，说明考虑group+item时肯定也不存在
            return new int[0];
        }
        Dictionary<int, List<int>> orderedGroups = new Dictionary<int, List<int>>();
        foreach (int item in itemOrder) { //把item放到对应的group里
            orderedGroups[group[item]] = orderedGroups.GetValueOrDefault(group[item], new List<int>());
            orderedGroups[group[item]].Add(item);
        }
        List<int> answerList = new List<int>();
        foreach (int groupIndex in groupOrder) {
            if (orderedGroups.ContainsKey(groupIndex)) {
                answerList.AddRange(orderedGroups[groupIndex]); //然后按照拓扑排序好的groupOrder将对应group里的元素拼在一起即可
            }
        }
        return answerList.ToArray();
    }

    private List<int> TopologicalSort(Dictionary<int, List<int>> graph, int[] indegree) {
        List<int> visited = new List<int>();
        Stack<int> stack = new Stack<int>();
        for (int key = 0; key < graph.Count; key++) {
            if (indegree[key] == 0) {
                stack.Push(key);
            }
        }
        while (stack.Count > 0) {
            int curr = stack.Pop();
            visited.Add(curr);

            foreach (int prev in graph[curr]) {
                indegree[prev]--;
                if (indegree[prev] == 0) {
                    stack.Push(prev);
                }
            }
        }
        return visited.Count == graph.Count ? visited : new List<int>();
    }
}
```
```
Runtime
227 ms
Beats
100%
Memory
61.2 MB
Beats
90.91%
```
提示里有说把这题看作graph题并用拓扑排序，但是我想不出来怎么看作graph。毕竟我看了答案后才知道题目问的究竟是啥。