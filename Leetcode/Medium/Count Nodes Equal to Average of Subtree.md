# [Count Nodes Equal to Average of Subtree](https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree)

我能不能优化一下这破代码啊.jpg
```c++
class Solution {
public:
    int res=0;
    pair<int,int> ans;
    int averageOfSubtree(TreeNode* root) {
        Traverse(root);
        return res;
    }
    void SumAndCount(TreeNode* root, bool first){
        if(!root) return;
        if(first){
            ans={};
            first=!first;
        }
        ans.first+=1;
        ans.second+=root->val;
        SumAndCount(root->left,first);
        SumAndCount(root->right,first);
    }
    void Traverse(TreeNode* root){
        if(!root) return;
        if(!root->right&&!root->left){
            res++;
            return;
        }
        SumAndCount(root,true);
        if(ans.second/ans.first==root->val) res++;
        Traverse(root->left);
        Traverse(root->right);
    }
};
```
这个破玩意的时间复杂度应该是 $n^2$ ，毕竟每走到一个node就要遍历这个node下面所有的子树。查看[editorial](https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/editorial)，标准的O(n)递归做法是用[后序遍历](https://www.geeksforgeeks.org/postorder-traversal-of-binary-tree/)（post order）
```c++
class Solution {
public:
    int count = 0;
    pair<int, int> postOrder(TreeNode* root) {
        if (root == NULL) {
            return {0, 0};
        }
        // First iterate over left and right subtrees.
        pair<int, int> left = postOrder(root->left);
        pair<int, int> right = postOrder(root->right);
        int nodeSum = left.first + right.first + root->val;
        int nodeCount = left.second + right.second + 1;
        // Check if the average of the subtree is equal to the node value.
        if (root->val == nodeSum / (nodeCount)) {
            count++;
        }
        // Return the sum of nodes and the count in the subtree.
        return {nodeSum, nodeCount};
    }
    int averageOfSubtree(TreeNode* root) {
        postOrder(root);
        return count;
    }
};
```
后序遍历遵循左右根的顺序遍历二叉树。这题先遍历左右子树记录node数量与node的和，然后回到根比较。这题难的不是后序遍历，我虽然之前没学过但是很容易搜到怎么写，然而如何记录必要的值却难住了我，最后选择回到舒适圈