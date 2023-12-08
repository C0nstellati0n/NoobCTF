# [Largest Odd Number in String](https://leetcode.com/problems/largest-odd-number-in-string)

我靠我害怕，要是leetcode过几天突然暴起用hard杀人怎么办？
```c++
class Solution {
public:
    string largestOddNumber(string num) {
        for(int i = num.length()-1;i>=0;i--){
            if((num[i]-'0')%2){
                return num.substr(0,i+1);
            }
        }
        return "";
    }
};
```
但至少今天的题超级简单