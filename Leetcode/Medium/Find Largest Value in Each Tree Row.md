# [Find Largest Value in Each Tree Row](https://leetcode.com/problems/find-largest-value-in-each-tree-row)

简单捏，鉴定为bfs。找找之前的模版：[Maximum Level Sum of a Binary Tree](./Maximum%20Level%20Sum%20of%20a%20Binary%20Tree.md)
```c#
public class Solution {
    public IList<int> LargestValues(TreeNode root) {
        List<int> ans=new();
        if(root==null) return ans;
        Queue<TreeNode> q = new();
        q.Enqueue(root);
        int max;
        for (int level = 1; q.Count!=0; ++level) {
            max=Int32.MinValue;
            for (int sz = q.Count; sz > 0; --sz) {
                TreeNode n = q.Dequeue();
                max=Math.Max(max,n.val);
                if (n.left != null) { 
                    q.Enqueue(n.left);
                }
                if (n.right != null) {
                    q.Enqueue(n.right);
                }
            }
            ans.Add(max);
        }
        return ans;
    }
}
```
[editorial](https://leetcode.com/problems/find-largest-value-in-each-tree-row/editorial)还有dfs递归，dfs遍历做法（用stack）