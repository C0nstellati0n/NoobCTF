# [Maximum Score Words Formed by Letters](https://leetcode.com/problems/maximum-score-words-formed-by-letters)

天啊！这是我代码写的最好的一集！
```c++
class Solution {
private:
    int ans=0;
public:
    int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& scores) {
        vector<int> cnt(26);
        for(const char& c:letters){
            cnt[c-'a']++;
        }
        int score=0;
        dfs(words,cnt,scores,0,score);
        return ans;
    }
    void dfs(const vector<string>& words,vector<int>& cnt,const vector<int>& scores,int index,int& curScore){
        if(index>=words.size()) return;
        dfs(words,cnt,scores,index+1,curScore);
        if(checkWord(words[index],cnt)){
            int score=calculate(words[index],scores);
            curScore+=score;
            ans=max(ans,curScore);
            dfs(words,cnt,scores,index+1,curScore);
            curScore-=score;
        }
        restore(words[index],cnt);
    }
    bool checkWord(const string& word,vector<int>& cnt){
        bool ans=true;
        for(const char& c:word){
            if(cnt[c-'a']==0) ans=false;
            cnt[c-'a']--;
        }
        return ans;
    }
    int calculate(const string& word,const vector<int>& scores){
        int ans=0;
        for(const char& c:word){
            ans+=scores[c-'a'];
        }
        return ans;
    }
    void restore(const string& word,vector<int>& cnt){
        for(const char& c:word){
            cnt[c-'a']++;
        }
    }
};
```
其实这题最多算个medium，和昨天的[The Number of Beautiful Subsets](../Medium/The%20Number%20of%20Beautiful%20Subsets.md)套路一致。但好歹标的是hard，人生第一次在标着hard的题目上写出表现这么好的代码，纪念一下

还是按照惯例看了一眼editorial，采样区和solutions区。backtrack上大家思路都差不多，不过实现细节不同。你问dp？什么dp？哪有dp？我不会啊