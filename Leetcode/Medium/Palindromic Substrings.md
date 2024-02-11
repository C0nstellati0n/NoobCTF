# [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings)

继续打卡经典题型（这可比subsequence简单多了）
```c++
class Solution {
public:
    int countSubstrings(string s) {
        int ans=0;
        int i,j;
        for(int curr=0;curr<s.length();curr++){
            i=j=curr;
            while(i>=0&&j<s.length()&&s[i]==s[j]){
                ans++;
                i--;
                j++;
            }
            i=curr;
            j=i+1;
            while(i>=0&&j<s.length()&&s[i]==s[j]){
                ans++;
                i--;
                j++;
            }
        }
        return ans;
    }
};
```
个人看了discussion区magicsign的评论后就做出来了。关键在于将奇数长度和偶数长度的回文字符串分开考虑