# Buddy Strings

[题目](https://leetcode.com/problems/buddy-strings/description/)

感觉我的代码总是有一种明明什么也不会但是硬要写的美感。
```c#
public class Solution {
    public bool BuddyStrings(string s, string goal) {
        if(s.Length!=goal.Length){
            return false;
        }
        int numDifferent=0;
        Dictionary<char,char> different=new();
        int[] same=new int[26];
        for(int i=0;i<s.Length;i++){
            if(s[i]!=goal[i]){
                numDifferent++;
                different[s[i]]=goal[i];
            }
            if(s[i]==goal[i]){
                same[s[i]-'a']++;
            }
            if(numDifferent>2){
                return false;
            }
        }
        if(numDifferent==1){
            return false;
        }
        if(numDifferent==2){
            foreach(var kv in different){
                if(!different.ContainsKey(kv.Value)){
                    return false;
                }
                return kv.Key==different[kv.Value];
            }
        }
        if(numDifferent==0){
            foreach(int val in same){
                if(val>=2){
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
73 ms
Beats
87.50%
Memory
39.2 MB
Beats
52.78%
```
其他大佬的解要么用数组，要么用hashset，只有我：哈哈，我全都要！关键我脑回路还是反的，我的数组用来记录一样的，[官方](https://leetcode.com/problems/buddy-strings/editorial/)用来记录不一样的；我的字典用来记录不一样的，别人的hashset用来记录一样的……
```c#
//采样区最佳，相同思路： https://leetcode.com/problems/buddy-strings/solutions/141780/easy-understood/
public class Solution {
    public bool BuddyStrings(string A, string B)
    {
        if (A.Length != B.Length || A.Length < 2)
            return false;

        if (A.Equals(B))
        {
            HashSet<char> uniqueChars = new HashSet<char>(A);

            return uniqueChars.Count < A.Length;
        }
        else
``
        {
            List<int> diffs = new List<int>();

            for (int i = 0; i < A.Length; i++)
            {
                if (A[i] != B[i])
                    diffs.Add(i);

                if (diffs.Count > 2)
                    return false;
            }

            return diffs.Count == 2 && A[diffs[0]] == B[diffs[1]] && A[diffs[1]] == B[diffs[0]];
        }
    }
}
```
```
Runtime
69 ms
Beats
97.22%
Memory
39.6 MB
Beats
15.28%
```