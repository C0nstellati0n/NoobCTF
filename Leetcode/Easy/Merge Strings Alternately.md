# Merge Strings Alternately

[题目](https://leetcode.com/problems/merge-strings-alternately/description/)

虽然想法有点奇怪，好歹也是做出来了。

```c#
public class Solution {
    public string MergeAlternately(string word1, string word2) {
        int j=0;
        StringBuilder sb=new();
        for(int i=0;i<word1.Length;i++){
            sb.Append(word1[i]);
            if(j<=word2.Length-1){
                sb.Append(word2[j]);
                j++;
            }
            if(i!=j-1){
                sb.Append(word1[(i+1)..]);
                break;
            }
        }
        if(j<word2.Length){
            sb.Append(word2[j..]);
        }
        return sb.ToString();
    }
}
```

```
Runtime
78 ms
Beats
62.80%
Memory
37 MB
Beats
93.29%
```

事实证明two pointers不用for循环，用while循环会简洁许多。

```c#
//https://leetcode.com/problems/merge-strings-alternately/solutions/3428689/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public string MergeAlternately(string word1, string word2) {
        StringBuilder mergedstring = new();
        int i = 0, j = 0;
        while (i < word1.Length && j < word2.Length) {
            mergedstring.Append(word1[i++]);
            mergedstring.Append(word2[j++]);
        }
        mergedstring.Append(word1[i..]);
        mergedstring.Append(word2[j..]);
        return mergedstring.ToString();
    }
}
```

```
Runtime
77 ms
Beats
68.90%
Memory
37.1 MB
Beats
85.37%
```

如果加几个if语句会快一点。名为two pointers，实际one pointer。

```c#
//https://leetcode.com/problems/merge-strings-alternately/solutions/3429116/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public string MergeAlternately(string word1, string word2) {
        StringBuilder result = new();
        int i = 0;
        while (i < word1.Length || i < word2.Length) {
            if (i < word1.Length) {
                result.Append(word1[i]);
            }
            if (i < word2.Length) {
                result.Append(word2[i]);
            }
            i++;
        }
        return result.ToString();
    }
}
```

```
Runtime
72 ms
Beats
91.46%
Memory
37.2 MB
Beats
66.46%
```