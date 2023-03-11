# Symmetric Tree

[题目](https://leetcode.com/problems/symmetric-tree/description/)

给出一棵二叉树，判断该树是否对称（镜像）。看到这题的我大脑一片空白，我怎么判断它对不对称？没想到今天才知道题目下面有个discussion，里面有好心人写出了完整思路：

```
This problem involves two point:

symmetric:

consider tree T:

if T is null, then T is symmetric

if T->left is mirror of T->right,then T is symmetric

mirror

consider two tree T and R:

if T=R=NULL, then T is mirror of R

if T and R both not NULL,and T->left is mirror of R->right,and T->right is mirror of R->left,then T and R is mirror

otherwise the mirror relationship cannot estabished
```

照着这个思路写，我竟然做出来了。

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
    public bool IsSymmetric(TreeNode root) {
        if(root==null){//这句特殊情况如果不加，综合表现会更差（例如这个解法不加这句的运行时间是98ms）
            return true;
        }
        return IsMirror(root.left,root.right);
    }
    bool IsMirror(TreeNode node1,TreeNode node2){
        if(node1==null&&node2==null){
            return true;
        }
        if(node1==null||node2==null){
            return false;
        }
        return node1.val==node2.val&&IsMirror(node1.left,node2.right)&&IsMirror(node1.right,node2.left);
    }
}
```

```
Runtime
96 ms
Beats
84.92%
Memory
40.9 MB
Beats
34.77%
```

然后我就意识到了这不和same tree几乎一样吗？最顶上那个root肯定是对称的，不用考虑，只用检查两边的tree。镜像的条件是左边的结构等于右边，检查过程完全就是一个left一个right，错开就行了。既然思路和same tree相似，肯定是有遍历做法的。

```c#
public class Solution {
    public bool IsSymmetric(TreeNode root) {
        if(root==null){
            return true;
        }
        Stack<TreeNode> stack = new();
        stack.Push(root.left);
        stack.Push(root.right);
        while (stack.Count!=0) {
            TreeNode n1 = stack.Pop(), n2 = stack.Pop();
            if (n1 == null && n2 == null) continue;
            if (n1 == null || n2 == null || n1.val != n2.val) return false;
            stack.Push(n1.left);
            stack.Push(n2.right);
            stack.Push(n1.right);
            stack.Push(n2.left);
        }
        return true;
    }
}
```

```
Runtime
99 ms
Beats
74.23%
Memory
40.9 MB
Beats
22.18%
```

或者再换种实现方式。左边和右边对称，如果我们按照左右左右的顺序往list里加node，它们应该是对称的，比如`[1,2,3,2,1]`。根据这个思路，就有下面的做法：

```c#
public class Solution {
    public bool IsSymmetric(TreeNode root) {
        if(root==null){
            return true;
        }
        List<TreeNode> last=new(){root};
        while(true){
            if(last.Count==0){
                return true;
            }
            List<TreeNode> current=new();
            foreach(TreeNode node in last){
                if(node!=null){
                    current.Add(node.left);
                    current.Add(node.right);
                }
            }
            if(!is_list_symmetric(current)){
                return false;
            }
            else{
                last=current;
            }
        }
    }
    bool is_list_symmetric(List<TreeNode> lst){
        int head=0;
        int tail=lst.Count-1;
        while(head<tail){
            TreeNode h=lst[head];
            TreeNode t=lst[tail];
            head++;
            tail--;
            if(h==null&&t==null){
                continue;
            }
            if(h==null||t==null||h.val!=t.val){
                return false;
            }
        }
        return true;
    }
}
```

```
Runtime
93 ms
Beats
91.51%
Memory
40.9 MB
Beats
34.77%
```