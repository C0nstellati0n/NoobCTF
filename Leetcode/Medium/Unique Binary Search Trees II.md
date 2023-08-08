# Unique Binary Search Trees II

[题目](https://leetcode.com/problems/unique-binary-search-trees-ii/)

根据前辈在editorial评论区和discussion的经验之谈，我决定只研究第一种解法。据说后两种是“外星人的作品”

首先复习一下啥是[bst](https://zhuanlan.zhihu.com/p/99949110)：任何一个节点的左子树上的点，都必须小于当前节点。任何一个节点的右子树上的点，都必须大于当前节点。还有很重要的一点，bst的子树也是bst。这不禁让人联想到递归。

所以我们计划着这么写递归。题目要求有n个值的node，当我们随机选择i为root时，它的左边所有可能的值只能在1到i-1范围内，同理右边所有可能值只能在i+1到n范围内。那让1到i-1的左子树继续进入递归，就又和最开始的情况一样了。
```c#
public class Solution {
    public IList<TreeNode> GenerateTrees(int n) {
        if (n == 0) return new List<TreeNode>();
        return DFS(1, n);
    }
    private IList<TreeNode> DFS(int start, int end) {
        if (start > end) { //base case，当start大于end时，无法拆出bst
            return new List<TreeNode>() { null };
        }
        var result = new List<TreeNode>();
        for (int i = start; i <= end; i++) {
            var leftList = DFS(start, i - 1); //按照上面分析的情况递归组成bst子树
            var rightList = DFS(i + 1, end);
            foreach (var left in leftList) {
                foreach (var right in rightList) {
                    var root = new TreeNode(i);
                    root.left = left;
                    root.right = right;
                    result.Add(root);
                }
            }
        }
        return result;
    }
}
```
```
Runtime
85 ms
Beats
88.64%
Memory
39.5 MB
Beats
41.82%
```
据说这题和[Catalan number](https://en.wikipedia.org/wiki/Catalan_number)有关系（leetcode在知乎的解释：https://zhuanlan.zhihu.com/p/97619085 ）。n个node所能形成的不重复bst的数量就是G(n)，G(n)表示第n个Catalan number。