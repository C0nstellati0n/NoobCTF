# Find Smallest Letter Greater Than Target

[题目](https://leetcode.com/problems/find-smallest-letter-greater-than-target/description/)

leetcode出问题了，怎么连续几天都这么简单？

```c#
public class Solution {
    public char NextGreatestLetter(char[] letters, char target) {
        foreach(char letter in letters){
            if(letter>target){
                return letter;
            }
        }
        return letters[0];
    }
}
```
```
Runtime
106 ms
Beats
87.85%
Memory
44.9 MB
Beats
44.13%
```
上面的解法确实太无脑了，还是用binary search改进一下吧。
```c#
//https://leetcode.com/problems/find-smallest-letter-greater-than-target/solutions/110005/easy-binary-search-in-java-o-log-n-time/
public class Solution {
    public char NextGreatestLetter(char[] a, char x) {
        int n = a.Length;

        //hi starts at 'n' rather than the usual 'n - 1'. 
        //It is because the terminal condition is 'lo < hi' and if hi starts from 'n - 1', 
        //we can never consider value at index 'n - 1'
        int lo = 0, hi = n;

        //Terminal condition is 'lo < hi', to avoid infinite loop when target is smaller than the first element
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] > x)     hi = mid;
            else    lo = mid + 1;                 //a[mid] <= x
        }
 
        //Because lo can end up pointing to index 'n', in which case we return the first element
        return a[lo % n];
    }
}
```
```
Runtime
104 ms
Beats
93.12%
Memory
45.3 MB
Beats
9.31%
```