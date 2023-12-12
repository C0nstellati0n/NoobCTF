# [Element Appearing More Than 25% In Sorted Array](https://leetcode.com/problems/element-appearing-more-than-25-in-sorted-array)

```c++
class Solution {
public:
    int findSpecialInteger(vector<int>& arr) {
        for(int i=0;i<arr.size();i++){
            //在discussion区Shubham_Raj22那里看到的条件，后面发现editorial里也有讲到
            if(arr[i] == arr[i+arr.size()/4]) return arr[i];
        }
        return -1;
    }
};
```
另外一种值得说道的做法是binary search。假如一个元素出现次数大于25%，那么当我们把数组切为4份，至少有一个交界处会出现那个元素。于是考虑所有交界处的4个元素，利用binary search确定哪个是我们要找的目标。editorial用了lower_bound和upper_bound，也可以用equal_range：
```c++
//https://leetcode.com/problems/element-appearing-more-than-25-in-sorted-array/solutions/451286/java-binary-search 评论区StefanPochmann
class Solution {
public:
    int findSpecialInteger(vector<int>& arr) {
        int n = arr.size();
        for (int i : {n/4, n/2, n*3/4}) {
            auto p = equal_range(arr.begin(), arr.end(), arr[i]);
            if (p.second - p.first > n / 4)
                return arr[i];
        }
        return 0;
    }
};
```