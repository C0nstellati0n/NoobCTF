# [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array)

"给我过吧……"不好好读题也不看edge case的我在连续错了三次后说到
```c#
public class Solution {
    public int[] SearchRange(int[] nums, int target) {
        if(nums.Length==0){
            return new int[2]{-1,-1};
        }
        int mid=BinarySearch(nums,target,0,nums.Length-1);
        if(mid==-1) return new int[2]{-1,-1};
        int[] ans=new int[2];
        int temp=mid;
        int lastMid=0;
        while(mid!=-1){
            lastMid=mid;
            mid=BinarySearch(nums,target,0,lastMid-1);
        }
        ans[0]=lastMid;
        while(temp!=-1){
            lastMid=temp;
            temp=BinarySearch(nums,target,lastMid+1,nums.Length-1);
        }
        ans[1]=lastMid;
        return ans;
    }
    int BinarySearch(int[] nums,int target,int i,int j){
        int left = i;
        int right = j;
        int mid;
        while (left <= right) {
            mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
```
```
Runtime
122 ms
Beats
97.4%
Memory
44.9 MB
Beats
63.93%
```
进一步加深了对binary search的认知，if里面那些等于号，小于号之类的会影响算法的运行。参考 https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/solutions/14699/clean-iterative-solution-with-two-binary-searches-with-explanation ，这位大佬没有像我一样手动指定binary search的起始和结束，而是通过修改算法使算法永远找到最左边/右边的元素。我这个基础款的只会找到偏中间的，所以得一次search确定中间，不知道多少次search找偏最左边的，右边的同理。这种应该叫biased binary search，算法运行时会有意倾向于左边/右边