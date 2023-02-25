# Length of Last Word

[题目](https://leetcode.com/problems/length-of-last-word/description/)

给定一个包含单词和空格的字符串，返回最后一个单词的长度。我最开始觉得直接用Split函数将字符串依照空格分割，然后返回最后一项的长度不就行了吗？直到我看见了一个测试用例，原来空格不只有一个啊！如果直接像刚才我说的那样做，分割后的最后一项长度为0，不对。

```c#
using System;
public class HelloWorld
{
    public static void Main(string[] args)
    {
        string s="   fly me   to   the moon  ";
        string[] temp=s.Split(' ');
        for(int i=0;i<temp.Length;i++){
            Console.WriteLine($"{i}:{temp[i].Length}"); //最后应该返回的是moon的长度4
        }
    }
}
```

应对方法也很简单，倒着遍历Split的结果数组，哪一项的长度不是0就返回哪一项的长度。

```c#
public class Solution {
    public int LengthOfLastWord(string s) {
        string[] temp=s.Split(' '); //string[] temp=s.Split(); 不带参数的结果是一样的
        for(int i=temp.Length-1;i>=0;i--){
            if(temp[i].Length!=0){
                return temp[i].Length;
            }
        }
        return 0;
    }
}
```

```
Runtime
64 ms
Beats
71.30%
Memory
36.4 MB
Beats
59.46%
```

接着看到了用栈的做法。

```c#
public class Solution {
    public int LengthOfLastWord(string s) {
        Stack<char> s1=new();
        int count=0;
        for(int i=0;i<s.Length;i++){
            s1.Push(s[i]);
        }
//here we push all the element of the string to stack
        /*
now we will pop() all the blank spaces from the top of stack so 
that we reach the last later of the last word.
*/
        while(s1.Peek()==' '){
            s1.Pop();
        }
    /*
now we run the while loop util the stack is empty in the case of 
only one word is there or the blank space comes which seperate the two words.

*/

        while(!(s1.Count==0)&&s1.Peek()!=' '){
            count++;
            s1.Pop();   
        }
        // now we itterate the count to count the length of the last word and return  it.
        return count;
    }
}
```

```
Runtime
57 ms
Beats
93.93%
Memory
36.9 MB
Beats
9.8%
```

直接遍历也行。

```c#
public class Solution {
    public int LengthOfLastWord(string s) {
        int n=s.Length;
        int cnt=0;
        for(int i=n-1;i>=0;i--)
        {
            if (Char.IsWhiteSpace(s,i) && cnt>0) break;
            else
            {
                if (Char.IsWhiteSpace(s,i) && cnt==0) continue;
                else cnt++;
            }
        }
        return cnt;
    }
}
```

```
Runtime
67 ms
Beats
53.63%
Memory
36.5 MB
Beats
58.26%
```

最后试了用Trim和TrimEnd剔除空格后再Split再返回最后一项的长度，不过效果不太好。

```c#
public class Solution {
    public int LengthOfLastWord(string s) {
        string[] temp=s.Trim().Split(' ');
        return temp[^1].Length;
    }
}
```

```
Runtime
67 ms
Beats
53.63%
Memory
36.8 MB
Beats
24.42%
```

```c#
public class Solution {
    public int LengthOfLastWord(string s) {
        string[] temp=s.TrimEnd().Split(' ');
        return temp[^1].Length;
    }
}
```

```
Runtime
68 ms
Beats
49.28%
Memory
36.8 MB
Beats
15.79%
```