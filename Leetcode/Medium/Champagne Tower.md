# Champagne Tower

[题目](https://leetcode.com/problems/champagne-tower)

除以2.我竟然没看出来就是个简单的除以2？
```c#
//采样区。这道题editorial的写法不是最好的
//这个做法我觉得类似 https://leetcode.com/problems/champagne-tower/solutions/1817822/java-simple-explained
public class Solution {
    public double ChampagneTower(int poured, int query_row, int query_glass) {
        double[] cur = new double[]{poured};
        while(query_row-- > 0){
            double[] tmp = new double[cur.Length + 1]; //杯子一层一层往下叠，下一层杯子的数量是上一层+1
            tmp[0] = tmp[tmp.Length - 1] = Math.Max((cur[0] - 1) / 2,0); //这一层两边的杯子=上层两边的杯子中的酒数量-1（上一层杯子占掉了1，杯子满了才会溢出）/2（溢出的酒平均地流到两边）
            for(int i = 1;i < tmp.Length - 1;i++){
                tmp[i] = Math.Max((cur[i - 1] - 1) / 2,0) + Math.Max((cur[i] - 1) / 2,0); //中间的杯子的酒由左上和右上流下，所以是+（区别于两旁的杯子只有一个杯子中的酒会留下来）
            }
            cur = tmp;
        }
        return Math.Min(1,cur[query_glass]); //一个杯子最多装1个单位的酒
    }
}
```
```
Runtime
14 ms
Beats
97.22%
Memory
29.5 MB
Beats
100%
```
现在看来我没看出来的似乎不是除以2，而是中间杯子的累加。