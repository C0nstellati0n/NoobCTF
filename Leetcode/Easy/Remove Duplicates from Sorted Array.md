# Remove Duplicates from Sorted Array

[题目](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

这题看了半天才看懂要求。要去除数组重复的值，返回去重后数组的长度，同时修改参数nums传入的数组。C#其实自带一个数组去重的函数。

```c#
//平时用要加上这句代码，环境里面已经引用了
//using System.Linq;
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        nums=nums.Distinct().ToArray();
        Console.WriteLine(nums[1]);
        return nums.Length;
    }
}
```

参数nums确实被修改了，但是传入的数组没有，导致过不了。看[文档](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/arrays/passing-arrays-as-arguments)不是说数组是引用类型吗，可是我怎么也改不了。加个ref关键字？不行啊，加了后传参也要ref关键字，但是环境可没有。好吧我去看看别人怎么写的。

```c#
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        if(nums.Length == 0)
            return 0;
        int addIndex = 1; //index that unique characters will be inserted at

        for(int i = 0; i < nums.Length - 1; i++) {
            
            if(nums[i] < nums[i + 1]){ //if true, num[i + 1] is a new unique number
              nums[addIndex] = nums[i + 1];
              addIndex++;
            }
        }
        return addIndex;
    }
}
```

```
Runtime
159 ms
Beats
37.99%
Memory
44.8 MB
Beats
92.93%
```

不是为什么又能直接`num[x]=xxx`这样改了？emmm，再试几个用linq的做法，顺便比较下哪种复制数组的方法快。

直接for循环遍历赋值：

```c#
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        int[] temp=nums.Distinct().ToArray();
        for(int i=0;i<temp.Length;i++){
            nums[i]=temp[i];
        }
        return temp.Length;
    }
}
```

```
Runtime
174 ms
Beats
19.92%
Memory
45.6 MB
Beats
84.96%
```

用Array.Copy：

```c#
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        int[] temp=nums.Distinct().ToArray();
        Array.Copy(temp,nums,temp.Length);
        return temp.Length;
    }
}
```

```
Runtime
167 ms
Beats
23.12%
Memory
45.4 MB
Beats
85.64%
```

用CopyTo：

```c#
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        int[] temp=nums.Distinct().ToArray();
        temp.CopyTo(nums,0);
        return temp.Length;
    }
}
```

```
Runtime
165 ms
Beats
25.19%
Memory
45.4 MB
Beats
85.40%
```

C#里面数组定好长度就不能改了，所以不用ref关键字似乎没法在函数里按引用删除值。应该是我没找到引用赋值的正确方法，不然怎么这么慢？