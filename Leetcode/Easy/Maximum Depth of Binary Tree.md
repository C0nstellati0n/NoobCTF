# Maximum Depth of Binary Tree

[题目](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)

给定一棵二叉树，返回该二叉树的最大深度（根到最远叶子的距离）。

```c#
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
public class Solution {
    public int MaxDepth(TreeNode root) {
        if(root==null){
            return 0;
        }
        int left=Traverse(root.left,1);
        int right=Traverse(root.right,1);
        return left>right?left:right;
    }
    int Traverse(TreeNode node,int count){
        if(node==null){
            return count;
        }
        count++;
        int left=Traverse(node.left,count);
        int right=Traverse(node.right,count);
        return left>right?left:right;
    }
}
```

```
Runtime
86 ms
Beats
85.92%
Memory
39.7 MB
Beats
58.49%
```

……好像有点不对。Traverse和MaxDepth的代码高度重合，所以……

```c#
public class Solution {
    public int MaxDepth(TreeNode root) {
        if(root==null){
            return 0;
        }
        int left=1+MaxDepth(root.left);
        int right=1+MaxDepth(root.right);
        return left>right?left:right;
    }
}
```

```
Runtime
86 ms
Beats
85.92%
Memory
40 MB
Beats
10.53%
```

直接这样不就好了吗？虽然不知道为啥数据更差了。或者继续缩减：

```c#
public class Solution {
    public int MaxDepth(TreeNode root) {
        if(root==null){
            return 0;
        }
        int left=MaxDepth(root.left);
        int right=MaxDepth(root.right);
        return Math.Max(left,right)+1;
    }
}
```

```
Runtime
89 ms
Beats
76.31%
Memory
39.4 MB
Beats
88.94%
```