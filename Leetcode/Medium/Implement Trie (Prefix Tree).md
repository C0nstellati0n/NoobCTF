# Implement Trie (Prefix Tree)

[题目](https://leetcode.com/problems/implement-trie-prefix-tree/description/)

树家族怎么有这么多成员啊？查了一下，这次的树是[字典树](https://zhuanlan.zhihu.com/p/28891541)（前缀树）。而且这道题超级加倍，实现3个方法。我只做到了模仿之前的树题写了个TrieNode，剩下的看大佬的吧。

```c#
//https://leetcode.com/problems/implement-trie-prefix-tree/solutions/3305923/image-explanation-complete-stepwise-diagrams-c-java-python/
class TrieNode {
    public bool isCompleteWord;
    public TrieNode[] children;
    
    public TrieNode() {
        isCompleteWord = false; // when the word is complete (mark that node as true)
        children = new TrieNode[26]; // for 26 possible Childrens (for next letter)
    }
}
public class Trie {
    TrieNode root;
    public Trie() {
        root = new TrieNode();
    }
    public void Insert(string word) {
        TrieNode node = root;
        foreach(char c in word) {
            int index = c - 'a';
            if (node.children[index] == null) {
                node.children[index] = new TrieNode();
            }
            node = node.children[index];
        }
        node.isCompleteWord = true;
    }
    public bool Search(string word) {
        TrieNode node = root;
        foreach(char c in word) {
            int index = c - 'a';
            if (node.children[index] == null) {
                return false;
            }
            node = node.children[index];
        }
        return node.isCompleteWord;
    }
    public bool StartsWith(string prefix) {
        TrieNode node = root;
        foreach(char c in prefix) {
            int index = c - 'a';
            if (node.children[index] == null) {
                return false;
            }
            node = node.children[index];
        }
        return true;
    }
}
/**
 * Your Trie object will be instantiated and called as such:
 * Trie obj = new Trie();
 * obj.Insert(word);
 * bool param_2 = obj.Search(word);
 * bool param_3 = obj.StartsWith(prefix);
 */
```

```
Runtime
243 ms
Beats
76.67%
Memory
81.1 MB
Beats
14.36%
```

或者把方法的本体放在TrieNode上。

```c#
//https://leetcode.com/problems/implement-trie-prefix-tree/solutions/3307680/easy-explanation-in-detail-with-code/
public class TrieNode{
    bool end;
    TrieNode[] child;
    public TrieNode(){
        this.end = false;
        child=new TrieNode[26];
    }
    public void setEnd(){
        this.end = true;
    }
    public void setNode(char ch){
        child[ch-'a'] = new TrieNode();
    }

    public bool isEnd(){
        return this.end;
    }
   public bool isSet(char ch){
        return child[ch-'a'] != null;
    }

    public TrieNode getNode(char ch){
        return child[ch-'a'];
    }
}
public class Trie {
    TrieNode root;
    public Trie() {
        root = new TrieNode();
    }
    public void Insert(string word) {
        TrieNode p = root;
        for(int i = 0; i < word.Length; i++){
            char ch = word[i];
            Console.WriteLine(p);
            if(p.isSet(ch)){
                p = p.getNode(ch);
            }else{
                p.setNode(ch);
                p = p.getNode(ch);
            }
        }
        p.setEnd();
    }
    
    public bool Search(string word) {
        TrieNode p = root;
        for(int i = 0; i < word.Length; i++){
            char ch = word[i];
            if(p.isSet(ch)){
                p = p.getNode(ch);
            }else{
                return false;
            }
        }
        return p.isEnd();
    }
    
    public bool StartsWith(string prefix) {
        TrieNode p = root;
        for(int i = 0; i < prefix.Length; i++){
            char ch = prefix[i];
            if(p.isSet(ch)){
                p = p.getNode(ch);
            }else{
                return false;
            }
        }
        return true;
    }
}
```

```
Runtime
369 ms
Beats
13.8%
Memory
82 MB
Beats
5.13%
```

虽然不知道为啥非常拉胯。