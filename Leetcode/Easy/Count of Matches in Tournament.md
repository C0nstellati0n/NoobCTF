# [Count of Matches in Tournament](https://leetcode.com/problems/count-of-matches-in-tournament)

leetcode你最好真的让这个月变为Easember
```c++
class Solution {
public:
    int numberOfMatches(int n) {
        return n-1;
    }
};
```
不要管题目描述，也不用作模拟，就思考一件事：只输一场比赛就会被淘汰，一场比赛都没输的肯定是最后的胜者。一场比赛只能淘汰一个队伍，那么淘汰n-1个队伍需要多少场比赛呢？也是n-1