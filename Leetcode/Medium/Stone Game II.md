# Stone Game II

[题目](https://leetcode.com/problems/stone-game-ii/description/)

又是这类答案相对好理解但是自己就是想不出来类型的题。话说类似的题我感觉已经见过好多遍了，现在还是毫无思路。只能说我真的摆到极限了。

```c#
//https://leetcode.com/problems/stone-game-ii/solutions/345230/java-python-dp-solution/
public class Solution {
    public int StoneGameII(int[] piles) {
    if (piles == null || piles.Length == 0) return 0;
    
    // cache[i][j] is the max number of stones a player can get when the first pile is piles[i] and M == j.
    int[,] cache = new int[piles.Length,piles.Length]; 
    
    int[] suffixSum = new int[piles.Length];    // suffixSum[i] starting from i sum up everything to the right: sum(piles[i, piles.Length - 1])
    suffixSum[suffixSum.Length - 1] = piles[piles.Length - 1];  
    for (int i = piles.Length - 2; i >= 0; --i) suffixSum[i] = piles[i] + suffixSum[i + 1];
    
    return helper(piles, suffixSum, cache, 0, 1);
}
    // dfs with memoization
    private int helper(int[] piles, int[] suffixSum, int[,] cache, int firstPile, int M) {
        if (firstPile == piles.Length) return 0;    // no more piles left 
        // Number of remaining piles is <= than the number of piles we can take in the current turn 2*M. We just take all remaining piles.
        if (piles.Length - firstPile <= 2 * M) return suffixSum[firstPile];
        if (cache[firstPile,M] != 0) return cache[firstPile,M];
        
        int result = 0;
        // Try out all possible next moves, store the max amount of stones we can get
        for (int x = 1; x <= 2 * M; ++x) {
            // suffixSum[firstPile] is the total number of stones left in the game, it's the maximum possible gain.
            // helper(...) is the max amount of stones the next player can get if we make the current move x.
            // We want to make the move that minimizes the final gain of the next player, this move maximizes our own final gain.
            result = Math.Max(result, suffixSum[firstPile] - helper(piles, suffixSum, cache, firstPile + x, Math.Max(M, x)));
        }
        
        cache[firstPile,M] = result;
        return result;
    }
}
```
```
Runtime
74 ms
Beats
100%
Memory
39.3 MB
Beats
87.50%
```