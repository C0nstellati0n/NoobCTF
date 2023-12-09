# [Construct String from Binary Tree](https://leetcode.com/problems/construct-string-from-binary-tree)

步入靠直觉写代码时代
```c++
class Solution {
public:
    string ans="";
    string tree2str(TreeNode* root) {
        Traverse(root);
        return ans;
    }
    void Traverse(TreeNode* node){
        if(!node) return;
        ans+=to_string(node->val);
        if(node->right||node->left){
            ans+="(";
            Traverse(node->left);
            ans+=")";
        }
        if(node->right){
            ans+="(";
            Traverse(node->right);
            ans+=")";
        }
    }
};
```