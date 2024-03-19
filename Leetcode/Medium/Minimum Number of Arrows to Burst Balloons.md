# [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons)

本来是不想记的，但是这种题好像整体属于一种类型：[Overlapping Interval Problem](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/solutions/93735/a-concise-template-for-overlapping-interval-problem)，跟之前见过的Non-overlapping Interval问题一样，都是贪心问题
```c++
class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        sort(points.begin(), points.end(), []( const vector<int>& first, const vector<int>& second )
        {
            return first[1] < second[1];
        });
        int arrow=1;
        int currentEnd=points[0][1];
        for(int i=1;i<points.size();i++){
            if(points[i][0]>currentEnd){
                arrow++;
                currentEnd=points[i][1];
            }
        }
        return arrow;
    }
};
```