# [Two Best Non-Overlapping Events](https://leetcode.com/problems/two-best-non-overlapping-events)

站在巨人的肩膀上跑得就是快（？）
```c++
class Solution {
public:
    int maxTwoEvents(vector<vector<int>>& events) {
        int n = events.size(); 
        vector<pair<int, int>> st(n);
        for(int i = 0; i < n; i++) st[i] = {events[i][0], i};
        sort(st.begin(), st.end());
        vector<int> dp(n+1); //dp[i]表示st[i]到末尾的这些event里最大的value。dp[n]是base case，为0
        for(int i = n-1;i>-1;i--){
            dp[i]=max(dp[i+1],events[st[i].second][2]);
        }
        int ans=0;
        //按start time顺序考虑全部event。用lower_bound可以找到索引i后所有不与当前考虑的event重合的event的索引。配合之前计算的dp就能找到不与当前event重合的event中的最大值
        //不用考虑i之前的event。这种情况在之前就考虑过了
        for(int i=0;i<n;i++){
            //正好lower_bound没找到符合要求的值就会返回st.end()。st.end()-st.begin()正好是n，对应上面的base case
            ans=max(ans,events[st[i].second][2] + dp[lower_bound(st.begin(), st.end(), make_pair(events[st[i].second][1]+1, 0)) - st.begin()]);
        }
        return ans;
    }
};
```
discussion里有人提到这题和`Maximum Profit in Job Scheduling`有点像。跑去看了一眼，偷了个表现好的代码改成这题的解法。而且发现我这个代码的用时很不错，editorial和solutions里类似思路的解法跑起来没那么快，因为实现算法时用了array或map

但其实editorial里的`Approach 3: Greedy`整体是比我的做法聪明+应该表现更好的。constraints太小惹的祸