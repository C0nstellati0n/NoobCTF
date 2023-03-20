# Design Add and Search Words Data Structure

[题目](https://leetcode.com/problems/design-add-and-search-words-data-structure/description/)

这题官方推荐用Trie的做法，于是我找了两个（其实差不多）。第一种就是最基础的Trie实现。

```c#
//https://leetcode.com/problems/design-add-and-search-words-data-structure/solutions/3313792/image-explanation-easy-trie-c-java-python/
class WordDictionary {
    private WordDictionary[] children;
    bool isCompleteWord;

    public WordDictionary() {
        children = new WordDictionary[26];
        isCompleteWord = false;
    }
    
    public void AddWord(string word) {
        WordDictionary curr = this;
        foreach(char c in word){
            if(curr.children[c - 'a'] == null)
                curr.children[c - 'a'] = new WordDictionary();
            curr = curr.children[c - 'a'];
        }
        curr.isCompleteWord = true;
    }
    
    public bool Search(string word) {
        WordDictionary curr = this;
        for(int i = 0; i < word.Length; ++i){
            char c = word[i];
            if(c == '.'){
                foreach(WordDictionary ch in curr.children)
                    if(ch != null && ch.Search(word[(i+1)..])) return true;
                return false;
            }
            if(curr.children[c - 'a'] == null) return false;
            curr = curr.children[c - 'a'];
        }
        return curr != null && curr.isCompleteWord;
    }
}
/**
 * Your WordDictionary object will be instantiated and called as such:
 * WordDictionary obj = new WordDictionary();
 * obj.AddWord(word);
 * bool param_2 = obj.Search(word);
 */
```

```
Runtime
1896 ms
Beats
40.19%
Memory
147.6 MB
Beats
66.82%
```

第二种加了个Dfs方法，Search本体就是Dfs，也是递归。

```c#
//https://leetcode.com/problems/design-add-and-search-words-data-structure/solutions/3313633/python-simple-solution-easy-to-understand/
class TrieNode{
    public Dictionary<char,TrieNode> children;
    public bool is_word;
    public TrieNode(){
        children = new();
        is_word=false;
    }
}
        
public class WordDictionary{
    TrieNode root;
    public WordDictionary(){
        root = new TrieNode();
    }
    public void AddWord(string word){
        TrieNode current_node=root;
        foreach(char character in word){
            if (!current_node.children.TryGetValue(character, out TrieNode temp))           {
                current_node.children.Add(character,new TrieNode());
                current_node=current_node.children[character];
            }
            else{
                current_node=temp;
            }
        }
        current_node.is_word = true;
    }
    bool Dfs(TrieNode node,int index,string word){
        if(index==word.Length){
            return node.is_word;
        }
        if(word[index]=='.'){
            foreach(TrieNode child in node.children.Values){
                if(Dfs(child,index+1,word)){
                    return true;
                }
            }
        }
        if(node.children.ContainsKey(word[index])){
            return Dfs(node.children[word[index]],index+1,word);
        }
        return false;
    }
    public bool Search(string word){
        return Dfs(root,0,word);
    }
}
```

```
Runtime
1691 ms
Beats
65.42%
Memory
142.6 MB
Beats
76.17%
```

最后在隔壁python3遇见了一种不用Trie用字典的做法，不过我没能用c#写出来。

```python
#https://leetcode.com/problems/design-add-and-search-words-data-structure/solutions/3313896/python-3-t-m-100-100/
class WordDictionary:
        def __init__(self):

            self.words = defaultdict(list)


        def addWord(self, word: str) -> None:

            self.words[len(word)].append(word)


        def search(self, word: str) -> bool:

            n = len(word)

            if '.' in word:
                
                for w in self.words[n]:
                    if all(word[i] in (w[i], '.') for i in range(n)):#这个列表生成式把我干沉默了
                        return True

                else: return False #这个else匹配的是哪个if？

            return word in self.words[n]
```

```
Runtime
4735 ms
Beats
91.43%
Memory
21.5 MB
Beats
99.66%
```

我确实找到了一个c#里面的defaultdict实现：

```c#
//https://stackoverflow.com/questions/15622622/analogue-of-pythons-defaultdict
public class DefaultDictionary<TKey, TValue> : Dictionary<TKey, TValue> where TValue : new() //new约束限制TValue不能是抽象类型 https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/keywords/new-constraint
{
    public new TValue this[TKey key]
    {
        get
        {
            TValue val;
            if (!TryGetValue(key, out val))
            {
                val = new TValue();
                Add(key, val);
            }
            return val;
        }
        set { base[key] = value; }
    }
}
```

也在[这里](https://www.yanning.wang/archives/681.html)看见了c#里的“列表生成式”（其实是LINQ）。不知道为啥就是不行，代码编译过不去。