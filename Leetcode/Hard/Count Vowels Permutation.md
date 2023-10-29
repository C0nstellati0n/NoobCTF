# [Count Vowels Permutation](https://leetcode.com/problems/count-vowels-permutation)

好！这回自己写出for循环嵌套+dp equation！但是dp[i,j]的关系还是从hint拿的，而且这题的dp equation直接写题目脸上了。也算进步吧，但不多
```c#
public class Solution {
    public int CountVowelPermutation(int n) {
        //dp[i][j] be the number of strings of length i that ends with the j-th vowel
        long[,] dp=new long[n+1,5]; //干脆以后dp和ans无脑用long得了，再次被整数溢出摆了一道wrong answer
        int mod=(int)(1e9+7);
        for(int j=0;j<5;j++){
            dp[1,j]=1;
        }
        for(int i=2;i<n+1;i++){
            for(int j=0;j<5;j++){
                switch(j){
                    case 0:
                        dp[i,j]=(dp[i-1,1]+dp[i-1,4]+dp[i-1,2])%mod;
                        break;
                    case 1:
                        dp[i,j]=(dp[i-1,0]+dp[i-1,2])%mod;
                        break;
                    case 2:
                        dp[i,j]=(dp[i-1,1]+dp[i-1,3])%mod;
                        break;
                    case 3:
                        dp[i,j]=dp[i-1,2]%mod;
                        break;
                    case 4:
                        dp[i,j]=(dp[i-1,2]+dp[i-1,3])%mod;
                        break;  
                }
            }
        }
        long ans=0;
        for(int j=0;j<5;j++){
            ans=(ans+dp[n,j])%mod;
        }
        return (int)ans;
    }
}
```
然后我发现我这个j的for循环和switch case完全多此一举。参考 https://leetcode.com/problems/count-vowels-permutation/solutions/398222/detailed-explanation-using-graphs-with-pictures-o-n ，直接一个i的for循环然后手动0，1，2，3，4不就得了吗？我在干什么？

以及采样区的空间优化版本：
```c#
//类似 https://leetcode.com/problems/count-vowels-permutation/solutions/398286/simple-python-with-diagram
public class Solution {
    private static ulong _mod = 1000000007;
    public int CountVowelPermutation(int n) {
        ulong a = 1, e = 1, i = 1, o = 1, u = 1;
        for (int iter = 1; iter < n; iter++) {
            ulong nextA = e + i + u, nextE = a + i, nextI = e + o, nextO = i, nextU = i + o;
            a = nextA % _mod;
            e = nextE % _mod;
            i = nextI % _mod;
            o = nextO % _mod;
            u = nextU % _mod;
        }
        return (int)((a + e + i + o + u) % _mod);
    }
}
```