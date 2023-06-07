# Check If It Is a Straight Line

[题目](https://leetcode.com/problems/check-if-it-is-a-straight-line/description/)

感觉我的解法像一个数学不好且精神状态欠佳的人写出来的。
```c#
public class Solution {
    public bool CheckStraightLine(int[][] coordinates) {
        if(coordinates.Length==2){
            return true;
        }
        Array.Sort(coordinates,(a,b)=>a[0]-b[0]+a[1]-b[1]); //将点按照从低到高的顺序排序。如果不排序，最开始算的那个斜率就无法拿来作为参考，出现wrong answer
        int[] last=coordinates[1];
        bool zero=false;
        int line=0;
        if(last[0]-coordinates[0][0]==0){
            zero=true;
        }
        else{
            line=(last[1]-coordinates[0][1])/(last[0]-coordinates[0][0]);
        }
        for(int i=2;i<coordinates.Length;i++){
            if(zero){
                if(last[0]-coordinates[i][0]!=0){
                    return false;
                }
            }
            else if((last[0]-coordinates[i][0])==0){
                return false;
            }
            else if((last[1]-coordinates[i][1])/(last[0]-coordinates[i][0])!=line){
                return false;
            }
            last=coordinates[i];
        }
        return true;
    }
}
```
```
Runtime
105 ms
Beats
67.72%
Memory
41.9 MB
Beats
32.28%
```
我的解法的基本想法是：首先算出最开始两个点的斜率，如果所有点能形成一条线，任意两点之间的斜率应该是相同的（所以排序到底是为了啥呢？个人认为的答案写在上面了，不过不确定）。用的公式是 $slope=\frac{y_1-y_0}{x_1-x_0}$ 。代码里判断是否除以0很麻烦，能不能使用没有除法的公式？
```c#
//https://leetcode.com/problems/check-if-it-is-a-straight-line/solutions/408984/java-python-3-check-slopes-short-code-w-explanation-and-analysis/
public class Solution {
    public bool CheckStraightLine(int[][] coordinates) {
        int x0 = coordinates[0][0], y0 = coordinates[0][1], 
            x1 = coordinates[1][0], y1 = coordinates[1][1];
        int dx = x1 - x0, dy = y1 - y0;
        foreach(int[] co in coordinates) {
            int x = co[0], y = co[1];
            if (dx * (y - y1) != dy * (x - x1))
                return false;
        }
        return true;
    }
}
```
```
Runtime
96 ms
Beats
94.49%
Memory
41.7 MB
Beats
62.99%
```
把基础款公式变形一下就行了。

$y-y_1=m(x-x_1)$<br>
$y-y_1=(\frac{\Delta y}{\Delta x})(x-x_1)$<br>
$\Delta x(y-y_1)=\Delta y(x-x_1)$

在程序一开始获取前两个点的dy和dx以及其中一个点的x和y坐标作为参考，剩下的就是一个一个算比较了。最后是升级版：一次检查3个点。平面上，如果3个点形成一条直线，则这3个点形成的三角形面积为0。
```c#
//https://leetcode.com/problems/check-if-it-is-a-straight-line/solutions/408968/check-collinearity/
public class Solution {
     public bool CheckStraightLine(int[][] coordinates) {
        int n = coordinates.Length;
        for(int end=0;end<=n-3;end++) {
            int[] c1 = coordinates[end];
            int[] c2 = coordinates[end+1];
            int[] c3 = coordinates[end+2];
            if(!isCollinear(c1[0],c1[1],c2[0],c2[1],c3[0],c3[1])) {
                return false;
            }
        }
        return true;
    }

    private bool isCollinear(int x1, int y1, int x2,int y2, int x3, int y3) {
        int result = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
        return result==0;
    }
}
```
```
Runtime
95 ms
Beats
96.85%
Memory
41.9 MB
Beats
48.3%
```