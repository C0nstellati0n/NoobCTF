# [Majority Element II](https://leetcode.com/problems/majority-element-ii)

你说得对，但是我用trivial解法
```c#
public class Solution {
    public IList<int> MajorityElement(int[] nums) {
        Dictionary<int,int> freq=new();
        List<int> ans=new();
        int n=nums.Length;
        foreach(int num in nums){
            if(!freq.ContainsKey(num)){
                freq[num]=0;
            }
            freq[num]++;
            if(freq[num]>n/3&&!ans.Contains(num)){
                ans.Add(num);
                if(ans.Count>=2){ //数组里出现次数大于n/3的数字最多有两个
                    break;
                }
            }
        }
        return ans;
    }
}
```
```
Runtime
133 ms
Beats
89.74%
Memory
46.3 MB
Beats
67.95%
```
O(1)解法是之前没见过的全新算法——[Boyer-Moore Majority Vote algorithm](https://zh.wikipedia.org/wiki/%E5%A4%9A%E6%95%B0%E6%8A%95%E7%A5%A8%E7%AE%97%E6%B3%95)
```c#
//https://leetcode.com/problems/majority-element-ii/solutions/63520/boyer-moore-majority-vote-algorithm-and-my-elaboration
public class Solution {
    public IList<int> MajorityElement(int[] nums) {
        int count1=0;
        int count2=0;
        int candidate1=0; //nums里随机的元素即可
        int candidate2=1;
        List<int> ans=new();
        foreach(int n in nums){
            if(n == candidate1){
                count1++;
            }
            else if(n == candidate2){
                count2++;
            }
            else if(count1 == 0){
                candidate1=n;
                count1=1;
            }
            else if(count2 == 0){
                candidate2=n;
                count2=1;
            }
            else{
                count1=count1-1;
                count2=count2-1;
            }
        }
        count1=count2=0;
        foreach(int n in nums){
            if(n==candidate1){
                count1++;
            }
            else if(n==candidate2){
                count2++;
            }
        }
        if(count1>nums.Length/3){
            ans.Add(candidate1);
        }
        if(count2>nums.Length/3){
            ans.Add(candidate2);
        }
        return ans;
    }
}
```
```
Runtime
130 ms
Beats
94.44%
Memory
46.4 MB
Beats
52.56%
```
这个算法从“抵消”而不是“计数”入手。原算法只找一个元素，所以只需一个count和candidate。设想一下，若数组里一半以上都是一个元素，称之为1，其余的都是-1。那么数组里全部元素加起来一定是正数。反过来看，若我们将数组里某个元素标为1 ，其余是-1时，结果为正数，则那个被标为1的元素就是要找的目标。这道题是变种版本，要找两个，那就来两个candidate和两个count

若数组里没有这样的元素，这个算法的结果就是随机元素了。所以我们需要最后的foreach循环验证。