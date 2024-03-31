# [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers)

我这么笨，要不还是算了？
```c++
//采样区，比editorial里的方法快很多
//但是方法在 https://leetcode.com/problems/subarrays-with-k-different-integers/editorial 有介绍
int cnt[20001];
class Solution {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        return subcount(nums, k) - subcount(nums, k-1);
    }
    int subcount(vector<int>& nums, int k) {
        memset(cnt, 0, 20001 * sizeof(int));
        int c=1, res=0;
        cnt[nums[0]] = 1;
        auto head = nums.begin(), tail = nums.begin();
        while (head < nums.end()) {
            if (c <= k && tail < nums.end()) {
                tail++;
                if (tail < nums.end()) {
                    cnt[*tail]++;
                    if (cnt[*tail] == 1) c++;
                }
            } else {
                res += (int)(tail - head - 1);
                cnt[*head]--;
                if (cnt[*head] == 0) c--;
                head++;
            } 
        }
        return res;
    }
};
```
这几天把sliding window的几个变种都看了一遍。at Least K写过了，Less Than K写过了，那么这个正好K该怎么办？首先要知道，在获取一个满足条件的window后，怎么计算subarray的数量？答案在editorial里有：

For each valid window, we can calculate the total number of subarrays it can form using the formula right - left + 1. This represents the number of subarrays ending at the current element (right) and starting anywhere from the current left boundary (left) to the right pointer (right) (inclusive).

如left是0，right是3，里面满足“at Most K”条件的subarray数量为left-right+1。拿0，1，2，3作为所有可能的起始点，固定结束点为right，数量正好是left-right+1=4。然后呢？这里的数量是at most K，或者说Less Than K，我们要正好K啊？不急，假如我们先算at most k的subarray数量，再算at most k-1的subarray数量，两者一减，不就是正好k的subarray数量了吗？