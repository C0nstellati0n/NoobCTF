# [Distribute Coins in Binary Tree](https://leetcode.com/problems/distribute-coins-in-binary-tree)

别人都提示那么明显了还做不出来我自杀吧
```c++
//采样区
// https://leetcode.com/problems/distribute-coins-in-binary-tree/editorial 有小变种做法，注意绝对值
class Solution {
private:
    int dis(TreeNode* root, int& ans) {
        if(root==NULL) return 0;
        int coins = root->val + dis(root->left, ans) + dis(root->right, ans); //理论上这个公式应该是这题的关键
        coins--;
        ans += abs(coins); //但我卡在不知道要用ans记录一下……我直接返回dis函数return的值了，想都不想一下
        return coins;
    }
public:
    int distributeCoins(TreeNode* root) {
        int ans = 0;
        dis(root, ans);
        return ans;
    }
};
```
这题的关键在于，硬币的数量等同于tree里node的数量，多coin和少coin（给其他node coin或者向其他node索取coin）在绝对值下是一样的。从leaf node开始考虑，假如leaf node的val是0，说明它需要一个coin；如果不是0，说明它多了val-1个coin，要给出去。无论是哪种情况，val-1都可以概括。然后考虑有子node的node root。root左边的node需要（或者可以给出）`dis(root->left)`个coin,右边需要（或者可以给出）`dis(root->right)`个coin，自己有`root->val`个coin。但是还要留一个coin给自己，所以有个`coins--`。最后的`abs(coins)`就是要交换的coin的数量，包括node需要的或者可以给出的