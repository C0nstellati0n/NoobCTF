# [K-th Smallest Prime Fraction](https://leetcode.com/problems/k-th-smallest-prime-fraction)

到底是谁看这题一眼就能做出来啊？trivial做法确实简单，但是这个binary search做法就太逆天了
```c++
//https://leetcode.com/problems/k-th-smallest-prime-fraction/editorial
class Solution {
public:
    vector<int> kthSmallestPrimeFraction(vector<int>& arr, int k) {
        int n = arr.size();
        double left = 0, right = 1.0; //根据题目描述，arr里所有要考虑的分数值在0到1之间
        // Binary search for finding the kth smallest prime fraction
        while (left < right){
            // Calculate the middle value
            double mid = (left + right) / 2;
            // Initialize variables to keep track of maximum fraction and indices
            double maxFraction = 0.0; //小于mid的分数里面最大的分数
            int totalSmallerFractions = 0, numeratorIdx = 0, denominatorIdx = 0;
            int j = 1;
            // Iterate through the array to find fractions smaller than mid
            for (int i = 0; i < n - 1; i++){ //从小到大考虑所有分子
                while (j < n && arr[i] >= mid * arr[j]){ //arr[i]/arr[j]>=mid,我们要找所有小于mid的分数，所以不断j++直到条件满足。j是分母，j越大分数越小，而且这个数组是严格递增的
                    j++;
                }
                // Count smaller fractions
                totalSmallerFractions += (n - j); //剩下的分数一定都比mid小
                // If we have exhausted the array, break
                if (j == n) break;
                // Calculate the fraction
                double fraction = static_cast<double>(arr[i]) / arr[j];
                // Update maxFraction and indices if necessary
                if (fraction > maxFraction) {
                  numeratorIdx = i;
                  denominatorIdx = j;
                  maxFraction = fraction;
                }
            }
            // Check if we have found the kth smallest prime fraction
            if (totalSmallerFractions == k) { //如果小于mid的分数正好有k个，那么这k个分数里面最大的就是题目要求的。maxFraction正好记录了这个分数
                return {arr[numeratorIdx], arr[denominatorIdx]};
            } else if (totalSmallerFractions > k) {
                right = mid; // Adjust the range for binary search
            } else {
                left = mid; // Adjust the range for binary search
            }
        }
        return {}; // Return empty vector if kth smallest prime fraction not found
    }
};
```
谁能想到mid能间接拿来当参考啊？算法多少算是聪明人的游戏