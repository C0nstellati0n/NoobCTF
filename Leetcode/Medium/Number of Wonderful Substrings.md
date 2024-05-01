# [Number of Wonderful Substrings](https://leetcode.com/problems/number-of-wonderful-substrings)

我是什么很笨的人吗？是的
```c++
//https://leetcode.com/problems/number-of-wonderful-substrings/solutions/1299773/intuitive-explanation-easy-to-understand
class Solution {
public:
    long long wonderfulSubstrings(string word) {
        int cnt[1024]={1}; //注意这个语法是将cnt[0]设置为1，不是全部设为1
        int mask=0;
        long long ans=0;
        for(const char&c:word){
            mask^=1<<(c-'a');
            ans+=cnt[mask];
            for(int i=0;i<10;i++){
                ans+=cnt[mask^(1<<i)];
            }
            cnt[mask]++;
        }
        return ans;
    }
};
```
substring，根据我以往的经验，要么单调栈（monotonic stack）要么dp。这题没单调性，那就只有dp了。爆破做法很简单，遍历全部的substring，dp再记点东西即可。但 $n^2$ 的复杂度让我根本就不想试，反正下场都是TLE

然后就到这个天杀的bitmask+linear dp做法了。发现和bit manipulation沾边的题都不会简单。一般substring dp的思路是来个代表substring索引（i，j）的二维dp，但这题substring的索引根本就不重要。题目要求最多只有一个字符的出现次数为奇数，最多10个字符。那一个字符最多两种状态，要么出现偶数次，要么出现奇数次。可以用bitmask表示这两个状态，第i个bit为0意味着第i个字符出现偶数次；为1则是出现奇数次

所以有没有这么一种记录dp的方式，使其在不记录所有substring的state的情况下考虑到全部substring？答案是，`dp[i]`表示`word[0:i]`处的mask，即n个prefix。通过这n个prefix就可以计算出全部的substring

假如目前的索引为i，mask为a，如果`cnt[a]`不为0，说明在某个比i小的索引处j，这个mask出现过一次。那么某个substring`word[j:i]`中全部的字符出现次数都为偶数。这是一个满足条件的substring，所以`ans+=cnt[mask]`

还有另一种情况，即有一个字符出现次数为奇次。看看当前这个mask，有一个字符出现为奇数次即只有一个bit与mask异或了1次，改变了mask的一个bit。所以我们for循环遍历10次，每次修改一个bit，若在cnt里有这个mask，同样`word[j:i]`是一个符合条件的substring（如果n个的话就是n个substring）