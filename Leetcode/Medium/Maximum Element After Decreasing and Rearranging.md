# [Maximum Element After Decreasing and Rearranging](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging)

回归舒适区
```c++
class Solution {
public:
    int maximumElementAfterDecrementingAndRearranging(vector<int>& arr) {
        sort(arr.begin(), arr.end());
        int ans=1;
        for(int i=1;i<arr.size();i++){
            if(arr[i]>ans){
                ans++;
            }
        }
        return ans;
    }
};
```
[editorial](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/editorial)还有一个count sort解法，理论时间复杂度比直接sort低