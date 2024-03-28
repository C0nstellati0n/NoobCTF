# [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k)

再不学组合学我要在这种题死多少次？
```c++
//https://leetcode.com/problems/subarray-product-less-than-k/editorial
class Solution {
public:
  int numSubarrayProductLessThanK(vector<int>& nums, int k) {
    // Handle edge cases where k is 0 or 1 (no subarrays possible)
    if (k <= 1) return 0;
    int totalCount = 0;
    int product = 1;
    // Use two pointers to maintain a sliding window
    for (int left = 0, right = 0; right < nums.size(); right++) {
      // Expand the window by including the element at the right pointer
      product *= nums[right];
      // Shrink the window from the left while the product is greater than or equal to k
      while (product >= k) {
        // Remove the element at the left pointer from the product
        product /= nums[left++];
      }
      // Update the total count by adding the number of valid subarrays with the current window size
      totalCount += right - left + 1;  // right - left + 1 represents the current window size，也是新增的subarray数量
    }
    return totalCount;
  }
};
```
这题的sliding window我很容易就想出来了，因为有点像之前做过的另一道[Minimum Size Subarray Sum](./Minimum%20Size%20Subarray%20Sum.md)。但是这题要求算的是subarray的数量，我就懵了。一个长度为N的window内subarray的数量为`N*(N+1)/2`，这点不难。问题是，要是两个window重叠了呢？那就要减去两个window重叠部分的subarray数量。于是怎么记录这个重叠部分让我很头疼。然后翻到了 https://leetcode.com/problems/subarray-product-less-than-k/solutions/560093/python3-two-pointer-o-n-o-1-with-breakdown 评论区下 biggem 的评论，这才明白了。咱就是说为啥非要算一个window里的subarray数量然后再考虑什么重叠部分，直接算新增加的不好吗？算新增加的subarray数量的公式是`right - left + 1`，不要和window的size计算搞混了