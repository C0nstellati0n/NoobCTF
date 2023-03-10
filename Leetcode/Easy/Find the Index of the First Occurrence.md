# Find the Index of the First Occurrence in a String

[题目](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/description/)

给定两个字符串，haystack和needle，返回needle在haystack里出现的最小索引；如果没有则返回-1。我寻思C#不是自带一个IndexOf函数吗，还是一模一样的功能。一行代码解决。

```c#
public class Solution {
    public int StrStr(string haystack, string needle) {
        return haystack.IndexOf(needle);
    }
}
```

```
Runtime
56 ms
Beats
94.73%
Memory
37.1 MB
Beats
6.31%
```

但是内存拉胯。有没有别的不用内置函数的解法？

```c#
public class Solution {
    public int StrStr(string haystack, string needle) {
        if(needle.Length>haystack.Length){//特殊情况，needle大于haystack时不可能有索引值
            return -1;
        }
        for(int i=0;i<haystack.Length;i++)
        {
            int j=i;//做个索引i的拷贝，本质上还是一个字符一个字符地遍历haystack
            int ptr=0;//needle的索引
            int count=0;//有多少个相同字符
            while(ptr<needle.Length&&j<haystack.Length&&haystack[j]==needle[ptr])//两个检查不超界的条件必须在前面
            {
                //依次增加指针和计数
                j++;
                ptr++;
                count++;
            }
            if(count==needle.Length) return i;//找到的情况
        }
        return -1;//没找到的情况
    }
}
```

```
Runtime
54 ms
Beats
96.30%
Memory
36.3 MB
Beats
77.70%
```

还有别的解法。

```C#
public class Solution {
    public int StrStr(string haystack, string needle) {
        int hLen = haystack.Length;
        int nLen = needle.Length;
        int nIndex = 0;
        for(int i=0; i<hLen; i++){
            // as long as the characters are equal, increment needleIndex
            if(haystack[i]==needle[nIndex]){
                nIndex++;
            }
            else{
                // start from the next index of previous start index
                i=i-nIndex;
                // needle should start from index 0
                nIndex=0;
            }
            // check if needleIndex reached needle length
            if(nIndex==nLen){
                // return the first index
                return i-nLen+1;
            }
        }
        return -1;
    }
}
```

```
Runtime
69 ms
Beats
36.46%
Memory
36.6 MB
Beats
37.17%
```

其实是差不多的思路，不知道为啥数据差了一大截。最后再看一个。

```c#
public class Solution {
    public int StrStr(string haystack, string needle) {
        int l1 = haystack.Length;
        int l2 = needle.Length;
        int p1=0;//haystack索引
        int p2=0;//needle索引
        while(p1<=l1){//循环直到haystack索引达到haystack长度
            if(p2==l2){//如果needle索引达到needle的长度，说明haystack包含needle。因为每一轮都检查这
                return p1-l2;//因为每一轮都检查上面的条件，所以此时p1一定已经读取了needle这么长的索引，减去即返回第一次出现的位置
            }
            else if(p1==l1){//p1已经达到haystack长度，p2却没有达到needle的长度，说明不包含
                return -1;
            }
            if(haystack[p1]==needle[p2]){
                p2+=1;//相同则增加p2索引
            }
            else{
                p1=p1-p2;//回溯到原来的位置
                p2=0;
            }
            p1+=1;
        }
        return -1;
    }
}
```

```
Runtime
52 ms
Beats
98.9%
Memory
36.4 MB
Beats
69.68%
```