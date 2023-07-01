# Fair Distribution of Cookies

[题目](https://leetcode.com/problems/fair-distribution-of-cookies/)

[回溯算法](https://github.com/labuladong/fucking-algorithm/blob/master/%E7%AE%97%E6%B3%95%E6%80%9D%E7%BB%B4%E7%B3%BB%E5%88%97/%E5%9B%9E%E6%BA%AF%E7%AE%97%E6%B3%95%E8%AF%A6%E8%A7%A3%E4%BF%AE%E8%AE%A2%E7%89%88.md)（backtrack）。似乎曾在某道CTF题靠自己莫名其妙解出过类似思想的题，然而这题比我之前做的复杂，不会了。

回溯最佳表现还要看采样区，官方的editorial还差了一大截。
```c#
//解释参考 https://leetcode.com/problems/fair-distribution-of-cookies/solutions/3702398/back-track-c-java-beginner-friendly/
public class Solution {
    int answer = Int32.MaxValue;

    public int DistributeCookies(int[] cookies, int k) {
        int[] distribution = new int[k];
        Backtrack(distribution, cookies, k, 0);
        return answer;
    }

    private int Backtrack(int[] distribution, int[] cookies, int k, int cookieIndex)
    {
        if(cookieIndex == cookies.Length)
        {
            int unfairness = Int32.MinValue;
            foreach(var val in distribution)
            {
                unfairness = Math.Max(unfairness, val);
            }
            return unfairness;
        }
        
        // try to distribute cookies to every child
        for(int i = 0; i < k; i++)
        {           
            // there not enough cookies left for the remaining kids
            if((k - i - 1) > (cookies.Length - cookieIndex - 1))
            {
                continue;
            }
            distribution[i] += cookies[cookieIndex];
            answer = Math.Min(answer, Backtrack(distribution, cookies, k, cookieIndex + 1));
            distribution[i] -= cookies[cookieIndex];     
        }
        return answer;        
    }
}
```
```
Runtime
81 ms
Beats
90%
Memory
38.2 MB
Beats
85%
```
我可以说每步都看得懂，但是你要让我说这代码是怎么运行的，为什么可以，那不行，我不会。回溯算法其实就是爆破，爆破所有的可能性找到符合题目要求的那个。因此这类题看constraint会发现数量不大，毕竟时间复杂度可是按指数级增长的。

这个循环套递归有点像dfs，但是所谓的“选择”和“撤销选择”直接给我cpu干烧了。我靠脑子完全模拟不出来运行过程。不过这类题是有模板的，递归+for循环+一加一减是标配。

既然是爆破组合，也可以用bitmask表示。
```c#
//https://leetcode.com/problems/fair-distribution-of-cookies/solutions/2141573/dp-submask-enumeration-most-optimal-solution-100-faster-c/
class Solution {
    public int DistributeCookies(int[] cookies, int k) {
        int n = cookies.Length;
        int[][] dp=new int[k+1][];
        for(int i=0;i<k+1;i++){
            int[] temp=new int[1<<n];
            Array.Fill(temp,Int32.MaxValue);
            dp[i]=temp;
        }
        
        int[] sum=new int[1 << n];
        for(int mask = 0;mask<(1 << n); mask++){
            int total = 0;
            for(int i = 0;i<n;i++){
                if((mask & (1 << i))!=0){
                    total += cookies[i];
                }
            }
            sum[mask] = total;
        }

        dp[0][0] = 0;
        for(int person = 1;person<=k;person++){
            for(int mask = 0;mask<(1 << n);mask++){
                for(int submask=mask;submask!=0;submask=(submask - 1)&mask){
                    dp[person][mask] = Math.Min(dp[person][mask], Math.Max(sum[submask], dp[person - 1][mask ^ submask]));
                }
            }
        }

        return dp[k][(1 << n) - 1];
    }
}
```
```
Runtime
73 ms
Beats
100%
Memory
38.6 MB
Beats
15%
```