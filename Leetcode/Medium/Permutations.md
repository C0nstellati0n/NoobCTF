# Permutations

[题目](https://leetcode.com/problems/permutations/description/)

某人会用bitmask了！
```c#
public class Solution {
    public IList<IList<int>> Permute(int[] nums) {
        List<IList<int>> ans=new();
        Generate(nums,ans,new List<int>(),0);
        return ans;
    }
    private void Generate(int[] nums, List<IList<int>> ans,List<int> cur,int bitmask) {
        if (cur.Count == nums.Length) {
            ans.Add(new List<int>(cur));
            return;
        }
        for(int j=0;j<nums.Length;j++){
            if(((bitmask>>j)&1)!=1){
                cur.Add(nums[j]);
                Generate(nums,ans,cur,bitmask|(1<<j));
                cur.RemoveAt(cur.Count-1);
            }
        }
    }
}
```
```
Runtime
119 ms
Beats
99.21%
Memory
43.4 MB
Beats
75.79%
```
这题做法差不多就是这样，除了标记nums中的数字是否被用过的方法不同。我用bitmask,[editorial](https://leetcode.com/problems/permutations/editorial/)用contains（靠我竟然忘了还有这东西），采样区/solution用used数组。难得和大家做法差不多啊！