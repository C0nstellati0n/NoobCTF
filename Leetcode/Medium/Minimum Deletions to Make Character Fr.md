# Minimum Deletions to Make Character Frequencies Unique

[题目](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique)

偏简单的medium。注意value到0就结束循环即可。
```c#
public class Solution {
    public int MinDeletions(string s) {
        Dictionary<char,int> freq=new();
        List<int> unique=new();
        foreach(char c in s){
            if(!freq.ContainsKey(c)){
                freq[c]=0;
            }
            freq[c]++;
        }
        var freqList=freq.ToList();
        freqList.Sort((pair1,pair2) => pair1.Value.CompareTo(pair2.Value));
        int ans=0;
        foreach(var kv in freqList){
            int value=kv.Value;
            while(unique.Contains(value)){
                value--;
                ans++;
                if(value<=0){
                    break;
                }
            }
            unique.Add(value);
        }
        return ans;
    }
}
```
```
Runtime
100 ms
Beats
36.23%
Memory
43 MB
Beats
24.64%
```
所以为什么表现还是这么垃圾呢？freq字典用于记录每个字符的出现频率，但是字符是什么重要吗？加上constraint里仅包含小写字母的提示，直接用列表即可。以及unique list都说了是unique了，为啥不用set？排序是因为看了hint，事实上也不需要。
```c#
//采样区
public class Solution {
    public int MinDeletions(string s) {
        var count = new int[26];
        foreach (var c in s)
            count[c - 'a']++;
        var set = new HashSet<int>();
        var result = 0;
        foreach (var cnt in count)
        {
            var c = cnt;
            while (c > 0 && !set.Add(c))
            {
                c--;
                result++;
            }
        }
        return result;
    }
}
```
```
Runtime
50 ms
Beats
100%
Memory
42.9 MB
Beats
53.62%
```