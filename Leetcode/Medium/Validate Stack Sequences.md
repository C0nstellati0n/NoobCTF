# Validate Stack Sequences

[题目](https://leetcode.com/problems/validate-stack-sequences/description/)

discussion区的第一个动图的思路非常清晰，看几遍就会写了。

```c#
public class Solution {
    public bool ValidateStackSequences(int[] pushed, int[] popped) {
        int j=0;
        Stack<int> stack=new();
        foreach(int val in pushed){
            stack.Push(val);
            if(val==popped[j]){
                while(stack.Count!=0 && stack.Peek()==popped[j]){
                    stack.Pop();
                    j++;
                }
            }
        }
        return stack.Count==0;
        //或者
        //return j==pushed.Length;
    }
}
```

```
Runtime
97 ms
Beats
80.77%
Memory
42.1 MB
Beats
88.46%
```

但是还有更省空间的做法：two pointers。我们直接让参数pushed变为我们的栈，索引i表示栈的指针。

```c#
//https://leetcode.com/problems/validate-stack-sequences/solutions/1853250/java-c-space-complexity-going-from-o-n-o-1/
class Solution {
    public bool ValidateStackSequences(int[] pushed, int[] popped) {
        int i = 0; // Intialise one pointer pointing on pushed array
        int j = 0; // Intialise one pointer pointing on popped array
        
        foreach(int val in pushed){
            pushed[i++] = val; // using pushed as the stack.
            while(i > 0 && pushed[i - 1] == popped[j]){ // pushed[i - 1] values equal to popped[j];
                i--; // decrement i
                j++; // increment j
            }
        }
        return i == 0; // Since pushed is a permutation of popped so at the end we are supposed to be left with an empty stack
    }
}
```

```
Runtime
97 ms
Beats
80.77%
Memory
41.8 MB
Beats
100%
```