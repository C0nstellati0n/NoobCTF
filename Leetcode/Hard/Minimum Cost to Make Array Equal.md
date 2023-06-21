# Minimum Cost to Make Array Equal

[题目](https://leetcode.com/problems/minimum-cost-to-make-array-equal/description/)

怎么大家都用c++写啊？有个用python的倒是能看懂语法，然而想用c#写出python内置函数的功能相对来说比较麻烦，尝试改写后总是会遇到莫名其妙的之前没见过的bug。罢了，直接把python摆出来得了。首先是binary search解法。
```c#
//https://leetcode.com/problems/minimum-cost-to-make-array-equal/solutions/2734162/java-c-python-binary-search/
public class Solution {
    private long findCost(int[] nums, int[] cost, long x) {
        long res = 0;
        for (int i = 0; i < nums.Length; i++){
            res += Math.Abs(nums[i] - x) * cost[i];
        }
        return res;
    }
    public long MinCost(int[] nums, int[] cost) {
        long left = 1;
        long right = 1000000;
        foreach(int num in nums) {
            left = Math.Min(num, left);
            right = Math.Max(num, right);
        }
        long ans = findCost(nums, cost, 1);
        while (left < right) {
            long mid = (left + right) / 2;
            long y1 = findCost(nums, cost, mid);
            long y2 = findCost(nums, cost, mid + 1);
            ans = Math.Min(y1, y2);
            if (y1 < y2){
                right = mid;
            }
            else{
                left = mid + 1;
            }
        }
        return ans;
    }
}
```
```
Runtime
152 ms
Beats
100%
Memory
52.2 MB
Beats
100%
```
然后是dp解法。
```c#
//https://leetcode.com/problems/minimum-cost-to-make-array-equal/solutions/2734091/dp-vs-w-median-vs-binary-search/
//java版在评论区里，众所周知java和c#是一家人。这里面还有dp等解法，包含了这道题常见的三种解法
class Solution {
    public long MinCost(int[] nums, int[] cost) {
        int n = nums.Length;
        int[][] data = new int[n][];
        for(int i=0;i<n;i++){
            data[i]=new int[2];
            data[i][0]=nums[i];
            data[i][1]=cost[i];
        }
        Array.Sort(data, (a,b)=>a[0]-b[0]);
        
        long[] l2rCost = new long[n+1];
        long costSum=0;
        for(int i=0;i<n-1;i++){
            costSum += data[i][1];
            l2rCost[i+1] = l2rCost[i]+ costSum*(data[i+1][0]-data[i][0]);
        }
        
        long[] r2lCost = new long[n+1];
        costSum=0;
        for(int i=n-1;i>0;i--){
            costSum+=data[i][1];
            r2lCost[i-1] = r2lCost[i] + costSum*(data[i][0]-data[i-1][0]);
        }
        
        long ans =Int64.MaxValue;
        for(int i=0;i<n;i++){
            ans = Math.Min(ans, l2rCost[i]+r2lCost[i]);
        }
        return ans;
    }
}
```
```
Runtime
160 ms
Beats
75%
Memory
55.3 MB
Beats
25%
```
最后是python的weighted-median解法。
```py
#https://leetcode.com/problems/minimum-cost-to-make-array-equal/solutions/2734183/python3-weighted-median-o-nlogn-with-explanations/
class Solution:
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        arr = sorted(zip(nums, cost))
        total, cnt = sum(cost), 0
        for num, c in arr:
            cnt += c
            if cnt > total // 2:
                target = num
                break
        return sum(c * abs(num - target) for num, c in arr)
```
```
Runtime
382 ms
Beats
98.53%
Memory
34.5 MB
Beats
45.59%
```
在看到这道题的第一眼我就感觉是个dp题。然而看hint和评论区后才发现更像是binary search题。有人说：`Whenever you confused regarding it will be dynamic programming or binary search you can check the value of n here it was 10^5 so obviously either some pre-computation or stack or binary search was there and then choose one out `，看来在样本数较大的情况下dp不一定是最优解。

然而在评论区的提示下，我还是没看出来这到底怎么是个binary search。binary search在我的印象里就是“两边夹击”：被搜寻的对象因为某种特性导致当排除某个答案后，其前面或者后面的数绝对不可能是解。所以这道题我就有点迷糊了，cost的值和nums里的数字我没看出来有什么规律，排除一个值后无法根据规律一起排除掉某个区间的值。既然找不到规律那就只能爆破了。不过爆破肯定会tle。直到第一个解里提到计算cost的函数`f(x)`是一个凸函数（函数开口向上），这种函数我们都知道，最底下有个顶点，那里肯定就是答案了。联想凸函数的图像，相信这时就能看出来能用binary search了（然而解法里说这是trinary search，没搜到）。

关于为什么cost函数是凸函数的证明：https://leetcode.com/problems/minimum-cost-to-make-array-equal/solutions/2734728/pure-math-based-explanation-of-why-cost-function-is-convex/