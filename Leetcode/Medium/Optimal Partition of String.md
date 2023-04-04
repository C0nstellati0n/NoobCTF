# Optimal Partition of String

[题目](https://leetcode.com/problems/optimal-partition-of-string/description/)

借用discussion里的一句话：“Something wrong with this question if I can solve it”。结合提示里的“贪心”和discussion里的set，这题很快就出来了。

```c#
public class Solution {
    public int PartitionString(string s) {
        HashSet<char> set=new();
        int count=1;
        foreach(char c in s){
            if(!set.Add(c)){
                set.Clear();
                count++;
            }
            set.Add(c);//这句表示当前字符已经见过了。如果上面没加成功，说明当前的字符与之前重复了，清空了再加。如果上面已经加成功了，这里再加也无伤大雅
        }
        return count;
    }
}
```

```
Runtime
77 ms
Beats
83.74%
Memory
42.1 MB
Beats
94.31%
```

类似的解法还有用字典，这里就不放了。更厉害的一种写法是用位运算。

```c#
//https://leetcode.com/problems/optimal-partition-of-string/solutions/3376693/image-explanation-3-approaches-o-1-space-c-java-python/
public class Solution {
    public int PartitionString(String s) {
        int i = 0, ans = 1, flag = 0;
        while(i < s.Length) {
            int val = s[i] - 'a';
            if ((flag & (1 << val)) != 0) {//一旦当前字符之前有标记，按位与的结果就是1
                flag = 0;
                ans++;
            }
            flag = flag | (1 << val);//按位或是个常见的位运算小技巧，把当前字符标记到flag里
            i++;
        }
        return ans;
    }
}
```

```
Runtime
66 ms
Beats
100%
Memory
42 MB
Beats
96.75%
```