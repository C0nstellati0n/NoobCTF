# [Determine if a Cell Is Reachable at a Given Time](https://leetcode.com/problems/determine-if-a-cell-is-reachable-at-a-given-time)

edge case的坑全踩完了
```c++
class Solution {
public:
    bool isReachableAtTime(int sx, int sy, int fx, int fy, int t) {
        if(sx==fx&&sy==fy&&t==1) return false;
        return max(abs(fx-sx),abs(fy-sy))<=t;
    }
};
```
这个`max(abs(fx-sx),abs(fy-sy))`算的是[Chebyshev distance](https://en.wikipedia.org/wiki/Chebyshev_distance)(切比雪夫距离)。只要距离小于等于t，我们就能按时到达（主要是我们能斜着走，x和y同时增加。x和y中最大的值小于t，保证能到达）。等于t就斜着走，走到与目标同一条线时直接走过去即可；小于t的话就要在目标旁边绕圈子

edge case是起点和终点相等但是步子等于1.大于这个数还好，走出去之后绕圈子回来即可。等于1说明我们必须往外走一步，但是回不来了