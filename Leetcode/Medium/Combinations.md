# Combinations

[题目](https://leetcode.com/problems/combinations/description/)

我之前说backtrack就是最模板的技巧，今天得到验证了。我直接抄了[Fair Distribution of Cookies](./Fair%20Distribution%20of%20Cookies.md)的模板然后手动改了一下，成了。
```c#
public class Solution {
    List<IList<int>> ans=new();
    public IList<IList<int>> Combine(int n, int k) {
        Backtrack(new int[k],n,k,0,1);
        return ans;
    }
    private void Backtrack(int[] cur,int n, int k, int curIndex,int i)
    {
        if(curIndex == k)
        {
            ans.Add(cur.ToList());
            return;
        }
        for(int j = i; j <= n; j++)
        {      
            i++;     
            cur[curIndex]+=j;
            Backtrack(cur[..], n, k, curIndex + 1,i);
            cur[curIndex]-=j;
        } 
    }
}
```
```
Runtime
154 ms
Beats
16.3%
Memory
117.3 MB
Beats
5.34%
```
就是又慢又耗内存，毫无优点“而已”。更好的backtrack解法如下：
```c#
//https://leetcode.com/problems/combinations/solutions/27002/backtracking-solution-java/
public class Solution {
        public List<IList<int>> Combine(int n, int k) {
		List<IList<int>> combs = new();
		Backtrack(combs, new(), 1, n, k);
		return combs;
	}
	public void Backtrack(List<IList<int>> combs, List<int> comb, int start, int n, int k) {
		if(k==0) {
			combs.Add(new List<int>(comb)); //c#里面拷贝数组的写法。要是直接加的话加的是引用
			return;
		}
		for(int i=start;i <= n-k+1;i++) { //根据评论区的建议修改了一下，确实比直接i<=n快点
			comb.Add(i);
			Backtrack(combs, comb, i+1, n, k-1);
			comb.RemoveAt(comb.Count-1);
		}
	}
}
```
```
Runtime
79 ms
Beats
100%
Memory
44.3 MB
Beats
57.25%
```
然后是采样区的递归解法。没有backtrack标志性的选择+撤销，但是快啊。
```c#
public class Solution {
    public IList<IList<int>> Combine(int n, int k) {
        var ans = new List<IList<int>>();
        var cur = new int[k];

        Generate(cur, ans, n, 0, k);

        return ans;
    }

    private void Generate(int[] cur, List<IList<int>> ans, int n, int i, int remaining) {
        if (remaining == 0) {
            ans.Add(cur.ToArray());
            return;
        }

        for (; i <= n - remaining; ++i) {
           cur[cur.Length - remaining] = i + 1;
           Generate(cur, ans, n, i + 1, remaining - 1); 
        }
    }
}
```
```
Runtime
65 ms
Beats
100%
Memory
43.8 MB
Beats
98.47%
```
你甚至还可以不用递归，遍历完成。
```c#
//https://leetcode.com/problems/combinations/solutions/26992/short-iterative-c-answer-8ms/
public class Solution {
    public IList<IList<int>> Combine(int n, int k) {
        List<IList<int>> result=new();
		int i = 0;
	    int[] p=new int[k];
		while (i >= 0) {
			p[i]++;
			if (p[i] > n) --i;
			else if (i == k - 1) result.Add(p.ToList());
			else {
			    ++i;
			    p[i] = p[i - 1];
			}
		}
		return result;
    }
}
```
```
Runtime
92 ms
Beats
99.24%
Memory
44.4 MB
Beats
42.37%
```
总之就是大佬各显神通，我一个人挨打。