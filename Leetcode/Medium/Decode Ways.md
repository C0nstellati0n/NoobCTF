# [Decode Ways](https://leetcode.com/problems/decode-ways)

我说怎么不对呢，原来我遍历反了
```c++
//https://leetcode.com/problems/decode-ways/solutions/30451/evolve-from-recursion-to-dp
//建议看discussion区renwopang的评论
//其实看了那个评论应该就能自己写出来了，但是我以为是从头开始遍历……不带脑子的下场
class Solution {
public:
    int numDecodings(string s) {
        int p = 1, pp, n = s.size();
        for(int i=n-1;i>=0;i--) {
            int cur = s[i]=='0' ? 0 : p;
            if(i<n-1 && (s[i]=='1'||s[i]=='2'&&s[i+1]<'7')) cur+=pp;
            pp = p;
            p = cur;
        }
        return p;   
    }
};
```
