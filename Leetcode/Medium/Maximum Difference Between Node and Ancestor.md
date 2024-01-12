# [Maximum Difference Between Node and Ancestor](https://leetcode.com/problems/maximum-difference-between-node-and-ancestor)

不听hint言，吃亏在眼前
```c++
//采样区
//https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/solutions/274610/java-c-python-top-down 为一行代码解法。不过学习的话还是采样区的好理解
class Solution {
public:
    int result = 0;
    int maxAncestorDiff(TreeNode* root) {
        if (root == nullptr) return 0;
        dfs(root, root->val, root->val);
        return result;
    }
    void dfs(TreeNode* root, int curMax, int curMin) { //记录当前node及其后代node中的最大值和最小值
        if (root == nullptr) return;
        int possibleResult = max(abs(curMax - root->val), abs(curMin - root->val));
        result = max(result, possibleResult);
        curMax = max(root->val, curMax);
        curMin = min(root->val, curMin);
        dfs(root->left, curMax, curMin);
        dfs(root->right, curMax, curMin);
        return;
    }
};
```
其实我自己已经写出来一半了，但是最终没做出来的原因是我只记录了最小值。明明都看过hint说“记录最大值和最小值”了，但是我想“最大差值肯定从当前node减最小值来对吧，我要最大值有何用？”，遂浪费了人生宝贵的40分钟。不是我为啥会觉得最大值没用啊，题目都说了绝对值，有没有一种可能，最大值减当前node也可能产生结果？