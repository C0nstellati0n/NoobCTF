# Same Tree

[题目](https://leetcode.com/problems/same-tree/description/)

比较两个二叉树是否完全相同（包括结构和值）。这题本来想偷懒，用遍历二叉树那道题的函数对两个树都跑一遍，比较结果就行了。很不幸错了，因为遍历函数只能检查值是否相同，不检查结构。其实思路和遍历也差不多，不过要改一下顺序。先检查当前节点是否相同，然后检查左，最后检查右。我思路是对了，实现得也差不多，但是一个很关键的逻辑写反了，导致最后没跑出来。正确的逻辑是这样的：

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
    public bool IsSameTree(TreeNode p, TreeNode q) {
        if(p==null && q==null)    return true;//两个节点都是null就是相等
        if(p==null || q==null)    return false;//一个是null一个不是null说明结构不同，直接为false
        return (p.val == q.val && IsSameTree(p.right, q.right) && IsSameTree(p.left, q.left));//检查值和子节点
    }
}
```

```
Runtime
95 ms
Beats
79.60%
Memory
40 MB
Beats
50.52%
```

我把第二个if条件写成`if(p!=null || q!=null)`了，这样会导致明明相同的节点会返回True。比如两个节点的值都是1，不会进入第一个if语句，但是会进入第二个，因为两者都不是null，导致结果错误。接下来是遍历做法。

```c#
public class Solution {
    public bool IsSameTree(TreeNode p, TreeNode q) {
        Stack<Tuple<TreeNode,TreeNode>> stack=new();//源代码为c++，用的是pair。C#里比较像的结构是Tuple
        stack.Push(new Tuple<TreeNode, TreeNode>(p, q));
        while(stack.Count!=0){
            var (node1,node2)=stack.Pop();//var跟C++里的auto关键字差不多
            if(node1==null&&node2==null) continue;
            if (node1==null || node2==null || node1.val != node2.val) return false;
            stack.Push(new Tuple<TreeNode, TreeNode>(node1.left, node2.left));
            stack.Push(new Tuple<TreeNode, TreeNode>(node1.right, node2.right));
        }
        return true;
    }
}
```

```
Runtime
92 ms
Beats
90.19%
Memory
40 MB
Beats
50.52%
```

差不多的思路，只不过用栈回溯而不是递归。和遍历树的操作一样一样的，只不过加了个判断节点是否相等的逻辑。