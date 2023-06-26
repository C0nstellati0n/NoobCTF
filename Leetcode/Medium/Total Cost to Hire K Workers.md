# Total Cost to Hire K Workers

[题目](https://leetcode.com/problems/total-cost-to-hire-k-workers/description/)

我的代码除了不好看+没法ac之外，就没什么别的缺点了。
```c#
//https://leetcode.com/problems/total-cost-to-hire-k-workers/solutions/3683067/beats-100-c-java-python-beginner-friendly/
class Solution {
    public long TotalCost(int[] costs, int k, int candidates) {
        int i = 0;
        int j = costs.Length - 1;
        PriorityQueue<int,int> pq1 = new(Comparer<int>.Create((x, y) => x-y));
        PriorityQueue<int,int> pq2 = new(Comparer<int>.Create((x, y) => x-y));
        long ans = 0;
        while (k-- > 0) {
            //这种index时刻在变的果然还是用while更好。用for循环的话疯狂判断边界，错了还找不出来
            while (pq1.Count < candidates && i <= j) {
                pq1.Enqueue(costs[i],costs[i]);
                i++;
            }
            while (pq2.Count < candidates && i <= j) { //i<=j保证两个heap不添加重复的元素
                pq2.Enqueue(costs[j],costs[j]);
                j--;
            }
            int t1 = pq1.Count > 0 ? pq1.Peek() : Int32.MaxValue; //保证不超heap的界
            int t2 = pq2.Count > 0 ? pq2.Peek() : Int32.MaxValue;
            if (t1 <= t2) {
                ans += t1;
                pq1.Dequeue();
            } else {
                ans += t2;
                pq2.Dequeue();
            }
        }
        return ans;
    }
}
```
```
Runtime
236 ms
Beats
78.85%
Memory
52.2 MB
Beats
73.8%
```
当然硬要只用1个heap也是可以的。
```c#
//https://leetcode.com/problems/total-cost-to-hire-k-workers/editorial/
class Solution {
    public long TotalCost(int[] costs, int k, int candidates) {
        // The worker with the lowest cost has the highest priority, if two players has the
        // same cost, break the tie by their indices (0 or 1).
        PriorityQueue<int[],int[]> pq = new(Comparer<int[]>.Create((a, b) => {
            if (a[0] == b[0]) {
                return a[1] - b[1];
            }
            return a[0] - b[0];}));
        
        // Add the first k workers with section id of 0 and 
        // the last k workers with section id of 1 (without duplication) to pq.
        for (int i = 0; i < candidates; i++) {
            pq.Enqueue(new int[] {costs[i], 0},new int[] {costs[i], 0});
        }
        for (int i = Math.Max(candidates, costs.Length - candidates); i < costs.Length; i++) {
            pq.Enqueue(new int[] {costs[i], 1},new int[] {costs[i], 1});
        }

        long answer = 0;
        int nextHead = candidates;
        int nextTail = costs.Length - 1 - candidates;

        for (int i = 0; i < k; i++) {
            int[] curWorker = pq.Dequeue();
            int curCost = curWorker[0], curSectionId = curWorker[1];
            answer += curCost;
            
            // Only refill pq if there are workers outside.
            if (nextHead <= nextTail) {
                if (curSectionId == 0) {
                    pq.Enqueue(new int[]{costs[nextHead], 0},new int[]{costs[nextHead], 0});
                    nextHead++;
                } else {
                    pq.Enqueue(new int[]{costs[nextTail], 1},new int[]{costs[nextTail], 1});
                    nextTail--;
                }
            }
        }

        return answer;
    }
}
```
```
Runtime
295 ms
Beats
34.61%
Memory
58 MB
Beats
5.77%
```