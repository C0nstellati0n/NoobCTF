# Minimum Speed to Arrive on Time

[题目](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/description/)

从来没有写过这么大起大落的题……
```c#
public class Solution {
    public int MinSpeedOnTime(int[] dist, double hour) {
        int n=dist.Length;
        if(n-1>=hour){
            return -1;
        }
        int start = 1;
        int end = (int)1e7;
        while (start <= end) {
            int mid = start + (end-start)/2;
            if (GetTime(dist,mid,n) > hour) start = mid+1;
            else end = mid - 1;
        }
        return start;
    }
    double GetTime(int[] dist,int speed,int n){
        double res=0;
        for(int i=0;i<n-1;i++){
            res+=Math.Ceiling((double)dist[i]/speed);
        }
        return res+(double)dist[^1]/speed;
    }
}
```
```
Runtime
303 ms
Beats
100%
Memory
52.3 MB
Beats
93.33%
```
你问我大起大落的地方在哪？啊，最开始我为了准确性，GetTime里用的是decimal而不是double（一看就是c#没学好，decimal是给钱用的不是在这里用的！）。各位可以自己试一下，把double换成deciaml并且将`GetTime(dist,mid,n) > hour`的hour也用decimal（`GetTime(dist,mid,n) > (decimal)hour`），你就会知道什么叫天差地别。

然后去editorial和discussion和采样区逛了一圈，我这个确实是大佬们使用的方法。好耶！