# [Find Words That Can Be Formed by Characters](https://leetcode.com/problems/find-words-that-can-be-formed-by-characters)

美好的周末从easy开始
```c++
class Solution {
public:
    int countCharacters(vector<string>& words, string chars) {
        char freq[26]={0};
        char temp[26];
        bool flag;
        int ans=0;
        for(const char& c : chars) {
            freq[c-'a']++;
        }
        for(const string& word:words){
            copy(std::begin(freq), std::end(freq), std::begin(temp)); //也可以参考采样区或editorial再用一次frequency count而不是两个数组左右手倒
            flag=true;
            for(const char& c:word){
                if(temp[c-'a']==0){
                    flag=false;
                    break;
                }
                temp[c-'a']--;
            }
            if(flag) ans+=word.size();
        }
        return ans;
    }
};
```