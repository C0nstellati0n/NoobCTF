# Longest Common Prefix

[题目地址](https://leetcode.com/problems/longest-common-prefix/)

Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string "". 写一个返回众多字符串共同前缀的函数，如果没有就返回""。

这题真的凸显了我算法蠢材的性质(._.)。我自己写出的代码是这样的：

```c#
public class Solution {
    public string LongestCommonPrefix(string[] strs) {
        string res="";
        if(strs.Length<=0){
            return res;
        }
        if(strs.Length==1){
            return strs[0];
        }
        for(int i=1;i<=strs[0].Length;i++){ //不是我为什么要在外面加个没用的for循环？把这个去掉就有下面Horizontal scanning的意思了
            string temp=strs[0][0..i];
            Console.WriteLine(temp);
            for(int j=1;j<strs.Length;j++){
                if(strs[j].IndexOf(temp)!=0){
                    return res;
                }
            }
            res=temp;
        }
        return res;
    }
}
```

跑是能跑，就是慢得要死，内存也耗得多，毫无优点。去看了下官方解，有4种解法，但是那种最好呢？

1. Horizontal scanning

默认strs[0]为最长共同前缀prefix。然后遍历strs中剩下的字符串，判断字符串内是否包含prefix，不包含就缩短prefix直到包含。遍历完全部字符串或缩短到长度0时返回prefix。

```c#
public class Solution {
    public string LongestCommonPrefix(string[] strs) {
        if (strs.Length == 0) return "";
        string prefix = strs[0];
        for (int i = 1; i < strs.Length; i++)
        {
            while (strs[i].IndexOf(prefix) != 0) 
            {
                //prefix = prefix[0..(prefix.Length - 1)];
                prefix = prefix.Substring(0, prefix.Length - 1);
                if (prefix.Length==0) return "";
            }
        }
        return prefix;
    }        
}
```

Runtime:96 ms(Beats 86.11%)
Memory:40.6 MB(Beats 20.11%)

注释的内容使用了C#的语法糖：范围运算符来借取字符串。范围运算符的内存使用和Substring差不多，但是速度从105 ms提升至96 ms。这语法糖真好吃啊！

2. Vertical scanning

遍历strs中的第一个字符串的所有字符，将这个字符与strs中剩下的字符串的字符做比较。如果strs[0]i处的字符不等于strs[j][i]处的字符；或是i超过了j，最长共同前缀就是strs[0][0..i]。

```c#
public class Solution {
    public string LongestCommonPrefix(string[] strs) 
    {
        if (strs == null || strs.Length == 0) return "";
        for (int i = 0; i < strs[0].Length ; i++)
        {
            char c = strs[0][i];
            for (int j = 1; j < strs.Length; j ++) 
            {
                if (i == strs[j].Length || strs[j][i] != c)
                {
                    return strs[0][0..i];        
                }     
            }
        }
        return strs[0];
    }        
}
```

Runtime:98 ms(Beats 78.14%)
Memory:39.5 MB(Beats 72.13%)

跟上一种差不多，少了1 MB的内存。2 ms换1 MB，我也不知道值不值。

3. Divide and conquer

将strs数组从中间不断拆分，例如["leetcode","leet","lee","le"]会被拆成["leetcode","leet"]和["lee","le"]，然后两个数组又分别被拆成"leetcode"和"leet"；"lee"和"le"。现在拆分的结果不是数组了，就能调用commonPrefix找到它们的共同最长前缀，这里两者都是"le"。然后反回去，找"le"和"le"的共同最长前缀，那就是"le"了。

```c#
public class Solution {
    public string LongestCommonPrefix(string[] strs) 
    {
        if (strs == null || strs.Length == 0) return "";
        return longestCommonPrefix(strs, 0 , strs.Length - 1);
    }
    private string longestCommonPrefix(string[] strs, int l, int r) {
    if (l == r) 
    {
        return strs[l];
    }
    else 
    {
        int mid = (l + r)/2;
        string lcpLeft =   longestCommonPrefix(strs, l , mid);
        string lcpRight =  longestCommonPrefix(strs, mid + 1,r);
        return commonPrefix(lcpLeft, lcpRight);
    }
}

    string commonPrefix(string left,string right) 
    {
        int min = Math.Min(left.Length, right.Length);       
        for (int i = 0; i < min; i++) 
        {
            if ( left[i] != right[i] )
                return left[0..i];
        }
        return left[0..min];
    }        
}
```

Runtime:97 ms(Beats 81.96%)
Memory:39.6 MB(Beats 64.86%)

速度和内存都可以，但考虑到这类算法编写的困难性，我选上一种。另外在测试时，原代码是java，我改成C#时忘记把String换成string了，结果也能跑，不过没string快。

4. Binary Search

这种看官方给的图就好，各方面表现都很拉，除了思想没啥好学的（我是不是改写错了，怎么这么拉胯？）

```c#
public class Solution {
    public string LongestCommonPrefix(string[] strs) 
    {
        if (strs == null || strs.Length == 0) return "";
    int minLen = int.MaxValue;
    foreach (string str in strs)
    {
        minLen = Math.Min(minLen, str.Length);
    }
    int low = 1;
    int high = minLen;
    while (low <= high) 
    {
        int middle = (low + high) / 2;
        if (isCommonPrefix(strs, middle))
            low = middle + 1;
        else
            high = middle - 1;
    }
    return strs[0][0..((low + high) / 2)];
    }
    private bool isCommonPrefix(string[] strs, int len)
    {
        string str1 = strs[0][0..len];
        for (int i = 1; i < strs.Length; i++)
        {
            if (!strs[i].StartsWith(str1)) return false;
        }
        return true;
    }   
}
```

Runtime:106 ms(Beats 45.27%)
Memory:40 MB(Beats 37.32%)