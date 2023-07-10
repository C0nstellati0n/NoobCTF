# Minimum Depth of Binary Tree

[题目](https://leetcode.com/problems/minimum-depth-of-binary-tree/description/)

原本以为和[Maximum Depth of Binary Tree](./Maximum%20Depth%20of%20Binary%20Tree.md)是一个做法，把Math.Max换成Math.Min即可。看了discussion才知道不行。不过我确实从那道题得到了灵感。
```c#
public class Solution {
    int ans=Int32.MaxValue;
    public int MinDepth(TreeNode root) {
        if(root==null){
            return 0;
        }
        Traverse(root,0);
        return ans;
    }
    bool Traverse(TreeNode node,int count){
        if(node==null){
            return true;
        }
        count++;
        bool left=Traverse(node.left,count);
        bool right=Traverse(node.right,count);
        if(left&&right){ //leaf是没有任何子node的node。所以要加个判断，当当前node是leaf时才更新答案
            ans=Math.Min(ans,count);
        }
        return false;
    }
}
```
```
Runtime
256 ms
Beats
84.70%
Memory
68.2 MB
Beats
64.1%
```
我这种dfs不太对，用了全局变量。[editorial](https://leetcode.com/problems/minimum-depth-of-binary-tree/editorial/)有不用的做法。以及不可或缺的，采样区最佳。
```c#
public class Solution {
    public int MinDepth(TreeNode root) {

        if (root == null)
            return 0;

        if (root.left == null && root.right == null)
            return 1;

        var queue = new Queue<TreeNode>();

        queue.Enqueue(root);
        root.val = 1;

        while (queue.Any())
        {
            var current = queue.Dequeue();

            if (current.left == null && current.right == null) //因为bfs是按顺序dequeue的，找到的第一个node一定就是距离最短的node
                return current.val; //同时利用node的val字段记录层级，少了个变量

            if (current.left != null)
            {
                current.left.val = current.val + 1;
                queue.Enqueue(current.left);
            }
            if (current.right != null)
            {
                current.right.val = current.val + 1;
                queue.Enqueue(current.right);
            }
        }

        return 0;
        
    }
}
```
```
Runtime
251 ms
Beats
93.10%
Memory
67.6 MB
Beats
90.95%
```