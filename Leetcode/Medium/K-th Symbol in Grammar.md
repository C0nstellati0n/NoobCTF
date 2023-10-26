# [K-th Symbol in Grammar](https://leetcode.com/problems/k-th-symbol-in-grammar)

[editorial](https://leetcode.com/problems/k-th-symbol-in-grammar/editorial)非常不错，按照常规想法->进阶思考->提升->飞升的顺序列出了4种解法（评论区还有一个）。一眼相中了外星人做法——数学
```c#
//这是第四种，不必完全读懂
public class Solution {
    public int KthGrammar(int n, int k) {
        return BitOperations.PopCount((uint)(k-1))%2;
    }
}
```
简述前三种做法：
1. Binary Tree Traversal：有没有发现这种一个分裂成两个的形式很像二叉树？拿到n和k后，直接按照遍历二叉树的方法遍历下去即可。但是笨蛋遍历会TLE，需要个聪明点的做法。假如有一层二叉树有32个node，k为21，说明k肯定在右半边二叉树，左边的子树完全不用管。把树一砍，留下右半边。此时层级少了一级（砍树的时候把左子树+root都砍掉了，因为n肯定不是1。要是n是1的话，直接base case返回0即可），最底下只剩下16个node。原本的k在整个层是第21个，现在是第5个。好这回改砍右子树了。循环这个步骤，直到最后只剩下一个node就是结果（editorial有图，非常清楚）
2. Normal Recursion：假如把每一层从中间砍一半的话，会发现前一部分和上一层的node一模一样，后一部分就是前一部分取反。知道这个关系一层一层推上去即可
3. Recursion to Iteration：上个做法的递归一定是一层一层的来的，直到n=1。那直接来个for循环即可