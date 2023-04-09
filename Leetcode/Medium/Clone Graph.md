# Clone Graph

[题目](https://leetcode.com/problems/clone-graph/description/)

拷贝图表，但是拷贝结果需要和原图一致（包括邻接情况）。不能直接返回题目的参数。让我们来看看又有咋样的dfs/bfs。

```c#
//https://leetcode.com/problems/clone-graph/solutions/1793436/java-simple-code-with-heavy-comments/
class Solution {
    public void dfs(Node node , Node copy , Node[] visited){
        visited[copy.val] = copy;// store the current node at it's val index which will tell us that this node is now visited
        
//         now traverse for the adjacent nodes of root node
        foreach(Node n in node.neighbors){
//             check whether that node is visited or not
//              if it is not visited, there must be null
            if(visited[n.val] == null){
//                 so now if it not visited, create a new node
                Node newNode = new Node(n.val);
//                 Add this node as the neighbor of the prev copied node
                copy.neighbors.Add(newNode);
//                 make dfs call for this unvisited node to discover whether it's adjacent nodes are explored or not
                dfs(n , newNode , visited);
            }else{
//                 if that node is already visited, retrieve that node from visited array and Add it as the adjacent node of prev copied node
//                 THIS IS THE POINT WHY WE USED NODE[] INSTEAD OF BOOLEAN[] ARRAY
                copy.neighbors.Add(visited[n.val]);
            }
        }
        
    }
    public Node CloneGraph(Node node) {
        if(node == null) return null; // if the actual node is empty there is nothing to copy, so return null
        Node copy = new Node(node.val); // create a new node , with same value as the root node(given node)
        Node[] visited = new Node[101]; // in this question we will create an array of Node(not boolean) why ? , because i have to Add all the adjacent nodes of particular vertex, whether it's visited or not, so in the Node[] initially null is stored, if that node is visited, we will store the respective node at the index, and can retrieve that easily.
        Array.Fill(visited , null); // initially store null at all places
        dfs(node , copy , visited); // make a dfs call for traversing all the vertices of the root node
        return copy; // in the end return the copy node
    }
}
```

```
Runtime
141 ms
Beats
97.22%
Memory
43.3 MB
Beats
22.50%
```

或者下面这个用字典的dfs。除此之外，dfs递归函数本体就是本身，因此看上去比较短。

```c#
//https://leetcode.com/problems/clone-graph/solutions/1793212/c-detailed-explanation-w-dfs-bfs-commented-code-with-extra-test-case/
class Solution {
    Dictionary<Node , Node> mp=new();
    public Node CloneGraph(Node node) {
        if(node == null) // if node is null, then simply return null
        {
            return null;
        }
        
        // for a node, we will check whether we already creates a copy of thiis or not. If it is present in map that means we already creates a copy of this.
        //But if not present in map, that means we have not a copy of this.
        // Also, if we create a copy, then being a good neighbor, we find whether our neighbor have a copy or not, so we will travel all around our adjcant.
        
        if(!mp.ContainsKey(node)) // if not present in map
        {
            mp[node] = new Node(node.val); // make a copy
            
            foreach(var adj in node.neighbors) // travel in adjcant
            {
                mp[node].neighbors.Add(CloneGraph(adj)); //add copy
            }
        }
        
        return mp[node]; // and at last, return mp[node] as till now we clone our whole graph
    }
}
```

```
Runtime
149 ms
Beats
85.28%
Memory
43.1 MB
Beats
53.89%
```

当然还有bfs。

```c#
//https://leetcode.com/problems/clone-graph/solutions/1792858/python3-iterative-bfs-beats-98-explained/
class Solution {
    public Node CloneGraph(Node node) {
        if(node==null) return node;
        Queue<Node> q=new();
        Dictionary<int,Node> clones=new Dictionary<int,Node>{
            {node.val,new Node(node.val)}
        };
        q.Enqueue(node);
        while(q.Count!=0){
            Node cur=q.Dequeue();
            Node cur_clone = clones[cur.val];
            foreach(Node ngbr in cur.neighbors){
                if(!clones.ContainsKey(ngbr.val)){
                    clones.Add(ngbr.val,new Node(ngbr.val));
                    q.Enqueue(ngbr);
                }
                cur_clone.neighbors.Add(clones[ngbr.val]);
            }         
        }
        return clones[node.val];
    }
}
```

```
Runtime
149 ms
Beats
85.28%
Memory
42.7 MB
Beats
86.11%
```