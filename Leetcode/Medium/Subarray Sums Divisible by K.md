# [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k)

[昨天的题](https://leetcode.com/problems/continuous-subarray-sum)和今天这题思路有异曲同工之妙，但这题多了个负数。死于不知道如何处理负数和base case
```c++
//https://leetcode.com/problems/subarray-sums-divisible-by-k/editorial
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) {
        vector<int> mod(k);
        mod[0]=1; //base case。假如下面我们算preMod时结果是0，那么 ans+=mod[preMod] 时应该直接加上1，无论是不是第一次见
        int preMod=0;
        int ans=0;
        for(const int& n:nums){
            preMod=(preMod+n%k+k)%k; //用于处理n是负数的情况
            ans+=mod[preMod];
            mod[preMod]++;
        }
        return ans;
    }
};
```