# ey-or

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=fe889614-a6d2-42c7-bc03-7c3e65e03358_2&task_category_id=4)

这就是为什么逆向做题不能啥也不看直接莽冲。

题目file了一下，确认是elf。ghidra识别出来了，然而ida没有。我还挺疑惑的，怎么识别不出来呢？后来看了一下文件信息，24mb？这东西逆向起来不会死吗？我真的头铁，用ghidra分析，分析半天没出来放弃了。看[wp](https://blukat.me/2015/12/32c3ctf-ey_or/)。

strings真的是神器。以后遇到这种很大的题应该先strings，毕竟谁想得到出题人往里面塞了什么没用的东西撑体积呢？

- strings ey_or > result.txt

然后在里面发现了很可疑的一段内容。

```
] ==secret
] ==f
 secret len ==l
 [ ] ==buffer
 0 ==i
 0 ==j
 "Enter Password line by line\n" sys .out .writeall
  #str .fromArray secret bxor
  txt .consume .u
  =j
[ buffer _ len dearray j ] =buffer
[ secret _ len dearray j eq { } { 1 sys .exit } ? * ] =secret
  i 1 add =i 
  i l eq {
  buffer f bxor str .fromArray sys .out .writeall
 0 sys .exit
} { } ? *
} sys .in .eachLine
"ey_or" sys .freeze
```

这其实是一种名叫[Elymas](https://github.com/Drahflow/Elymas)的语言。看语言的文档将这串代码翻译成python。

```python
secret = [ ???? ]
f = [ ???? ]
l = len(secret)
buffer = []
i = 0
j = 0
print "Enter Password line by line"
for line in sys.stdin.readlines():
    j = read_int(line)
    buffer = buffer + [j]
    if secret[i] != j:
        sys.exit(1)
    i += 1
    if i == l:
        print to_string(map(lambda x,y: x^y, buffer, f))
        sys.exit(0)
```

可以直接爆破，因为密码的每一个字符是分行输入的，如果当前输入的字符不对就直接exit(1)，对了就往下走。全部对了exit(0)。exit返回的信息就是我们爆破的依据。

```python
import sys
import subprocess

ans = []
while True:
    for j in range(256):
        if j % 16 == 15:
            print j
        p = subprocess.Popen("./ey_or.elf", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for x in ans:
            p.stdin.write(str(x) + '\n')
        p.stdin.write(str(j) + '\n')
        p.stdin.close()
        ret = p.wait()
        if ret != 1:
            ans.append(j)
            print ans
            break
```

## Flag
> 32C3_wE_kNoW_EvErYbOdY_LiKeS_eLyMaS