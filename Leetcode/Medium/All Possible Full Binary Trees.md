# All Possible Full Binary Trees

[题目](https://leetcode.com/problems/all-possible-full-binary-trees/description/)

乍一看感觉简单过头了，这样答案就出来了？但细看又没毛病。
```c#
//https://leetcode.com/problems/all-possible-full-binary-trees/editorial/
//https://leetcode.com/problems/all-possible-full-binary-trees/solutions/167402/c-c-java-python-recursive-and-iterative-solutions-doesn-t-create-frankenstein-trees/ 的讲解也可以
class Solution {
    private Dictionary<int, List<TreeNode>> memo = new();
    public IList<TreeNode> AllPossibleFBT(int n) {
        if (n % 2 == 0) {
            return new List<TreeNode>();
        }

        if (n == 1) {
            return new List<TreeNode>{new TreeNode()};
        }

        if (memo.ContainsKey(n)) {
            return memo[n];
        }

        List<TreeNode> res = new List<TreeNode>();
        for (int i = 1; i < n; i += 2) {
            IList<TreeNode> left = AllPossibleFBT(i);
            IList<TreeNode> right = AllPossibleFBT(n - i - 1);

            foreach(TreeNode l in left) {
                foreach(TreeNode r in right) {
                    TreeNode root = new TreeNode(0, l, r);
                    res.Add(root);
                }
            }
        }

        memo[n]=res;
        return res;
    }
}
```
```
Runtime
97 ms
Beats
94.59%
Memory
48.3 MB
Beats
100%
```
首先要熟悉这个递归的3个base case。
1. n%2==0：这种情况不会有任何可能的完整二叉树。因为完整二叉树每个node都有偶数个子node（0或者2）。那么再加上最顶上那个root，这不就单数了吗？
2. n==1：这种情况显而易见，只有一种可能，它自己。没有递归的必要了。
3. memo.ContainsKey(n)：之前已经解过相同的问题，直接返回结果

到了for循环这部分，感觉直觉上 https://leetcode.com/problems/all-possible-full-binary-trees/solutions/167402/c-c-java-python-recursive-and-iterative-solutions-doesn-t-create-frankenstein-trees/ 讲得又简单又好。其实没有那么复杂，我们把n个node（假设5吧）标上号:1,2,3,4,5。我们可以选取其中一个node作为root，可以是3吗？3将剩下的node分为两个分支，1，2和4，5。诶这都是双数啊，所以是不行的。所以我们只能选2或者4作为root，这也是for循环从索引1开始并递增2的原因。接着进入for循环，i个node为左子树走，n-i-1个node为右子树都很容易看出来。况且二叉树的子树也是二叉树，放心递归。最后把返回的所有可能用foreach组合起来，最后的最后memo记录，完成。

还有个遍历做法，这里不再赘述。