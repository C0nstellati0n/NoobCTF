# [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string)

one pass反常识，可没说two pass反常识？
```c++
class Solution {
public:
    bool checkValidString(string s) {
        int parenthesis=0;
        int wildcard=0;
        for(int i=0;i<s.length();i++){
            if(s[i]=='(') parenthesis++;
            else if(s[i]==')') parenthesis--;
            else if(s[i]=='*') wildcard++;
            if(parenthesis<0&&wildcard<abs(parenthesis)) return false;
        }
        parenthesis=0;
        wildcard=0;
        for(int i=s.length()-1;i>=0;i--){
            if(s[i]==')') parenthesis++;
            else if(s[i]=='(') parenthesis--;
            else if(s[i]=='*') wildcard++;
            if(parenthesis<0&&wildcard<abs(parenthesis)) return false;
        }
        return parenthesis==0?true:wildcard>=abs(parenthesis);
    }
};
```
个人记录这个纯粹是因为似乎见到了这种“括号题”的规律。昨天（没记）有道题是前面遍历一遍后面遍历一遍就能解出来，今天这题也是。莫不是这其中有什么规律吧？先记下来看看。one pass做法参考lee佬： https://leetcode.com/problems/valid-parenthesis-string/solutions/107570/java-c-python-one-pass-count-the-open-parenthesis ,别人的解析我都看不懂，就他的一眼就懂了。简短但是每个字都是重点