# Find the Difference of Two Arrays

[题目](https://leetcode.com/problems/find-the-difference-of-two-arrays/description/)

连续三天都是easy，感觉自己又行了。

```c#
public class Solution {
    public IList<IList<int>> FindDifference(int[] nums1, int[] nums2) {
        //这块的初始化参考 https://stackoverflow.com/questions/48574660/unable-to-convert-listlistint-to-return-type-ilistilistint
        List<IList<int>> res=new List<IList<int>>();
        IList<int> res1=new List<int>();
        IList<int> res2=new List<int>();
        foreach(int num in nums1){
            if(!nums2.Contains(num)&&!res1.Contains(num)){
                res1.Add(num);
            }
        }
        foreach(int num in nums2){
            if(!nums1.Contains(num)&&!res2.Contains(num)){
                res2.Add(num);
            }
        }
        res.Add(res1);
        res.Add(res2);
        return res;
    }
}
```

```
Runtime
193 ms
Beats
27.50%
Memory
54.7 MB
Beats
97.50%
```

这题真正的知识点：set。这是一个不包含重复元素的集合。

```c#
//https://leetcode.com/problems/find-the-difference-of-two-arrays/solutions/3480249/easy-solution-c-explained-using-sets/
public class Solution {
    public IList<IList<int>> FindDifference(int[] nums1, int[] nums2) {
        HashSet<int> set1=new(nums1);
        HashSet<int> set2=new(nums2);
        
        IList<int> distinct_nums1=new List<int>();
        IList<int> distinct_nums2=new List<int>();
        foreach(int num in set1) {
            if (!set2.Contains(num)) {
                distinct_nums1.Add(num);
            }
        }

        foreach(int num in set2) {
            if (!set1.Contains(num)) {
                distinct_nums2.Add(num);
            }
        }

        return new List<IList<int>> {distinct_nums1, distinct_nums2};
    }
}
```

```
Runtime
158 ms
Beats
98.75%
Memory
56.4 MB
Beats
81.25%
```