# 132 Pattern

[题目](https://leetcode.com/problems/132-pattern)

指数级时间复杂的倒是挺容易写，但是我看了discussion有人说用stack，尝试直接冲。啊他们的提示确实没错，确实难。
```c#
//https://leetcode.com/problems/132-pattern/editorial 第四种解法，前三种都不难理解而且时间复杂度高，可以跳过
//第四种解法的解释有点长，建议直接看文字过后的图解
public class Solution {
    public bool Find132pattern(int[] nums) {
        if (nums.Length < 3)
            return false;
        Stack<int> stack = new();
        int[] min = new int[nums.Length];
        min[0] = nums[0];
        for (int i = 1; i < nums.Length; i++)
            min[i] = Math.Min(min[i - 1], nums[i]); //min[i]代表题目描述里的nums[i]。i和j之间数值（不是index）的差距越大，k的选择就越多。所以直接取min即可
        for (int j = nums.Length - 1; j >= 0; j--) {
            if (nums[j] > min[j]) { //nums[j]代表j
                while (stack.Any() && stack.Peek() <= min[j]) //stack里的数字代表可能的k。k是第二大的，若小于min[j](i)，应该pop跳过
                    stack.Pop();
                if (stack.Any() && stack.Peek() < nums[j]) //若stack存在一个小于nums[j]的数字，由于之前已经剔除过小于min[j]的数字，这个就是要找的132序列
                    return true;
                stack.Push(nums[j]); //nums[j] push进stack就变成了可能的k
            }
        }
        return false;
    }
}
```
```
Runtime
137 ms
Beats
94.74%
Memory
58.7 MB
Beats
10.53%
```
采样区有个优化版本。
```c#
public class Solution
{
    public bool Find132pattern(int[] nums)
    {
        var s = new Stack<int>();
        var max2 = int.MinValue;
        for(var i=nums.Length-1; i>=0; i--)
        {
            if(nums[i] < max2) //max2根据下面，从stack里pop出来的，所以它肯定在当前nums[i]后面，这里相当于确定了i和k
                return true;
            while(s.Count > 0 && nums[i] > s.Peek()) //max2代表k，因为只有在nums[i] > s.Peek()时才会pop出max2.nums[i]为j，一定在k前面
                max2 = s.Pop();
            if(s.Count == 0 || s.Peek() != nums[i])
                s.Push(nums[i]);
        }
        return false;
    }
}
```
```
Runtime
132 ms
Beats
98.68%
Memory
56.5 MB
Beats
82.89%
```