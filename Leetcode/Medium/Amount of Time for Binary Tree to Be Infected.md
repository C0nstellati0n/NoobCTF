# [Amount of Time for Binary Tree to Be Infected](https://leetcode.com/problems/amount-of-time-for-binary-tree-to-be-infected)
```c++
class Solution {
public:
    int amountOfTime(TreeNode* root, int start) {
        unordered_map<int,vector<int>> graph;
        stack<TreeNode*> s;
        s.push(root);
        TreeNode* cur;
        while(!s.empty()){
            cur=s.top();
            s.pop();
            if(cur->left){
                s.push(cur->left);
                graph[cur->val].push_back(cur->left->val);
                graph[cur->left->val].push_back(cur->val);
            }
            if(cur->right){
                s.push(cur->right);
                graph[cur->val].push_back(cur->right->val);
                graph[cur->right->val].push_back(cur->val);
            }
        }
        unordered_map<int,int> visited;
        int minutes=0;
        queue<int> q;
        q.push(start);
        int curr;
        int size;
        while(!q.empty()){
            size=q.size();
            for(int i=0;i<size;i++){
                curr=q.front();
                q.pop();
                visited[curr]=1;
                for(int next:graph[curr]){
                    if(!visited[next]) q.push(next);
                }
            }
            minutes++;
        }
        return minutes-1;
    }
};
```
这种做法将tree中的node转换成了无向图，然后用bfs计算一共有多少层。但想一想，二叉树本身就有层级之类的概念吧，完全可以直接利用二叉树计算。假如初始感染的node是最顶上那个root，直接dfs往下算（leetcode里记得有类似的题）。可如果初始感染的node是二叉树中间某个呢？[editorial](https://leetcode.com/problems/amount-of-time-for-binary-tree-to-be-infected/editorial)有非常好的解释，但个人觉得精华是：
```
In the image above the start node is the red node, 5.
subDepth = 2 // red subtree's depth (Nodes below the start node)
depth = 1 // red node's depth (the start node)
otherDepth = 2 // green subtree depth (nodes above the start node)
distance = depth + other_depth = 3 // distance of any node above the start node from the start node
maxDistance = max(distance, sub_depth) = 3
```
这时看代码就不懵了：
```c++
class Solution {
private:
    int maxDistance = 0;
public:
    int amountOfTime(TreeNode* root, int start) {
        traverse(root, start);
        return maxDistance;
    }
    int traverse(TreeNode* root, int start) {
        int depth = 0; //depth表示当前node在二叉树里的深度
        if (root == nullptr) {
            return depth;
        }
        //分别获取左右子树相对当前node的深度
        int leftDepth = traverse(root->left, start);
        int rightDepth = traverse(root->right, start);
        //如果当前node（某个子树或者整个树的root）是初始感染的node
        if (root->val == start) {
            //因为是一层一层感染，所需时间（distance）是左右子树两者之间的最大值
            maxDistance = max(leftDepth, rightDepth);
            depth = -1; //自身的depth为-1，代码里标记初始node的方法
        } else if (leftDepth >= 0 && rightDepth >= 0) { //如果左右子树都不包含初始感染的node
            depth = max(leftDepth, rightDepth) + 1; //正常计算自身的depth
        } else { //如果左右子树其中一个包含初始感染的node，那么leftDepth和rightDepth里总有一个是-1
            //无论初始感染的node在哪个子树，都能用这个公式计算出另一个不包含初始感染的node的子树里最远的那个node的距离
            int distance = abs(leftDepth) + abs(rightDepth);
            maxDistance = max(maxDistance, distance);
            //这里是为什么上面的公式能成立的关键。min一定会选到负数，即包含初始感染的node的子树的层级。由于公式里用了abs，这里的-1表达的意思反而是+1
            depth = min(leftDepth, rightDepth) - 1;
        }
        return depth;
    }
};
```