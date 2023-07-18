# LRU Cache

[题目](https://leetcode.com/problems/lru-cache/description/)

技能点全点内存了是吧？
```c#
public class LRUCache {
    Dictionary<int,int> d;
    int capacity;
    Queue<int> q;
    int last;
    public LRUCache(int capacity) {
        this.capacity=capacity;
        this.d=new();
        this.q=new();
    }
    
    public int Get(int key) {
        if(d.ContainsKey(key)){
            q.Enqueue(key);
            return d[key];
        }
        return -1;
    }
    
    public void Put(int key, int value) {
        d[key]=value;
        last=-1;
        while(d.Count>capacity){
            last=q.Dequeue();
            if(!q.Contains(last)){
                d.Remove(last);
            }
        }
        q.Enqueue(key);
    }
}
```
```
Runtime
938 ms
Beats
5.10%
Memory
152.2 MB
Beats
99.82%
```
没啥优点，总之就是慢。不过内存这么少我是没想到的，我还以为两个方面都是倒数。还是看看大佬们的解法吧。
```c#
//https://leetcode.com/problems/lru-cache/solutions/45911/java-hashtable-double-linked-list-with-a-touch-of-pseudo-nodes/ 评论区
class LRUCache {
  
  Node head = new Node(0, 0), tail = new Node(0, 0);
  Dictionary<int, Node> dictionary = new();
  int capacity;
  
  public LRUCache(int _capacity) {
    capacity = _capacity;
    head.next = tail; //初始化双向链表
    tail.prev = head;
  }

  public int Get(int key) {
    if(dictionary.ContainsKey(key)) { //若字典里存在key
      Node node = dictionary[key]; //取出对应的node
      remove(node);
      insert(node); //将node从双向链表中移除再加进去，那么新加入的node更靠近head。此举是为了更新key的used情况
      return node.value;
    } else {
      return -1;
    }
  }

  public void Put(int key, int value) {
    if(dictionary.ContainsKey(key)) {
      remove(dictionary[key]); //与Get处的remove作用相同
    }
    if(dictionary.Count == capacity) { //因为接下来要insert，所以要给新insert的node腾位置
      remove(tail.prev); //也是移除least recently used node
    }
    insert(new Node(key, value));
  }
  
  private void remove(Node node) { //remove和insert都是基本的双向链表功能
    dictionary.Remove(node.key);
    node.prev.next = node.next;
    node.next.prev = node.prev;
  }
  
  private void insert(Node node){
    dictionary[node.key]= node;
    Node headNext = head.next;
    head.next = node;
    node.prev = head;
    headNext.prev = node;
    node.next = headNext;
  }
  
  class Node{
    public Node prev, next;
    public int key, value;
    public Node(int _key, int _value) {
      key = _key;
      value = _value;
    }
  }
}
```
```
Runtime
809 ms
Beats
72.52%
Memory
154.1 MB
Beats
72%
```
这题的考点为[双向链表](https://cloud.tencent.com/developer/article/1511615)(doubly linked list)。因为链表往头部插入，所以越least recently used的node越靠近尾部tail。这才是这道题的正确打开方式，我那个是啥玩意啊，完美绕过知识点。