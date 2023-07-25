# Peak Index in a Mountain Array

[题目](https://leetcode.com/problems/peak-index-in-a-mountain-array/description/)

所以为什么一个binary search也能算medium？关键这还是那种没有其他坑的binary search啊？
```c#
public class Solution {
    public int PeakIndexInMountainArray(int[] arr) {
        int start = 0;
        int end = arr.Length - 1;
        while (start <= end) {
            int mid = start + (end-start)/2;
            if (arr[mid] < arr[mid+1]) start = mid+1;
            else end = mid-1;
        }
        return start;
    }
}
```
```
Runtime
199 ms
Beats
96.30%
Memory
52.3 MB
Beats
19.14%
```
更搞笑的是，[editorial](https://leetcode.com/problems/peak-index-in-a-mountain-array/editorial/)里竟然有个linear search方法？啊？啊？啊？

solution区的著名大佬lee215提出可以用[Golden-section search](https://en.wikipedia.org/wiki/Golden-section_search)： https://leetcode.com/problems/peak-index-in-a-mountain-array/solutions/139848/c-java-python-better-than-binary-search/ 。这里他是用python实现的，c#难写。又是留给读者的拓展阅读，我对这个算法真的不熟。