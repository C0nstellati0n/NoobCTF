# [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle)

不是你们采样区代码的作者都是外星人吗？
```c++
//采样区
class Solution {
public:
int largestRectangleArea(vector < int > & histo) {
	stack < int > st;
	int maxA = 0;
	int n = histo.size();
	for (int i = 0; i <= n; i++) {
		while (!st.empty() && (i == n || histo[st.top()] >= histo[i])) {
			int height = histo[st.top()];
			st.pop();
			int width;
			if (st.empty())
				width = i;
			else
				width = i - st.top() - 1;
			maxA = max(maxA, width * height);
		}
		st.push(i);
	}
	return maxA;
}
int solve(vector<vector<char>>&mat, int n, int m) {
	int maxArea = 0;
	vector<int> height(m, 0);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			if (mat[i][j] == '1') height[j]++;
			else height[j] = 0;
		}
		int area = largestRectangleArea(height);
		maxArea = max(area, maxArea);
	}
	return maxArea;
}
    int maximalRectangle(vector<vector<char>>& matrix) {
        int n = matrix.size();
        int m = matrix[0].size();
        return solve(matrix, n, m);
    }
};
```
根据discussion区`eggplantkiller`的评论，只需要把这题的matrix转换成histogram，就能用[Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram)的解法做了。最后在 https://leetcode.com/problems/largest-rectangle-in-histogram/solutions/28905/my-concise-c-solution-ac-90-ms/ 的评论区里找到了个略带小错误但是能用的[解析](https://abhinandandubey.github.io/posts/2019/12/15/Largest-Rectangle-In-Histogram.html)

关键点在于monotonic stack（又是你）。我们需要维持一个递增的monotonic stack，若遇见高度小于栈顶的bar，就需要一直pop，直到那个bar高度大于栈顶。在pop的过程中计算最大的rectangle。这算法就属于那种，看了实现觉得很合理，但是你叫我想或者解释为什么要用monotonic stack我就做不出来。只是隐隐约约地感觉，rectangle的大小和其宽和高有关系，递增的monotoni stack是为了找到目前最高的bar。如果下一个bar更矮了，就要计算那个最高的bar是多少面积，因为再不算就没机会了，两边的bar都比它矮，肯定是没法一起拼成个rectangle。感觉还是用脑算比较好理解这题的逻辑