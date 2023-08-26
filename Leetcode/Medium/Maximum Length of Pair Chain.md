# Maximum Length of Pair Chain

[题目](https://leetcode.com/problems/maximum-length-of-pair-chain/description/)

完全和[Non-overlapping Intervals](./Non-overlapping%20Intervals.md)思路一样，甚至更简单了。
```c#
public class Solution {
    public int FindLongestChain(int[][] pairs) {
        Array.Sort(pairs,(a,b)=>a[1]-b[1]);
        int last=pairs[0][1];
        int ans=1;
        for(int i=1;i<pairs.Length;i++){
            if(pairs[i][0]>last){
                ans++;
                last=pairs[i][1];
            }
        }
        return ans;
    }
}
```
```
Runtime
110 ms
Beats
100%
Memory
48.9 MB
Beats
78.79%
```
[editorial](https://leetcode.com/problems/maximum-length-of-pair-chain/editorial/)除了这种贪心还有两种dp，但是表现上都不如贪心。为什么能用贪心的证明： https://leetcode.com/problems/maximum-length-of-pair-chain/solutions/225801/proof-of-the-greedy-solution/