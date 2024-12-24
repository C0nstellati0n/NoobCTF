# [Find Minimum Diameter After Merging Two Trees](https://leetcode.com/problems/find-minimum-diameter-after-merging-two-trees)

hint都把答案摆在眼前了结果发现自己好像不会找树的直径
```c++
//最后还是chatgpt拯救了我
class TreeDiameter {
private:
    vector<vector<int>> adj;
    vector<bool> visited;
    int maxDistance, farthestNode;
    void dfs(int node, int distance) {
        visited[node] = true;
        if (distance > maxDistance) {
            maxDistance = distance;
            farthestNode = node;
        }
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor, distance + 1);
            }
        }
    }
public:
    TreeDiameter(int n) : adj(n), visited(n, false), maxDistance(0), farthestNode(0) {}
    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    int findDiameter() {
        maxDistance = 0;
        dfs(0, 0);
        int startNode = farthestNode;
        maxDistance = 0;
        fill(visited.begin(), visited.end(), false);
        dfs(startNode, 0);
        return maxDistance;
    }
};
class Solution {
public:
    int minimumDiameterAfterMerge(vector<vector<int>>& edges1, vector<vector<int>>& edges2) {
        TreeDiameter tree1(edges1.size()+1);
        TreeDiameter tree2(edges2.size()+1);
        for(const auto& edge:edges1){
            tree1.addEdge(edge[0],edge[1]);
        }
        for(const auto& edge:edges2){
            tree2.addEdge(edge[0],edge[1]);
        }
        int d1=tree1.findDiameter();
        int d2=tree2.findDiameter();
        return max(d1,max(d2,(d1+1)/2+(d2+1)/2+1));
    }
};
```
editorial有找直径的bfs和dfs做法。其中dfs没有使用全局变量，感觉很难理解