# Detonate the Maximum Bombs

[题目](https://leetcode.com/problems/detonate-the-maximum-bombs/description/)

万物皆可图表。我压根没看出来这题是个有序图表。既然扯到图表了，自然就是bfs/dfs了。union find只能在无序图表使用。

```c#
//https://leetcode.com/problems/detonate-the-maximum-bombs/solutions/1623333/bfs-or-dfs/
public class Solution {
    int dfs(int i, List<List<int>> al, bool[] detonated) {
        if (!detonated[i]) {
            detonated[i] = true;
            foreach(int j in al[i])
                dfs(j, al, detonated);
        }
        return detonated.Count(c=>c);
    }
    public int MaximumDetonation(int[][] bs) {
        int res = 0, sz = bs.Length;
        List<List<int>> al=new();
        for (int i = 0; i < sz; ++i) {
            al.Add(new());
            long x = bs[i][0];
            long y = bs[i][1];
            long r2 = (long)bs[i][2] * bs[i][2];
            for (int j = 0; j < bs.Length; ++j){
                if ((x - bs[j][0]) * (x - bs[j][0]) + (y - bs[j][1]) * (y - bs[j][1]) <= r2){
                    al[i].Add(j);
                }
            }
        }
        for (int i = 0; i < sz && res < sz; ++i)
            res = Math.Max(dfs(i, al, new bool[100]), res);
        return res;
    }
}
```
```
Runtime
388 ms
Beats
25.72%
Memory
53.9 MB
Beats
54.29%
```
bfs表现要好一点。
```c#
//https://leetcode.com/problems/detonate-the-maximum-bombs/solutions/1897718/java-bfs-dfs-with-comments-easy/
public class Solution {
    public int MaximumDetonation(int[][] bombs) {
        int max = 0;
        //iterate through each bomb and keep track of max
        for(int i = 0; i<bombs.Length; i++){
            max = Math.Max(max, getMaxBFS(bombs, i));    
        }
        return max;
    }
    
    private int getMaxBFS(int[][] bombs, int index){
        Queue<int> queue = new();
        bool[] seen = new bool[bombs.Length];
        
        seen[index] = true;
        queue.Enqueue(index);
        
        int count = 1; // start from 1 since the first added bomb can detonate itself
        
        while(queue.Count!=0){
            int currBomb = queue.Dequeue();
            for(int j = 0; j<bombs.Length; j++){ //search for bombs to detonate
                if(!seen[j] && isInRange(bombs[currBomb], bombs[j])){
                    seen[j] = true;
                    count++;
                    queue.Enqueue(j);
                }
            }
        }
        
        return count;
    }
    
    //use the distance between two points formula
    //then check if curr bomb radius is greater than the distance; meaning we can detonate the second bombs
    private bool isInRange(int[] point1, int[] point2) {
        long dx = point1[0] - point2[0], dy = point1[1] - point2[1], radius = point1[2];
        long distance =  dx * dx + dy * dy;
        return distance <= radius * radius;
    }
}
```
```
Runtime
195 ms
Beats
80%
Memory
44.5 MB
Beats
71.43%
```
这题的难度在于看出潜在的有序图表。至于bfs和dfs，我忘了怎么数连接起来的node了，现在记:)