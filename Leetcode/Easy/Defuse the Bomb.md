# [Defuse the Bomb](https://leetcode.com/problems/defuse-the-bomb)

两次wrong answer后直接自暴自弃
```c++
class Solution {
public:
    vector<int> decrypt(vector<int>& code, int k) {
        if(k==0) return vector<int>(code.size());
        vector<int> cp_code(code.size()*2);
        //脑抽想不到怎么处理circular array的sliding window，直接粗暴拼接按普通sliding window做
        for(size_t i=0;i<cp_code.size();i++){
            cp_code[i]=code[i%code.size()];
        }
        size_t i,j;
        size_t curr=0;
        size_t count=0;
        if(k<0){
            k=-k;
            //区别只有i和j的起始位置
            i=j=cp_code.size()/2-k;
            for(;count<=code.size();j++){
                curr+=cp_code[j];
                if(j-i+1==k){
                    count++;
                    code[(j+1)%code.size()]=curr;
                    curr-=cp_code[i];
                    i++;
                }
            }
        }
        else{
            i=j=0;
            for(;count<=code.size();j++){
                curr+=cp_code[j];
                if(j-i+1==k){
                    code[(i-1)%code.size()]=curr;
                    count++;
                    curr-=cp_code[i];
                    i++;
                }
            }
        }
        return code;
    }
};
```
更简洁，不用拼接数组的做法见 https://leetcode.com/problems/defuse-the-bomb/editorial

另外c++对负数的模好像和python不一样。比如python -1%5是4，c++ -1%5还是-1