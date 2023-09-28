# Decoded String at Index

[题目](https://leetcode.com/problems/decoded-string-at-index)

我的脑子只有在看过答案后才会开始思考，还想不出来。
```c#
//https://leetcode.com/problems/decoded-string-at-index/solutions/156747/java-c-python-o-n-time-o-1-space
//https://leetcode.com/problems/decoded-string-at-index/solutions/4094710/100-reverse-stack-commented-code 有更详细的解释
public class Solution {
    public string DecodeAtIndex(string S, int K) {
        int i;
        long N = 0;
        for (i = 0; N < K; i++) {
            N = Char.IsDigit(S[i]) ? N * (S[i] - '0') : N + 1; //这个for循环是为了计算解码后字符串的长度（只用计算到K，超过了也没用）
        }
        for (i--; i > 0; i--) { //初始化语句是i--可能是为了抵消刚才for循环最后的i++。倒序遍历
            if (Char.IsDigit(S[i])) {
                N /= S[i] - '0'; //这段有点数学。假设我们有leetleetleet，很明显是leet*3，N为12.假设K=10，根据模的概念，我们可以将其转换为更小但是等价的值。N/=3=4,K%=4==2。K=2等同于K=10的情况，都是e。
                K %= (int)N;
            }
            else {
                if (K % N == 0) { //我不理解的地方，似乎当K%N==0时，此时的i对应的字符就是结果了
                    break;
                }
                N--;
            }
        }
        return S[i].ToString();
    }
}
```
```
Runtime
62 ms
Beats
100%
Memory
36.7 MB
Beats
94.44%
```
根据题目描述，最后要求输出的结果肯定在最开始给的字符串里。所以只要我们能找到一种将K转换为更小的等价值的方法，就能在不存储解码字符串的情况下，从参数字符串里直接取出答案。为什么这题不是hard，我觉得这种“智商题”比纯粹算法题难多了