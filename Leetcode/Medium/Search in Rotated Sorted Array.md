# Search in Rotated Sorted Array

[题目](https://leetcode.com/problems/search-in-rotated-sorted-array/description/)

心态在连续三次错误后彻底爆炸。我参考的是discussion区mandy1339的提示。
```c#
class Solution {
    public int Search(int[] nums, int target) {
        int n = nums.Length;
        int left = 0, right = n - 1;

        // Find the index of the pivot element (the smallest element)
        while (left <= right) {
            int mid = (left + right) / 2;
            if (nums[mid] > nums[n - 1]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return shiftedBinarySearch(nums, left, target);
    }
    // Shift elements in a circular manner, with the pivot element at index 0.
    // Then perform a regular binary search
    private int shiftedBinarySearch(int[] nums, int pivot, int target) {
        int n = nums.Length;
        int shift = n - pivot;
        int left = (pivot + shift) % n; //不懂为啥要这样，直接int left = 0;int right = n-1; 不好吗
        int right = (pivot - 1 + shift) % n;

        while (left <= right) {
            int mid = (left + right) / 2;
            if (nums[(mid - shift + n) % n] == target) { //？？？ shift = n - pivot; ，mid - shift + n=mid-n+pivot+n=mid+pivot???为啥不直接来
                return (mid - shift + n) % n;
            } else if (nums[(mid - shift + n) % n] > target) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return -1;
    }
}
```
```
Runtime
68 ms
Beats
99.51%
Memory
39 MB
Beats
83.5%
```
拿[4,5,6,7,0,1,2]举例。它的pivot index是3，本来应该是[0,1,2,4,5,6,7]的。不要管那个旋转后的数组，假如是本来的情况，start应该是0，end应该是7对应index 6。 那旋转后还是一样的，start还是0，但是对应的index是4了，同理7对应着index 3。那怎么算这个index？答案是加上pivot再模数组长度。

然后我把我错误的的代码改对了。
```c#
public class Solution {
    public int Search(int[] nums, int target) {
        int start = 0;
        int end = nums.Length - 1;
        int mid=0;
        while (start <= end) {
            mid = start + (end-start)/2;
            if (nums[mid] > nums[^1]) start = mid + 1;
            else end = mid - 1;
        }
        int pivot=start;
        start=0;
        end = nums.Length - 1;
        while (start <= end) {
            mid = start + (end-start)/2;
            if (nums[(mid+pivot)%nums.Length] == target) return (mid+pivot)%nums.Length;
            else if (nums[(mid+pivot)%nums.Length] > target) end = mid-1;
            else start = mid + 1;
        }
        return -1;
    }
}
```
```
Runtime
77 ms
Beats
91.44%
Memory
39.3 MB
Beats
45.51%
```
然后还有一种解法是，找到pivot后，从pivot那里把数组分成两个，分别进行binary search。这种就很好理解了。还有一种只用一次binary search的，也挺有意思。