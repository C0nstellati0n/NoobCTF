# [Maximum Product of Two Elements in an Array](https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array)

再这么做下去脑子要生锈了
```c++
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        return (nums[nums.size()-2]-1)*(nums[nums.size()-1]-1);
    }
};
```
O(n)的做法： https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array/solutions/661780/c-biggest-and-second-biggest