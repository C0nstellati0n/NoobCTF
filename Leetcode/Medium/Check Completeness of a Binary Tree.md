# Check Completeness of a Binary Tree

[题目](https://leetcode.com/problems/check-completeness-of-a-binary-tree/description/)

检查一个二叉树是不是[完全二叉树](https://zhuanlan.zhihu.com/p/152285749)。这个定义我第一次见。稍微观察了一下，如果把二叉树从中间砍开，左边的二叉树是满的，右边的二叉树不一定满，但是一定只有左节点或者左右节点都有，不能只有右节点。第一反应还是用递归做，最近做的二叉树题都是递归比遍历简单。事实并不如此，总之我一种也没想出来(⌒-⌒; )。

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
//https://leetcode.com/problems/check-completeness-of-a-binary-tree/solutions/3298346/clean-codes-full-explanation-b-f-s-c-java-python3/
public class Solution {
    public bool IsCompleteTree(TreeNode root) {
        // Check if the root node is null, if so, return true (an empty tree is complete)
        if (root == null)
            return true;

        // Create a queue to store the nodes of the tree in level order
        Queue<TreeNode> q = new();
        q.Enqueue(root);
        // Traverse the tree in level order
        while (q.Peek() != null) {
            // Remove the first node from the queue
            TreeNode node = q.Dequeue();
            // Add the left and right child nodes of the current node to the queue
            q.Enqueue(node.left);
            q.Enqueue(node.right);
        }

        // Remove any remaining null nodes from the end of the queue
        while (q.Count!=0 && q.Peek() == null)
            q.Dequeue();

        // Check if there are any remaining nodes in the queue
        // If so, the tree is not complete, so return false
        // Otherwise, the tree is complete, so return true
        return q.Count==0;
    }
}
```

```
Runtime
84 ms
Beats
100%
Memory
41.1 MB
Beats
23.33%
```

或者我们用经典思想[BFS](https://en.wikipedia.org/wiki/Breadth-first_search)和[DFS](https://en.wikipedia.org/wiki/Depth-first_search)来做。

```c#
//BFS
//https://leetcode.com/problems/check-completeness-of-a-binary-tree/solutions/3298282/image-explanation-dfs-bfs-solution-complete-intuition/
public class Solution {
    public bool IsCompleteTree(TreeNode root) {
        if (root == null)
            return true;
        Queue<TreeNode> q=new();
        q.Enqueue(root);
        bool gotNullSoFar = false;
        while(q.Count!=0){
            TreeNode node = q.Dequeue();

            if(node==null){
                gotNullSoFar = true;
            }else{
                if(gotNullSoFar==true) return false;
                q.Enqueue(node.left);
                q.Enqueue(node.right);
            }
        }
        return true;
    }
}
```

```
Runtime
98 ms
Beats
70%
Memory
40.7 MB
Beats
80%
```

```c#
//DFS
//https://leetcode.com/problems/check-completeness-of-a-binary-tree/solutions/3298282/image-explanation-dfs-bfs-solution-complete-intuition/
public class Solution {
    public bool IsCompleteTree(TreeNode root) {
        if (root == null)
            return true;
        int totalNodes = countNodes(root);
        return dfsHelper(root, 1, totalNodes);
    }
    int countNodes(TreeNode root){
        if(root==null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }
    bool dfsHelper(TreeNode root, int idx, int total){
        if(root==null) return true;
        if(idx > total) return false;

        return dfsHelper(root.left, 2*idx, total) && dfsHelper(root.right, 2*idx+1, total);
    }
}
```

```
Runtime
87 ms
Beats
100%
Memory
40.5 MB
Beats
90%
```