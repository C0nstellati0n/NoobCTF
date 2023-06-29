# Shortest Path to Get All Keys

[题目](https://leetcode.com/problems/shortest-path-to-get-all-keys/description/)

你甚至可以在leetcode学游戏相关算法。这题可以说是bfs的究极形态了，多维state+bit mask，这题搞懂了还有啥bfs做不出来？
```c#
//https://leetcode.com/problems/shortest-path-to-get-all-keys/solutions/146878/java-bfs-solution/
class Solution {
    class State {
        public int keys, i, j;
        public State(int keys, int i, int j) {
            this.keys = keys;
            this.i = i;
            this.j = j;
        }
    }
    public int ShortestPathAllKeys(string[] grid) {
        int x = -1, y = -1, m = grid.Length, n = grid[0].Length, max = -1;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                char c = grid[i][j];
                if (c == '@') { //先找到初始的坐标
                    x = i;
                    y = j;
                }
                if (c >= 'a' && c <= 'f') {
                    max = Math.Max(c - 'a' + 1, max); //计算总共有多少key
                }
            }
        }
        State start = new State(0, x, y); //state记录：拥有的钥匙，当前坐标
        Queue<State> q = new(); //普通的bfs根据坐标判断是否已访问，这里通过state，那么就允许了普通bfs不允许的格子重复访问
        HashSet<string> visited = new();
        visited.Add($"0 {x} {y}");
        q.Enqueue(start);
        int[][] dirs = new int[][]
        {
            new int[]{0, 1}, 
            new int[]{1, 0}, 
            new int[]{0, -1}, 
            new int[]{-1, 0}
        };
        int step = 0;
        while (q.Count!=0) {
            int size = q.Count;
            while (size-- > 0) { //这个结构就有点像多源bfs了，一层一层地遍历。很多找最短路径的算法都用多源bfs，方便计算step
                State cur = q.Dequeue();
                if (cur.keys == (1 << max) - 1) { //如果当前已获得全部的key，就能直接返回结果了
                    return step;
                }
                foreach(int[] dir in dirs) {
                    int i = cur.i + dir[0];
                    int j = cur.j + dir[1];
                    int keys = cur.keys;
                    if (i >= 0 && i < m && j >= 0 && j < n) {
                        char c = grid[i][j];
                        if (c == '#') { //墙就continue，无法继续往这个方向走
                            continue;
                        }
                        if (c >= 'a' && c <= 'f') { //key就捡起来
                            keys |= 1 << (c - 'a'); //keys使用bitmask记录
                        }
                        if (c >= 'A' && c <= 'F' && ((keys >> (c - 'A')) & 1) == 0) { //锁就检查有没有对应的key。没有则continue，无法继续往这个方向走
                            continue;
                        }
                        if (!visited.Contains($"{keys} {i} {j}")) { //若之前没有达到过这个状态，则将状态加入队列
                            visited.Add($"{keys} {i} {j}"); //i和j可能相同，但只要keys不同，相同的格子就会被重复访问
                            q.Enqueue(new State(keys, i, j));
                        }
                    }
                }
            }
            step++;
        }
        return -1;
    }
}
```
```
Runtime
179 ms
Beats
53.85%
Memory
60.9 MB
Beats
38.46%
```
[editorial](https://leetcode.com/problems/shortest-path-to-get-all-keys/editorial/)也是差不多的思路。这么分析下来感觉也不是太难，hard主要还是因为每个点都难想出来。解出此题的关键点如下：
1. 判断一个地方是否可走。墙好判断，可是锁方块是否能走取决于我们有没有对应的key。需要找个方法记录已有的key
2. bfs无法往回走。此题可能会出现往回走的情况，因为之前的锁方格在我们获取到对应的钥匙后就能走了。这个“回头走”怎么实现？就算实现了，到底什么时候才能回头走？

解决方法如下：
1. 使用bitmask。将一个数用二进制表示，如`1101`。每i位表示我们是否有对应的key。1101对应DCBA，表示我们有D，C和A key。添加key用按位或，代码里的`c-'a'`是为了将索引置为0。判断是否有key则用按位与。
2. 使用State。visited数组不再通过格子的坐标判断是否来过，而是通过格子坐标+拥有的key判断。只要key数量不同，相同的格子坐标也可能再次入队列。只要入了队列，就相当于是“回头走”。无需担心无限循环，走到最后key的状态一定就固定了。

最后，我在采样区发现了一个表现超级逆天的算法。思路差不多，不过内容不如上一个简洁，甚至可以说繁琐，然而真的快。
```c#
public class Solution
{
    public int ShortestPathAllKeys(string[] grid)
    {
        var m = grid.Length;
        var n = grid[0].Length;
        var cKey = 0;
        var startI = 0;
        var startJ = 0;
        for (var i = 0; i < m; ++i)
        {
            for (var j = 0; j < n; ++j)
            {
                if (grid[i][j] >= 'a' && grid[i][j] <= 'f')
                {
                    cKey++;
                }
                if (grid[i][j] == '@')
                {
                    startI = i;
                    startJ = j;
                }
            }
        }
        var visited = new bool[m * n * (int)Math.Pow(2, cKey)];
        var q = new Queue<State>();
        q.Enqueue(new State { Moves = 0, I = startI, J = startJ, Key1 = false, Key2 = false, Key3 = false, Key4 = false, Key5 = false, Key6 = false });
        while (q.TryDequeue(out State cur))
        {
            if (Process(q, grid, visited, cur.Move(1, 0), m, n, cKey) ||  // right
            Process(q, grid, visited, cur.Move(-1, 0), m, n, cKey) || // left
            Process(q, grid, visited, cur.Move(0, -1), m, n, cKey) || // up
            Process(q, grid, visited, cur.Move(0, 1), m, n, cKey))  // down
            {
                return cur.Moves + 1;
            }
        }
        return -1;
    }

    private int GetStateIndex(State state, int m, int n)
    {
        var ret = state.I + state.J * m;
        var kBase = m * n;
        if (state.Key1)
        {
            ret += kBase;
        }
        kBase *= 2;
        if (state.Key2)
        {
            ret += kBase;
        }
        kBase *= 2;
        if (state.Key3)
        {
            ret += kBase;
        }
        kBase *= 2;
        if (state.Key4)
        {
            ret += kBase;
        }
        kBase *= 2;
        if (state.Key5)
        {
            ret += kBase;
        }
        kBase *= 2;
        if (state.Key6)
        {
            ret += kBase;
        }
        return ret;
    }

    private bool Process(Queue<State> q, string[] grid, bool[] visited, State state, int m, int n, int cKey)
    {
        if (state.I < 0 || state.I >= m || state.J < 0 || state.J >= n) return false;
        var ch = grid[state.I][state.J];
        if (ch == '#') return false;
        var idx = GetStateIndex(state, m, n);
        if (visited[idx]) return false;
        visited[idx] = true;
        var upgraded = false;
        switch (ch)
        {
            case 'a':
                if (!state.Key1)
                {
                    upgraded = true;
                    state.Key1 = true;
                }
                break;
            case 'b':
                if (!state.Key2)
                {
                    upgraded = true;
                    state.Key2 = true;
                }
                break;
            case 'c':
                if (!state.Key3)
                {
                    upgraded = true;
                    state.Key3 = true;
                }
                break;
            case 'd':
                if (!state.Key4)
                {
                    upgraded = true;
                    state.Key4 = true;
                }
                break;
            case 'e':
                if (!state.Key5)
                {
                    upgraded = true;
                    state.Key5 = true;
                }
                break;
            case 'f':
                if (!state.Key6)
                {
                    upgraded = true;
                    state.Key6 = true;
                }
                break;
            case 'A':
                if (!state.Key1) return false;
                break;
            case 'B':
                if (!state.Key2) return false;
                break;
            case 'C':
                if (!state.Key3) return false;
                break;
            case 'D':
                if (!state.Key4) return false;
                break;
            case 'E':
                if (!state.Key5) return false;
                break;
            case 'F':
                if (!state.Key6) return false;
                break;
        }
        if (upgraded)
        {
            idx = GetStateIndex(state, m, n);
            if (visited[idx]) return false;
            visited[idx] = true;
        }
        if (state.HasAllKeys(cKey))
        {
            return true;
        }
        q.Enqueue(state);
        return false;
    }

    private struct State
    {
        public int Moves;
        public int I;
        public int J;
        public bool Key1;
        public bool Key2;
        public bool Key3;
        public bool Key4;
        public bool Key5;
        public bool Key6;

        public bool HasAllKeys(int cKey)
        {
            return cKey == (Key1 ? 1 : 0)
            + (Key2 ? 1 : 0)
            + (Key3 ? 1 : 0)
            + (Key4 ? 1 : 0)
            + (Key5 ? 1 : 0)
            + (Key6 ? 1 : 0);
        }

        public State Move(int i, int j)
        {
            return new State
            {
                Moves = this.Moves + 1,
                I = this.I + i,
                J = this.J + j,
                Key1 = this.Key1,
                Key2 = this.Key2,
                Key3 = this.Key3,
                Key4 = this.Key4,
                Key5 = this.Key5,
                Key6 = this.Key6,
            };
        }
    }
}
```
```
Runtime
97 ms
Beats
100%
Memory
39.5 MB
Beats
100%
```