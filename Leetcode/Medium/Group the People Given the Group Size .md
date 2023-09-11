# Group the People Given the Group Size They Belong To

[题目](https://leetcode.com/problems/group-the-people-given-the-group-size-they-belong-to)

这要不是easy怎么对得起那些给我极大震撼的easy题？
```c#
public class Solution {
    public IList<IList<int>> GroupThePeople(int[] groupSizes) {
        List<IList<int>> ans=new();
        Dictionary<int,List<int>> buckets=new();
        for(int i=0;i<groupSizes.Length;i++){
            if(!buckets.ContainsKey(groupSizes[i])){
                buckets[groupSizes[i]]=new();
            }
            buckets[groupSizes[i]].Add(i);
        }
        List<int> group=new();
        foreach(var kv in buckets){
            foreach(int person in kv.Value){
                group.Add(person);
                if(group.Count==kv.Key){
                    ans.Add(group);
                    group=new();
                }
            }
        }
        return ans;
    }
}
```
```
Runtime
120 ms
Beats
98.55%
Memory
48.7 MB
Beats
26.9%
```
和[editorial](https://leetcode.com/problems/group-the-people-given-the-group-size-they-belong-to/editorial)差不多了，只是我没有在for循环里就添加答案，是在for循环结束后再另开个遍历统一填充答案。我这种直觉上感觉比editorial慢？