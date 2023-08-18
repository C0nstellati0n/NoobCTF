# Maximal Network Rank

[题目](https://leetcode.com/problems/maximal-network-rank/description/)

感觉我这代码写得挺无脑的。
```c#
public class Solution {
    Dictionary<int,List<int>> connections=new();
    public int MaximalNetworkRank(int n, int[][] roads) {
        if(roads.Length==0){
            return 0;
        }
        int[] degrees=new int[n];
        foreach(int[] road in roads){
            degrees[road[0]]++;
            degrees[road[1]]++;
            if(!connections.ContainsKey(road[0])){
                connections[road[0]]=new();
            }
            if(!connections.ContainsKey(road[1])){
                connections[road[1]]=new();
            }
            connections[road[0]].Add(road[1]);
            connections[road[1]].Add(road[0]);
        }
        int ans=0;
        int temp;
        for(int i=0;i<n;i++){
            for(int j=i+1;j<n;j++){
                temp=degrees[i]+degrees[j];
                if(Check(i,j)){
                    temp--;
                }
                ans=Math.Max(temp,ans);
            }
        }
        return ans;
    }
    bool Check(int city1,int city2){
        if(!connections.ContainsKey(city1)){
            return false;
        }
        foreach(int city in connections[city1]){
            if(city==city2){
                return true;
            }
        }
        return false;
    }
}
```
```
Runtime
136 ms
Beats
100%
Memory
55.7 MB
Beats
84.85%
```
很容易看出来这题要求的“两个城市i和j之间的rank”就是i的road数量+j的road数量-i和j的共同道路（只要i和j相连就有这么一条共同的）。[editorial](https://leetcode.com/problems/maximal-network-rank/editorial/)和我思路差不多，不过人家少用个degrees数组（我也不知道为啥我要用，可能贪方便吧，明明一个connections字典够用了）。以及我Check函数也是多余的，都用list了为啥不直接contains呢？只能说我有点憨。

以及一个时间复杂度O(n+roads.Length)的解法： https://leetcode.com/problems/maximal-network-rank/solutions/3924639/100-2-approaches-o-n-r-o-n-2-iterative-pairwise-comparison-direct-connection-check/ 。与其像上面那种解法一样for循环全部可能node，不如在计算degrees后找出degree数量前2的city，然后直接检查两者是否连着就得了。答案一定在这两者之间。