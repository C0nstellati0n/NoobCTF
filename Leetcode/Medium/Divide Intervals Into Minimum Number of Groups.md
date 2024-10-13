# [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups)

关于我脑子转过来了但又没完全转过来这回事
```c++
//其实思路和 https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/solutions/2560020/min-heap 完全一样
//但是我为啥要让priority_queue记一个完整的vector？明明只有第二个数重要，记一个数不就完了吗？导致整体慢了很多
class Compare {
public:
    bool operator()(const vector<int>& a, const vector<int>& b)
    {
        return a[1]>b[1];
    }
};
class Solution {
public:
    int minGroups(vector<vector<int>>& intervals) {
        sort(intervals.begin(),intervals.end());
        priority_queue<vector<int>, vector<vector<int>>,Compare> groups;
        for(const auto& interval:intervals){
            if(groups.empty()||groups.top()[1]>=interval[0]){
                groups.push(interval);
            }
            else if(!groups.empty()&&groups.top()[1]<interval[0]){
                vector<int> temp=groups.top();
                groups.pop();
                temp[1]=interval[1];
                groups.push(temp);
            }
        }
        return groups.size();
    }
};
```
主要还是记录line sweep算法。在[editorial](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/editorial)和 https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/solutions/2560101/java-c-python-meeting-room 都有。在hint里可以看到，“The minimum number of groups we need is equivalent to the maximum number of intervals that overlap at some point”。把所有interval看成一条横直线，拿一条竖线扫过去，最多有多少交点？最多的交点数量就是这题的答案

editorial的版本为线性复杂度，第二种做法加了个排序算法的复杂度。线跨度大选后者；跨度小选前者