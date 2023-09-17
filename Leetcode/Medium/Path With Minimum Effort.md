# Path With Minimum Effort

[题目](https://leetcode.com/problems/path-with-minimum-effort)

这个算法怎么这么慢？这个算法怎么又这么快？
```c#
//https://leetcode.com/problems/path-with-minimum-effort/solutions/4049557/97-67-optimal-dijkstra-with-heap
public class Solution {
    public int MinimumEffortPath(int[][] heights) {
        int rows = heights.Length, cols = heights[0].Length;
        int[,] dist = new int[rows, cols]; //dist[i,j]记录目前最小的effort
        var minHeap = new SortedSet<(int effort, int x, int y)>(); //记录到(x,y)时的effort
        minHeap.Add((0, 0, 0));
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                dist[i, j] = int.MaxValue;
            }
        }
        dist[0, 0] = 0; 
        int[][] directions = new int[][] { new int[]{ 0, 1 }, new int[]{ 0, -1 }, new int[]{ 1, 0 }, new int[]{ -1, 0 }};
        while (minHeap.Count > 0) {
            var (effort, x, y) = minHeap.Min;
            minHeap.Remove(minHeap.Min);
            if (effort > dist[x, y]) continue; //若新的effort不如之前的，跳过
            if (x == rows - 1 && y == cols - 1) return effort; //若到达终点，返回目前的effort
            foreach (var dir in directions) {
                int nx = x + dir[0], ny = y + dir[1]; //访问当前(x,y)的所有邻居
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols) {
                    int new_effort = Math.Max(effort, Math.Abs(heights[x][y] - heights[nx][ny]));
                    if (new_effort < dist[nx, ny]) { //若新的effort小于之前记录的最小effort
                        dist[nx, ny] = new_effort;
                        minHeap.Add((new_effort, nx, ny)); //更新effort并添加至minHeap
                    }
                }
            }
        }
        return -1;
    }
}
```
```
Runtime
243 ms
Beats
40.12%
Memory
64.9 MB
Beats
38.37%
```
除了dijkstra，还有另外两种：Bellman Ford和Binary Search，参考 https://leetcode.com/problems/path-with-minimum-effort/solutions/909002/java-python-3-3-codes-binary-search-bellman-ford-and-dijkstra-w-brief-explanation-and-analysis 。binary search老朋友了，不再赘述，而且这题graph能用binary search完全是因为constraint里指出height最大就10的6次方。所以我们可以无脑去猜effort是多少，然后套到graph看这么多effort能不能走到终点。慢慢search就出来了。Bellman Ford我倒是改了，但是长的和dijkstra其实差不多，就是没用SortedSet而是普通的queue，导致非常慢，不如直接学dijkstra。

万能的采样区给出了最快答案。
```c#
public class Solution {
    public int MinimumEffortPath(int[][] heights) {
        int col = heights.Length;
        int row = heights[0].Length;
        int[,] ans = new int[col, row];
        int[] dirX = new int[]{0, 1, 0, -1};
        int[] dirY = new int[]{1, 0, -1, 0};
        for(int i = 0; i < col; i++){
            for(int j =0; j < row; j++){
                ans[i, j] = int.MaxValue;
            }
        }
        ans[0, 0] = 0;
        PriorityQueue<(int x, int y),int> pq = new PriorityQueue<(int disX, int disY),int>();
        pq.Enqueue((0, 0), 0);
        while(pq.Count > 0){
            var cur = pq.Dequeue();
            if(cur.x == col - 1 && cur.y == row - 1) break;
            for(int i = 0; i < 4; i++){
                int tempX = cur.x + dirX[i];
                int tempY = cur.y + dirY[i];
                if(tempX < 0 || tempX >= col || tempY < 0 || tempY >= row){
                    continue;
                }
                int comp = Math.Max(ans[cur.x, cur.y], Math.Abs(heights[tempX][tempY] - heights[cur.x][cur.y]));
                if(ans[tempX, tempY] > comp){
                    ans[tempX, tempY] = comp;
                    pq.Enqueue((tempX, tempY), comp);
                }
            }
        }
        return ans[col - 1, row - 1];
    }
}
```
```
Runtime
129 ms
Beats
100%
Memory
55.1 MB
Beats
69.77%
```
然后我就懵了，乍一看这思路不就和dijkstra差不多吗？不过用的是PriorityQueue，也没有专门记录effort，全部放ans里。以后留个心眼，这么做可以快很多。

都到这份上了不好好学学dijkstra就说不过去了。如果把dist数组看成visited，SortedSet看成queue，不就是bfs了吗？对啊为什么不直接用bfs呢？这是因为bfs找的最短路径是格子数最短的路径，而不是权重最短的路径。要是单纯用bfs的话，根本无法考虑此题特有的权重effort。更关键的是，bfs只会访问每个格子1次，而这道题访问相同格子的顺序不同是可能产生不同的effort的。所以要访问一个格子多次？这个多次是多少次？不可能无限不然就死循环了。我们只在产生的effort比之前更少时才会访问相同的格子。总不可能一直越来越小吧？这样便有了dijkstra的dist数组。同时优先考虑effort更少的格子，便有了sortedset。详细参考 https://leetcode.com/problems/path-with-minimum-effort/solutions/1000195/thought-process-from-naive-bfs-to-dijkstra