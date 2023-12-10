# Binary Tree Inorder Traversal

[题目](https://leetcode.com/problems/binary-tree-inorder-traversal/description/)

以中序遍历（左根右）输出二叉树的值。这题的描述提到递归做法“太简单了”，所以额外挑战要求用遍历的做法。稍微思考了一下递归的做法，肯定是在左节点那里递归，每个节点都尝试调用函数本身，传递给自己的左节点。这点我想到了，但是我没想到怎么把根节点和右节点找回来。事实证明我不懂递归，根本就不用考虑找回节点的问题。递归调用函数传递左节点这个步骤完成后直接接下去把自己的值加上，因为每个有左节点的调用者本身肯定都是一个根节点，只是大小关系。加上自己的值后在如法炮制，传入右节点继续递归就行了。我说的有亿点复杂，代码实际非常简单。

```c#
//这个定义我只放一次
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
    public IList<int> InorderTraversal(TreeNode root) {
        List<int> res=new();
        Traverse(root,res);
        return res;
    }
    public void Traverse(TreeNode node,List<int> res){
        if(node==null){//假如当前节点node是null，说明上一个调用的节点就是最左的节点
            return;//直接返回，不修改res
        }
        Traverse(node.left,res);//加上当前node全部的左节点，包括子、孙节点。如果没有也不会改变res
        res.Add(node.val);//加上自己
        Traverse(node.right,res);//全部的右节点
    }
}
```

```
Runtime
119 ms
Beats
99.78%
Memory
41.8 MB
Beats
87.75%
```

遍历做法就会遇到开始提到的“找回节点问题”。跟着左节点遍历下去很简单，但是怎么恢复根节点？子根节点？子子根节点？无论怎样，我们肯定是要一个数据结构记录走过的节点。栈最好用了，往左走再原路返回正好是栈的后进先出。

```c#
public class Solution {
    public IList<int> InorderTraversal(TreeNode root) {
        List<int> ans=new();
        Stack<TreeNode> stack=new();
        while(stack.Count!=0||root!=null){
            if(root!=null){//只要还有左节点，就一直往下走
                stack.Push(root);
                root=root.left;//更新当前root
            }
            else{//如果当前root是null，说明需要返回上一个节点
                TreeNode tmpNode=stack.Pop();//找回上一个节点
                ans.Add(tmpNode.val);//加上它的值
                root=tmpNode.right;//root更新为tmpNode的右节点。tmpNode可能没有右节点，也没关系，会继续往上走
            }
        }
        return ans;
    }
}
```

```
Runtime
138 ms
Beats
78.3%
Memory
42.1 MB
Beats
65.27%
```

我还找到了一种变种。

```c#
public class Solution {
    public IList<int> InorderTraversal(TreeNode root) {
        List<int> ans=new();
        if(root==null){
            return ans;
        }
        Stack<TreeNode> stack=new();
        pushAllLeft(root, stack);
        while(stack.Count!=0){
            TreeNode cur = stack.Pop();
            ans.Add(cur.val);
            pushAllLeft(cur.right, stack);
        }
        return ans;
    }
    public void pushAllLeft(TreeNode node, Stack<TreeNode> stack){
        while (node != null) {
            stack.Push(node);
            node = node.left;
        }
    }
}
```

```
Runtime
132 ms
Beats
92.44%
Memory
42.2 MB
Beats
65.27%
```

大致思路也差不多，不过这个解法把push node的操作一次完成，可能大体上更好理解一点。另外提一句，C#里的IList是一个接口，List实现于它。两者的对比具体可以看[这](https://stackoverflow.com/questions/400135/listt-or-ilistt)，这里返回List肯定是没问题的。

9个月后又遇到了这题，感觉时间过得好快啊。又拿c++写了一遍
```c++
class Solution {
public:
    vector<int> ans;
    vector<int> inorderTraversal(TreeNode* root) {
        Traverse(root);
        return ans;
    }
    void Traverse(TreeNode* node){
        if(!node) return;
        Traverse(node->left);
        ans.push_back(node->val);
        Traverse(node->right);
    }
};
```
bfs/dfs/morris traversal的c++解法： https://leetcode.com/problems/binary-tree-inorder-traversal/solutions/31231/c-iterative-recursive-and-morris 。评论区里有个Morris traversal的可视化ppt： https://docs.google.com/presentation/d/11GWAeUN0ckP7yjHrQkIB0WT9ZUhDBSa-WR0VsPU38fg/edit#slide=id.g61bfb572cf_0_16

editorial也有全3种解法，不过只有java。对Morris traversal的解释也不错