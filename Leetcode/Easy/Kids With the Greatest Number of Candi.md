# Kids With the Greatest Number of Candies

[题目](https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/description/)

这题也太简单了，和昨天巨难的题形成强烈反差。

```c#
public class Solution {
    public IList<bool> KidsWithCandies(int[] candies, int extraCandies) {
        List<bool> ans=new();
        int largest=candies.Max();
        foreach(int candy in candies){
            if(candy+extraCandies>=largest){
                ans.Add(true);
            }
            else{
                ans.Add(false);
            }
        }
        return ans;
    }
}
```

```
untime
146 ms
Beats
85.11%
Memory
44.3 MB
Beats
79.61%
```

不过在处理bool值时，无需if语句。

```c#
//https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/solutions/3425038/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public List<bool> KidsWithCandies(int[] candies, int extraCandies) {
        int maxCandies = candies.Max();
        List<bool> result = new();
        foreach(int candy in candies) {
            result.Add(candy + extraCandies >= maxCandies);
        }
        return result;
    }
}
```

```
Runtime
138 ms
Beats
95.15%
Memory
44.5 MB
Beats
67.31%
```