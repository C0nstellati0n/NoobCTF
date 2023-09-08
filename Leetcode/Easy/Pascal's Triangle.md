# Pascal's Triangle

[题目](https://leetcode.com/problems/pascals-triangle)

要不是我[见过](../Hard/Number%20of%20Ways%20to%20Reorder%20Array%20to%20Get.md)这样的代码怎么写，这题我可能直接傻掉。
```c#
public class Solution {
    public IList<IList<int>> Generate(int numRows) {
        int[,] triangle = new int[numRows,numRows];
        List<IList<int>> res=new();
        for (int i = 0; i < numRows; i++) {
            triangle[i,0] = triangle[i,i] = 1; //三角形外围填上0
        }
        for (int i = 2; i < numRows; i++) {
            for (int j = 1; j < i; j++) { //第二行就两个元素，都算外围所以之前填过了，从1开始
                triangle[i,j] = triangle[i - 1,j] + triangle[i - 1,j - 1]; //顶上和斜上方元素相加
            }
        }
        for(int i=0;i<numRows;i++){ //烦人的数组转list
            res.Add(new List<int>());
            for(int j=0;j<i+1;j++){ //上面那个方法出来的triangle后面大于等于i+1的地方是0，不用加进去
                res[i].Add(triangle[i,j]);
            }
        }
        return res;
    }
}
```
```
Runtime
71 ms
Beats
99.89%
Memory
37.2 MB
Beats
6.25%
```
来个不用烦人转化的做法。
```c#
//采样区
//https://leetcode.com/problems/pascals-triangle/solutions/4016165/99-53-recursion-math-dynamic-programming/ 有三种解法。不过我仔细看了一眼发现这种好像没有？
public class Solution {
    public IList<IList<int>> Generate(int numRows) {
        IList<IList<int>> lst = new List<IList<int>>
        {
            new List<int> { 1 }
        };
        for (int i = 1; i < numRows; i++)
        {
            var newRow = new List<int>(i+1);
            newRow.Add(1);
            for (int k = 1; k < i / 2 + 1; k++)
            {
                newRow.Add((i - k + 1) * newRow[k - 1] / k);
            }
            for (int j = newRow.Count - 1 - (i + 1) % 2; j >= 0; j--)
            {
                newRow.Add(newRow[j]);
            }
            lst.Add(newRow);
        }
        return lst;
    }
}
```
```
Runtime
76 ms
Beats
99.22%
Memory
36.9 MB
Beats
61.27%
```