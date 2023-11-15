# [Unique Length-3 Palindromic Subsequences](https://leetcode.com/problems/unique-length-3-palindromic-subsequences)

两个TLE后认清现实
```c++
//https://leetcode.com/problems/unique-length-3-palindromic-subsequences/solutions/1330165/leftmost-rightmost-and-in-between
//和 https://leetcode.com/problems/unique-length-3-palindromic-subsequences/editorial 第二种一样思路，但是表现稍微好一点
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        int first[26] = {[0 ... 25] = INT_MAX}, last[26] = {}, res = 0;
        for (int i = 0; i < s.size(); ++i) { //计算每个字符第一次和最后一次出现的索引
            first[s[i] - 'a'] = min(first[s[i] - 'a'], i);
            last[s[i] - 'a'] = i;
        }
        for (int i = 0; i < 26; ++i) //代表a到z
            if (first[i] < last[i]) //大于则是当前字符不存在，跳过
                res += unordered_set<char>(begin(s) + first[i] + 1, begin(s) + last[i]).size(); //长度为三的回文字符串其实就是头尾字符相等，中间随便组合。题目要求是unique，所以用unordered_set算那些独特的字符数量
        return res;
    }
};
```
要炸裂还得看采样区。上面解法230ms起步，采样区直接干到23ms
```c++
class Solution {
public:
    int countPalindromicSubsequence(string s) {
        int start[26], end[26];
        memset(start, -1, sizeof(start));
        memset(end, -1, sizeof(end));
        for (int i = 0; i < s.size(); i ++) {
            if (start[s[i] - 'a'] == -1) start[s[i] - 'a'] = i;
            else end[s[i] - 'a'] = i;
        }
        int count = 0;
        for (int i = 0; i < 26; i ++) {
            if (end[i] != -1 && start[i] != -1) {
                bool found[26] = {false};
                int tmp = 0;
                for (int j = start[i] + 1; j < end[i]; j ++) {
                    if (!found[s[j] - 'a']) tmp ++, found[s[j] - 'a'] = 1;
                    if(tmp == 26) break; //26是最大可能的字符数
                }
                count += tmp;
            }
        }
        return count;
    }
};
```
其实思路也差不多，但是一个found数组比unordered_set优化了很多