# Number of Music Playlists

[题目](https://leetcode.com/problems/number-of-music-playlists/description/)

感觉题目的难度不能看代码的多少，要看到底有多难想之间的逻辑关系。比如这题的dp，代码非常简单，但是你让我想一天我都想不出来这题的subproblem两个量都要变，所以需要二维dp。你再让我想一天我也想不出来最后的数学解法。

首先这题不能用类似backtrack的爆破方法组合出所有情况然后剔除不符合题目的组合，因为constraint太大了。好的又是dp。
```c#
//为什么editorial总是先放遍历的再放递归的，明明递归做法通常更符合直觉也更简单
public class Solution {
    public int NumMusicPlaylists(int n, int goal, int k) {
        long[,] dp=new long[goal+1,n+1]; //dp[i,j]表示包含j首不重复歌曲的长度为i的playlist数量。注意这个“不重复歌曲”是关键
        int mod=(int)(1e9+7);
        dp[0,0]=1; //base case。长度为0且包含0首歌的playlist数量，只有一种，就是空playlist
        //隐藏base case：当i小于j时，dp[i,j]=0。不过创建数组默认值就是0，不用特意赋值
        for(int i=1;i<=goal;i++){
            for(int j=1;j<=Math.Min(i,n);j++){
                dp[i,j] = dp[i - 1,j - 1] * (n - j + 1) % mod; //这里表示加入一首新歌，新加入的歌与之前的不重复。既然这样，按照dp的定义，i和j都要加1（于是从-1的地方取上次的值）。目前dp[i-1,j-1]处有j-1首不重复的歌曲，共有n首歌可以选，所以乘上n-(j-1)=n-j+1种选择
                // The i-th song is a song we have played before
                if (j > k) { //当j大于k时，我们可以播放之前放过的一首歌了。因为要放的歌与之前的重复了，所以j不用动，不过i的长度还是会加一。这里能选择播放的歌的数量为j-k，因为每k首歌后才能重复播放
                    dp[i,j] = (dp[i,j] + dp[i - 1,j] * (j - k)) % mod; //dp[i,j]最终数量=能不包含重复歌曲的长度为i的playlist数量+重复后的playlist数量
                }
            }
        }
        return (int)dp[goal,n];
    }
}
```
```
Runtime
19 ms
Beats
96.74%
Memory
28.7 MB
Beats
50%
```
数学解法要用组合学。我没学过，不过editorial也讲得很详细了，这里不再赘述。