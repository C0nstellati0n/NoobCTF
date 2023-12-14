# [Special Positions in a Binary Matrix](https://leetcode.com/problems/special-positions-in-a-binary-matrix)

c++给我摆了一道
```c++
class Solution {
public:
    int numSpecial(vector<vector<int>>& mat) {
        int m=mat.size();
        int n=mat[0].size();
        int count[m+n]; //不要写int count[m+n]={0}; ，会报错Variable-sized object may not be initialized，参考 https://stackoverflow.com/questions/3082914/c-compile-error-variable-sized-object-may-not-be-initialized
        memset(count,0,(m+n)*sizeof(int)); //所以这里初始化用了memset
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(mat[i][j]){
                    count[i]++;
                    count[m+j]++;
                }
            }
        }
        int ans=0;
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(mat[i][j]){
                    if(count[i]==1&&count[m+j]==1){ //至于为什么要初始化成全0，要是不初始化的话，这里count的数字会因为残留的内存而变得奇奇怪怪的
                        ans++;
                    }
                }
            }
        }
        return ans;
    }
};
```