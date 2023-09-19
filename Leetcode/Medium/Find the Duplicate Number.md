# Find the Duplicate Number

[题目](https://leetcode.com/problems/find-the-duplicate-number)

这题竟然有9种做法？
```c#
//https://leetcode.com/problems/find-the-duplicate-number/solutions/1892921/9-approaches-count-hash-in-place-marked-sort-binary-search-bit-mask-fast-slow-pointers
//Fast Slow Pointers
public class Solution {
    public int FindDuplicate(int[] nums) {
        int slow = 0;
        int fast = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
}
```
```
Runtime
172 ms
Beats
80.97%
Memory
54.6 MB
Beats
14.19%
```
不过要是严格按照description，使用constant space且不修改nums数组，Brute Force（TLE），count/Hashtable（space是O(n)），Marking visited value within the array/Sort/Index Sort（修改了nums数组）都不能算在里面。那就只剩下binary search，bit和Fast Slow Pointers。这个Fast Slow Pointers在图论里见过，常用于检测图里是否有cycle。所以它为什么能用在这道题？关键在于nums中元素的限制。
- Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.

意味着数字等于其index+1.这下就能把它看成图了。重复的数字会导致cycle，就是我们要找的了。先一个do-while确定cycle的区域，然后break进入另一个while找到导致cycle的那个数字。类似 https://leetcode.com/problems/linked-list-cycle-ii/solutions/1701055/JavaC++Python-best-explanation-ever-happen's-for-this-problem/ 提到的。

binary search做法也是相当巧妙的。一个鸽笼原理：假如有n+1个数字，要放在n个地方，必定有1个数字重复。这个原理似乎小学就讲过了，当时我还觉得蠢，这不是说废话吗？没想到多年后的一天我用上了。我们有个mid，然后遍历nums数组，计算小于等于mid的数字的数量m。假如m大于mid，说明重复的数字一定在[left,mid]。为什么？从起始处1一直到中间的mid，我们只有mid个位置，但却有m个数字小于mid。根据鸽笼原理，必定有数字重复。再加上此题的限制，唯一重复数字一定在[left,mid].反之，则重复数字在[mid+1,right]

bit做法不懂，我是笨蛋。