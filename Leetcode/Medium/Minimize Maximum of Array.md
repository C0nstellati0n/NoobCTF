# Minimize Maximum of Array

[题目](https://leetcode.com/problems/minimize-maximum-of-array/description/)

原来不止我一个人看不懂这道题的描述。最简单也是最佳的做法如下：

```c#
//https://leetcode.com/problems/minimize-maximum-of-array/solutions/3381323/image-explanation-brute-better-o-nlogm-optimal-o-n-c-java-python/
class Solution {
    public int MinimizeArrayValue(int[] A) {
        long sum = 0, res = 0;
        for (int i = 0; i < A.Length; ++i) {
            sum += A[i];
            res = Math.Max(res, (sum + i) / (i + 1));//平均值
        }
        return (int)res;
    }
}
```

```
Runtime
196 ms
Beats
100%
Memory
55 MB
Beats
62.50%
```

根据题目描述里写的步骤“一个加一个减”，操作不会改变全部数字的总和。如果把满足1 <= i < n的索引全取一遍，最小的最大值只能是平均值。

```
Imagine having two number 5 10 . We need to decrease one and increase other, how would we minimize the maximum number among them? By Evenly distributing them! We can then take the ceiling of their average (10+5)/2 = 7.5 = 8 .

If there are three numbers, we need to take average of all of them and update our ans if it's bigger than the previously achieved answer, same for the whole array.

Take a prefix sum variable, an ans variable, iterate through the array from 1st index, keep finding the ceiling of average until current iteration and update the answer as ans = max(ans, (total+i)/(i+1)).

To summarize, we are evenly distributing all the elements so as to make the maximum[ceil of average] among them minimum, and keeping track of the maximum value as answer to return it.

Note: - Do a dry run to understand why total+i is done there to calculate ceil of average
```

不过根据题目的提示，似乎官方推荐的是binary search做法。

```c#
//https://leetcode.com/problems/minimize-maximum-of-array/solutions/3381375/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public bool check(int[] nums, int k) {
        // variable to keep track of how many moves we have
        long have = 0;
        // iterate over the array
        foreach(int n in nums) {
            // if the number is less than or equal to k, we don't need to do anything
            if (n <= k) {
                // add the number of moves needed to make it k to the total number of moves we have
                have += k - n;
            } else {
                // if the number is greater than k, we need to move some of its value to the previous element
                // check if we have enough moves left to make this move
                if (have < n - k)
                    return false;
                else
                    // if we have enough moves, subtract the number of moves needed to make this move from the total number of moves we have
                    have -= (n - k);
            }
        }
        // if we reach here, it means we were able to achieve a maximum value of k or less using the given number of moves
        return true;
    }

    public int MinimizeArrayValue(int[] nums) {
        // initialize left and right pointers for binary search
        int left = 0, right = nums.Max();
        // perform binary search to find the minimum possible value of the maximum integer of nums after performing any number of operations
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (check(nums, mid))
                right = mid;
            else
                left = mid + 1;
        }
        // return the minimum possible value of the maximum integer of nums after performing any number of operations
        return left;
    }
}
```

```
Runtime
216 ms
Beats
93.75%
Memory
54.9 MB
Beats
68.75%
```