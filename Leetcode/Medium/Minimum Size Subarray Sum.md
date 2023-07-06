# Minimum Size Subarray Sum

[题目](https://leetcode.com/problems/minimum-size-subarray-sum/description/)

我脑子卡在昨天了，把题想复杂了。首先这题的难点在于，虽然是sliding window，但是window的长度未知，而且要找最短的。然后我就卡在这了，数组nums没排序，无规律，那我要把window全部可能的长度都试一遍？这肯定TLE啊。
```c#
//https://leetcode.com/problems/minimum-size-subarray-sum/editorial/
class Solution {
    public int MinSubArrayLen(int target, int[] nums) {
        int left = 0, right = 0, sumOfCurrentWindow = 0;
        int res = Int32.MaxValue;

        for(right = 0; right < nums.Length; right++) {
            sumOfCurrentWindow += nums[right]; //扩张窗户

            while (sumOfCurrentWindow >= target) {
                res = Math.Min(res, right - left + 1); //窗户的和到target了就记录当前窗户的长度
                sumOfCurrentWindow -= nums[left++]; //同时尝试是否还能缩减窗户
            }
        }

        return res == Int32.MaxValue ? 0 : res;
    }
}
```
```
Runtime
130 ms
Beats
41.54%
Memory
47.1 MB
Beats
76.73%
```
我是怎么能想不出来的啊！这题不是很简单吗，我只能归咎于我想得太复杂结果连续submit两个错误答案之后心态炸了。还有一个binary search的做法。
```c#
//https://leetcode.com/problems/minimum-size-subarray-sum/solutions/59123/o-n-o-nlogn-solutions-both-o-1-space/
public class Solution {
    public int MinSubArrayLen(int s, int[] nums) {
        int i = 1, j = nums.Length, min = 0;
        while (i <= j) {
            int mid = (i + j) / 2;
            if (windowExist(mid, nums, s)) {
                j = mid - 1;
                min = mid;
            } else i = mid + 1;
        }
        return min;
    }


    private bool windowExist(int size, int[] nums, int s) {
        int sum = 0;
        for (int i = 0; i < nums.Length; i++) { //尝试所有大小为size的window
            if (i >= size) sum -= nums[i - size];
            sum += nums[i];
            if (sum >= s) return true;
        }
        return false;
    }
}
```
```
Runtime
123 ms
Beats
72.88%
Memory
46.7 MB
Beats
99.23%
```
binary search我乍一听觉得不可能，这数字更本没有排序过，怎么search？后来发现，原来search的不是window的起始或者结束索引，是window的大小。window的大小确实遵循递增的规律，便能使用binary search了。