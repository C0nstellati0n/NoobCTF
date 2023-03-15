# Sum Root to Leaf Numbers

[题目](https://leetcode.com/problems/sum-root-to-leaf-numbers/description/)

这题我的大致思路对了，然而错了一个小地方满盘皆输。遍历一个二叉树全部从根到叶子（没有子节点）的路径，要把路上节点的数字值拼在一起并加起来。最容易想到的自然是递归。感觉还是直接看代码吧，不好写出思路，但是代码肯定是一眼就能看懂的。

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
    int sum=0;//差点忘了这是个类，可以在外面写属性的
    public int SumNumbers(TreeNode root) {
        helper(root,"");
        return sum;
    }
    void helper(TreeNode root,string str){
        if(root==null){
            return;
        }
        str+=root.val;
        if(root.left==null && root.right==null){//如果只检查left或right是不是null就返回，会导致返回错误值以及双倍值
            sum+=Int32.Parse(str);
            return;
        }
        helper(root.left,str);
        helper(root.right,str);
    }
}
```

```
Runtime
83 ms
Beats
83.72%
Memory
38.2 MB
Beats
55.81%
```

这种拼接数字类型的题其实不用转字符串也能做。

```c#
public class Solution {
    public int SumNumbers(TreeNode root) {
        return sum(root,0);
    }
    int sum(TreeNode node,int s){
        if(node == null) return 0;
        if(node.left==null && node.right==null) return s*10+node.val;
        return sum(node.left,s*10+node.val)+sum(node.right,s*10+node.val);
    }
}
```

```
Runtime
91 ms
Beats
44.19%
Memory
38.1 MB
Beats
71.32%
```

似乎数字的总比字符串慢，不过需要的内存比字符串少。递归看完了自然就到遍历了，使用队列和Tuple。

```c#
//https://leetcode.com/problems/sum-root-to-leaf-numbers/solutions/3294304/image-explanation-3-methods-recursive-bfs-o-1-space-morris-traversal-preorder/
public class Solution {
    public int SumNumbers(TreeNode root) {
        int totalSum=0;
        Queue<Tuple<TreeNode,int>> q=new(); // <TreeNode*, sumSoFar>
        q.Enqueue(new Tuple<TreeNode,int>(root,0));
        while(q.Count!=0){
            var (node, currentSum) = q.Dequeue();
            currentSum = currentSum*10 + node.val;
            if(node.left==null && node.right==null) totalSum += currentSum;

            if(node.left!=null) q.Enqueue(new Tuple<TreeNode,int>(node.left, currentSum));
            if(node.right!=null) q.Enqueue(new Tuple<TreeNode,int>(node.right, currentSum));
        }
        return totalSum;
    }
}
```

```
Runtime
81 ms
Beats
89.92%
Memory
38.2 MB
Beats
55.81%
```

或者用[Morris遍历](https://zhuanlan.zhihu.com/p/101321696)（前序preorder）。

```c#
public class Solution {
    public int SumNumbers(TreeNode root) {
        TreeNode cur = root;
        int totalSum=0, currentSum=0, depth=0;
        while(cur != null){
            if(cur.left == null){ // left side is not there
                currentSum = currentSum * 10 + cur.val; // preorder(cur.val)
                if(cur.right == null) totalSum += currentSum;
                cur = cur.right;
            }else{ // left side is there (explore it) 
                TreeNode prev = cur.left;
                depth=1;
                while(prev.right!=null && prev.right!=cur){
                    prev = prev.right;
                    depth++;
                }
                if(prev.right == null){ // Root's Left's Rightmost node has no attachments (means first time visit)
                    prev.right = cur;
                    currentSum = currentSum * 10 + cur.val; // preorder(cur.val)
                    cur = cur.left;
                }else{ // Root's Left's Rightmost node has threaded attachments (means Root's Left Visited already)
                    prev.right = null;
                    if(prev.left == null) totalSum += currentSum; // that node is being visited last time
                    currentSum = (int)(currentSum/Math.Pow(10, depth));
                    cur = cur.right;
                }
            }
        }
        return totalSum;
    }
}
```

```
Runtime
81 ms
Beats
89.92%
Memory
38.6 MB
Beats
5.43%
```