# Matrix Diagonal Sum

[Matrix Diagonal Sum](https://leetcode.com/problems/matrix-diagonal-sum/description/)

easy题能难到哪去呢？

```c#
public class Solution {
    public int DiagonalSum(int[][] mat) {
        int res=0;
        int length=mat.Length;
        for(int i=0;i<length;i++){
            res+=mat[i][i];
            res+=mat[i][(length-1)-i];
        }
        if(length%2!=0){
            res-=mat[length/2][length/2];
        }
        return res;
    }
}
```

```
Runtime
93 ms
Beats
83.90%
Memory
42.3 MB
Beats
7.32%
```

还有变种解法。

```c#
//https://leetcode.com/problems/matrix-diagonal-sum/solutions/1270211/c-solution-easy-o-n-runtime/
public class Solution {
    public int DiagonalSum(int[][] mat) {
        int n=mat.Length,ans=0;
        for(int i=0;i<n;i++){
            if(i!=n-i-1) ans+=mat[i][i]+mat[i][n-i-1];
            else ans+=mat[i][i];   
        }
        return ans;
    }
}
```

```
Runtime
92 ms
Beats
87.81%
Memory
42.1 MB
Beats
30.24%
```