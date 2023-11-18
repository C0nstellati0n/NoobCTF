# [Minimize Maximum Pair Sum in Array](https://leetcode.com/problems/minimize-maximum-pair-sum-in-array)

美好的一天从简单的medium开始
```c++
class Solution {
public:
    int minPairSum(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        int ans=0,n = nums.size();;
        for(int i=0;i<n/2;i++){
            ans=max(ans,nums[i]+nums[n-i-1]);
        }
        return ans;
    }
};
```