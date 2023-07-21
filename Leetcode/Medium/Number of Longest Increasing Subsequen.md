# Number of Longest Increasing Subsequence

[题目](https://leetcode.com/problems/number-of-longest-increasing-subsequence/description/)

我见过那么多Longest xxx Subsequence的题，我相信再给我一个类似的题目我肯定能在10分钟内写（抄）出答案。但是为什么你是number of啊？
```c#
//https://leetcode.com/problems/number-of-longest-increasing-subsequence/editorial/ 的Bottom-up Dynamic Programming解法，采样区的优化写法
//editorial有点长，也可以搭配discussion区oops_moment发表的内容食用，这个比较短
public class Solution {
    public int FindNumberOfLIS(int[] nums) {
        int n = nums.Length;
        int[] lengths = new int[n]; // Length of longest increasing subsequence ending at index i
        int[] counts = new int[n]; // Count of longest increasing subsequences ending at index i
        int maxLength = 0; // Length of longest increasing subsequence
        int result = 0; // Number of longest increasing subsequences

        for (int i = 0; i < n; i++)
        {
            lengths[i] = 1; //无论怎么样，长度最小有1，可以看作是dp的统一初始化
            counts[i] = 1;

            for (int j = 0; j < i; j++)
            {
                if (nums[i] > nums[j]) //只在满足Increasing条件时才更新搭dp
                {
                    //if和else if语句只和counts的更新有关
                    if (lengths[j] + 1 > lengths[i]) //说明我们找到了在i处更长的Increasing Subsequence，一定是第一次（再有下一次就进else if分支了）
                    {
                        lengths[i] = lengths[j] + 1; //Increasing Subsequence更新。i处的数字小于j处的，所以能形成的subsequence为j处的数量lengths[j]+1
                        counts[i] = counts[j]; //那么次数等于j处的。毕竟是第一次形成，无论counts[j]有多少种方式，这里只有某种方式+某个数
                    }
                    else if (lengths[j] + 1 == lengths[i]) //说明我们又找到了i处最大Increasing Subsequence的另一种形成方式
                    {
                        counts[i] += counts[j]; //能形成i处最大Increasing Subsequence的方式已经有counts[i]种，这下我们发现从lengths[j]处加上某个数也能获得i处最大Increasing Subsequence，那么加等于就是全部方式了
                    }
                }
            }

            maxLength = Math.Max(maxLength, lengths[i]);
        }

        for (int i = 0; i < n; i++)
        {
            if (lengths[i] == maxLength)
            {
                result += counts[i];
            }
        }

        return result;
    }
}
```
```
Runtime
92 ms
Beats
88%
Memory
39.6 MB
Beats
100%
```
这个解法的时间复杂度是 $O(n^2)$ .我还发现个用binary search获得O(nlogn)的解法： https://leetcode.com/problems/number-of-longest-increasing-subsequence/solutions/1643753/python-o-nlogn-solution-w-detailed-explanation-of-how-to-develop-a-binary-search-solution-from-300/ 。dp已经够我吃一壶的了，这个就放在这当拓展好了。