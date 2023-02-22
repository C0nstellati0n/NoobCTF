# Valid Parentheses

[题目](https://leetcode.com/problems/valid-parentheses/)

我到底会不会编程啊？答案是不会，因为在这道题之前我都没用过C#的Stackʕ •ᴥ•ʔ。

这题要求我们检查括号是否合法。共有3种括号，`[]`,`()`和`{}`。几种括号都必须按照正确顺序闭合，比如`[{}]`正确，`[{]}`错误。然后我就不会了。我隐隐约约感觉有对称的感觉，但是`[]()`这种情况显然就不对称了，却也是合法括号。去看答案，啊我是憨憨。我们把括号拆开来看，每个括号的前半部分看成一部分，后半部分看成一部分。所谓的“顺序闭合”其实就是后进先出，那不就是栈吗？我们遍历字符串s的每个字符，如果是前半部分括号，就压栈；如果是后半部分括号，就弹栈。如果弹栈时栈是空（没有前半部分括号）或者弹出来不是各自对应的前半部分（闭合顺序错误），就返回False。完成遍历后返回栈是否为空（是否闭合全部前半部分括号）。

```c#
public class Solution {
    public bool IsValid(string s) {
        Stack<char> stack=new();
        foreach(char c in s){
            switch(c){
                case '(':
                case '{':
                case '[':
                    stack.Push(c);
                    break;
                case ')':
                    if(stack.Count == 0||stack.Pop()!='('){
                        return false;
                    }
                    break;
                case '}':
                    if(stack.Count == 0||stack.Pop()!='{'){
                        return false;
                    }
                    break;
                case ']':
                    if(stack.Count == 0||stack.Pop()!='['){
                        return false;
                    }
                    break;
            }
        }
        return stack.Count == 0;
    }
}
```

```
Runtime
70 ms
Beats
93.28%
Memory
37.8 MB
Beats
56.52%
```

又试了一下字典，还是慢。之前做另一道题时已经发现小样本情况下字典没switch-case快了，这次彻底死心。

```c#
public class Solution {
    public bool IsValid(string s) {
        Stack<char> stack=new();
        Dictionary<char,char> dic=new Dictionary<char,char>{
            {')','('},
            {']','['},
            {'}','{'}
        };
        foreach(char c in s){
            switch(c){
                case '(':
                case '{':
                case '[':
                    stack.Push(c);
                    break;
                case ')':
                case '}':
                case ']':
                    if(stack.Count == 0||stack.Pop()!=dic[c]){
                        return false;
                    }
                    break;
            }
        }
        return stack.Count == 0;
    }
}
```

```
Runtime
87 ms
Beats
29.99%
Memory
37.8 MB
Beats
68.14%
```

接着往下翻了翻，发现可以缩减几种处理情况。看下面的脚本就知道了。

```c#
public class Solution {
    public bool IsValid(string s) {
        Stack<char> stack=new();
        foreach(char c in s){
            switch(c){
                case '(':
                    stack.Push(')');
                    break;
                case '{':
                    stack.Push('}');
                    break;
                case '[':
                    stack.Push(']');
                    break;
                default:
                    if(stack.Count==0||stack.Pop()!=c){
                        return false;
                    }
                    break;
            }
        }
        return stack.Count == 0;
    }
}
```

```
Runtime
82 ms
Beats
47.73%
Memory
37.4 MB
Beats
85.45%
```

```c#
public class Solution {
    public bool IsValid(string s) {
        Stack<char> stack=new();
        foreach(char c in s){
            if (c == '(')
			    stack.Push(')');
		    else if (c == '{')
			    stack.Push('}');
		    else if (c == '[')
			    stack.Push(']');
		    else if (stack.Count==0 || stack.Pop() != c)
			    return false;
        }
        return stack.Count == 0;
    }
}
```

```
Runtime
72 ms
Beats
90.44%
Memory
37.9 MB
Beats
56.52%
```

看来带default的switch-case又没有if-else if-else快啊……不过内存少了。