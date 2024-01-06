# [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence)

虽然这题自己写出来了而且solution区有非常好的解释，我补充也多少有些班门弄斧；但是这可是大名鼎鼎的LIS！之前遇见好多个变种了，今天才遇见本尊。秒了，但是复杂度 $n^2$ ，所以到底是谁把谁秒了？
```c++
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> lengths(nums.size(),1);
        int ans=1;
        for(int i=1;i<nums.size();i++){
            for(int j=0;j<i;j++){
                if(nums[i]>nums[j]){
                    lengths[i]=max(lengths[i],lengths[j]+1);
                    ans=max(lengths[i],ans);
                }
            }
        }
        return ans;
    }
};
```
推荐阅读 https://leetcode.com/problems/longest-increasing-subsequence/solutions/1326308/c-python-dp-binary-search-bit-segment-tree-solutions-picture-explain-o-nlogn ，其中第二种做法用binary search，不难理解而且表现比dp好得多；剩下几种就比较难懂了