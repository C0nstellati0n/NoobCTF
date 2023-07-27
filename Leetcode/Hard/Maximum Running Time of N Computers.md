# Maximum Running Time of N Computers

[题目](https://leetcode.com/problems/maximum-running-time-of-n-computers/description/)

起猛了，竟然看见binary search是hard而且我还做不出来。[editorial](https://leetcode.com/problems/maximum-running-time-of-n-computers/editorial/)有两种方式，binary search和直接计算。感觉都值得说道说道。
```c#
class Solution {
    public long MaxRunTime(int n, int[] batteries) {
        // Get the sum of all extra batteries.
        Array.Sort(batteries); //从小到大排序电池
        long extra = 0;
        for (int i = 0; i < batteries.Length - n; i++) {
            extra += batteries[i]; //从最大的电池用起，所以把前length-n个电池作为extra
        }

        // live stands for the n largest batteries we chose for n computers.

        int[] live = batteries[(batteries.Length - n)..batteries.Length]; //使用最大的n个电池

        // We increase the total running time using 'extra' by increasing 
        // the running time of the computer with the smallest battery.
        for (int i = 0; i < n - 1; i++) {
            // If the target running time is between live[i] and live[i + 1].
            if (extra < (long)(i + 1) * (live[i + 1] - live[i])) {
                return live[i] + extra / (long)(i + 1);
            }

            // Reduce 'extra' by the total power used.
            extra -= (long)(i + 1) * (live[i + 1] - live[i]);
        }

        // If there is power left, we can increase the running time 
        // of all computers.
        return live[n - 1] + extra / n;
    }
}
```
```
Runtime
183 ms
Beats
100%
Memory
52.9 MB
Beats
100%
```
editorial有图，我反而没啥好补充的。不过我看完后还是有一个小问题：extra为什么可以直接加起来？举个例子，有[3,4,5,6]和3台电脑，那按照上面的逻辑，先把大的用了，那目前用的就是4，5，6，extra是3。进for循环，`extra>(0+1)*(4-3)`，所以可以匀，把3的一格电匀到4上，所以目前能同时运行5分钟，extra是2.然后我的问题来了，这时是第二次for循环,`extra=(1+1)*(5-4)`，第一个if语句的小于是不满足的，所以继续减，直到extra为0，第三次for循环时返回，结果为6。但是这第二次时怎么匀？虽然extra有两格电，但是总归是一个电池啊，有两台电脑要同时运行，这匀不动啊？

我重新看了一遍description。里面有一句话：`You may assume that the removing and inserting processes take no time.`。于是我有了个想法：上面的匀法，不会是两个电脑在那里疯狂拔插，每个电脑平均用无限小的时间，然后换成第二个电脑，无限循环（毕竟拔插不用时间）。虽然是无限小，但是也是有值的，最后收敛成2。相当于两台电脑用一个电池？但是不是说`After that and at any integer time moment, you can remove a battery from a computer and insert another battery any number of times.`，得是整数啊？

于是我又看了一遍。它没说一个电池不能多个电脑用，虽然example里都是一个电池一个电脑但确实没规定不能这么用。我想太多了。
```c#
class Solution {
    public long MaxRunTime(int n, int[] batteries) {
        long sumPower = 0;
        foreach(int power in batteries)
            sumPower += power;
        long left = 1, right = sumPower / n;
        
        while (left < right){
            long target = right - (right - left) / 2; //target是一台电脑的用电量
            long extra = 0;
            
            foreach(int power in batteries)
                extra += Math.Min(power, target); //这句最关键，若power小于target，用完全部power。若大于，只用到target。小于的情况很好理解，但是为什么大于只用到target呢？
                //感觉要结合上一种做法来看的话，这个大于target的power相当于上一种解法的live里最大的。这个值能算数的前提是比它更小的电池能匀上来。如果把它算进去的话，这个extra的值可能虚高

            if (extra >= (long)(n * target))
                left = target;
            else
                right = target - 1;
        }
        return left;
    }
}
```
```
Runtime
179 ms
Beats
100%
Memory
52.4 MB
Beats
100%
```