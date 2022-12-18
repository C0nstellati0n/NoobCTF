# [网鼎杯 2020 青龙组]singal

[题目地址](https://buuoj.cn/challenges#[%E7%BD%91%E9%BC%8E%E6%9D%AF%202020%20%E9%9D%92%E9%BE%99%E7%BB%84]singal)

ida的显示奇怪了一回。

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4[117]; // [esp+18h] [ebp-1D4h] BYREF

  __main();
  qmemcpy(v4, &unk_403040, 0x1C8u);
  vm_operad(v4, 114);
  puts("good,The answer format is:flag {}");
  return 0;
}
```

main函数里面调用了另一个函数。

```c
int __cdecl vm_operad(int *a1, int a2)
{
  int result; // eax
  char input[200]; // [esp+13h] [ebp-E5h] BYREF
  char v4; // [esp+DBh] [ebp-1Dh]
  int v5; // [esp+DCh] [ebp-1Ch]
  int v6; // [esp+E0h] [ebp-18h]
  int v7; // [esp+E4h] [ebp-14h]
  int v8; // [esp+E8h] [ebp-10h]
  int v9; // [esp+ECh] [ebp-Ch]

  v9 = 0;
  v8 = 0;
  v7 = 0;
  v6 = 0;
  v5 = 0;
  while ( 1 )
  {
    result = v9;
    if ( v9 >= a2 )
      return result;
    switch ( a1[v9] )                           // 该函数就是通过a1这个传进来的数组的值决定操作
    {
      case 1:
        input[v6 + 100] = v4;                   // 这里反编译有些问题，就把input[v6+100]看作另外一个数组[v6]好了。就能得到每个case都是在将输入变换后放入结果数组
        ++v9;
        ++v6;
        ++v8;
        break;
      case 2:
        v4 = a1[v9 + 1] + input[v8];
        v9 += 2;
        break;
      case 3:
        v4 = input[v8] - LOBYTE(a1[v9 + 1]);
        v9 += 2;
        break;
      case 4:
        v4 = a1[v9 + 1] ^ input[v8];
        v9 += 2;
        break;
      case 5:
        v4 = a1[v9 + 1] * input[v8];
        v9 += 2;
        break;
      case 6:
        ++v9;
        break;
      case 7:
        if ( input[v7 + 100] != a1[v9 + 1] )    // 这里也是，input[v7+100]是结果数组
        {
          printf("what a shame...");
          exit(0);
        }
        ++v7;
        v9 += 2;
        break;
      case 8:
        input[v5] = v4;
        ++v9;
        ++v5;
        break;
      case 10:
        read(input);
        ++v9;
        break;
      case 11:
        v4 = input[v8] - 1;
        ++v9;
        break;
      case 12:
        v4 = input[v8] + 1;
        ++v9;
        break;
      default:
        continue;
    }
  }
}
```

结合main函数可知，a1数组就是v4就是`unk_403040`。这个数组的值在程序里，拷贝出来。然后根据case 7的比较得出结果数组的值，并将结果数组和a1数组倒过来，实现逆向switch语句的操作。注意a1数组和生成的结果数组都要反过来。

```python
v4=[]
s=[10, 4, 16, 8, 3, 5, 1, 4, 32, 8, 5, 3, 1, 3, 2, 8, 11, 1, 12, 8, 4, 4, 1, 5, 3, 8, 3, 33, 1, 11, 8, 11, 1, 4, 9, 8, 3, 32, 1, 2, 81, 8, 4, 36, 1, 12, 8, 11, 1, 5, 2, 8, 2, 37, 1, 2, 54, 8, 4, 65, 1, 2, 32, 8, 5, 1, 1, 5, 3, 8, 2, 37, 1, 4, 9, 8, 3, 32, 1, 2, 65, 8, 12, 1, 7, 34, 7, 63, 7, 52, 7, 50, 7, 114, 7, 51, 7, 24, 7, 167, 255, 255, 255, 7, 49, 7, 241, 255, 255, 255, 7, 40, 7, 132, 255, 255, 255, 7, 193, 255, 255, 255, 7, 30, 7, 122]
for i in range(0,len(s)):
          if s[i]==7:
                    v4.append(s[i+1])
v4.reverse()

a=[10, 4, 16, 8, 3, 5, 1, 4, 32, 8, 5, 3, 1, 3, 2, 8, 11, 1, 12, 8, 4, 4, 1, 5, 3, 8, 3, 33, 1, 11, 8, 11, 1, 4, 9, 8, 3, 32, 1, 2, 81, 8, 4, 36, 1, 12, 8, 11, 1, 5, 2, 8, 2, 37, 1, 2, 54, 8, 4, 65, 1, 2, 32, 8, 5, 1, 1, 5, 3, 8, 2, 37, 1, 4, 9, 8, 3, 32, 1, 2, 65, 8, 12, 1]
a.reverse()

v9 = 0
us=0
v5=0
flag=[]
for i in range(0,len(a)):
          if i ==len(a)-1:
                    flag.append(us)
                    
          if a[i]==1 and a[i-1]!=1: #这些原程序没有的条件都是必须加的，比如这个不要下一行就会报错IndexError: list index out of range
                    v5 = v4[v9]
                    v9+=1
                    flag.append(us)
                    
          if a[i]==2:
                    if(a[i+1]!=3 and a[i+1]!=4 and a[i+1]!=5):
                              us = v5 - a[i-1]
                              #print(us,v5,a[i-1])
                    
          if a[i]==3:
                    if(a[i+1]!=2 and a[i+1]!=4 and a[i+1]!=5):               
                              us = v5 + a[i-1]  #LOBYTE是al有8位，参与运算的5、33、32是全值，所以LOBYTE可省略
                    
          if a[i]==4:
                    if(a[i+1]!=3 and a[i+1]!=2 and a[i+1]!=5):
                              us = v5^a[i-1]

          if a[i]==5:
                    if(a[i+1]!=3 and a[i+1]!=4 and a[i+1]!=2):
                              us = int(v5/a[i-1])
          if a[i]==8:
                    v5 = us
                              
          if a[i]==11:
                    us = v5 +1
          if a[i]==12:
                    us = v5 -1
                    #print("12:",us)

flag.reverse()
out=''
for j in flag:
          out +=chr(j)
print("flag{"+out+"}")
```

## Flag
> flag{757515121f3d478}