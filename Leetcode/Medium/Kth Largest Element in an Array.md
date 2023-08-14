# Kth Largest Element in an Array

[题目](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)

我甚至懒得搞倒序排序。
```c#
public class Solution {
    public int FindKthLargest(int[] nums, int k) {
        Array.Sort(nums);
        return nums[^k];
    }
}
```
```
Runtime
155 ms
Beats
94.31%
Memory
51.2 MB
Beats
32.3%
```
但是吧，题目描述都说了“能不能不用sort”，我们还是看[editorial](https://leetcode.com/problems/kth-largest-element-in-an-array/editorial/)有何见解吧。

一共给了4种解法，前两种sort和minHeap的太简单了，没啥说的。第三种quickSelect我第一次见。算法在nums范围中随机选一个索引pivot，然后遍历nums，比nums[pivot]大的放到名为left的数组里，等于的放到mid，小于的放到right（原本quickSelect是小的放left大的放right，不过原本的是用于选第k个最小元素的，我们要选第k个最大元素）。若left的元素个数大于等于k，说明第k个最大元素在left里面，对left数组再来一次quickSelect。若left的元素个数和mid的元素个数小于k，说明第k个最大元素在right里面，对right数组再来一次quickSelect。但这里要注意，对right数组执行时我们相当于把left和mid里的元素都丢掉了，它们都是比right里任何元素要大的。所以现在在right里找的不是第k个最大元素，而是k-left元素个数-mid元素个数。最后一种情况，left元素个数+mid元素个数==k，那选的那个nums[pivot]就是第k个最大元素了。

第4种解法是Counting Sort但没有sort。遍历整个nums数组，找到最大的元素（这题还要找个最小元素，因为题目输入有负值，而后续的count数组又是根据元素本身作为索引来记录的，没有负值。所以maxValue-minValue，要是是负数的话数组会更长）用于初始化count数组。`int[] count=new int[maxValue-minValue]`。count数组用于记录数组中每个数字的出现次数。由于我们根据元素本身作为索引来记录，所以只用倒着遍历count数组就能获取最大元素的数量，从而返回结果了。