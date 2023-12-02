# [Check If Two String Arrays are Equivalent](https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent)

和采样区最佳所见略同
```c++
class Solution {
public:
    bool arrayStringsAreEqual(vector<string>& word1, vector<string>& word2) {
        string s1="";
        string s2="";
        for(const string& s:word1){
            s1+=s;
        }
        for(const string& s:word2){
            s2+=s;
        }
        return s1==s2;
    }
};
```
editorial还有two pointers做法。不对应该是four pointers