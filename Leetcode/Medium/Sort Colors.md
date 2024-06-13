# [Sort Colors](https://leetcode.com/problems/sort-colors)

好奇怪的算法名称
```c++
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int colors[3]={};
        for(const int& n:nums){
            colors[n]++;
        }
        int index=0;
        for(int i=0;i<3;i++){
            while(colors[i]){
                colors[i]--;
                nums[index]=i;
                index++;
            }
        }
    }
};
```
counting sort，O(2n)也是n。但是题目的follow up要求one pass解法，便翻了翻solution
```c++
//https://leetcode.com/problems/sort-colors/solutions/3464652/beats-100-c-java-python-javascript-two-pointer-dutch-national-flag-algorithm
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int low = 0, mid = 0, high = nums.size()-1;
        while(mid <= high){
            if(nums[mid] == 0){
                swap(nums[low], nums[mid]);
                low++;
                mid++;
            }
            else if(nums[mid] == 1){
                mid++;
            }
            else{
                swap(nums[mid], nums[high]);
                high--;
            }
        }
    }
};
```
这算法叫Dutch National Flag algorithm，用于排序只有三种元素的数组。算法内部有3个pointer：low，mid和high。low之前是第一种元素；high之后是第三种元素；low和high中间是第二种元素。mid在排序过程中用来遍历数组