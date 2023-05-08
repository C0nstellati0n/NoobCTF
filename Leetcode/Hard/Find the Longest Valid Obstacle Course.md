# Find the Longest Valid Obstacle Course at Each Position

[题目](https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/description/)

这题的答案看了老半天都不太懂。

```c#
//https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/solutions/1390162/java-c-python-mono-increasing-stack/
public class Solution {
        public int[] LongestObstacleCourseAtEachPosition(int[] A) {
        int n = A.Length, Length = 0;
        int[] res= new int[n];
        int[] mono = new int[n];
        for (int i = 0; i < n; ++i) {
            int l = 0, r = Length;
            while (l < r) {
                int m = (l + r) / 2;
                if (mono[m] <= A[i]) //感觉关键点在于比较的是mono
                    l = m + 1;
                else
                    r = m;
            }
            res[i] = l + 1;
            if (Length == l)
                Length++;
            mono[l] = A[i]; //l处为A[i]，表示当前数字代表的最长递增序列到l
        }
        return res;
    }
}
```

```
Runtime
422 ms
Beats
50%
Memory
63.2 MB
Beats
25%
```