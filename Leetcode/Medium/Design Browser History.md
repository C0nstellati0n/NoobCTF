# Design Browser History

[题目](https://leetcode.com/problems/design-browser-history/description/)

4种解法，两种用List（变种），一种用两个栈，一种用自实现的Node（双向链表）。

```c#
//https://leetcode.com/problems/design-browser-history/solutions/3309557/image-explanation-both-array-stack-approaches-c-java-python/
class BrowserHistory {

    List<string> list;
    int total = 0,curr = 0;

    public BrowserHistory(string homepage) {
        list = new();
        list.Add(homepage);
        total++;
        curr++;
    }

    public void Visit(string url) {
        if (list.Count > curr) {
            list[curr]=url;
        } else {
            list.Add(url);
        }
        curr++;
        total = curr;
    }

    public string Back(int steps) {
        curr = Math.Max(1, curr - steps);
        return list[curr - 1];
    }

    public string Forward(int steps) {
        curr = Math.Min(total, curr + steps);
        return list[curr - 1];
    }
}

/**
 * Your BrowserHistory object will be instantiated and called as such:
 * BrowserHistory obj = new BrowserHistory(homepage);
 * obj.Visit(url);
 * string param_2 = obj.Back(steps);
 * string param_3 = obj.Forward(steps);
 */
```

```
Runtime
295 ms
Beats
84.16%
Memory
62.5 MB
Beats
44.55%
```

```c#
//https://leetcode.com/problems/design-browser-history/solutions/3309336/python-simple-solution-easiest-video/
public class BrowserHistory {
    int current;
    List<string> history=new();
    public BrowserHistory(string homepage){
        history.Add(homepage);
        current = 0;
    }

    public void Visit(string url){
        history = history.GetRange(0,current+1);//List是不能用范围运算符的
        history.Add(url);
        current += 1;
    }

    public string Back(int steps){
        current = Math.Max(0, current - steps);
        return history[current];
    }

    public string Forward(int steps){
        current = Math.Min(history.Count-1, current + steps);
        return history[current];
    }
}
```

```
Runtime
293 ms
Beats
86.14%
Memory
62.9 MB
Beats
10.89%
```

用栈的：

```c#
//https://leetcode.com/problems/design-browser-history/solutions/3309557/image-explanation-both-array-stack-approaches-c-java-python/
public class BrowserHistory {
    Stack<string> history = new();
    Stack<string> future = new();
    public BrowserHistory(string homepage) {
        history.Push(homepage);
        future.Clear();
    }
    
    public void Visit(string url) {
        history.Push(url);
        future.Clear();
    }
    
    public string Back(int steps) {
        while (steps > 0 && history.Count > 1) {
            future.Push(history.Pop());
            steps--;
        }
        return history.Peek();
    }
    
    public string Forward(int steps) {
        while (steps > 0 && future.Count > 0) {
            history.Push(future.Pop());
            steps--;
        }
        return history.Peek();
    }
}
```

```
Runtime
288 ms
Beats
91.9%
Memory
63.2 MB
Beats
5.94%
```

速度较快，但是两个栈导致需要的内存更多。

最后是Node。这种目前来看是最好的做法。

```c#
//https://leetcode.com/problems/design-browser-history/solutions/3309592/clean-codes-full-explanation-doubly-linked-list-c-java-python3/
// A class to represent a node in a linked list
class Node {
  // The previous and next nodes in the list
  public Node prev;
  public Node next;
  // The URL represented by this node
  public string url;
  
  // Constructor that sets the URL for this node
  public Node(string url) {
    this.url = url;
  }
}

// A class to represent a browser history
class BrowserHistory {
  // The current node in the history
  private Node curr;
  
  // Constructor that creates a new history with the given homepage
  public BrowserHistory(string homepage) {
    // Create a new node to represent the homepage
    curr = new Node(homepage);
  }

  // Method to add a new URL to the history
  public void Visit(string url) {
    // Create a new node to represent the new URL
    curr.next = new Node(url);
    // Set the previous node for the new node to be the current node
    curr.next.prev = curr;
    // Make the new node the current node
    curr = curr.next;
  }

  // Method to navigate back in the history by the given number of steps
  public string Back(int steps) {
    // While there are previous nodes and we haven't gone back enough steps yet
    while (curr.prev != null && steps-- > 0) {
      // Move back one node by setting the current node to the previous node
      curr = curr.prev;
    }
    // Return the URL represented by the current node
    return curr.url;
  }

  // Method to navigate forward in the history by the given number of steps
  public string Forward(int steps) {
    // While there are next nodes and we haven't gone forward enough steps yet
    while (curr.next != null && steps-- > 0) {
      // Move forward one node by setting the current node to the next node
      curr = curr.next;
    }
    // Return the URL represented by the current node
    return curr.url;
  }
}
```

```
Runtime
287 ms
Beats
92.8%
Memory
62.4 MB
Beats
50.50%
```