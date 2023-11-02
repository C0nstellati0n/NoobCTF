# [Find Mode in Binary Search Tree](https://leetcode.com/problems/find-mode-in-binary-search-tree)

进军c++！主要c#基础语法挺熟的了，而且c#有别的地方练，c++就找不到契机。正好今天是个easy，算法不难想，然而语法给我查了好久（教程看了理解了但是没进脑子），比如怎么遍历unordered_map，传参数要传引用……
```c++
class Solution {
public:
    int maxVal=0;
    vector<int> findMode(TreeNode* root) {
        unordered_map<int, int> map; 
        Traverse(root,map);
        vector<int> res;
        for (auto& [key, value]: map) {
            if(value==maxVal){
                res.push_back(key);
            }
        }
        return res;
    }
    void Traverse(TreeNode* node,unordered_map<int, int> &map){
        if(node==NULL){
            return;
        }
        Traverse(node->left,map);
        map[node->val]++;
        maxVal=max(map[node->val],maxVal);
        Traverse(node->right,map);
    }
};
```
[editorial](https://leetcode.com/problems/find-mode-in-binary-search-tree/editorial)介绍了很多种做法。前三种做法都是用字典，只不过一个dfs，一个遍历dfs，一个bfs。第四和第五种利用了BST的特性：如果用中序遍历（左根右），就能保证遍历的node按从小到大的顺序排列。这样计算出现次数最多的node就不难了。直接遍历，然后记录当前的node和其数量，再记录一个最大数量。每次遇见node就将数量加一，遇见其他的node就把数量设置回0，node改成新见过的node。同时再push符合最大数量的node进res

最后是Morris Traversal。建议直接看editorial，有图好理解