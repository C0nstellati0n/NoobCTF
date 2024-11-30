# [Valid Arrangement of Pairs](https://leetcode.com/problems/valid-arrangement-of-pairs)

提示看到了关键算法还去搜了，结果还是wrong answer。完辣！我是傻子
```c++
//采样区
class Solution {
public:
    vector<vector<int>> validArrangement(vector<vector<int>>& pairs) {
        unordered_map<int, vector<int>> adjacencyList;
        unordered_map<int, int> inOutDegree;
        // Build graph and count in/out degrees
        for (const auto& pair : pairs) {
            adjacencyList[pair[0]].push_back(pair[1]);
            inOutDegree[pair[0]]++;  // out-degree
            inOutDegree[pair[1]]--;  // in-degree
        }
        // Find starting node (head)
        int startNode = pairs[0][0];
        for (const auto& [node, degree] : inOutDegree) {
            //接下来要用的Hierholzer's Algorithm用于在Eulerian Graph（全部node的度数都是双数）和Semi-Eulerian Graph中找到Eulerian path
            //对于Eulerian Graph，随便拿一个node作为起始点即可
            //但对于Semi-Eulerian Graph（有两个度数为单数的node），起始点需要是其中一个单数node
            //加上这题是有向图，则需要找到出度-入度=1的node
            if (degree == 1) {
                startNode = node;
                break;
            }
        }
        vector<int> path;
        stack<int> nodeStack;
        nodeStack.push(startNode);
        //Hierholzer's Algorithm
        while (!nodeStack.empty()) {
            auto& neighbors = adjacencyList[nodeStack.top()];
            if (neighbors.empty()) {
                path.push_back(nodeStack.top());
                nodeStack.pop();
            } else {
                int nextNode = neighbors.back();
                nodeStack.push(nextNode);
                neighbors.pop_back();
            }
        }
        vector<vector<int>> arrangement;
        int pathSize = path.size();
        arrangement.reserve(pathSize - 1);
        //注意算法跑出来的路径是倒着的
        for (int i = pathSize - 1; i > 0; --i) {
            arrangement.push_back({path[i], path[i-1]});
        }
        return arrangement;
    }
};
```