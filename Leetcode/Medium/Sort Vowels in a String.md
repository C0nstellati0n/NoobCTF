# [Sort Vowels in a String](https://leetcode.com/problems/sort-vowels-in-a-string)

发现了一个神奇的检查字符是不是元音的办法
```c++
class Solution {
public:
    string sortVowels(string s) {
        vector<char> temp;
        for(char c:s){
            if(isvowel(c)) temp.push_back(c);
        }
        sort(temp.begin(), temp.end());
        string ans="";
        int index=0;
        for(char c:s){
            if(isvowel(c)){
                ans+=temp[index];
                index++;
            }
            else{
                ans+=c;
            }
        }
        return ans;
    }
    //https://stackoverflow.com/questions/47846406/c-fastest-way-to-check-if-char-is-vowel-or-consonant
    //解析：https://leetcode.com/problems/sort-vowels-in-a-string/solutions/4281015/c-o-n-count-freq-bitmask-check-vowels-15ms-beats-100
    bool isvowel(char v) {
        return (0x208222>>(v&0x1f))&1;
    }
};
```
或者用另一种sort：counting sort
```c++
//虽然都是counting sort，但是采样区要比editorial表现好
class Solution {
public:
    bool isVowel(char ch){
        if(ch=='a' || ch=='e' || ch=='i' || ch=='o' || ch=='u' ||
        ch=='A' || ch=='E' || ch=='I' || ch=='O' || ch=='U')return true;
        return false;
    }
    string sortVowels(string s) {
        int freq[128]={0};
        for(int i=0;i<s.size();i++){
            if(isVowel(s[i]))freq[(int)s[i]]++;
        }
        int idx=0;
        for(int i=0;i<s.size();i++){
            if(isVowel(s[i])){
                while(freq[idx]==0)idx++;
                s[i]=(char)idx;
                freq[idx]--;
            }
        }
        return s;
    }
};
```