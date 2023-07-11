# All Nodes Distance K in Binary Tree

[题目](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/description/)

看discussion有人说buildgraph，然而有人评论说根本不需要。于是我就去想不需要的做法，结果没想出来。看完[editorial](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/editorial/)的常规buildgraph解法就在solution区看见了那个不用的做法。我只能说，我想不出来可太正常了。
```c#
//采样区最佳，同样是buildgraph，但是比editorial快
public class Solution {
    public IList<int> DistanceK(TreeNode root, TreeNode target, int k) {        
        var adjList = new Dictionary<int, List<int>>();
        BuildGraph(adjList, root, null);
        var result = new List<int>();
        FindFarFromNode(result, adjList, new HashSet<int>(), target.val, k, 0);
        return result;
    }    

    private void BuildGraph(Dictionary<int, List<int>> adjList, TreeNode node, TreeNode prev) {
        if (node == null) return;

        var neighbors = new List<int>();

        if (prev != null) neighbors.Add(prev.val);
        if (node.left != null) {
            neighbors.Add(node.left.val);
            BuildGraph(adjList, node.left, node);
        }
        if (node.right != null) {
            neighbors.Add(node.right.val);
            BuildGraph(adjList, node.right, node);
        }

        adjList[node.val] = neighbors;
    }

    private void FindFarFromNode(List<int> nodes, Dictionary<int, List<int>> adjList, HashSet<int> visited, int nodeVal, int k, int distance){
        visited.Add(nodeVal);
        if (distance == k) nodes.Add(nodeVal);
        if (distance > k) return;

        foreach (var neighbor in adjList[nodeVal]) {
            if (!visited.Contains(neighbor)) FindFarFromNode(nodes, adjList, visited, neighbor, k, distance + 1);
        }
    }
}
```
```
Runtime
145 ms
Beats
74.24%
Memory
44 MB
Beats
27.27%
```
说实话没啥好说的，邻接表会吧，dfs会吧，那合在一起也会……吧？但是这个[解法](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/solutions/143798/1ms-beat-100-simple-java-dfs-with-without-hashmap-including-explanation/)把这道题上升到了一个它不属于的高度。原作者没写解释，解析参考`vanhalen5150`评论的`Can anyone explain the version without hashmap?`下的评论区中`kanishka01`的评论。非常详细。