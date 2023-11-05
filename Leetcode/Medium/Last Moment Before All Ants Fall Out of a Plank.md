# [Last Moment Before All Ants Fall Out of a Plank](https://leetcode.com/problems/last-moment-before-all-ants-fall-out-of-a-plank)

烟雾弹之下是其easy的本质
```c++
class Solution {
public:
    int getLastMoment(int n, vector<int>& left, vector<int>& right) {
        int ans=0;
        for(int val:left){
            ans=max(ans,val);
        }
        for(int val:right){
            ans=max(ans,n-val);
        }
        return ans;
    }
};
```
这题棘手的点在于，两只蚂蚁迎面相撞后会改变方向。但是仔细一想，这和蚂蚁相撞后继续走又有什么区别呢？只不过是把两边的蚂蚁交换了一下，该怎么走，走了多久，还差多少没有任何变化。这题我们完全不关心到底是哪只蚂蚁最后掉落，我们只关心最后的时间。所以无脑遍历+max就完事了