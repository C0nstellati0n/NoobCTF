# Top K Frequent Elements

[题目](https://leetcode.com/problems/top-k-frequent-elements/description/)

看题目还以为挺简单的，还是高估了自己的实力。做法是bucket sort。

```c#
//https://leetcode.com/problems/top-k-frequent-elements/solutions/81602/java-o-n-solution-bucket-sort/
public class Solution {
    public int[] TopKFrequent(int[] nums, int k) {
        List<int>[] bucket = new List<int>[nums.Length + 1];
        Dictionary<int, int> frequencyDictionary = new();
        foreach(int n in nums) {
            frequencyDictionary[n]=frequencyDictionary.GetValueOrDefault(n, 0) + 1;
        }
        foreach(var pair in frequencyDictionary) {
            int frequency = pair.Value;
            if (bucket[frequency] == null) {
                bucket[frequency] = new();
            }
            bucket[frequency].Add(pair.Key);
        }
        List<int> res = new();
        for (int pos = bucket.Length - 1; pos >= 0 && res.Count < k; pos--) {
            if (bucket[pos] != null) {
                res.AddRange(bucket[pos]);
            }
        }
        return res.ToArray();
    }
}
```
```
Runtime
138 ms
Beats
99.23%
Memory
46.4 MB
Beats
33.17%
```
也能用sortedDictionary。
```c#
//https://leetcode.com/problems/top-k-frequent-elements/solutions/81635/3-java-solution-using-array-maxheap-treemap/
//原解法使用treemap，在c#里最像的是sortedDictionary。链接里还有个heap做法，但是没改出来
public class Solution {
    public int[] TopKFrequent(int[] nums, int k) {
        Dictionary<int, int> map = new();
        foreach(int n in nums){
            map[n]=map.GetValueOrDefault(n,0)+1;
        }
        SortedDictionary<int, List<int>> freqMap = new();
        foreach(var num in map){
           int freq = num.Value;
           if(!freqMap.ContainsKey(freq)){
               freqMap[freq]=new();
           }
           freqMap[freq].Add(num.Key);
        }
        List<int> res = new();
        while(res.Count<k){
            res.AddRange(freqMap[freqMap.Keys.Last()]);
            freqMap.Remove(freqMap.Keys.Last());
        }
        return res.ToArray();
    }
}
```
```
Runtime
153 ms
Beats
82.26%
Memory
46.1 MB
Beats
55.3%
```
介绍一下bucket sort。
```
Bucket sort is a sorting algorithm that divides the unsorted array elements into several groups called buckets. Each bucket is then sorted by using any of the suitable sorting algorithms or recursively applying the same bucket algorithm. Finally, the sorted buckets are combined to form a final sorted array.

Bucket sort can be exceptionally fast because of the way elements are assigned to buckets, typically using an array where the index is the value.

Bucket sort is mainly useful when input is uniformly distributed over a range.

Bucket sort is not useful if we have a large array because it increases the cost.

It is not an in-place sorting algorithm, because some extra space is required to sort the buckets.

The basic procedure of performing the bucket sort is as follows:

Create n empty buckets.
Scatter the elements of the array into the buckets.
Sort each bucket individually by applying a sorting algorithm.
Gather the sorted elements from each bucket in order.
The time complexity of bucket sort is O(n + k), where n is the number of elements and k is the number of buckets. The Auxiliary Space of bucket sort is O(n + k). This is because we need to create a new array of size k to store the buckets and another array of size n to store the sorted elements.
```