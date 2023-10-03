# Number of Good Pairs

[题目](https://leetcode.com/problems/number-of-good-pairs)

从来没有在每日挑战连续见过这么多easy
```c#
public class Solution {
    public int NumIdenticalPairs(int[] nums) {
        Dictionary<int,int> count=new();
        int res=0;
        foreach(int num in nums){
            if(!count.ContainsKey(num)){
                count[num]=0;
            }
            count[num]++;
        }
        foreach(var c in count){
            res+=c.Value*(c.Value-1)/2;
        }
        return res;
    }
}
```
```
Runtime
66 ms
Beats
97.87%
Memory
38.3 MB
Beats
35.88%
```
还可以继续优化，直接在遍历nums的时候计算combinations。参考[editorial](https://leetcode.com/problems/number-of-good-pairs/editorial)