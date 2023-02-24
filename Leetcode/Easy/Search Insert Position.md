# Search Insert Position

[题目](https://leetcode.com/problems/search-insert-position/description/)

要求在升序数组nums中搜寻target，找得到就返回target的索引，找不到就返回应该被插入的索引。nums已排序这点很重要，我们可以遍历nums，如果nums[i]==target就返回i；同时如果nums[i]>target也返回i，毕竟升序排列，接下来不可能有位置给target插入了。

```c#
public class Solution {
    public int SearchInsert(int[] nums, int target) {
        for(int i=0;i<nums.Length;i++){
            if(nums[i]==target || nums[i]>target){
                return i;
            }
        }
        return nums.Length;
    }
}
```

```
Runtime
86 ms
Beats
80.26%
Memory
39.3 MB
Beats
36.90%
```

这样还不快，因为排序数组很明显是可以用binary search的，看看用了之后和正常做有什么区别？

```c#
public class Solution {
    public int SearchInsert(int[] nums, int target) {
        int low=0;
        int high=nums.Length;
        int mid;
        if(target>nums[high-1]){
            return high;
        }
        while(low<=high){
            mid=(low+high)/2;
            if(nums[mid]==target){  //if found return its position
                return mid;
            }
          
            if(target<nums[mid]){     
                high=mid-1;    
            }
            else{
                low=mid+1;        
            }
        }
         return  low;   //if not found return the location where it should be
    }
}
```

```
Runtime
98 ms
Beats
24.23%
Memory
37.9 MB
Beats
91.70%
```

这么慢？我不信邪，同样的代码提交了第二次。结果不一样了。

```
Runtime
89 ms
Beats
67.49%
Memory
38.8 MB
Beats
86.99%
```

感觉leetcode应该固定测试用例，这太不对劲了。又找了另一个实现方法。

```c#
public class Solution {
    public int SearchInsert(int[] nums, int target) {
        int start = 0;
        int end = nums.Length - 1;

        while (start <= end) {
            int mid = start + (end-start)/2; //等同于(end+start)/2,但是更加安全，对于较大的start和end值也不会报错
            if (nums[mid] == target) return mid;
            else if (nums[mid] > target) end = mid-1;
            else start = mid + 1;
        }

        return start;
    }
}
```

运行结果选了个比较好的：

```
Runtime
86 ms
Beats
80.54%
Memory
39.2 MB
Beats
66.92%
```

最后去看了java，c++等语言的相同解法实现，发现运行时间7ms都只能打败35.15%……有点恐怖。