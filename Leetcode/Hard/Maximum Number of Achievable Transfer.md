# Maximum Number of Achievable Transfer Requests

[题目](https://leetcode.com/problems/maximum-number-of-achievable-transfer-requests/description/)

我宣布，backtrack就是最模板的题目，你甚至可以在完全不理解该算法的情况下照着模板写出80%的解。
```c#
//https://leetcode.com/problems/maximum-number-of-achievable-transfer-requests/editorial/
class Solution {
    int answer = 0;
    void maxRequest(int[][] requests, int[] indegree, int n, int index, int count) {
        if (index == requests.Length) {
            // Check if all buildings have an in-degree of 0.
            for (int i = 0; i < n; i++) {
                if (indegree[i] != 0) {
                    return;
                }
            }
            answer = Math.Max(answer, count);
            return;
        }
        
        // Consider this request, increment and decrement for the buildings involved.
        indegree[requests[index][0]]--;
        indegree[requests[index][1]]++;
        // Move on to the next request and also increment the count of requests.
        maxRequest(requests, indegree, n, index + 1, count + 1);
        // Backtrack to the previous values to move back to the original state before the second recursion.
        indegree[requests[index][0]]++;
        indegree[requests[index][1]]--;
        
        // Ignore this request and move on to the next request without incrementing the count.
        maxRequest(requests, indegree, n, index + 1, count);
        //所以做选择不止有for循环，还可以像上面这样。可能仅限于k值不固定的题，固定的就用for循环
    }
    
    public int MaximumRequests(int n, int[][] requests) {
        int[] indegree = new int[n];
        maxRequest(requests, indegree, n, 0, 0);
        return answer;
    }
}
```
```
Runtime
108 ms
Beats
100%
Memory
38.7 MB
Beats
100%
```
为啥我说“能写出80%的解”呢？因为我就是那个写出只能过5个testcases的解的人。这也是唯一一道我竟然能完全靠自己过这么多testcase的hard题。我“借鉴”昨天的[题](../Medium/Fair%20Distribution%20of%20Cookies.md)，发觉这题似乎只有一点不同：k值，表示要分配多少个transfer。如果k值是固定的，我就能直接抄昨天的答案。然而今天这题要找的就是最大的k值。所以我是这么做的：来一个for循环获得所有可能的k值，然后按照k值固定的写法照搬昨天的解，ans用上面一样的方式求。还真让我过了几个testcase。
```c#
//错的，别学
public class Solution {
    int[] buildings;
    int ans;
    public int MaximumRequests(int n, int[][] requests) {
        buildings=new int[n+1];
        for(int i=1;i<=requests.Length;i++){
            Backtrack(requests,i,0);
        }
        return ans;
    }
    private void Backtrack(int[][] requests,int transferNum,int currentNum)
    {
        if(currentNum == transferNum)
        {
            foreach(var val in buildings)
            {
                if(val!=0){
                    return;
                }
            }
            ans=Math.Max(ans,transferNum);
            return;
        }
        for(int i = 0; i < transferNum; i++)
        {
            buildings[requests[currentNum][0]]--;
            buildings[requests[currentNum][1]]++;
            Backtrack(requests, transferNum,currentNum + 1);
            buildings[requests[currentNum][0]]++;
            buildings[requests[currentNum][1]]--;
        }    
    }
}
```
当然我也说不出来为啥不能ac。总之就是给大家提个醒，不能这么写。

editorial还有个bitmask做法。本质上就是利用数字的二进制的1位爆破所有transfer的可能性，表现还不如backtrack，就不放了。