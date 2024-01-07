# [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling)

炸了，我连大佬的c++代码都看不懂
```c++
//https://leetcode.com/problems/maximum-profit-in-job-scheduling/solutions/409009/java-c-python-dp-solution
class Solution {
public:
    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<vector<int>> jobs;
        for (int i = 0; i < n; ++i) {
            jobs.push_back({endTime[i], startTime[i], profit[i]});
        }
        sort(jobs.begin(), jobs.end());
        map<int, int> dp = {{0, 0}}; //某个endTime下能获取的最大profit
        for (auto& job : jobs) {
            //这个prev应该是拿当前迭代器的上一个（map是排序好的），参考 https://stackoverflow.com/questions/20215463/c-map-previous-item-of-a-key
            //这个cur的逻辑应该是，考虑当前job的开始时间，upper_bound找最小的大于这个数的数，即最小的endTime；prev找endTime的前面一个，即上一次取job的endTime。如果要这个job，就加上profit。要是大于目前最大的profit就更新map
            int cur = prev(dp.upper_bound(job[1]))->second + job[2]; //https://www.geeksforgeeks.org/map-upper_bound-function-in-c-stl/
            if (cur > dp.rbegin()->second) //https://www.geeksforgeeks.org/map-rbegin-function-in-c-stl/
                dp[job[0]] = cur;
        }
        return dp.rbegin()->second; //map内部是一个个pair，所以这里就是在取pair的第二个元素： https://stackoverflow.com/questions/15451287/what-does-iterator-second-mean
    }
};
```