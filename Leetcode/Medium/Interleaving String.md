# Interleaving String

[题目](https://leetcode.com/problems/interleaving-string/description/)

没有直接抄，偷偷瞄了一眼而已。
```c#
//https://leetcode.com/problems/interleaving-string/solutions/31879/my-dp-solution-in-c/
public class Solution {
    public bool IsInterleave(string s1, string s2, string s3) {
        if(s1.Length+s2.Length!=s3.Length){ //s3由s1和s2的众多子字符串组成，所以s3的长度一定等于s1+s2
            return false;
        }
        //原作者认为dp[i,j] represents if s3 is interleaving at (i+j)th position when s1 is at ith position, and s2 is at jth position. 0th position means empty string.
        bool[,] dp=new bool[s1.Length+1,s2.Length+1]; //dp[i,j]个人认为表示“截取s1长度为i的子字符串和s2长度为j的子字符串时是否可组成长度为i+j的s3“。和链接里原作者的解析不一样。我下面慢慢说
        for(int i=0;i<s1.Length+1;i++){
            for(int j=0;j<s2.Length+1;j++){
                if(i==0&&j==0){ //假如i和j表示s1和s2的索引的话，那这里（base case）为何一定是true？只有当s1和s2长度均为0时，根据题目描述，默认为true
                    dp[i,j]=true;
                }
                else if(i==0){ //只取s2的子字符串
                    dp[i,j]=dp[i,j-1]&&s2[j-1]==s3[i+j-1]; //因为j表示s2截取的长度，所以这里比对s2[j-1]==s3[i+j-1]。因为末尾索引=长度-1（目前s3组成的长度是i+j）。然后还要要求之前的可组成(dp[i,j-1])
                }
                else if(j==0){ //类似上面
                    dp[i,j]=dp[i-1,j]&&s1[i-1]==s3[i+j-1];
                }
                else{ //当i和j都不等于0时，s2和s1的子字符串都能取。那就选择其中一个，有一个是true即可
                    dp[i,j]=(dp[i-1,j]&&s1[i-1]==s3[i+j-1])||(dp[i,j-1]&&s2[j-1]==s3[i+j-1]);
                }
            }
        }
        return dp[s1.Length,s2.Length];
    }
}
```
```
Runtime
60 ms
Beats
97.55%
Memory
38.2 MB
Beats
86.27%
```
描述里提到的O(n)空间解法： https://leetcode.com/problems/interleaving-string/solutions/1247494/python-3-from-top-down-to-bottom-up-2d-to-1d-space/