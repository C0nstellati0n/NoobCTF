# Summary Ranges

[题目](https://leetcode.com/problems/summary-ranges/)

two pointers都用错了的屑。

```c#
//https://leetcode.com/problems/summary-ranges/solutions/1805583/c-detailed-explanation-w-dry-run-faster-than-100-basic-concept-used/
public class Solution {
    public IList<string> SummaryRanges(int[] arr) {
        int n = arr.Length; // extracting size of the array
        List<string> ans=new(); // declaring answer array to store our answer
        string temp = ""; // temproray string that stores all possible answer
        for(int i = 0; i < n; i++) // start traversing from the array
        {
            int j = i; // declare anthor pointer that will move
            
            // run that pointer until our range is not break
            while(j + 1 < n && arr[j + 1] == arr[j] + 1)
            {
                j++;
            }
            
            // if j > i, that means we got our range more than one element
            if(j > i)
            {
                temp += $"{arr[i]}->{arr[j]}";
            }
            else // we got only one element as range
            {
                temp += arr[i].ToString(); // then store that element in temp
            }
            
            ans.Add(temp); // push one possible answer string to our answer
            temp = ""; // again reintiliaze temp for new possible answers
            i = j; // and move i to j for a fresh start
        }
        return ans; // and at last finally return the answer array
    }
}
```
```
Runtime
141 ms
Beats
97.8%
Memory
43 MB
Beats
88.69%
```
我的第一反应也是two pointers，但是没有想到while循环。导致边界的检查非常痛苦，然后就寄了。