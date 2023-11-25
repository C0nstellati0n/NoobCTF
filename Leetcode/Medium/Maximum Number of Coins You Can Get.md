# [Maximum Number of Coins You Can Get](https://leetcode.com/problems/maximum-number-of-coins-you-can-get)

就喜欢这种披着medium的皮本质是easy的题
```c++
class Solution {
public:
    int maxCoins(vector<int>& piles) {
        sort(piles.begin(),piles.end());
        int i=0,j=piles.size()-1;
        int ans=0;
        while(i<j){
            i++;
            j--;
            ans+=piles[j];
            j--;
        }
        return ans;
    }
};
```
editorial和这个差不多，不过使用for循环一次到位。采样区的counting sort：
```c++
//又见到你了，提速魔法。是真的魔法，我那个做法本身100多ms，用魔法后冲70ms
#pragma GCC optimize("Ofast","inline","ffast-math","unroll-loops","no-stack-protector")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,avx2,tune=native","f16c")
static const auto fast = []() { std::ios_base::sync_with_stdio(false); std::cin.tie(0); std::cout.tie(0); return 0; } ();
class Solution
{
public:
    int maxCoins(vector<int> &piles)
    {
        int hash[10001] = { 0 };
        for(auto x : piles) //counting sort
        {
            hash[x]++;
        }
        int last = 1'0000;
        int front = 0;
        int n = ((piles.size() / 3));
        int res = 0;
        while(n--)
        {
            while(last > 0 && hash[last] == 0)
            {
                last--;
            }
            hash[last]--;
            while(last > 0 && hash[last] == 0)
            {
                last--; // second largest
            }
            res += last;
            hash[last]--;
        }
        return res;
    }
};
```