# [Sort Integers by The Number of 1 Bits](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits)

constraints不仔细看的下场
```c#
public class Solution {
    public int[] SortByBits(int[] arr) {
        List<int> ans=new();
        List<int>[] buckets=new List<int>[14]; //这里本来用的是字典的，但是意识到字典是无序的。那就用SortedDictionary吧，结果非常不好用。后面发现constraint说每个数字最多1e4，那14位bit足够了
        int temp;
        foreach(int num in arr){
            temp=BitOperations.PopCount((uint)num);
            if(buckets[temp]==null) buckets[temp]=new();
            buckets[temp].Add(num);
        }
        foreach(List<int> value in buckets){
            if(value==null) continue;
            value.Sort();
            ans.AddRange(value);
        }
        return ans.ToArray();
    }
}
```
除了用builtin计算bit 1的数量，还能自己实现
```c#
//https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits
//Approach 3: Brian Kerninghan's Algorithm
public class Solution {
    public int[] SortByBits(int[] arr) {
        Array.Sort(arr,Compare);
        return arr;
    }
    int Compare(int a,int b){
        if (FindWeight(a) == FindWeight(b)) {
            return a - b;
        }
        return FindWeight(a) - FindWeight(b);
    }
    int FindWeight(int num){
        int weight = 0;
        while (num > 0) {
            weight++;
            num &= (num - 1); //技巧在于num &= (num - 1)可以取到最后一个1 bit（last significant bit），比一个一个数字异或省了不少步骤
        }
        return weight;
    }
}
```