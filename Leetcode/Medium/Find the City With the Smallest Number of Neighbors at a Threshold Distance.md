# [Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance)

原来我还没正式写过Floyd-Warshall啊？
```c++
class Solution {
public:
    int findTheCity(int n, vector<vector<int>>& edges, int distanceThreshold) {
        vector<vector<int>> dist(n,vector<int>(n,-1));
        for(const auto& edge:edges){
            dist[edge[0]][edge[1]]=edge[2];
            dist[edge[1]][edge[0]]=edge[2];
        }
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if ((dist[i][j]==-1||dist[i][j] > (dist[i][k] + dist[k][j]))
                        && (dist[k][j] != -1
                            && dist[i][k] != -1))
                        dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
        int ans=-1;
        int curr=INT_MAX;
        int count;
        for(int i=0;i<n;i++){
            count=0;
            for(int j=0;j<n;j++){
                if(j==i) continue;
                if(dist[i][j]!=-1&&dist[i][j]<=distanceThreshold){
                    count++;
                }
            }
            if(ans==-1||count<=curr){
                ans=i;
                curr=count;
            }
        }
        return ans;
    }
};
```
在[这里](https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16)找的实现，但是自己改动了一点。由于不知道路径长度的上限，选择用-1代替。不是很好的做法，if条件一堆。还是大佬的实现简洁： https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/solutions/490312/java-c-python-easy-floyd-algorithm