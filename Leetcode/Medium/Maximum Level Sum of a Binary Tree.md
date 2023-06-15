# Maximum Level Sum of a Binary Tree

[题目](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/description/)

感觉类似的考点之前做过啊。
```c#
public class Solution {
    Dictionary<int,int> record=new();
    public int MaxLevelSum(TreeNode root) {
        Traverse(root,1);
        var maxKVP = KeyValuePair.Create(Int32.MinValue, Int32.MinValue); 
        foreach(var kvp in record)
        {
            if (kvp.Value > maxKVP.Value)
                maxKVP = kvp;
        }
        return maxKVP.Key;
    }
    void Traverse(TreeNode node,int level){
        if(node==null){
            return;
        }
        record.TryGetValue(level,out int res);
        record[level]=res+node.val;
        Traverse(node.right,level+1);
        Traverse(node.left,level+1);
    }
}
```
```
Runtime
205 ms
Beats
84.69%
Memory
49.3 MB
Beats
89.80%
```
我这是用字典的dfs，还可以用list。
```c#
public class Solution {
    public int MaxLevelSum(TreeNode root) {
        List<int> list = new();
        dfs(root, list, 0);
        return 1 + list.IndexOf(list.Max());
    }
    private void dfs(TreeNode n, List<int> l, int level) {
        if (n == null) { return; } 
        if (l.Count == level) { l.Add(n.val); } // never reach this level before, Add first value.
        else { l[level] =l[level] + n.val; } // reached the level before, accumulate current value to old value.
        dfs(n.left, l, level + 1);
        dfs(n.right, l, level + 1);
    }
}
```
```
Runtime
205 ms
Beats
84.69%
Memory
49.7 MB
Beats
58.16%
```
当然bfs也少不了。这种bfs叫BFS level traversal，姑且叫它层级遍历bfs。
```c#
//https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/solutions/360968/java-python-3-two-codes-language-bfs-level-traversal-and-dfs-level-sum/
public class Solution {
    public int MaxLevelSum(TreeNode root) {
        int max = Int32.MinValue, maxLevel = 1;
        Queue<TreeNode> q = new();
        q.Enqueue(root);
        for (int level = 1; q.Count!=0; ++level) {
            int sum = 0;
            for (int sz = q.Count; sz > 0; --sz) {
                TreeNode n = q.Dequeue();
                sum += n.val;
                if (n.left != null) { 
                    q.Enqueue(n.left);
                }
                if (n.right != null) {
                    q.Enqueue(n.right);
                }
            }
            if (max < sum) {
                max = sum;
                maxLevel = level;
            }
        }
        return maxLevel;
    }
}
```
```
Runtime
197 ms
Beats
97.96%
Memory
49.6 MB
Beats
69.39%
```