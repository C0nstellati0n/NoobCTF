# Search in Rotated Sorted Array II

[题目](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/)

绷不住了。
```c#
class Solution {
    public bool Search(int[] nums, int target) {
        return nums.Contains(target);
    }
}
```
```
Runtime
79 ms
Beats
96.70%
Memory
41.5 MB
Beats
88.46%
```
主要这题constraint的nums.Length太小了，直接linear search完全没有问题。况且binary search做法的最差情况时间复杂度也是O(n)。
```c#
//https://leetcode.com/problems/search-in-rotated-sorted-array-ii/editorial/
class Solution {
    public bool Search(int[] nums, int target) {
        int n = nums.Length;
        if (n == 0) return false;
        int end = n - 1;
        int start = 0;

        while (start <= end) {
            int mid = start + (end - start) / 2;

            if (nums[mid] == target) {
                return true;
            }

            if (!isBinarySearchHelpful(nums, start, nums[mid])) {
                start++;
                continue;
            }
            // which array does pivot belong to.
            bool pivotArray = existsInFirst(nums, start, nums[mid]);

            // which array does target belong to.
            bool targetArray = existsInFirst(nums, start, target);
            if (pivotArray ^ targetArray) { // If pivot and target exist in different sorted arrays, recall that xor is true when both operands are distinct
                if (pivotArray) {
                    start = mid + 1; // pivot in the first, target in the second
                } else {
                    end = mid - 1; // target in the first, pivot in the second
                }
            } else { // If pivot and target exist in same sorted array
                if (nums[mid] < target) {
                    start = mid + 1;
                } else {
                    end = mid - 1;
                }
            }
        }
        return false;
    }
    // returns true if we can reduce the search space in current binary search space
    private bool isBinarySearchHelpful(int[] arr, int start, int element) {
        return arr[start] != element;
    }
    // returns true if element exists in first array, false if it exists in second
    private bool existsInFirst(int[] arr, int start, int element) {
        return arr[start] <= element;
    }
}
```
```
Runtime
80 ms
Beats
96.70%
Memory
41.7 MB
Beats
39.1%
```
这题和[Search in Rotated Sorted Array](./Search%20in%20Rotated%20Sorted%20Array.md)很像，不过数组中可能会出现重复元素。那么想解出这题就要知道这会对binary search造成什么影响。此题的排序数组被“旋转”了一下，那就看成两个不同的排序数组好了，第一个叫F，第二个叫S。S中的任何元素一定小于等于F的第一个元素。若target大于nums[start],target肯定在F里，反之在S里。等于的话不用管它在哪，直接返回true完事。mid也是同理。

现在知道了怎么判断某个数在F还是S里，就能开始binary search了。若arr[mid]在F里，target在S里，则target在(mid,end]里。反之在[start,mid)里。若两者都在F里，F是一个已排序的数组，正常binary search怎么缩减搜索空间就怎么缩，都在S里同理。

所以重复元素会有啥影响？注意这句话“S中的任何元素一定小于等于F的第一个元素”。要是我们遇见arr[mid]=arr[start]的情况咋办？那arr[mid]既可能在F也可能在S啊，咋缩？那没办法了，直接一个一个缩，即代码里的start++.

类似做法还有 https://leetcode.com/problems/search-in-rotated-sorted-array-ii/solutions/1890199/c-algorithm-binary-search/ 。这种是一旦遇见重复元素就自动增加左右指针，剩下的正常binary search即可。