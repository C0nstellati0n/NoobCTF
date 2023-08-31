# Minimum Number of Taps to Open to Water a Garden

[题目](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/description/)

有点难受。死在了第34/39个testcase。我明明完全跟着hint来做的，最后不知道为啥莫名其妙比正确答案多了一个。
```c#
//https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/editorial/
class Solution {
    public int MinTaps(int n, int[] ranges) {
        // Create an array to track the maximum reach for each position
        int[] maxReach = new int[n + 1];
        // Calculate the maximum reach for each tap
        for (int i = 0; i < ranges.Length; i++) {
            // Calculate the leftmost position the tap can reach
            int start = Math.Max(0, i - ranges[i]);
            // Calculate the rightmost position the tap can reach
            int end = Math.Min(n, i + ranges[i]);
            // Update the maximum reach for the leftmost position
            maxReach[start] = Math.Max(maxReach[start], end);
        }
        // Number of taps used
        int taps = 0;
        // Current rightmost position reached
        int currEnd = 0;
        // Next rightmost position that can be reached
        int nextEnd = 0;
        // Iterate through the garden
        for (int i = 0; i <= n; i++) {
            // Current position cannot be reached
            if (i > nextEnd) {
                return -1;
            }
            // Increment taps when moving to a new tap
            if (i > currEnd) {
                taps++;
                // Move to the rightmost position that can be reached
                currEnd = nextEnd;
            }
            // Update the next rightmost position that can be reached
            nextEnd = Math.Max(nextEnd, maxReach[i]);
        }
        // Return the minimum number of taps used
        return taps;
    }
}
```
```
Runtime
80 ms
Beats
100%
Memory
42.3 MB
Beats
46.15%
```
editorial还有个dp做法。经典又不好理解又不如greedy。