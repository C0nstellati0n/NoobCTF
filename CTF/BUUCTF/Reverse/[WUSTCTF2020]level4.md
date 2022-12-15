# [WUSTCTF2020]level4

[题目地址](https://buuoj.cn/challenges#[WUSTCTF2020]level4)

今天终于认识了二叉树这个听了很多次却总是懒得学的东西。

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("Practice my Data Structure code.....");
  puts("Typing....Struct.....char....*left....*right............emmmmm...OK!");
  init("Typing....Struct.....char....*left....*right............emmmmm...OK!", argv);
  puts("Traversal!");
  printf("Traversal type 1:");
  type1(byte_601290);
  printf("\nTraversal type 2:");
  type2(byte_601290);
  printf("\nTraversal type 3:");
  puts("    //type3(&x[22]);   No way!");
  puts(&byte_400A37);
  return 0;
}
```

看了半天，好像没有输入点啊？看看里面调用的几个函数。

```c
unsigned __int64 init()
{
  int i; // [rsp+Ch] [rbp-34h]
  char v2[40]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v3; // [rsp+38h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  strcpy(v2, "I{_}Af2700ih_secTS2Et_wr");
  for ( i = 0; i <= 23; ++i )
    x[24 * i] = v2[i];
  qword_601298 = (__int64)&unk_6011E8;
  qword_6011F0 = (__int64)&unk_601260;
  qword_601268 = (__int64)&unk_6010F8;
  qword_601100 = (__int64)&unk_601110;
  qword_601108 = (__int64)&unk_601140;
  qword_601270 = (__int64)&unk_601230;
  qword_601238 = (__int64)&unk_601158;
  qword_601240 = (__int64)&unk_601098;
  qword_6010A0 = (__int64)&unk_601200;
  qword_6010A8 = (__int64)&unk_601188;
  qword_6011F8 = (__int64)&unk_601170;
  qword_601178 = (__int64)&unk_6011B8;
  qword_601180 = (__int64)&unk_6010B0;
  qword_6010B8 = (__int64)x;
  qword_6010C0 = (__int64)&unk_601218;
  qword_6012A0 = (__int64)&unk_601278;
  qword_601280 = (__int64)&unk_6010E0;
  qword_601288 = (__int64)&unk_6011A0;
  qword_6011B0 = (__int64)&unk_601128;
  qword_601130 = (__int64)&unk_6012A8;
  qword_601138 = (__int64)&unk_6011D0;
  qword_6011D8 = (__int64)&unk_601248;
  qword_6011E0 = (__int64)&unk_6010C8;
  return __readfsqword(0x28u) ^ v3;
}
```

不知道这是在干啥，虽然看到了一串可疑的字符串，但这肯定不是flag。

```c
__int64 __fastcall type1(char *a1)
{
  __int64 result; // rax

  if ( a1 )
  {
    type1(*((_QWORD *)a1 + 1));
    putchar(*a1);
    result = type1(*((_QWORD *)a1 + 2));
  }
  return result;
}
```

是个递归，利用递归输出某个东西，结合main函数是`byte_601290`，不知道为啥找交叉引用没找到。

```c
int __fastcall type2(char *a1)
{
  int result; // eax

  if ( a1 )
  {
    type2(*((_QWORD *)a1 + 1));
    type2(*((_QWORD *)a1 + 2));
    result = putchar(*a1);
  }
  return result;
}
```

和type1差不多，也是输出东西。不对，没有输入点吗？运行一下确实没有，而且无其他藏起来的函数。我要干啥？一脸懵逼地去看[wp](https://blog.csdn.net/qaq517384/article/details/123490164)，原来是二叉树考点。

type1是二叉树的中序遍历，type2是二叉树的后序遍历。关于[二叉树三序遍历](https://www.jianshu.com/p/456af5480cee)还剩个先序，这个先序可能就是flag。三种序分别为：

- 先序：根左右，先输出根节点，再输出左子树，最后是右子树
- 中序：左根右，先输出左子树，再输出根节点，最后是右子树
- 后序：左右根，先输出左子树，再输出右子树，最后是根节点

比如下面这个二叉树：

```
                1
               / \
              2   3
             /     \
            4       5
             \
              6
             / \
            7   8
```

三序遍历结果是：

```
先序：1 2 4 6 7 8 3 5
中序：4 7 6 8 2 1 3 5
后序：7 8 6 4 2 5 3 1
```

先序很好理解，根节点是1，1的左子树是2，2的左子树是4，4没有左子树，就到右子树6。6这个节点的左子树是7，右子树是8。这样2这个节点下的所有节点就遍历完了，到右子树。

中序找到1的左子树2，但是2不仅仅有一个节点，所以又会按照中序的顺序去遍历2的左子树4；4尝试遍历左子树没有，根节点自己已经输出了，就往右子树6看。6有左子树7。这个分支的左子树就输出完了，到根节点（不是最上面的根节点，是分支的根节点）6，右子树8。然后回到2。2没有右子树，直接回到根节点1，1再往下遍历右子树。

后序一个道理。1找到2，2找到4，4虽然没有左子树，但是不确定6有没有，而6有左子树7，这即是第一个输出。然后到右子树8，分支根节点6，4，2，总根节点1。最后是右子树，1找到3，3找到5，输出5后最后输出3。

看起来有点绕，其实只需要记住每种遍历顺序的定义，然后记住这个定义必须在二叉树的每一个部分都遵循。比如我截一个部分：

```
              2
             / 
            4 
             \
              6
             / \
            7   8
```

找到它们刚才遍历时在三个序里的遍历情况：

```
先序：2 4 6 7 8
中序：4 7 6 8 2
后序：7 8 6 4 2
```

发现仍然没有问题。再缩减也是这样，任何一个部分拆出来都是这样。回到题目，题目给出了中序和后序遍历，就能根据这两种遍历构造出原本的二叉树，从而得知先序遍历结果。

```python
def ToPreOrder(Postorder,Inorder):
    length = len(Postorder)
    if length == 0:
        return 0
    root = Postorder[length-1] #根节点　
    for i in range(length):#找到中序遍历中根节点的位序
        if root == Inorder[i]:
            break
    print(root,end="")
    ToPreOrder(Postorder[0:i],Inorder[0:i]) #递归，传入左子树的后序和中序遍历序列
    ToPreOrder(Postorder[i:length-1],Inorder[i+1:length])#递归，传入右子树的后序和中序遍历序列
    
ToPreOrder("20f0Th{2tsIS_icArE}e7__w","2f0t02T{hcsiI_SwA__r7Ee}")
```

这个算法利用递归，每次根据后序输出根节点。因为后序输出保证末尾一定是总根节点，这样递归下去就能还原出原来二叉树的先序遍历结果。

## Flag
> flag{This_IS_A_7reE}