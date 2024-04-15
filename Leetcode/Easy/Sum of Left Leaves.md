# [Sum of Left Leaves](https://leetcode.com/problems/sum-of-left-leaves)

最神奇的一次，写着写着答案自己就出来了……我还打算再调试一下呢，一下就好了ʕ •ᴥ•ʔ
```c++
class Solution {
public:
    int sumOfLeftLeaves(TreeNode* root) {
        if(!root) return 0;
        if(root->left){
            if(!(root->left->left)&&!(root->left->right))
                return root->left->val+sumOfLeftLeaves(root->right);
        }
        return sumOfLeftLeaves(root->left)+sumOfLeftLeaves(root->right);
    }
};
```
记录一下，感觉这也算二叉树里挺重要的一个问题？