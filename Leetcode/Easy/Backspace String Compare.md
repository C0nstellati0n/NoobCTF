# [Backspace String Compare](https://leetcode.com/problems/backspace-string-compare)

```c#
//无脑stack解法
public class Solution {
    public bool BackspaceCompare(string s, string t) {
        Stack<char> ss=new();
        Stack<char> ts=new();
        foreach(char c in s){
            if(ss.Any()&&c=='#'){
                ss.Pop();
            }
            else if(c!='#'){
                ss.Push(c);
            }
        }
        foreach(char c in t){
            if(ts.Any()&&c=='#'){
                ts.Pop();
            }
            else if(c!='#'){
                ts.Push(c);
            }
        }
        return String.Join("", ss)==String.Join("", ts);
    }
}
```
follow up提到的O(1)空间解法：
```c#
//https://leetcode.com/problems/backspace-string-compare/editorial
class Solution {
    public bool BackspaceCompare(string S, string T) {
        int i = S.Length - 1, j = T.Length - 1;
        int skipS = 0, skipT = 0;
        while (i >= 0 || j >= 0) { // While there may be chars in build(S) or build (T)
            while (i >= 0) { // Find position of next possible char in build(S)
                if (S[i] == '#') {skipS++; i--;}
                else if (skipS > 0) {skipS--; i--;}
                else break;
            }
            while (j >= 0) { // Find position of next possible char in build(T)
                if (T[j] == '#') {skipT++; j--;}
                else if (skipT > 0) {skipT--; j--;}
                else break;
            }
            // If two actual characters are different
            if (i >= 0 && j >= 0 && S[i] != T[j])
                return false;
            // If expecting to compare char vs nothing
            if ((i >= 0) != (j >= 0))
                return false;
            i--; j--;
        }
        return true;
    }
}
```