# [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning)

不是哥们，dp用着不好就没必要硬塞进去啊
```c++
class Solution {
private:
    vector<vector<string>> ans;
public:
    vector<vector<string>> partition(string s) {
        vector<vector<int>> dp(s.length(),vector<int>(s.length(),-1));
        for(int i=0;i<s.length();i++){
            for(int j=0;j<s.length();j++){
                if(i==j) dp[i][j]=1;
            }
        }
        for(int i=0;i<s.length();i++){
            dfs(s,{},0,i,dp);
        }
        return ans;
    }
    void dfs(const string& s,vector<string> partition,int i,int j,vector<vector<int>>& dp){
        if(dp[i][j]==-1) dp[i][j]=(int)check(s.substr(i,j-i+1));
        if(dp[i][j]==0) return;
        if(dp[i][j]==1){
            partition.push_back(s.substr(i,j-i+1));
            if(j>=s.size()-1){
                ans.push_back(partition);
                return;
            }
            for(int k=j+1;k<s.length();k++){
                dfs(s,partition,j+1,k,dp);
            }
            partition.pop_back();
        }
    }
    bool check(const string& s){
        int i;
        int j;
        if(s.length()%2==1){
            i=s.length()/2+1;
            j=s.length()/2-1;
        }
        else{
            i=s.length()/2-1;
            j=s.length()/2;
        }
        while(i>=0&&j<s.length()){
            if(s[i]!=s[j]) return false;
            i--;
            j++;
        }
        return true;
    }
};
```
这tm是什么？这50行代码要速度没速度，要内存没内存。写这个代码的我有脑子但不多。只需要50的一半行代码就能写出比这个好一万倍的东西：
```c++
class Solution {
public:
    vector<vector<string>> partition(string s) {
        vector<vector<string>> ans;
        vector<string> tmp;
        dfs(0, tmp, s, ans);
        return ans;
    }
    //蚌埠住了，我用了那么多行代码其实三行就行
    bool isPalindrome(const string& str) {
        for(int i = 0; i < (str.size() / 2); i++) {
            if (str[i] != str[str.size() - 1 - i]) return false;
        }
        return true;
    }
    //i：当前partition所在的索引
    //cur：当前partition
    //我以为cur不能用引用，怕push进ans后后续的backtrack操作影响到之前的partition。现在看来不会
    void dfs(int i, vector<string>& cur, const string& s, vector<vector<string>>& ans) {
        if (i == s.size()) {
            ans.push_back(cur);
        }
        for(int start = i; i < s.size(); i++) {
            //从i开始（start），考虑从start到字符串末尾的所有substring
            cur.push_back(s.substr(start, i - start + 1));
            if (isPalindrome(cur.back()))
                dfs(i + 1, cur, s, ans); //如果某个substring是回文字符串，从那个字符串的末尾继续进行partition
            cur.pop_back(); //经典backtrack取消操作
        }
    }
};
```
至少我现在会partition了