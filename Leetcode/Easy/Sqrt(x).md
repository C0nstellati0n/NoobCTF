# Sqrt(x)

[题目](https://leetcode.com/problems/sqrtx/description/)

自己实现一个开方算法，不能使用语言自带的函数。想到binary search，不过没有一下子写出来，还是瞄了一眼答案才写出来的。

```c#
public class Solution {
    public int MySqrt(int x) {
        if(x==0) return 0;
        int low=1;
        int high=x/2; //注意这里high是x/2，与接下来的变体区分
        int mid;
        while(low<=high){
            mid=low + (high-low)/2;
            if(x/mid==mid){ //最开始是mid*mid==x，溢出了，后面才知道可以用除法
                return mid;
            }
            if(x/mid<mid){     
                high=mid-1; 
            }
            else{
                if(x/(mid+1)<(mid+1)){ //这段不能去，去掉了当x=1就会出错误解
                    return mid;
                }
                low=mid+1;      
            }
        }
        return low;
    }
}
```

```
Runtime
23 ms
Beats
85.21%
Memory
26.6 MB
Beats
72.52%
```

更多人用的是下面的写法：

```c#
public class Solution {
    public int MySqrt(int x) {
        if (x == 0) {
            return 0;
        }
        int first = 1, last = x; //这里的last相当于上一个算法的high
        while (first <= last) {
            int mid = first + (last - first) / 2;
            if (mid == x / mid) {
                return mid;
            } else if (mid > x / mid) {
                last = mid - 1;
            } else {
                first = mid + 1;
            }
        }
        return last;
    }
}
```

```
Runtime
20 ms
Beats
95.11%
Memory
26.9 MB
Beats
17.33%
```

两种方法的区别在于high变量的初始赋值。如果选择赋值为x/2，就要多增加一个if语句;直接赋值为x则没有那么多顾虑，也不会慢（我想太多了）。接下来的解法跳出二分法的限制，还带我认识了c#里的ulong,

```c#
public class Solution {
    public int MySqrt(int x) {
        // Initializing variables 
        ulong y=0,i=3,cnt=0;
    
        //loop until y is greater than x
        while((ulong)x>y){
            y+=i;
            i+=2;
            cnt++;
        }

        // return cnt as the square root of x
        return (int)cnt;
    }
}
```

```
Runtime
25 ms
Beats
76.21%
Memory
26.8 MB
Beats
37.38%
```

这种解法根据完全平方数（1，4，9，16...）之间的规律找平方根。算法中cnt是最后的结果，y是完全平方数，i是相邻完全平方数之间的差值。