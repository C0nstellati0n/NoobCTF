# Boats to Save People

[题目](https://leetcode.com/problems/boats-to-save-people/description/)

我以为这个题目只在第一层，没想到我在-3层。翻了dicussion知道要排序数组，但是没想到搭配时要用two pointers。基本的two pointers实现如下：

```c#
//https://leetcode.com/problems/boats-to-save-people/solutions/1877945/java-c-a-very-easy-explanation-trust-me/
class Solution {
    public int NumRescueBoats(int[] people, int limit) {
        int boatCount = 0;
        Array.Sort(people);
        
        int left = 0;
        int right = people.Length - 1;
        
        while(left <= right){
            int sum = people[left] + people[right];
            if(sum <= limit){
                boatCount++;
                left++;
                right--;
            }
            else{
                boatCount++;
                right--;
            }
        }
        return boatCount;
    }
}
```

```
Runtime
161 ms
Beats
91.95%
Memory
49 MB
Beats
90.80%
```

还能继续优化，不过是在排序上下手，把Array.Sort扔掉，自己写个排序。

```c#
//https://leetcode.com/problems/boats-to-save-people/solutions/3372503/image-explanation-brute-better-optimal-c-java-python/
class Solution {
    public int NumRescueBoats(int[] people, int limit) {
        int[] count = new int[limit+1];
        foreach(int p in people) count[p]++;

        int idx = 0;
        for(int val=1; val<=limit; val++){
            while(count[val]-- > 0)
                people[idx++] = val;
        }
        
        int boatCount = 0, left = 0, right = people.Length - 1;
        while(left <= right){
            if(people[left] + people[right] <= limit){
                left++;
                right--;
            }
            else{
                right--;
            }
            boatCount++;
        }
        return boatCount;
    }
}
```

```
Runtime
147 ms
Beats
100%
Memory
47.5 MB
Beats
96.55%
```