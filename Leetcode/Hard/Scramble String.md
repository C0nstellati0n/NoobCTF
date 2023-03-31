# Scramble String

[题目](https://leetcode.com/problems/scramble-string/description/)

抄答案喽，hard题目我基本连题也读不懂。就算后面读懂了也要感叹一句：发明这道题的人你在地球不想家吗？

```c#
//https://leetcode.com/problems/scramble-string/solutions/3357439/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    // for storing already solved problems
    Dictionary<string, bool> mp = new();

    public bool IsScramble(string s1, string s2) {
        int n = s1.Length;
        // if both strings are equal
        if (s1==s2)
            return true;

        // if code is reached to this condition then following this are sure:
        // 1. size of both string is equal
        // 2. string are not equal
        // so size is equal (where size==1) and they are not equal then obviously false
        // example 'a' and 'b' size is equal ,string are not equal
        if (n == 1)
            return false;

        string key = s1 + " " + s2;

        // check if this problem has already been solved
        if (mp.ContainsKey(key))
            return mp[key];

        // for every iteration it can two condition
        // 1.we should proceed without swapping
        // 2.we should swap before looking next
        for (int i = 1; i < n; i++) {
            // ex of without swap: gr|eat and rg|eat
            bool withoutswap = (
                    // left part of first and second string
                    IsScramble(s1.Substring(0, i), s2.Substring(0, i))

                            &&

                            // right part of first and second string;
                            IsScramble(s1.Substring(i), s2.Substring(i))
            );

            // if without swap give us right answer then we do not need
            // to call the recursion withswap
            if (withoutswap) {
                mp.Add(key, true);
                return true;
            }

            // ex of withswap: gr|eat rge|at
            // here we compare "gr" with "at" and "eat" with "rge"
            bool withswap = (
                    // left part of first and right part of second
                    IsScramble(s1.Substring(0, i), s2.Substring(n - i))

                            &&

                            // right part of first and left part of second
                            IsScramble(s1.Substring(i), s2.Substring(0, n - i))
            );

            // if withswap give us right answer then we return true
            // otherwise the for loop do it work
            if (withswap) {
                mp.Add(key, true);
                return true;
            }
            // we are not returning false in else case
            // because we want to check further cases with the for loop
        }
        //不加这句TLE
        mp.Add(key, false);
        return false;
    }
}
```

```
Runtime
116 ms
Beats
33.33%
Memory
56.2 MB
Beats
19.26%
```

或者不递归，用dp+for循环解。

```c#
//https://leetcode.com/problems/scramble-string/solutions/3357574/day-364-100-java-c-python-explained-intution-dry-run-proof/
class Solution {
    public bool IsScramble(string s1, string s2) {
        int n = s1.Length;
        // Initialize a 3D table to store the results of all possible substrings of the two strings
        bool[][][] dp = new bool[n+1][][];
        for(int i=0;i<n+1;i++){
            dp[i]=new bool[n][];
            for(int j=0;j<n;j++){
                dp[i][j]=new bool[n];
            }
        }
        // Initialize the table for substrings of length 1
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dp[1][i][j] = s1[i] == s2[j];
            }
        }

        // Fill the table for substrings of length 2 to n
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n-length; i++) {
                for (int j = 0; j <= n-length; j++) {
                    // Iterate over all possible lengths of the first substring
                    for (int newLength = 1; newLength < length; newLength++) {
                        // Check if the two possible splits of the substrings are scrambled versions of each other
                        bool[] dp1 = dp[newLength][i];
                        bool[] dp2 = dp[length-newLength][i+newLength];
                        dp[length][i][j] |= dp1[j] && dp2[j+newLength];
                        dp[length][i][j] |= dp1[j+length-newLength] && dp2[j];
                    }
                }
            }
        }

        // Return whether the entire strings s1 and s2 are scrambled versions of each other
        return dp[n][0][0];
    }
}
```

```
Runtime
73 ms
Beats
98.52%
Memory
41 MB
Beats
58.52%
```

还是第一种好懂一点。这第二种就当拓展了。