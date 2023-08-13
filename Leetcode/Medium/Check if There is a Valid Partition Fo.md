# Check if There is a Valid Partition For The Array

[题目](https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/description/)

我真的只是偷瞄了亿眼editorial，并没有直接复制粘贴。
```c#
public class Solution {
    Dictionary<int,bool> dp=new();
    public bool ValidPartition(int[] nums) {
        return Check(nums,nums.Length-1);
    }
    bool Check(int[] nums,int i){
        if(i<0){
            return true;
        }
        if(i<1){
            return false;
        }
        if(dp.ContainsKey(i)){
            return dp[i];
        }
        bool res=false;
        if(i>=2&&nums[i]==nums[i-1]&&nums[i-1]==nums[i-2]){
            res|=Check(nums,i-3);
        }
        if(i>=1&&nums[i]==nums[i-1]){
            res|=Check(nums,i-2);
        }
        if(i>=2&&nums[i]==nums[i-1]+1&&nums[i-1]==nums[i-2]+1){
            res|=Check(nums,i-3);
        }
        dp[i]=res;
        return res;
    }
}
```
```
Runtime
248 ms
Beats
100%
Memory
59.8 MB
Beats
66.67%
```
[editorial](https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/editorial/)还有dp（内存优化）写法。说实话这题不算太难，直觉就够用了。这题的subproblem很简单，当你发现一个valid partition后，把剩下的数组从那里切开，剩下的数组继续检查是否有valid partition，然后再切。重复此步骤，总有一天会到头的。这题3种valid partition其实是个烟雾弹，可能会迷惑人，让人不知道如何选择partition来继续。事实上解法压根就不考虑这个，三种都试一下即可。