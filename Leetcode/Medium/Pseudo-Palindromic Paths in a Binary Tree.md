# [Pseudo-Palindromic Paths in a Binary Tree](https://leetcode.com/problems/pseudo-palindromic-paths-in-a-binary-tree)

我以为tirck只会影响我解法的优美程度，没想到直接阻拦了我解这道题

思路哪怕清晰一点都不至于卡在一个这么小的点上
```c++
class Solution {
public:
    int pseudoPalindromicPaths(TreeNode* root, int count = 0) {
        if (!root) return 0;
        count ^= 1 << (root->val - 1); //这个异或很妙,count的每一位代表node的各种val，若某一位不为0说明之前遇见过同样val的node。这里异或，若某个val出现的数量为偶数，此bit为0；否则为1
        int res = pseudoPalindromicPaths(root->left, count) + pseudoPalindromicPaths(root->right, count); //左右子树路径的长度
        if (root->left == root->right && (count & (count - 1)) == 0) res++; //(root->left == root->right 只有一种可能，就是两者都为null，此node为leaf。一个伪回文路径只能有一个val出现频率(一个bit)为单数，使用 count & (count - 1)) == 0 检查
        return res;
    }
};
```
这题我从最开始就有个误区,我以为count没法像现在这样全部累计下去，总感觉要像backtrack那样set了某个bit后要再取消。然后意识到完全不用，当前的count表示当前node与上面的root node，自然不用撤销；传给子node的count按值传递，也不会影响到其他path