# Equal Row and Column Pairs

[题目](https://leetcode.com/problems/equal-row-and-column-pairs/description/)

怎么觉得这个medium比一些easy还简单？主要是没什么编程技巧，字典一股脑记下来就完事了。
```c#
public class Solution {
    public int EqualPairs(int[][] grid) {
        Dictionary<string,int> record=new();
        foreach(var row in grid){
            string key=String.Join(",",row);
            if(!record.ContainsKey(key)){
                record[key]=1;
            }
            else{
                record[key]++;
            }
        }
        int res=0;
        for(int i=0;i<grid.Length;i++){
            StringBuilder sb=new();
            for(int j=0;j<grid.Length;j++){
                sb.Append($"{grid[j][i]},");
            }
            if(record.ContainsKey(sb.ToString()[..^1])){
                res+=record[sb.ToString()[..^1]];
            }
        }
        return res;
    }
}
```
```
Runtime
168 ms
Beats
94.78%
Memory
61.1 MB
Beats
13.79%
```
同样的思路还能用hashcode实现。
```c#
public class Solution {
    public int EqualPairs(int[][] grid) {

            int n = grid.Length;
            var xMap = new Dictionary<int, int>();
            int x = 0;
            int y = 0;

            while (y < n)
            {
                x = 0;
                var hash = 0;
                while (x < n)
                {
                    hash = HashCode.Combine(hash, grid[y][x].GetHashCode()); //计算row的hashcode。用combine累计计算row全部数字的hashcode。 https://learn.microsoft.com/en-us/dotnet/api/system.hashcode.combine?view=net-7.0
                    x++;
                }

                xMap.TryGetValue(hash, out var freq);
                xMap[hash] = freq+1;

                y++;
            }

            x = 0;
            y = 0;
            int count = 0;

            while (x < n)
            {
                y = 0;
                var hash = 0;
                while (y < n)
                {
                    hash = HashCode.Combine(hash, grid[y][x].GetHashCode()); //j=计算column的hashcode
                    y++;
                }

                if (xMap.ContainsKey(hash))
                {
                    count += xMap[hash];
                }

                x++;
            }

            return count;
       
    }
}
```
```
Runtime
165 ms
Beats
98.26%
Memory
60.3 MB
Beats
68.97%
```