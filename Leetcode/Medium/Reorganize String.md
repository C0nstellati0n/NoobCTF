# Reorganize String

[题目](https://leetcode.com/problems/reorganize-string/description/)

[editorial](https://leetcode.com/problems/reorganize-string/editorial/)非常好理解，不过这次的java改c#稍微有点繁琐。
```c#
class Solution {
    public string ReorganizeString(string s) {
        var charCounts = new int[26];
        //计算s中每个字符出现的频率
        foreach(char c in s) {
            charCounts[c - 'a'] = charCounts[c - 'a'] + 1;
        }
        // Max heap ordered by character counts
        //队列中的每个元素都是一个int[2]数组，数组中第一个元素表示字符，第二个元素表示该字符出现的频率
        PriorityQueue<int[],int> pq = new(Comparer<int>.Create((x, y) => y-x));
        for (int i = 0; i < 26; i++) {
            if (charCounts[i] > 0) {
                pq.Enqueue(new int[] {i + 'a', charCounts[i]},charCounts[i]);
            }
        }
        var sb = new StringBuilder();
        //当队列中元素不为0时，交替将队列中出现频率前2的字符加入stringbuilder
        while (pq.Count!=0) {
            var first = pq.Dequeue();
            if (sb.Length == 0 || first[0] != sb[sb.Length - 1]) { //当sb.Length == 0时，加上一个字符肯定不会与之前的重复。否则就要检查当前字符是否和上一个字符一样，不一样才能继续添加
                sb.Append((char) first[0]);
                if (--first[1] > 0) { //若频率仍大于0，重新加回队列
                    pq.Enqueue(first,first[1]);
                }
            } else { //first字符与之前的重复了，来加频率第二个字符
                if (pq.Count==0) { //这时如果发现队列已经没有元素了，而刚才的第一个字符又不能用。说明这个字符串不可能交替放置
                    return "";
                }
                var second = pq.Dequeue();
                sb.Append((char) second[0]);
                if (--second[1] > 0) {
                    pq.Enqueue(second,second[1]);
                }
                pq.Enqueue(first,first[1]);
            }
        }
        return sb.ToString();
    }
}
```
```
Runtime
65 ms
Beats
100%
Memory
37.2 MB
Beats
83.33%
```
还有一个更巧妙的做法。
```c#
class Solution {
    public string ReorganizeString(string s) {
        //第一步仍然是算频率
        var charCounts = new int[26];
        foreach(char c in s) {
            charCounts[c - 'a']++;
        }
        //但是对出现频率第一的字符留个心眼
        int maxCount = 0, letter = 0;
        for (int i = 0; i < charCounts.Length; i++) {
            if (charCounts[i] > maxCount) {
                maxCount = charCounts[i];
                letter = i;
            }
        }
        //根据上一个解法，我们将出现频率最高的字符交替放置。若出现频率第一的字符已经超过s字符长度的一半了，说明交替放置放不下出现频率最高的字符，那就必定重复，可以直接说不可能了
        if (maxCount > (s.Length + 1) / 2) {
            return "";
        }
        var ans = new char[s.Length];
        int index = 0;

        // Place the most frequent letter
        //把出现频率最高的字符放到偶数位
        while (charCounts[letter] != 0) {
            ans[index] = (char) (letter + 'a');
            index += 2;
            charCounts[letter]--;
        }

        // Place rest of the letters in any order
        //剩下的随便放，不过也是跳着放，防止重复
        for (int i = 0; i < charCounts.Length; i++) {
            while (charCounts[i] > 0) {
                if (index >= s.Length) {
                    index = 1;
                }
                ans[index] = (char) (i + 'a');
                index += 2;
                charCounts[i]--;
            }
        }

        return new string(ans);
    }
}
```
```
Runtime
70 ms
Beats
94.44%
Memory
36.8 MB
Beats
94.44%
```