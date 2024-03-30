# [Count Subarrays Where Max Element Appears at Least K Times](https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times)

找规律数学题+sliding window
```c++
//https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/editorial
class Solution {
public:
    long long countSubarrays(vector<int>& nums, int k) {
        int maxElement = *max_element(nums.begin(), nums.end());
        long long ans = 0, start = 0;
        for (int end = 0; end < nums.size(); end++) {
            if (nums[end] == maxElement) {
                k--;
            }
            while (!k) {
                if (nums[start] == maxElement) {
                    k++;
                }
                start++;
            }
            ans += start;
        }
        return ans;
    }
};
```
假设有一个subarray，其结尾index为j；在这个subarray中，最大元素至少出现了k次。那么这个subarray包含多少个同样满足“最大元素出现了k次”条件的subarray？这是这道题的关键问题。答案是找到最大元素第一次出现的索引，这个索引往前一直数到0就是答案。这个数量就是sliding window里的start。editorial里有动图，非常清晰