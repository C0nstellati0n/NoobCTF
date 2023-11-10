# [Count Number of Homogenous Substrings](https://leetcode.com/problems/count-number-of-homogenous-substrings)

discussion区的某人：use long EVERYWHERE

我：这个我知道，ans肯定用long。索引应该不用吧

wrong answer后：md我应该听你的
```c++
class Solution {
public:
    int countHomogenous(string s) {
        long ans=0;
        long i=0;
        long j=0;
        int mod=(int)1e9+7;
        while(i<s.length()&&j<s.length()){
            if(s[i]==s[j]) j++;
            else{
                ans=ans+((j-i)*(j-i+1)/2)%mod; //N * (N + 1) / 2,N为字符串长度
                i=j;
            }
        }
        ans=ans+((j-i)*(j-i+1)/2)%mod;
        return ans;
    }
};
```
也可以像[editorial](https://leetcode.com/problems/count-number-of-homogenous-substrings/editorial)一样用streak一个一个加