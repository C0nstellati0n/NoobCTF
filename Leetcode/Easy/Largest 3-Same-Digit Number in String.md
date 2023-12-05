# [Largest 3-Same-Digit Number in String](https://leetcode.com/problems/largest-3-same-digit-number-in-string)

尝试用优化解法sliding window一步到位，结果两个wrong answer心态爆炸。还是把脑子丢掉吧
```c++
class Solution {
public:
    string largestGoodInteger(string num) {
        string candidates[10]={"999","888","777","666","555","444","333","222","111","000"};
        for(const string& s:candidates){
            if(num.find(s)!=std::string::npos) return s;
        }
        return "";
    }
};
```
去看了editorial才发现我sliding window想得复杂了。两个知识点：
1. max函数可以用在ascii字符上
2. string(3, maxDigit)表示用maxDigit构造出一个长度为3的字符串