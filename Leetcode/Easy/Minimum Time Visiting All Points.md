# [Minimum Time Visiting All Points](https://leetcode.com/problems/minimum-time-visiting-all-points)

连续三个easy，还是周末……鸿门宴？
```c++
class Solution {
public:
    int minTimeToVisitAllPoints(vector<vector<int>>& points) {
        int ans=0;
        pair<int,int> last(points[0][0],points[0][1]); //笨蛋做法，压根就不用这个，直接拿points[i-1]即可
        int x;
        int y;
        for(int i=1;i<points.size();i++){
            x=abs(points[i][0]-last.first);
            y=abs(points[i][1]-last.second);
            if(x==y){ //这一堆if语句也有点繁琐了
                ans+=x;
            }
            else if(x>y){
                ans+=y;
                ans+=x-y;
            }
            else{
                ans+=x;
                ans+=y-x;
            }
            last.first=points[i][0];
            last.second=points[i][1];
        }
        return ans;
    }
};
```
我写代码主打一个不过脑子