# Longest String Chain

[题目](https://leetcode.com/problems/longest-string-chain)

诚然我确实不会dp。但如果类似的考点我之前做过，阁下又该如何应对？
```c#
public class Solution {
    public int LongestStrChain(string[] words) {
        Array.Sort(words,(x, y) => x.Length-y.Length);
        int n = words.Length;
        int[] lengths = new int[n];
        int maxLength = 0;
        for (int i = 0; i < n; i++)
        {
            lengths[i] = 1;
            for (int j = 0; j < i; j++)
            {
                if (CheckPredecessor(words[i],words[j]))
                {
                    lengths[i]=Math.Max(lengths[j] + 1,lengths[i]); 
                }
            }
            maxLength = Math.Max(maxLength, lengths[i]);
        }
        return maxLength;
    }
    bool CheckPredecessor(string a,string b){
        if(a.Length-b.Length==1){
            for(int i=0;i<a.Length;i++){
                if(a.Remove(i,1)==b){
                    return true;
                }
            }
        }
        return false;
    }
}
```
```
Runtime
159 ms
Beats
7.14%
Memory
120.6 MB
Beats
7.14%
```
类似题目:[Number of Longest Increasing Subsequence](./Number%20of%20Longest%20Increasing%20Subsequen.md).虽然但是，这表现怎么这么差啊？看看其他的写法。
```c#
//https://leetcode.com/problems/longest-string-chain/solutions/294890/java-c-python-dp-solution
public class Solution {
    public int LongestStrChain(string[] words) {
        Dictionary<string, int> dp = new();
        Array.Sort(words, (a, b)=>a.Length - b.Length);
        int res = 0;
        int temp;
        foreach(string word in words) {
            int best = 0;
            for (int i = 0; i < word.Length; ++i) {
                string prev = word.Substring(0,i) + word.Substring(i + 1); //跳过第i个字符，相当于删除第i个字符
                if(dp.ContainsKey(prev)){ //字典里包含删除一个字符后的字符串，说明当前字符串等于上一个字符串+任意一个字符，符合题目要求
                    temp=dp[prev];
                }
                else{
                    temp=0;
                }
                best = Math.Max(best, temp + 1);
            }
            dp[word]=best;
            res = Math.Max(res, best);
        }
        return res;
    }
}
```
```
Runtime
111 ms
Beats
28.57%
Memory
73.7 MB
Beats
17.86%
```
也就好了一点，没有那种爆炸提升。奇怪了，这个解法应该就是理论最优解啊（他们说的），估计是我java改c#给它改慢了
```c#
//采样区
public class Solution {
    public int LongestStrChain(string[] words) {
        int[] dp = new int[words.Length];
        Array.Sort(words, (w1, w2) => w1.Length - w2.Length);
        for(int i=words.Length-1; i>=0; i--){
            dp[i] = 1;
            int nextLen = words[i].Length+1;
            for(int j=i+1; j < words.Length && words[j].Length <= nextLen; j++){ //遍历所有比dp[i]长的字符串，只考虑那些长度小于nextLen的字符串（因为之前排序过了，所以一旦出现一个超过长度的字符串就可以直接break了）
                if(words[i].Length == words[j].Length){ //等于不符合题目“添加一个字符”的定义
                    continue;
                }
                if(IsPredecessor(words[i], words[j])){ //判断是不是添加一个字符
                    dp[i] = Math.Max(dp[i], 1 + dp[j]);
                }
            }
        }
        int res = 0;
        for(int i=0; i<words.Length; i++){
            res = Math.Max(res, dp[i]);
        }
        return res;
    }
    private bool IsPredecessor(string word1, string word2){
        int i=0, j=0, count = 1;
        while(i < word1.Length && j < word2.Length){
            if(word1[i] == word2[j]){
                i++;
                j++;
                continue;
            }
            else if(count == 0){
                return false;
            }
            else{
                count--;
                j++;
            }
        }
        return true;
    }
}
```
```
Runtime
94 ms
Beats
100%
Memory
41.3 MB
Beats
100%
```
这个就是我要找的炸裂最优解了。某种意义上大体思路其实和我的一样？除了IsPredecessor函数，这个解法通过计算不同字符的数量来判断（不同字符数超过1为false）,以及dp遍历的顺序不同（真就“除了不一样的其它都一样”是吧）

道理我都懂，可是为什么采样区这个这么快啊？