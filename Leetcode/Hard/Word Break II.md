# [Word Break II](https://leetcode.com/problems/word-break-ii)

如果我在2015年做出这道题，我可以被称作“大佬”;可惜现在是2024年
```c++
class Solution {
private:
    vector<string> ans;
public:
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        string cur;
        dfs(wordDict,cur,s,0);
        return ans;
    }
    void dfs(const vector<string>& words,string& cur,const string& s,int s_index){
        if(s_index>=s.length()){
            ans.push_back(cur.substr(0,cur.length()-1));
            return;
        }
        for(const string& word:words){
            if(s.substr(s_index).starts_with(word)){
                int wordLength=word.length();
                cur+=word+" ";
                dfs(words,cur,s,s_index+wordLength);
                wordLength++;
                while(wordLength--){
                    cur.pop_back();
                }
            }
        }
    }
};
```
从来没有感觉自己这么懂backtrack！连续两天在hard题写出表现不错的代码！虽然都是同一考点而且放到今天只能被看作medium……