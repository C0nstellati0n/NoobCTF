# Find the Difference

[题目](https://leetcode.com/problems/find-the-difference)

好久没有这么纯粹的简单题了。
```c#
public class Solution {
    public char FindTheDifference(string s, string t) {
        int res=0;
        foreach(char c in t){
            res+=c;
        }
        foreach(char c in s){
            res-=c;
        }
        return (char)res;
    }
}
```
```
Runtime
75 ms
Beats
93.62%
Memory
39.4 MB
Beats
75.5%
```
除了这种，还可以：
- 也是累加，但只用一次循环，参考 https://leetcode.com/problems/find-the-difference/solutions/86850/simple-java-8ms-solution-4-lines/?envType=daily-question&envId=2023-09-25
- 还是累加，但是把和放到字符串里。c++的做法，c#好像没法把字符串看作数组 https://leetcode.com/problems/find-the-difference/solutions/1751509/c-time-100-memory-98-6-3-lines-propagate-the-difference-ascii/?envType=daily-question&envId=2023-09-25 。评论区还有个异或解法