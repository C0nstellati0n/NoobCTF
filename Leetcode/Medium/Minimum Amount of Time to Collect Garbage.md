# [Minimum Amount of Time to Collect Garbage](https://leetcode.com/problems/minimum-amount-of-time-to-collect-garbage)

慢就慢在细节上
```c++
class Solution {
public:
    int garbageCollection(vector<string>& garbage, vector<int>& travel) {
        int ans=0;
        int highM=0;
        int highP=0;
        int highG=0;
        for(int i=1;i<garbage.size();i++){
            if(garbage[i].find("M")!=std::string::npos){
                highM=i;
            }
            if(garbage[i].find("P")!=std::string::npos){
                highP=i;
            }
            if(garbage[i].find("G")!=std::string::npos){
                highG=i;
            }
        }
        ans+=garbage[0].size();
        for(int i=1;i<garbage.size();i++){
            if(i<=highM){
                ans+=travel[i-1];
            }
            if(i<=highP){
                ans+=travel[i-1];
            }
            if(i<=highG){
                ans+=travel[i-1];
            }
            ans+=garbage[i].size();
        }
        return ans;
    }
};
```
editorial用unordered_map，比lee佬的数组慢了不少：
```c++
//https://leetcode.com/problems/minimum-amount-of-time-to-collect-garbage/solutions/2492774/java-c-python-explanation-with-observations
class Solution {
public:
    int garbageCollection(vector<string>& garbage, vector<int>& travel) {
        int last[128] = {}, res = 0;
        for (int i = 0; i < garbage.size(); ++i) {
            res += garbage[i].size();
            for (char c : garbage[i]) //不太确定是这种更快还是直接find更快。我觉得是这种，个人认为find内部除了遍历整个字符串也没什么其他做法，我调用了3次，那就是遍历3次，这里指用遍历一次
                last[c] = i;
        }
        for (int j = 1; j < travel.size(); ++j) //prefix sum。接下来直接通过每种垃圾最后出现的索引一加就完事了
            travel[j] += travel[j - 1];
        for (int c : "PGM")
            if (last[c])
                res += travel[last[c] - 1];
        return res;
    }
};
```