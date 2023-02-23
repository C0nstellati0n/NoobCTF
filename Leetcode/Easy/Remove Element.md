# Remove Element

[题目](https://leetcode.com/problems/remove-element/)

给定一个数组nums和一个值val，要求移除数组中所有等同于val的元素。不过这所谓的移除只是把val元素移到全部元素后面，再返回移除后的数组长度。不好描述，直接看代码。

```c#
public class Solution {
    public int RemoveElement(int[] nums, int val) {
        int index=0;
        for(int i=0;i<nums.Length;i++){
            if(nums[i]!=val){
                nums[index]=nums[i];
                index++;
            }
        }
        return index;
    }
}
```

```
Runtime
133 ms
Beats
90.6%
Memory
41.4 MB
Beats
88.98%
```

后来我试了index自增的写法，没想到速度瞬间就下来了。

```c#
public class Solution {
    public int RemoveElement(int[] nums, int val) {
        int index=0;
        for(int i=0;i<nums.Length;i++){
            if(nums[i]!=val){
                nums[index++]=nums[i];
            }
        }
        return index;
    }
}
```

```
Runtime
148 ms
Beats
39.68%
Memory
41.4 MB
Beats
87.1%
```

看来大家的解法，跟我这个差不多啊，难得有一次我赶上大家的思路。