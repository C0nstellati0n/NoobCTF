# Maximum Width of Binary Tree

[题目](https://leetcode.com/problems/maximum-width-of-binary-tree/description/)

这题如果对bfs有深刻的认知应该是能做出来的。我没有。

```c#
//https://leetcode.com/problems/maximum-width-of-binary-tree/solutions/3436593/image-explanation-why-long-to-int-c-java-python/
class Solution {
    public int WidthOfBinaryTree(TreeNode root) {
        if (root == null) return 0;
        
        Queue<Tuple<TreeNode, int>> queue = new();
        queue.Enqueue(new Tuple<TreeNode,int>(root, 0));
        int maxWidth = 0;
        
        while (queue.Count!=0) {
            int levelLength = queue.Count;
            int levelStart = queue.Peek().Item2;
            int index = 0;
            
            for (int i = 0; i < levelLength; i++) {
                Tuple<TreeNode, int> pair = queue.Dequeue();
                TreeNode node = pair.Item1;
                index = pair.Item2;
                
                if (node.left != null) {
                    queue.Enqueue(new Tuple<TreeNode,int>(node.left, 2*index));
                }
                
                if (node.right != null) {
                    queue.Enqueue(new Tuple<TreeNode,int>(node.right, 2*index+1));
                }
            }
            
            maxWidth = Math.Max(maxWidth, index - levelStart + 1);
        }
        
        return maxWidth;
    }
}
```

```
Runtime
83 ms
Beats
95%
Memory
39.9 MB
Beats
57.50%
```

这道题要找二叉树的宽度，即某一层node的数量（两个node中间夹的null也算）。很广度的定义很相似，于是用bfs。给所有node编号，root为0，记为n。接下来的左子node为2\*n+1,右子node为2\*n+2。计算某一层的宽度就是最右边的node的数字减去最左边的node的数字加1。

有了公式，题目的难点只剩下如何判断最左和最右的node了。答案是在里面套一个for循环。for循环的加入不会改变bfs的执行过程，因为本来就是这么执行的，for循环只是方便我们记录其中一层的遍历情况。for循环结束后，说明一层遍历完了，根据公式计算值，然后去到下一层。一直重复直到bfs完成。