# Binary Search

[题目](https://leetcode.com/problems/binary-search/description/)

binary search谁不会啊？况且我之前还写过，直接拿就完事了。

```c#
public class Solution {
    public int Search(int[] nums, int target) {
        if(!nums.Contains(target)){
            return -1;
        }
        int start = 0;
        int end = nums.Length - 1;
        while (start <= end) {
            int mid = start + (end-start)/2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] > target) end = mid-1;
            else start = mid + 1;
        }
        return start;
    }
}
```

```
Runtime
107 ms
Beats
98.36%
Memory
51.2 MB
Beats
13.23%
```

然后我寻思C#里就有这样的函数啊，于是一行也能搞定。

```c#
public class Solution {
    public int Search(int[] nums, int target) {
        return Array.IndexOf(nums,target);
    }
}
```

```
Runtime
115 ms
Beats
88.63%
Memory
51.1 MB
Beats
46.49%
```

或者各种细节上的不同。比如第一个解法的Contains有点耗时间，把它丢掉。

```c#
//https://leetcode.com/problems/binary-search/solutions/3363888/image-explanation-most-generalized-binary-search-c-java-python/
class Solution {
    public int Search(int[] nums, int target) {
        int l = 0, r = nums.Length - 1;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] >= target)
                r = mid;
            else
                l = mid + 1;  
        }
        if (nums[l] != target) return -1;
        return l;
    }
}
```

```
Runtime
115 ms
Beats
88.63%
Memory
51.1 MB
Beats
26.82%
```

第一个解法时的测试用例真的运气爆棚，导致似乎看起来数据更差了……或者中途返回。

```c#
//https://leetcode.com/problems/binary-search/solutions/3363885/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public int Search(int[] nums, int target) {
        int left = 0; // initialize left pointer to 0
        int right = nums.Length - 1; // initialize right pointer to the last index of the array
        while (left <= right) { // continue the loop till left pointer is less than or equal to right pointer
            int mid = left + (right - left) / 2; // calculate the middle index of the array
            
            if (nums[mid] == target) { // check if the middle element is equal to target
                return mid; // return the middle index
            } else if (nums[mid] < target) { // check if the middle element is less than target
                left = mid + 1; // move the left pointer to the right of middle element
            } else { // if the middle element is greater than target
                right = mid - 1; // move the right pointer to the left of middle element
            }
        }
        return -1; // target not found in the array
    }
}
```

```
Runtime
115 ms
Beats
88.63%
Memory
50.6 MB
Beats
93.52%
```