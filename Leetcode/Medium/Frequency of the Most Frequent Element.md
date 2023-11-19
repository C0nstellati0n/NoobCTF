# [Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element)

大家说counting sort做法只有O(n)复杂度，结果大家都用sliding window
```c++
//https://leetcode.com/problems/frequency-of-the-most-frequent-element/solutions/1175090/java-c-python-sliding-window
class Solution {
public:
    int maxFrequency(vector<int>& A, long k) {
        int i = 0, j;
        sort(A.begin(), A.end());
        for (j = 0; j < A.size(); ++j) {
            k += A[j];
            if (k < (long)A[j] * (j - i + 1)) //这里考虑A[j]，frequency为j - i + 1（window的大小）。A[j] * (j - i + 1)是使用k次增加操作后总共的值，k为实际的值。若总共的要求的值大于k，说明无法在k次操作内获取到(j - i + 1)个A[j],缩小window长度（但其实也没缩，因为后面j++补上了，所以只是不增加大小）
                k -= A[i++];
        }
        return j - i; //至于为什么最后一扇窗一定是最大的，参考评论区zengfei216的留言：the window size only increase when it's valid, it doesn't decrease when invalid, because we only care about max valid window size.
    }
};
```
[editorial](https://leetcode.com/problems/frequency-of-the-most-frequent-element/editorial)还有个binary search解法。前两种都和lee佬的一样