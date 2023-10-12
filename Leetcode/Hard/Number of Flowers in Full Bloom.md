# [Number of Flowers in Full Bloom](https://leetcode.com/problems/number-of-flowers-in-full-bloom)

上周的我：哇好多easy！谢谢你leetcode！

leetcode：来，多放松一下，因为……

我（警觉）：？？？

leetcode：猜猜看今天是easy还是medium呢？

我：medium吧，都这么多easy了

leetcode：不对！猜错了！今天是hard（甩给我一个hard），明天也是hard（砸在我脸上），后天还是hard！

我：看答案吧寄了

discussion：“诶我觉得这些hard都不是很难”，“这个应该算medium吧？”

我：冲！

leetcode：爬！不是说你！

求：请问我是什么精神状态？
```c#
//https://leetcode.com/problems/number-of-flowers-in-full-bloom/editorial
//Approach 3: Simpler Binary Search
//其实Approach 2有新的知识点：line sweep。但是没改成功……什么java的treemap没法用sorteddict替代吗？
class Solution {
    public int[] FullBloomFlowers(int[][] flowers, int[] people) {
        List<int> starts = new();
        List<int> ends = new();
        foreach(int[] flower in flowers) {
            starts.Add(flower[0]);
            ends.Add(flower[1] + 1);
        }
        starts.Sort();
        ends.Sort();
        int[] ans = new int[people.Length];
        for (int index = 0; index < people.Length; index++) {
            int person = people[index];
            int i = binarySearch(starts, person);
            int j = binarySearch(ends, person);
            ans[index] = i - j;
        }
        return ans;
    }
    public int binarySearch(List<int> arr, int target) {
        int left = 0;
        int right = arr.Count;
        while (left < right) {
            int mid = (left + right) / 2;
            if (target < arr[mid]) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }
}
```
```
Runtime
346 ms
Beats
100%
Memory
66.5 MB
Beats
87.50%
```
其实hint说的很明白了，遍历people的所有时间，用binary search找所有在这之前开的花的数量，减去所有在这之前凋谢的花的数量，就是当前时间能看到的所有花的总数。所以在这之前要分别提取花的开放时间和凋谢时间构成两个数组，分别排序和binary search

line sweep则要用个differnce排序字典（treemap）。遍历flowers，difference[start]++,difference[end]--，代表start处开了一朵花，可以多看到一朵；end处则凋谢了一朵花，少看一朵。来个positions，内容为difference所有的key（即代表某朵花开放/凋谢的关键点）。然后是prefix，慢慢累加difference[key]，用于优化，不然一个一个算肯定TLE。最后遍历people，利用binary search找到合适的position，prefix[position]就是答案