# Minimum Absolute Difference in BST

[题目](https://leetcode.com/problems/minimum-absolute-difference-in-bst/description/)

二叉树家族到底有多少成员？今天轮到[binary search tree](https://zhuanlan.zhihu.com/p/99949110)（BST）.BST有个特点，如果用中序（inorder）遍历树的话，得到的值将是排序好的，而且不会有重复的node值。
```c#
//https://leetcode.com/problems/minimum-absolute-difference-in-bst/solutions/99905/two-solutions-in-order-traversal-and-a-more-general-way-using-treeset/
public class Solution {
    int min = Int32.MaxValue;
    int prev = -10; //只是为了下面if语句区分，原本答案是null，不过c#里int好像赋不了null
    
    public int GetMinimumDifference(TreeNode root) {
        if (root == null) return min;
        
        GetMinimumDifference(root.left); //中序遍历，左根右
        
        if (prev != -10) {//保证前面有node。最开始遍历第一个最左node时是没有的
            min = Math.Min(min, root.val - prev); //这里其实只计算了左与根，根与右的差值。虽然题目要求返回任意两个node之前的最小差值，不过bst中序遍历是排序好的，假如根和右的差值不是最小的，根与左的差值就更不可能了
        }
        prev = root.val;
        
        GetMinimumDifference(root.right);
        
        return min;
    }
    
}
```
```
Runtime
88 ms
Beats
95.48%
Memory
42.3 MB
Beats
85.16%
```
有时候会要求不用全局变量，那可以传数组，利用引用赋值直接改值。
```c#
//https://leetcode.com/problems/minimum-absolute-difference-in-bst/solutions/201794/java-in-order-traversal-without-global-variable-beating-99-81/
class Solution {
    public int GetMinimumDifference(TreeNode root) {
        // info[0] is prev value in inorder sequence while info[1] holds the min difference
      	int[] info = new int[]{-1, Int32.MaxValue};
        inorder(root, info);
        return info[1];
    }
    
    private void inorder(TreeNode root, int[] info) {
        if (root == null) {
            return;
        }
        inorder(root.left, info);
      	// if the current node has a prev in inorder traversal
        if (info[0] != -1) {
          	// update difference, since it's inorder, root.val is guranteed to be greater than prev in a BST 
            info[1] = Math.Min(info[1], root.val - info[0]);
        }
      	// update prev node
        info[0] = root.val;
        inorder(root.right, info);
    }
}
```
```
Runtime
100 ms
Beats
60.64%
Memory
42.4 MB
Beats
58.71%
```
甚至可以不用中序遍历。
```c#
//https://leetcode.com/problems/minimum-absolute-difference-in-bst/solutions/99918/java-no-in-order-traverse-solution-just-pass-upper-bound-and-lower-bound/
public class Solution {
    int minDiff = Int32.MaxValue;
    public int GetMinimumDifference(TreeNode root) {
        helper(root,Int32.MinValue,Int32.MaxValue);
        return minDiff;
    }
    private void helper(TreeNode curr, int lb, int rb){
        if(curr==null) return;
        if(lb!=Int32.MinValue){
            minDiff = Math.Min(minDiff,curr.val - lb);
        }
        if(rb!=Int32.MaxValue){
            minDiff = Math.Min(minDiff,rb - curr.val);
        }
        helper(curr.left,lb,curr.val);
        helper(curr.right,curr.val,rb);
    }
}
```
```
Runtime
89 ms
Beats
94.19%
Memory
42.3 MB
Beats
85.16%
```
作者说了：
```
It is just sort of property of the BST. Since the value of all the nodes of the left subtree is smaller than the current node, the value of the current node is the upper bound of the all the nodes in the left subtree. And for the right subtree, the value of the current node is the lower bound.
```