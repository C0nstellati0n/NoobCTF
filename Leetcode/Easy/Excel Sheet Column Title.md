# Excel Sheet Column Title

[题目](https://leetcode.com/problems/excel-sheet-column-title/description/)

诶为什么减一可以？不是我怎么做出来的？
```c#
public class Solution {
    public string ConvertToTitle(int columnNumber) {
        StringBuilder res=new();
        while(columnNumber>0){
            if(columnNumber%26==0){
                res.Insert(0,'Z');
                columnNumber--;
            }
            else{
                res.Insert(0,(char)(64+columnNumber%26));
            }
            columnNumber/=26;
        }
        return res.ToString();
    }
}
```
```
Runtime
51 ms
Beats
100%
Memory
36.9 MB
Beats
16.15%
```
其实这题是个base 10转base 26，转换方法就是模后再除（打CTF时都熟悉了）。但是再仔细一看，好像又不是完全base 26，因为这里从1开始计数，为A，而一般的base 26应该是以0开始才对。所以参考[editorial](https://leetcode.com/problems/excel-sheet-column-title/editorial/)，每次模+除之前减去1，把它化为普通的base 26即可。

所以我的那种是怎么过的？我没有次次都-1啊？我写的时候没发现editorial说的内容，就把它当普通转base 26来做。但是做到第三个test case时发现Z那里columnNumber%26等于0。所以我加了个if语句给它。但是再后面columnNumber/=26=1，多了一个。所以我就减了一下。于是歪打正着。