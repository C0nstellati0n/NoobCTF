# [Restore the Array From Adjacent Pairs](https://leetcode.com/problems/restore-the-array-from-adjacent-pairs)

byd11月摸鱼摸到现在连基本graph都忘了是吧？
```c++
//https://leetcode.com/problems/restore-the-array-from-adjacent-pairs/editorial
class Solution {
public:
    vector<int> restoreArray(vector<vector<int>>& adjacentPairs) {
        unordered_map<int, vector<int>> graph;
        for (auto& edge : adjacentPairs) {
            graph[edge[0]].push_back(edge[1]);
            graph[edge[1]].push_back(edge[0]); //邻接表，注意目前是无向有环图，下面要留个心眼
        }
        int root = 0;
        for (auto& pair : graph) {
            if (pair.second.size() == 1) { //假如一个node只有一个邻居，那么它要么是最左边的，要么是最右边的。无论是哪个，都可以用作graph的起始点
                root = pair.first;
                break;
            }
        }
        int curr = root;
        vector<int> ans = {root};
        int prev = INT_MAX;
        while (ans.size() < graph.size()) {
            for (int neighbor : graph[curr]) { //遍历当前node的所有邻居
                if (neighbor != prev) { //这题是按照pair来构造的，所以一个node最多有两个邻居。要考虑的地方在于，假如有pair [1,2]，1的邻居里有2，2个邻居里有1，那要是遍历时1遍历到2，2又遍历回1就寄了。所以要加个判断，保证不会重复
                //无需利用visited数组，因为是一对一对的，某一个node最多有左右两个邻居a，b。若从a来到这个node，排除了a，剩下能走的只有b，一定不会重复
                    ans.push_back(neighbor);
                    prev = curr;
                    curr = neighbor;
                    break;
                }
            }
        }
        return ans;
    }
};
```