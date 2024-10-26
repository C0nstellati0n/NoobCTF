# [Height of Binary Tree After Subtree Removal Queries](https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries)

学二叉树就是为了有朝一日能看懂这题的答案（

[editorial](https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/editorial)里有五种解法，这里记录第一和第五种。其他三种的runtime表现都挺拉垮的。第一种最好，十几ms；最差的给我干到1800ms去了……
```c++
class Solution {
public:
    // Array to store the maximum height of the tree after removing each node
    int maxHeightAfterRemoval[100001];
    int currentMaxHeight = 0;
    vector<int> treeQueries(TreeNode* root, vector<int>& queries) {
        traverseLeftToRight(root, 0);
        currentMaxHeight = 0;  // Reset for the second traversal
        traverseRightToLeft(root, 0);
        // Process queries and build the result vector
        int queryCount = queries.size();
        vector<int> queryResults(queryCount);
        for (int i = 0; i < queryCount; i++) {
            queryResults[i] = maxHeightAfterRemoval[queries[i]];
        }
        return queryResults;
    }
private:
    // Left to right traversal
    void traverseLeftToRight(TreeNode* node, int currentHeight) {
        if (node == nullptr) return;
        // Store the maximum height if this node were removed
        maxHeightAfterRemoval[node->val] = currentMaxHeight;
        // Update the current maximum height
        currentMaxHeight = max(currentMaxHeight, currentHeight);
        // Traverse left subtree first, then right
        traverseLeftToRight(node->left, currentHeight + 1);
        traverseLeftToRight(node->right, currentHeight + 1);
    }
    // Right to left traversal
    void traverseRightToLeft(TreeNode* node, int currentHeight) {
        if (node == nullptr) return;
        // Update the maximum height if this node were removed
        maxHeightAfterRemoval[node->val] =
            max(maxHeightAfterRemoval[node->val], currentMaxHeight);
        // Update the current maximum height
        currentMaxHeight = max(currentHeight, currentMaxHeight);
        // Traverse right subtree first, then left
        traverseRightToLeft(node->right, currentHeight + 1);
        traverseRightToLeft(node->left, currentHeight + 1);
    }
};
```
第一个做法的关键点在于这句话：“For any node, the height after removing its subtree is simply the height of the tree before reaching that node”。整个代码最重要的内容是两个dfs里的`currentMaxHeight = max(currentMaxHeight, currentHeight);`。第一个traverseLeftToRight优先走左子树，因此假如maxHeight出现在左子树，右子树的全部node的maxHeightAfterRemoval值都是左子树的maxHeight。但这样没法照顾maxHeight出现在右子树的情况，所以还要反着遍历一次。加上`max(maxHeightAfterRemoval[node->val], currentMaxHeight);`取了最大值，把两个遍历的“短处”都处理了。妙啊，太妙了
```c++
class Solution {
public:
    vector<int> treeQueries(TreeNode* root, vector<int>& queries) {
        int n = 100000;
        // Vectors to store node depths and heights
        vector<int> nodeDepths(n + 1, 0);
        vector<int> subtreeHeights(n + 1, 0);
        // Vectors to store the first and second largest heights at each level
        vector<int> firstLargestHeight(n + 1, 0);
        vector<int> secondLargestHeight(n + 1, 0);
        // Perform DFS to calculate depths and heights
        dfs(root, 0, nodeDepths, subtreeHeights, firstLargestHeight,
            secondLargestHeight);
        vector<int> results;
        results.reserve(queries.size());
        // Process each query
        for (int queryNode : queries) {
            int nodeLevel = nodeDepths[queryNode];
            // Calculate the height of the tree after removing the query node
            if (subtreeHeights[queryNode] == firstLargestHeight[nodeLevel]) {
                results.push_back(nodeLevel + secondLargestHeight[nodeLevel] -1);
            } else {
                results.push_back(nodeLevel + firstLargestHeight[nodeLevel] -1);
            }
        }
        return results;
    }
private:
    // Depth-first search to calculate node depths and subtree heights
    int dfs(TreeNode* node, int level, vector<int>& nodeDepths,
            vector<int>& subtreeHeights, vector<int>& firstLargestHeight,
            vector<int>& secondLargestHeight) {
        if (node == nullptr) return 0;
        nodeDepths[node->val] = level;
        // Calculate the height of the current subtree
        int leftHeight = dfs(node->left, level + 1, nodeDepths, subtreeHeights,firstLargestHeight, secondLargestHeight);
        int rightHeight =
            dfs(node->right, level + 1, nodeDepths, subtreeHeights,
                firstLargestHeight, secondLargestHeight);
        int currentHeight = 1 + max(leftHeight, rightHeight);
        subtreeHeights[node->val] = currentHeight;
        // Update the largest and second largest heights at the current level
        if (currentHeight > firstLargestHeight[level]) {
            secondLargestHeight[level] = firstLargestHeight[level];
            firstLargestHeight[level] = currentHeight;
        } else if (currentHeight > secondLargestHeight[level]) {
            secondLargestHeight[level] = currentHeight;
        }
        return currentHeight;
    }
};
```
"At any node, the longest path through it is the sum of its depth and the height of its subtree. For each depth, the maximum tree height at that level will be the depth plus the maximum height of any node at that depth."。之后的重点就是怎么算一个node的depth和它子树的高度了。感觉实现代码时的关键点是“算depth从root开始（正着来），算子树height从leaf开始（倒着来）”。算query结果时有两个情况：query删除的node是当前depth里拥有最高子树的node；或者不是

为了处理这两种情况，需要记录当前depth下拥有最高子树的node和拥有第二高子树的node。假如是第一种情况，结果是有第二高子树的node的子树高度+当前depth；结果就是第一高子树高度+当前depth