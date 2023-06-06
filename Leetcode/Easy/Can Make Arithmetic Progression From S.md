# Can Make Arithmetic Progression From Sequence

[题目](https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence/description/)

提示看错了，没看清楚就写了，导致两个wrong answer……
```c#
public class Solution {
    public bool CanMakeArithmeticProgression(int[] arr) {
        Array.Sort(arr);
        int num=arr[1]-arr[0];
        for(int i=2;i<arr.Length;i++){
            if(arr[i]-arr[i-1]!=num){
                return false;
            }
        }
        return true;
    }
}
```
这题可以挑战一下不用Sort，不过就是大佬们的活了。
```c#
//https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence/solutions/720152/o-n-time-o-1-space/
public class Solution {
    public bool CanMakeArithmeticProgression(int[] arr) {
        if (arr.Length <= 2) return true;
        int min = Int32.MaxValue, max = Int32.MinValue;
        foreach(int num in arr) {
            min = Math.Min(min, num);
            max = Math.Max(max, num);
        }
        if ((max - min) % (arr.Length - 1) != 0) return false;
        int d = (max - min) / (arr.Length - 1);

        int i = 0;
        while (i < arr.Length) {
            if (arr[i] == min + i * d) i++;
            else if ((arr[i] - min) % d != 0) return false;
            else {
                int pos = (arr[i] - min) / d;
                if (pos < i || arr[pos] == arr[i]) return false;
                Swap(i,pos,ref arr);
            }
        }
        return true;
    }
    void Swap(int i,int pos,ref int[] arr) {
        int tmp = arr[i];
        arr[i] = arr[pos];
        arr[pos] = tmp;
    }
}
```
```
Runtime
92 ms
Beats
90.91%
Memory
40.3 MB
Beats
86.93%
```
还可以用hashSet。
```c#
//https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence/solutions/720253/java-python-3-o-n-and-o-nlogn-codes-w-brief-explanation-and-analysis/
public class Solution {
    public bool CanMakeArithmeticProgression(int[] arr) {
        HashSet<int> seen = new();
        int mi = Int32.MaxValue, mx = Int32.MinValue, n = arr.Length;
        foreach(int a in arr) {
            mi = Math.Min(mi, a);
            mx = Math.Max(mx, a);
            seen.Add(a);
        }
        int diff = mx - mi;
        if (diff % (n - 1) != 0) {
            return false;
        }
        diff /= n - 1;
        while (--n > 0) {
            if (!seen.Contains(mi)) {
                return false;
            }
            mi += diff;
        }
        return true;
    }
}
```
```
Runtime
93 ms
Beats
89.20%
Memory
41.3 MB
Beats
5.68%
```