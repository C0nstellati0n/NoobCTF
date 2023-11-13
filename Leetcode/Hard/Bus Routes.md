# [Bus Routes](https://leetcode.com/problems/bus-routes)

[editorial](https://leetcode.com/problems/bus-routes/editorial)和我的思路差不多，多源bfs。你问我的解法在哪里？我脑子抽了，一时竟没想到怎么找邻居（判断两个bus是否是连接起来）。其实很简单，就是没想。真的摸太多鱼了

试了一下，editorial的做法运行时间不是最好的。采样区永远有神人
```c++
class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& routes, int source, int target) {
        vector<int> dist(1000000, 501); //从constraint得到这些值
        dist[source] = 0; //dist[i]为到stop i所需的最少bus数量
        unordered_set<int> visited;
        int mindist;
        int count = 0;
        while(visited.size() < routes.size() && count < routes.size()) {
            for(int bus = 0; bus < routes.size(); ++bus) {
                if (visited.find(bus) != visited.end()) continue;
                mindist = 501; //默认值为最远距离。最多500辆bus
                for(auto i : routes[bus]) { //routes[bus]获取bus所有的站点
                    mindist = min(mindist, dist[i] + 1); //获取站点i的距离
                }
                for(auto i : routes[bus]) {
                    dist[i] = min(dist[i], mindist); //此处更新dist[i]
                }
                if (mindist < 501) {
                    visited.emplace(bus);
                }
            }
            count++;
        }
        if (dist[target] == 501) return -1;
        return dist[target];
    }
};
```
基本完全不懂。lee佬的[解法](https://leetcode.com/problems/bus-routes/solutions/122771/c-java-python-bfs-solution)没用多源bfs，而是直接bfs顺便记录数量。总之比editorial表现要好