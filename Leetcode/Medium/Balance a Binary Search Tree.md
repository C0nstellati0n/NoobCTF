# [Balance a Binary Search Tree](https://leetcode.com/problems/balance-a-binary-search-tree)

只是想记一下这个之前没见过的算法
```c++
class Solution {
private:
    vector<int> nodes;
public:
    TreeNode* balanceBST(TreeNode* root) {
        traverse(root);
        return construct(0,nodes.size()-1);
    }
    void traverse(TreeNode* root){
        if(!root) return;
        traverse(root->left);
        nodes.push_back(root->val);
        traverse(root->right);
    }
    TreeNode* construct(int start,int end){
        if(start>end) return NULL;
        const int mid=(start+end)/2;
        TreeNode* root=new TreeNode(nodes[mid]);
        root->left=construct(start,mid-1);
        root->right=construct(mid+1,end);
        return root;
    }
};
```
这个解法太简单了，重点在于dsw的in-place平衡算法
```c++
//https://leetcode.com/problems/balance-a-binary-search-tree/editorial
//图片解释见 https://leetcode.com/problems/balance-a-binary-search-tree/solutions/541785/c-java-with-picture-dsw-o-n-o-1
//何为树的旋转操作见 https://blog.csdn.net/q1007729991/article/details/88093023
class Solution {
public:
    TreeNode* balanceBST(TreeNode* root) {
        if (!root) return nullptr;

        // Step 1: Create the backbone (vine)
        // Temporary dummy node
        TreeNode* vineHead = new TreeNode(0);
        vineHead->right = root;
        TreeNode* current = vineHead;
        while (current->right) {
            if (current->right->left) {
                rightRotate(current, current->right);
            } else {
                current = current->right;
            }
        }

        // Step 2: Count the nodes
        int nodeCount = 0;
        current = vineHead->right;
        while (current) {
            ++nodeCount;
            current = current->right;
        }

        // Step 3: Create a balanced BST
        int m = pow(2, floor(log2(nodeCount + 1))) - 1;
        makeRotations(vineHead, nodeCount - m);
        while (m > 1) {
            m /= 2;
            makeRotations(vineHead, m);
        }

        TreeNode* balancedRoot = vineHead->right;
        // Delete the temporary dummy node
        delete vineHead;
        return balancedRoot;
    }

private:
    // Function to perform a right rotation
    void rightRotate(TreeNode* parent, TreeNode* node) {
        TreeNode* tmp = node->left;
        node->left = tmp->right;
        tmp->right = node;
        parent->right = tmp;
    }

    // Function to perform a left rotation
    void leftRotate(TreeNode* parent, TreeNode* node) {
        TreeNode* tmp = node->right;
        node->right = tmp->left;
        tmp->left = node;
        parent->right = tmp;
    }

    // Function to perform a series of left rotations to balance the vine
    void makeRotations(TreeNode* vineHead, int count) {
        TreeNode* current = vineHead;
        for (int i = 0; i < count; ++i) {
            TreeNode* tmp = current->right;
            leftRotate(current, tmp);
            current = current->right;
        }
    }
};
```