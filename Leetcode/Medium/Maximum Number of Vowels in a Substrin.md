# Maximum Number of Vowels in a Substring of Given Length

[题目](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/)

这题和一道叫“sliding window"的题目有关系。好的我没做过。最开始想了一个two pointers的做法，一个i一个j，j领先i k个字符。然后循环时自增再substring判断就行了。不出所料TLE。

```c#
//https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/solutions/3486567/easy-solutions-in-c-python-and-java/
class Solution {
    public bool IsVowel(char c){
        if(c=='a' || c== 'e' || c== 'i' || c== 'o' || c== 'u')
            return true;
        return false;
    }
    public int MaxVowels(string s, int k) {
        int n = s.Length;
        int i=0;
        int count = 0;
        for(;i<k;i++){ // First window of size k
            if(IsVowel(s[i]))
                count++;
        }
        int ans = count;
        for(;i<n;i++){ // Remaining n-k windows
            if(IsVowel(s[i])) // If new character is vowel the increment count
                count++;
            if(IsVowel(s[i-k])) // If previous character is vowel then decrement count
                count--;
            ans = Math.Max(ans,count);
        }
        return ans;
    }
}
```
```
Runtime
68 ms
Beats
98.39%
Memory
41.6 MB
Beats
96.77%
```

然后我发现跟我的思路有点像，不过只有一个指针，也不用截取字符串。我估计是我截取字符串才导致的TLE，或者是因为调用了LINQ的Count。大佬们的解法也是一看就懂。如果i处是元音，count++，简单；不过为什么i-k处是元音就要自减呢？因为i-k是上个substring的范围，上个substring的元音的数量可不能记在当前substring的count里。再给出一种看起来比较简洁的做法。

```c#
//https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/solutions/3486558/c-clean-code-sliding-window-well-explained/
class Solution {
    public int MaxVowels(string s, int k) {
        string vowels = "aeiou";
        int max_count = 0;
        int count = 0;
        for (int i = 0; i < s.Length; i++) {
            if (i >= k && vowels.Contains(s[i-k])) {
                count--;
            }
            if (vowels.Contains(s[i])) {
                count++;
            }
            max_count = Math.Max(max_count, count);
        }
        return max_count;
    }
}
```

```
Runtime
77 ms
Beats
80.65%
Memory
42.2 MB
Beats
43.55%
```