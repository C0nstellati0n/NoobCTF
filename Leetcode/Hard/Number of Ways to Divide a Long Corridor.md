# [Number of Ways to Divide a Long Corridor](https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor)

dp是天坑，有数学做法千万不要想dp做法
```c++
//采样区，editorial的Approach 4/5
class Solution {
public:
    int numberOfWays(string corridor) {
        long long ans = 0, prev = 0;
        const int n = corridor.length();        
        int last = -1, first = n;
        for (int i = n-1; i >= 0; --i) {
            if (corridor[i] == 'P') {
                continue;
            }
            if (last == -1) { //last==-1 && corridor[i] == 'S'
                last = i;
            } else { //last!=-1 && corridor[i] == 'S'
                ans = (first == n) ? 1 : ((first - last) * prev) % 1000000007; //从后往前数，first表示第一组seat，last表示第二组seat。那么first-last-1是两组seat中间P的数量，可提供P+1=first-last中分割方式。first==n的情况比较特殊，进入这个分支意味着之前有个seat，现在又遇到了个seat。在first=n的情况下两者应该是一组的，为base case的一个分割方式。相乘则是组合学的经典操作
                prev = ans;
                first = i; //后面first和last就表示两组不同seat的分界线了。建议脑运行一下才看得更明白
                last = -1;
            }
        }
        return (last == -1) ? ans : 0; //last=-1的情况对应seat总数为偶数。为单数直接返回0，不可能有分割方式
    }
};
```
关键点在于两组seat中间P的数量。SSPPSS，分割方式为P+1=3。同一组之内P不会提供更多分割方式，如SPPS，只能一种。然后dp做法个人没看懂，特别是空间优化做法