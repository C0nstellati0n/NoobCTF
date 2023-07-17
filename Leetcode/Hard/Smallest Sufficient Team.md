# Smallest Sufficient Team

[题目](https://leetcode.com/problems/smallest-sufficient-team/)

这题dp+bitmask可太阴间了，discussion区有人给出了较为简短的解释，[editorial](https://leetcode.com/problems/smallest-sufficient-team/editorial/)说的也很详细。但是当我看到采样区最佳的做法时，我整个人都炸了，这是人写出来的？
```c#
public class Solution {
        //k：当前考虑的skill对应的skillId
        //n：一共需要多少种skill
        //c：当前team中的成员数量
        //x：当前团队所有成员拥有的全部skill（bitmask）
        //p：当前团队所有成员（bitmask）
        //a：所有拥有某项skill（索引）的人的index
        //b：每个人所拥有的全部skill（bitmask数组）
        //max：team成员的最大数量
        //pm：当前被选入团队的成员（bitmask）
        void reks(int k, int n, int c, int x, long p, List<int>[] a, int[] b, ref int max, ref long pm)
        {
            if (x == n) //当前团队是一个拥有全部要求skill的团队
            {
                if (c >= max) return; //大于说明之前的更好，不用改
                max = c; //否则更改，最大数量改为当前团队的数量
                pm = p; //更改成员
                return;
            }
            if ((x & (1 << k)) > 0) //若当前考虑的skill已经在团队里了
            {
                reks(k + 1, n, c, x, p, a, b, ref max, ref pm); //考虑下一种skill
                return;
            }
            if (c+1 >= max) return; //再加一个人已经超过当前所拥有的max了，且还没有拥有全部要求的skill，那继续下去也没意义了
            for (int i = 0; i < a[k].Count; i++)
            {
                int y = a[k][i]; //遍历所有拥有k skill的人
                reks(k + 1, n, c + 1, x | b[y], p | (1L << y), a, b, ref max, ref pm); //考虑下一种skill（k+1），添加拥有当前k skill的人进团队（p | (1L << y)），人数加一（c+1），团队skill增加y所拥有的skill（x | b[y]），其他参数照抄
            }
            
        }
        public int[] SmallestSufficientTeam(string[] req_skills, IList<IList<string>> people)
        {
            int n = req_skills.Length;
            Dictionary<string, int> d = new Dictionary<string, int>(); //将skill和数字联系起来。比如req_skills[0]:0;req_skills[1]:1。可以将对应的数字看作id，方便接下来使用bitmask
            for (int i = 0; i < n; i++) d.Add(req_skills[i], i);
            List<int>[] a = new List<int>[n]; //这个数组记录所有拥有某项skill的人的index。a的索引联系上面的d字典表示某个skill
            for (int i = 0; i < n; i++) a[i] = new List<int>();
            int m = people.Count;
            int[] b = new int[m]; //people中每个人所拥有的skills（用bitmask记录）
            for (int j = 0; j < m; j++)
            {
                int x = 0;
                for (int i = 0; i < people[j].Count; i++)
                {
                    int y = d[people[j][i]];
                    a[y].Add(j);
                    x = x | (1 << y);
                }
                b[j] = x;
            }
            int max = n + 1; //team member的最大数量
            long pm = 0; //这也是个bitmask，记录当前被选入team的成员，或者说当前找到的“TheSmallestSufficientTeam”
            reks(0, (1 << n) - 1, 0, 0, 0, a, b, ref max, ref pm); //ref传引用进去，在函数里修改后也会影响外面的值
            List<int> res = new List<int>();
            for (int j = 0; j < m; j++)
                if ((pm & (1L << j)) > 0) res.Add(j); //pm经过reks函数，已经为TheSmallestSufficientTeam了。现在就是看谁在bitmask里，加进res
            return res.ToArray();
        }
}
```
```
Runtime
149 ms
Beats
100%
Memory
42.8 MB
Beats
100%
```
感谢chatgpt，没有它我不可能理解这么巧妙的答案。