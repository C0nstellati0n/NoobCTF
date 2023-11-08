# [Eliminate Maximum Number of Monsters](https://leetcode.com/problems/eliminate-maximum-number-of-monsters)

不对劲啊，这11月的题怎么我都能做出来？与10月形成鲜明对比
```c++
class Solution {
public:
    int eliminateMaximum(vector<int>& dist, vector<int>& speed) {
        for(int i=0;i<dist.size();i++){
            dist[i]=ceil(dist[i]/(double)speed[i]);
        }
        sort(dist.begin(),dist.end());
        int ans=1;
        for(int i=1;i<dist.size();i++){
            if(dist[i]<=i) return ans;
            ans++;
        }
        return ans;
    }
};
```
因为剑一分钟充能一次，所以索引i可用于比较。距离/速度=时间，i处的怪物用时小于等于i就到达了城市，说明剑来不及充能，游戏结束。默认一定能杀掉第一只，因为最开始是充能好的