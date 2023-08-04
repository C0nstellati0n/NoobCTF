# Letter Combinations of a Phone Number

[题目](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

笑死，这周backtrack可太爽了，模板套得不亦乐乎。
```c#
public class Solution {
    Dictionary<char,string> keyboard = new Dictionary<char,string>
    {
        ['2']="abc",
        ['3']="def",
        ['4']="ghi",
        ['5']="jkl",
        ['6']="mno",
        ['7']="pqrs",
        ['8']="tuv",
        ['9']="wxyz"
    };
    List<string> ans=new();
    public IList<string> LetterCombinations(string digits) {
        if(String.IsNullOrEmpty(digits)){
            return ans;
        }
        Backtrack(digits,0,ans,new StringBuilder());
        return ans;
    }
    private void Backtrack(string digits,int index,List<string> ans,StringBuilder current)
    {
        if(current.Length==digits.Length){
            ans.Add(current.ToString());
            return;
        }
        foreach(char digit in keyboard[digits[index]]){
            current.Append(digit);
            Backtrack(digits,index+1,ans,current);
            current.Remove(current.Length-1,1);
        }
    }
}
```
```
Runtime
117 ms
Beats
99.81%
Memory
43.7 MB
Beats
74.74%
```
但是去solution一看，递归解法太简单了，大佬们都卷遍历做法。
```c#
//采样区的linked list解法。我第一次知道原来c#里也有linked list啊？之前改写java做法时，java里的linked list等于c#的queue，我就以为c#里没有linked list
public class Solution {
    public static char[][] mapping = {
        "".ToCharArray(),
        "".ToCharArray(),
        "abc".ToCharArray(),
        "def".ToCharArray(),
        "ghi".ToCharArray(),
        "jkl".ToCharArray(),
        "mno".ToCharArray(),
        "pqrs".ToCharArray(),
        "tuv".ToCharArray(),
        "wxyz".ToCharArray(),
    };
    private static char[] CharToMapping(char c){
        return mapping[c - '0'];
    }
    public IList<string> LetterCombinations(string digits) {
        LinkedList<string> combinations = new LinkedList<string>();
        if(digits.Length == 0) return combinations.ToArray();
        // Initial starting points
        foreach(char c in CharToMapping(digits[0]))
            combinations.AddLast(Char.ToString(c)); //首先把digits[1]对应的字母开头加进去
        // Remaining additions
        for(int i = 1; i < digits.Length; i++){
            // Build on existing entries thus far
            int n = combinations.Count;
            for(int j = 0; j < n; j++){
                string prefix = combinations.First.Value; //不断取出当前的字符串
                combinations.RemoveFirst(); //移除之前的
                // Build on existing entries with new combinations
                foreach(char c in CharToMapping(digits[i]))
                    combinations.AddLast(prefix + c); //添加新的组合
            }
        }
        //这个解法第一个for循环遍历digits，第二个for循环更新linked list里已有的全部node
        return combinations.ToArray();
    }
}
```
```
Runtime
124 ms
Beats
98.22%
Memory
43.9 MB
Beats
42.82%
```
上面的解法类似 https://leetcode.com/problems/letter-combinations-of-a-phone-number/solutions/8064/my-java-solution-with-fifo-queue/ ，不过solution这个可能更巧妙一点，用了`while(ans.peek().length()!=digits.length())`。