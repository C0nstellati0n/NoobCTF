# Merge Sorted Array

[题目](https://leetcode.com/problems/merge-sorted-array/description/)

合并两个已排序数组，第一个数组的长度是两个数组合并后的总长度。第一想法是把第一个数组转为list，然后调用insert函数把第二个数组的元素插进去。结果发现老是超索引（后来想想可能是我的and条件把检查索引的放后面了，取值的却放在前面，导致溢出），于是去看了别人的答案。第一种方法有点偷懒，利用C#自带的Array.sort完成。

```c#
public class Solution {
    public void Merge(int[] nums1, int m, int[] nums2, int n) {
        for(int i=0; i<n; i++){
            nums1[m+i] = nums2[i];
        }
        Array.Sort(nums1);
    }
}
```

```
Runtime
128 ms
Beats
96.89%
Memory
42.8 MB
Beats
35.92%
```

剩下的解法基本都是双指针了。这里放两个变种。

```c#
public class Solution {
    public void Merge(int[] nums1, int m, int[] nums2, int n) {
        int i = m-1;
        int j = n-1;
        int k = m+n-1;
        while(i>=0 && j>=0){
            if(nums1[i] > nums2[j]){
                nums1[k] = nums1[i];
                i--; k--;
            }
            else{
                nums1[k] = nums2[j];
                j--; k--;
            }
        }
        while(j>=0){
            nums1[k] = nums2[j];
            j--; k--;
        }
    }
}
```

```
Runtime
128 ms
Beats
96.89%
Memory
42.8 MB
Beats
53.43%
```

下面的一个也是差不多的思路，不过有注释。

```c#
public class Solution {
    public void Merge(int[] nums1, int m, int[] nums2, int n) {
        //variables to work as pointers
        int i=m-1; // will point at m-1 index of nums1 array
        int j=n-1; // will point at n-1 index of nums2 array
        int k=nums1.Length-1; //will point at the last position of the nums1 array

        // Now traversing the nums2 array
        while(j>=0){
            // If element at i index of nums1 > element at j index of nums2
            // then it is largest among two arrays and will be stored at k position of nums1
            // using i>=0 to make sure we have elements to compare in nums1 array
            if(i>=0 && nums1[i]>nums2[j]){
                nums1[k]=nums1[i];
                k--; 
                i--; //updating pointer for further comparisons
            }else{
                // element at j index of nums2 array is greater than the element at i index of nums1 array 
                // or there is no element left to compare with the nums1 array 
                // and we just have to push the elements of nums2 array in the nums1 array.
                nums1[k] = nums2[j];
                k--; 
                j--; //updating pointer for further comparisons
            }
        }
    }
}
```

```
Runtime
136 ms
Beats
82.81%
Memory
42.7 MB
Beats
53.43%
```