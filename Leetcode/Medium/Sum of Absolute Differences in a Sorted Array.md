# [Sum of Absolute Differences in a Sorted Array](https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array)

我是hint仙人
```c++
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        vector<int> prefix;
        int n=nums.size();
        prefix.push_back(nums[0]);
        for(int i=1;i<n;i++){
            prefix.push_back(prefix[i-1]+nums[i]);
        }
        vector<int> ans;
        for(int i=0;i<n;i++){
            if(i!=0){
                ans.push_back(nums[i]*i-prefix[i-1]+prefix[n-1]-prefix[i]-nums[i]*(n-i-1));
            }
            else{
                ans.push_back(prefix[n-1]-nums[i]*n);
            }
        }
        return ans;
    }
};
```
经典“看了hint就会写了”。[editorial](https://leetcode.com/problems/sum-of-absolute-differences-in-a-sorted-array)还有几种prefix/suffix sum的变种