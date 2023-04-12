# Simplify Path

[题目](https://leetcode.com/problems/simplify-path/)

c#没有双端队列，有些解法改不出来。倒是能上网找个实现，但是我懒。这道题我卡的地方在于如何回退目录，因为`../`意为退回上个目录，放到Stack里就是Pop。但最开始我是一个一个字符遍历的，怎么记录上个目录在哪呢？其实最开始Split一下就好了……

```c#
//https://leetcode.com/problems/simplify-path/solutions/1847526/best-explanation-ever-possible-not-a-clickbait/
class Solution {
    public string SimplifyPath(string path) {
        Stack<string> s = new();
        StringBuilder res = new();
        string[] p =path.Split("/");
        for(int i=0;i<p.Length;i++){
            if(s.Count!=0  && p[i]=="..") s.Pop();
            else if(p[i].Length!=0 && p[i]!="." && p[i]!="..")
                s.Push(p[i]);
        }
        if(s.Count==0) return "/";
        while(s.Count!=0){
            res.Insert(0,s.Pop()).Insert(0,"/");
        }
        return res.ToString();
    }
}
```

```
Runtime
78 ms
Beats
86.87%
Memory
39 MB
Beats
65.66%
```

栈的使用基本是公认的，有区别的地方在于怎么把栈里的字符串连接成字符串。上个解法用while，用Join也行。

```c#
//https://leetcode.com/problems/simplify-path/solutions/3407361/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public string SimplifyPath(string path) {
        Stack<string> stack = new(); // create a stack to keep track of directories
        string[] directories = path.Split("/"); // split the path by slash '/'
        foreach(string dir in directories) { // iterate over the directories
            if (dir=="." || dir.Length==0) { // ignore the current directory '.' and empty directories
                continue;
            } else if (dir=="..") { // go one level up for double period '..'
                if (stack.Count!=0) { // if stack is not empty, pop the top element
                    stack.Pop();
                }
            } else { // for any other directory, push it to the stack
                stack.Push(dir);
            }
        }
        stack=new(stack);
        return "/" + string.Join("/", stack); // join the directories in the stack with slash '/' and add a slash at the beginning
    }
}
```

```
Runtime
74 ms
Beats
92.93%
Memory
38.7 MB
Beats
83.84%
```

或者直接用开始Split出来的List，不考虑那么多东西。

```c#
public class Solution {
    public string SimplifyPath(string path) {
        string str = path.Replace("../","/");
        List<string> dirList = new List<string>();
        foreach(string dir in path.Split('/'))
        {
            if(dir == "..")
            {
                if(dirList.Count>0)
                    dirList.RemoveAt(dirList.Count-1);

            }else if(!String.IsNullOrEmpty(dir) && dir != ".")
                dirList.Add(dir);
        }
        return "/" + String.Join("/", dirList.ToArray());
        
    }
}
```

```
Runtime
67 ms
Beats
98.99%
Memory
39.1 MB
Beats
54.4%
```