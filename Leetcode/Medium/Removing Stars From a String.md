# Removing Stars From a String

[题目](https://leetcode.com/problems/removing-stars-from-a-string/description/)

啊这题好简单啊，唯一一道我赞同dicussion里说的“应该被归为简单”的题。

```c#
public class Solution {
    public string RemoveStars(string s) {
        Stack<char> stack=new();
        foreach(char c in s){
            if(c=='*'){
                stack.Pop();
            }
            else{
                stack.Push(c);
            }
        }
        return string.Join("-",stack.ToArray().Reverse()).Replace("-","");
    }
}
```

```
Runtime
121 ms
Beats
47.17%
Memory
49.5 MB
Beats
```

但是吧我的解法有点邪门，为了把stack转为string真的是费了很多工夫。最后的做法结果还是错的。正确的做法如下：

```c#
public class Solution {
    public string RemoveStars(string s) {
        var stack = new Stack<char>();
        
        foreach(var chr in s) {
            if(chr == '*')
                stack.Pop();
            else
                stack.Push(chr);
        }

        return new string(stack.ToArray().Reverse().ToArray());
    }
}
```

```
Runtime
96 ms
Beats
100%
Memory
43.9 MB
Beats
35.85%
```

当然也可以用StringBuilder转字符串。

```c#
//https://leetcode.com/problems/removing-stars-from-a-string/solutions/3402529/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public string RemoveStars(string l) {
        // Create a new stack to keep track of characters encountered so far
        Stack<char> s =new();
        
        // Iterate over each character in the input string
        foreach(char c in l) {
            // If the current character is a star, remove the topmost character from the stack
            if (c == '*') {
                s.Pop();
            }
            // If the current character is not a star, add it to the stack
            else {
                s.Push(c);
            }
        }
        
        // Create a new stringBuilder to store the characters in the stack
        StringBuilder sb = new();
        
        // Iterate over each character in the stack and append it to the stringBuilder
        s=new(s);
        foreach(char c in s){
            sb.Append(c);
        }
        
        // Convert the stringBuilder to a string and return it as the output
        return sb.ToString();
    }
}
```

```
Runtime
117 ms
Beats
60.38%
Memory
42.9 MB
Beats
60.38%
```

从[这里](https://stackoverflow.com/questions/3297717/does-stack-constructor-reverse-the-stack-when-being-initialized-from-other-one)发现stack的初始化顺序是反的，也就是说可以用一个stack初始化另一个栈，初始化出来的栈里的值是原来栈里的值的逆序。便有了上面的改编解法。原解法直接就是stringbuilder遍历加字符了。

脱离栈的束缚，来看看two pointers。

```c#
//https://leetcode.com/problems/removing-stars-from-a-string/solutions/3402430/c-two-approaches-explanation-beginner-to-pro-solution/
class Solution {
    public string RemoveStars(string s) {
        char[] temp=s.ToCharArray();
        int i=0,j=0;
        for(i=0;i<s.Length;i++){
            if(temp[i]=='*'){
                j--;
            }else{
                temp[j++] = temp[i];
            }
        }
        return new string(temp[0..j]);
    }
}
```

```
Runtime
101 ms
Beats
100%
Memory
43 MB
Beats
60.38%
```

纯stringbuilder解法：

```c#
//https://leetcode.com/problems/removing-stars-from-a-string/solutions/3402366/python3-c-java-easy-and-understand-stack-simulation/
class Solution {
    public string RemoveStars(string s) {
        StringBuilder c = new();
        for (int i = 0; i < s.Length; i++) {
            if (s[i] == '*') {
                c.Remove(c.Length - 1,1);
            } else {
                c.Append(s[i]);
            }
        }
        return c.ToString();
    }
}
```

```
Runtime
112 ms
Beats
77.36%
Memory
43.4 MB
Beats
43.40%
```

究极简单但又表现最好的神奇解法：

```c#
public class Solution {
    public string RemoveStars(string s) {
        var sb = new StringBuilder(s.Length);
        foreach (char c in s) {
            if (c == '*') {
                sb.Length -= 1;
            }
            else {
                sb.Append(c);
            }
        }
        return sb.ToString();
    }
}
```

```
Runtime
97 ms
Beats
100%
Memory
42.6 MB
Beats
88.68%
```

查阅[文档](https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder?view=net-7.0)就知道是为什么了。主要StringBuilder的工作方式完全符合题目要求。