# Text Justification

[题目](https://leetcode.com/problems/text-justification/description/)

见过的第一个单纯靠烦人成为hard的题。没有任何可讲的，这里学到的东西遇见下一道题也没法用，因为压根就没有共通的考点。就是繁琐，就是看edge case，就是看处理。
```c#
//https://leetcode.com/problems/text-justification/editorial/
class Solution {
    public List<string> FullJustify(string[] words, int maxWidth) {
        List<string> ans = new();
        int i = 0;
        
        while (i < words.Length) {
            List<string> currentLine = getWords(i, words, maxWidth);
            i += currentLine.Count;
            ans.Add(createLine(currentLine, i, words, maxWidth));
        }
        return ans;
    }
    
    private List<string> getWords(int i, string[] words, int maxWidth) { //给定当前长度i，备选词words，最大长度maxWidth，返回maxWidth下最多可包含的全部词汇
        List<string> currentLine = new();
        int currLength = 0;

        while (i < words.Length && currLength + words[i].Length <= maxWidth) {
            currentLine.Add(words[i]);
            currLength += words[i].Length + 1; //额外加个1是因为还要把词与词之间的空格考虑上
            i++;
        }

        return currentLine;
    }
    
    private string createLine(List<string> line, int i, string[] words, int maxWidth) {
        int baseLength = -1;
        foreach(string word in line) {
            baseLength += word.Length + 1; //基础长度：全部词汇的长度加上必须的至少一个的空格
        }

        int extraSpaces = maxWidth - baseLength; //最大长度-至少需要的基础长度就是需要pad的空格数量

        if (line.Count == 1 || i == words.Length) { //若当前line只有一个词语或者是最后一个词语，按照题目要求的那样left-justified
            return string.Join(' ', line) + new string(' ',extraSpaces);
        }

        int wordCount = line.Count - 1;
        int spacesPerWord = extraSpaces / wordCount; //每个词语之间的空格数量
        int needsExtraSpace = extraSpaces % wordCount;

        for (int j = 0; j < needsExtraSpace; j++) { ////假如应该有的空格数量无法整除，就从最左边开始，给最左边的词语多加空格，满足题目要求的“右边空格比左边少”
            line[j]=line[j] + " ";
        }

        for (int j = 0; j < wordCount; j++) {
            line[j]=line[j] + new string(' ',spacesPerWord);
        }

        return string.Join(" ",  line);
    }
}
```
```
Runtime
137 ms
Beats
92.65%
Memory
43.5 MB
Beats
82.35%
```