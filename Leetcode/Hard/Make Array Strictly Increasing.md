# Make Array Strictly Increasing

[题目](https://leetcode.com/problems/make-array-strictly-increasing/description/)

关于我抄别人答案抄出TLE结果还要换个答案抄的这回事。
```c#
//https://leetcode.com/problems/make-array-strictly-increasing/solutions/377495/java-dp-solution-a-simple-change-from-longest-increasing-subsequence/
//可以看看评论区第一个人的解释，很详细
class Solution {
    public int MakeArrayIncreasing(int[] arr1, int[] arr2) {
        int n = arr1.Length;
		
        //sort and generate new arr2
        Array.Sort(arr2);
        List<int> list = new();
        for (int i = 0; i < arr2.Length; i++){
            if (i+1 < arr2.Length && arr2[i] == arr2[i+1])
                continue;
            list.Add(arr2[i]);
        }
        int[] newarr2 = new int[list.Count];
        for (int i = 0; i < list.Count; i++)
            newarr2[i] = list[i];
        arr2 = newarr2;
        
		//generate new arr1
        int[] newarr1 = new int[n+2];
        for (int i = 0; i < n; i++)
            newarr1[i+1] = arr1[i];
        newarr1[n+1] = Int32.MaxValue;
        newarr1[0] = Int32.MinValue;
        arr1 = newarr1;
        
		//perform dp based on LIS
        int[] dp = new int[n+2];
        Array.Fill(dp, Int32.MaxValue);
        //dp[i] -> answer to change array 0 to i
        dp[0] = 0;
        for (int i = 1; i < n+2; i++){
            for (int j = 0; j < i; j++){
                if (arr1[j] < arr1[i] && dp[j] != Int32.MaxValue){
                    int change = check(arr1, arr2, j, i);
                    if (change >= 0){
                        dp[i] = Math.Min(dp[i], dp[j] + change);
                    }
                }
            }
        }
        return dp[n+1] == Int32.MaxValue? -1:dp[n+1];
    }
    
    //change number from start+1 to end-1
    private int check(int[] arr1, int[] arr2, int start, int end){
        if (start+1 == end)
            return 0;
        int min = arr1[start];
        int max = arr1[end];
        //如果找到 value，则为指定 array 中的指定 value 的索引；否则为负数。 如果找不到 value 且 value 小于 array 中的一个或多个元素，则返回的负数是大于 value 的第一个元素的索引的按位求补。 如果找不到 value 且 value 大于 array 中的所有元素，则返回的负数是（最后一个元素的索引加 1）的按位求补。 如果使用非排序的 array 调用此方法，返回值则可能不正确并且可能会返回负数，即使 value 存在于 array 中也是如此。
        int idx = Array.BinarySearch(arr2, min); //https://learn.microsoft.com/zh-cn/dotnet/api/system.array.binarysearch?view=net-7.0
        if (idx < 0)
            idx = -idx-1; //所以这里是在逆向binarysearch函数的按位求补：https://blog.csdn.net/qq_37672438/article/details/105411583
        else
            idx = idx+1;
        
        int maxcount = end-start-1; //因为要严格递增，不能有重复的数。start到end区间至少要end-start-1个数
        int endi = idx + maxcount-1; //从idx开始要换数，要换maxcount个数。那么arr2至少要endi这么长
        if (endi < arr2.Length && arr2[endi] < max)
            return maxcount;
        else
            return -1;
    }
}
```
```
Runtime
171 ms
Beats
66.67%
Memory
39.1 MB
Beats
100%
```
最开始想参考这个解的：https://leetcode.com/problems/make-array-strictly-increasing/solutions/3646689/java-c-python-solution-easy-to-understand/ 。但是java的treeset c#里没有，强行用sortedset的结果是higher函数要自己实现。最后是一个采样里最佳的答案，正好有我要找的higher（本体就是binarySearch）,似乎也是类似的思路
```c#
public class Solution {
    private static int Higher(int[] array, int value) {
        if (value == int.MaxValue)
            return -1;
        
        int result = Array.BinarySearch(array, value + 1);
        
        if (result >= 0)
            return result;
        
        result = ~result;
        
        if (result >= array.Length)
            result = -1;
        
        return result;
    }
    
    public int MakeArrayIncreasing(int[] arr1, int[] arr2) {
        arr2 = arr2
            .Distinct()
            .OrderBy(x => x)
            .ToArray();
        
        int p = Math.Min(arr1.Length, arr2.Length);
        
        int[][] dp = Enumerable
            .Range(0, arr1.Length)
            .Select(_ => Enumerable.Repeat(int.MaxValue, p + 1).ToArray())
            .ToArray();
        
        dp[0][0] = arr1[0];
        
        for (int i = 1; i < arr1.Length; ++i)
            if (arr1[i] <= arr1[i - 1])
                break;
            else
                dp[i][0] = arr1[i];
        
        for (int j = 1; j <= p; ++j)
            dp[0][j] = Math.Min(arr1[0], arr2[0]);
        
        for (int i = 1; i < arr1.Length; ++i) {
            for (int j = 1; j <= Math.Min(i + 1, p); ++j) {
                if (arr1[i] > dp[i - 1][j])
                    dp[i][j] = arr1[i];
                
                if (dp[i - 1][j - 1] == int.MaxValue)
                    continue;
                    
                int index = Higher(arr2, dp[i - 1][j - 1]);
                
                if (index >= 0)
                    dp[i][j] = Math.Min(dp[i][j], arr2[index]);
            }
        }
        
        for (int i = 0; i <= p; ++i)
            if (dp[arr1.Length - 1][i] != int.MaxValue)
                return i;
        
        return -1;
    }
}
```
```
Runtime
117 ms
Beats
100%
Memory
59.9 MB
Beats
66.67%
```