# easyjava

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=3b8d4e97-25c9-46c8-ab8f-ade1eeb79051_2&task_category_id=6)

不会又要学一门java吧？

直接上jadx，发现函数和类的命名全是a，b，c这种。工具栏选择反混淆后再分析。

Encrypt函数中取出输入的flag的中间部分，然后分别初始化Encryptor1和Encryptor2。主要加密函数是m6a，m6a内部是一个嵌套调用。先看Encryptor1类。

构造函数初始化nums的状态，根据传入的参数做轮转的操作。MainActivity的Encrypt函数里调用的m1a逻辑不难，找到参数在charTable里的位置，然后在f2486a（构造函数中轮转操作的结果）中找到对应位置的索引。最后调用m2a，m2a这个函数还是个轮转操作，把charTable第一个字母插入到末尾再删掉第一个字母，f2486a同理，每轮转一次f2488d加一，这个就是个计数的参数罢了。

Encryptor2和Encryptor1差不多，构造函数先转几圈，f2482a是初始轮转后的结果，f2484d计数。MainActivity的Encrypt函数里调用的m3a找到参数在f2482a里的索引并根据索引返回f2482a在索引处的值。无论是第一个if语句里的m4a，还是返回前的m4a，程序都不会进入。就算进入了，m4a函数内部会判断f2484d的值，超过25才会执行轮转。根据MainActivity的Encrypt函数末尾的equals，我们知道输入不可能有25位长，故怎么也不可能满足条件。

粗略分析后就能逆向了。整个程序加密时将输入的每一个字符找到其在Encryptor的f2486a中的索引，然后f2486a轮转一次；接着把刚刚返回的索引放到Encryptor2的f2482a中取出对应元素并返回。逆向的话只需要找到期望字符串在f2482a的索引，然后输出f2486a索引的字符并轮转f2486a一次。分析出来了不会写脚本，索性直接看[wp](https://blog.csdn.net/qq_41429081/article/details/90234730)，发现类似的操作可以用python自带的[双端队列](https://blog.csdn.net/weixin_37589575/article/details/106630235)来实现。

```python
from collections import deque#双端队列
alpha = deque("abcdefghijklmnopqrstuvwxyz") 
t1 = deque([8, 25, 17, 23, 7, 22, 1, 16, 6, 9, 21, 0, 15, 5, 10, 18, 2, 24, 4, 11, 3, 14, 19, 12, 20, 13]) 
t2 = deque([7, 14, 16, 21, 4, 24, 25, 20, 5, 15, 9, 17, 6, 13, 3, 18, 12, 10, 19, 0, 22, 2, 11, 23, 1, 8])

ss = 'wigwrkaugala'
for _ in range(2): 
    t1.append(t1.popleft()) #实现转动
for _ in range(3): 
    t2.append(t2.popleft()) 
print(t1) 
print(t2)

def dec(s): 
    i = t2[(ord(s) - ord('a'))] #ord(s) - ord('a')就可以得到在那个a到z的字符中的索引值
    i = t1[(i)] 
    print(alpha[i], end='')
    t1.append(t1.popleft()) 
    alpha.append(alpha.popleft())
for s in ss: dec(s)
```

## Flag
> flag{venividivkcr}