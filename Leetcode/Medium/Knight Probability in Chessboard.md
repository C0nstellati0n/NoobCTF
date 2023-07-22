# Knight Probability in Chessboard

[题目](https://leetcode.com/problems/knight-probability-in-chessboard/description/)

我被dp+概率吓到了。这俩玩意我都不熟（咱就是说见了几十道dp了咋还不熟？压根就没学），于是想了半天无果就去看了答案。其实是比较简单的。
```c#
//https://leetcode.com/problems/knight-probability-in-chessboard/editorial/
//editorial三种方式这种时间空间均最佳
public class Solution {
    public double KnightProbability(int n, int k, int row, int column) {
        // Define possible directions for the knight's moves
        int[][] directions = {
            new int[]{1, 2}, 
            new int[]{1, -2}, 
            new int[]{-1, 2}, 
            new int[]{-1, -2},
            new int[]{2, 1}, 
            new int[]{2, -1}, 
            new int[]{-2, 1}, 
            new int[]{-2, -1}
        };

        // Initialize the previous and current DP tables
        double[,] prevDp = new double[n,n];
        double[,] currDp = new double[n,n];

        // Set the probability of the starting cell to 1
        prevDp[row,column] = 1;

        // Iterate over the number of moves
        for (int moves = 1; moves <= k; moves++) {
            // Iterate over the cells on the chessboard
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    currDp[i,j] = 0;

                    // Iterate over possible directions
                    foreach(int[] direction in directions) {
                        int prevI = i - direction[0];
                        int prevJ = j - direction[1];

                        // Check if the previous cell is within the chessboard
                        if (prevI >= 0 && prevI < n && prevJ >= 0 && prevJ < n) { //假如不在棋盘内部的话更新了也没意义，不是题目要找的目标
                            // Update the probability by adding the previous probability divided by 8
                            currDp[i,j] += prevDp[prevI,prevJ] / 8;
                        }
                    }
                }
            }

            // Swap the previous and current DP tables
            double[,] temp = prevDp;
            prevDp = currDp;
            currDp = temp;
        }

        // Calculate the total probability by summing up the probabilities for all cells
        double totalProbability = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                totalProbability += prevDp[i,j];
            }
        }

        // Return the total probability
        return totalProbability;
    }
}
```
```
Runtime
30 ms
Beats
100%
Memory
27.4 MB
Beats
100%
```
为啥说比较简单呢？因为这题的dp单纯就是起到记忆作用，不是那种需要Math.Max或者什么乱七八糟的需要筛选最优的dp。以及这题dp各项之间的关系都不难看，当前格子的概率只跟上一个格子有关系，而且是固定的除以8。从开始的格子1的概率以及题目描述给定的8个方向一直往下推就好了。我甚至都不知道有什么好解释的，我是笨蛋。