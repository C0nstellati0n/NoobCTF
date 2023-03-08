# snek

[题目](https://github.com/uclaacm/lactf-archive/tree/main/2023/rev/snek)

[wp](https://justinapplegate.me/2023/lactf-snek/)讲的已经很明白了，加上[这篇](https://hackmd.io/@lamchcl/r1zQkbvpj#revsnek)还拓宽了思路。这里总结一下。

因为给的文件和python的pickle序列化对象有关，所以可以用[pickletools](https://docs.python.org/3/library/pickletools.html)反编译出来。将题目里的字节单独提取出来写入另一个文件（snek.pickle），运行`python3 -m pickletools snek.pickle`即可获得反编译结果。出来的结果遵循`line: rawopcode OPCODENAME opcodevalue`的格式。[文档](https://docs.juliahub.com/Pickle/LAUNc/0.1.0/opcode/)里标注了各个pickle opcodes。可以人工翻译，不过题目太长了，于是wp作者自己实现了一个[解释器](https://justinapplegate.me/static/lactf-snek/pickletools_interpreter.py)：

```python
import operator
import functools
import pickle
import itertools

instructions = open("ins.txt",'r').read().split('\n')

stack = []
memo = {}
frozensets = []

for inst in instructions:
    # parse instruction + value
    try:
        brk = inst.index(' ')
        opcode = inst[:brk]
        val = inst[brk:].strip()
    except ValueError:
        opcode = inst
        val = ""

    match opcode:
        case "PROTO":
            print("Protocol: " + val)

        case "FRAME":
            print("Frame: " + val)

        case "MARK":
            stack.append("MARK")

        case "NONE":
            "do nothing"

        case "POP":
            stack.pop()

        case "BININT1":
            stack.append(int(val))

        case "BININT2":
            stack.append(int(val))

        case "BINFLOAT":
            stack.append(float(val))

        case "BINUNICODE":
            stack.append(val.replace("'",""))

        case "UNICODE":
            stack.append(val.replace("'",""))

        case "SHORT_BINUNICODE":
            stack.append(val.replace("'",""))

        case "MEMOIZE":
            memo[val.replace("(as ","").replace(")","")] = stack[-1]

        case "TUPLE1":
            stack.append((stack.pop(),))

        case "TUPLE2":
            second = stack.pop()
            first = stack.pop()
            stack.append((first,second))

        case "LONG1":
            stack.append(val)

        case "FROZENSET":
            frozenset = {stack.pop()} # first element
            while stack[-1] != "MARK":
                frozenset.add(stack.pop()) # may add in wrong order
            stack.pop() # MARK
            frozensets.append(frozenset)

        case "BINGET":
            stack.append(memo[val])

        case "LONG_BINGET":
            stack.append(memo[val])

        case "NEWTRUE":
            stack.append(True)

        case "TUPLE":
            tup = []
            while (stack[-1] != "MARK"):
                tup.insert(0,stack.pop())
            stack.pop() # MARK
            stack.append(tuple(tup))

        case "LIST":
            ls = []
            while (stack[-1] != "MARK"):
                ls.insert(0,stack.pop())
            stack.pop() # MARK
            stack.append(ls)

        case "DICT":
            dictry = {}
            second = stack.pop()
            first = stack.pop()
            while (stack[-1] != "MARK"):
                ls[first] = second
            stack.pop() # MARK
            stack.append(dictry)

        case "GLOBAL":
            stack.append(eval(""+val[val.index(' '):].strip()[:-1]))

        case "STACK_GLOBAL":
            second = stack.pop()
            first = stack.pop()
            if first == "builtins": stack.append(eval(second))
            else: stack.append(eval(first+"."+second))

        case "GET":
            stack.append(memo[val])

        case "STOP":
            "do nothing"

        case "REDUCE":
            args = stack.pop()
            func = stack.pop()
            print("=========== FUNCTION EVAL ===========")
            print("    Stack: " + str(stack))
            print("    Evaluating: " + func.__qualname__ + str(args))
            if type(args[0]) == reversed: 
                output = bytes(reversed('省略',))
            elif (func.__qualname__ == "loads") and (len(stack) == 13):
                output = pickle.loads(b'省略')
            elif (func.__qualname__ == "bytes") and (len(stack) == 12): 
                output = bytes(map(functools.partial(operator.and_,255), itertools.starmap(operator.xor,enumerate(b'省略'))))
            else: output = func(*args)
            try:
                print("    Output: " + list(output))
            except:
                print("    Output: " + str(output))
            stack.append(output)
            print()

        case "EMPTY_DICT":
            stack.append({})

        case "DUP":
            stack.append(stack[-1])

        case "INT":
            stack.append(int(val))

        case "BINBYTES":
            stack.append(bytes(eval(val[1:]),'utf-8'))

        case _:
            print("Unknown opcode: " + opcode)
            print("Value: " + val)
            print("Stack: " + str(stack))
            exit(1)


print("Stack length:",len(stack))
print("Memo length:",len(memo))
print("Frozensets length:",len(frozensets))


print("Stack:",stack)
print("Memo:",memo)
print("Frozensets:",frozensets)
```

该解释器的输入文件格式为`OPCODENAME opcodevalue`，即pickle tools结果文件不要`line: rawopcode`部分。省略的部分是硬编码部分，因为有些表达式只能用一次：

```
>>> b = reversed(b'abc')
>>> bytes(b)
b'cba'
>>> bytes(b)
b''
```

导致原作者不得不自己提前把这些值摘抄下来。运行代码会发现一个code object（CodeType），可用dis.dis反编译。

```python
from types import CodeType
import dis
code = CodeType(0, 0, 0, 21, 11, 67, ...) # object from above
dis.dis(code)
```

出来的结果原作者是手译的，因为uncompyle6不支持python3.8以后的代码，pycdc不能识别[frozenset](https://blog.csdn.net/lilong117194/article/details/78522459)。代码如下：

```python
#!/usr/bin/python3

import time
from collections import deque

SIZE = 20
key = 140447092963680462851258172325

fruit = [
    frozenset({(6, 12), (3, 4), (4, 9), (19, 6), (9, 5), (14, 19), (5, 16), (19, 9), (10, 0), (8, 6), (8, 9), (10, 9), (17, 12), (8, 3), (1, 3), (16, 7), (7, 7), (14, 9), (17, 5), (14, 12), (4, 11), (5, 12), (8, 11), (19, 8), (8, 14), (19, 14), (9, 16), (0, 16), (11, 16), (16, 3), (18, 12), (16, 18), (7, 18), (4, 7), (4, 1), (4, 4), (4, 16), (5, 5), (8, 4), (17, 1), (19, 1), (11, 0), (14, 17), (0, 6), (16, 2), (1, 13), (2, 15), (18, 5), (15, 12), (16, 11)}), 
    frozenset({(6, 18), (6, 15), (17, 3), (5, 1), (17, 9), (14, 13), (5, 10), (8, 9), (14, 19), (11, 5), (10, 9), (9, 11), (8, 15), (2, 5), (1, 18), (12, 3), (14, 6), (15, 9), (14, 9), (3, 9), (5, 3), (17, 11), (4, 11), (5, 15), (8, 14), (11, 10), (2, 7), (9, 19), (2, 13), (6, 7), (18, 6), (6, 3), (14, 2), (5, 2), (12, 17), (3, 8), (3, 17), (17, 10), (17, 16), (0, 3), (2, 0), (17, 19), (8, 13), (2, 9), (10, 16), (15, 0), (13, 3), (1, 16), (13, 15), (18, 11)}),
    frozenset({(18, 17), (7, 17), (3, 1), (3, 10), (3, 16), (5, 13), (5, 1), (8, 3), (8, 18), (1, 12), (6, 2), (16, 16), (15, 17), (6, 17), (14, 0), (17, 2), (14, 9), (5, 3), (9, 1), (17, 14), (8, 11), (8, 5), (10, 5), (8, 17), (2, 7), (15, 4), (13, 1), (1, 5), (0, 13), (19, 17), (7, 9), (6, 13), (12, 8), (17, 7), (4, 13), (19, 1), (9, 9), (14, 17), (5, 14), (5, 17), (11, 9), (10, 7), (10, 1), (9, 15), (0, 12), (0, 15), (10, 19), (18, 2), (16, 11), (15, 15)}),
    frozenset({(3, 4), (14, 4), (12, 10), (3, 7), (4, 6), (5, 7), (19, 6), (4, 15), (19, 3), (0, 5), (0, 8), (11, 17), (2, 8), (15, 17), (7, 13), (3, 0), (4, 5), (14, 3), (14, 18), (3, 18), (12, 18), (3, 15), (19, 5), (8, 11), (19, 11), (0, 10), (11, 10), (13, 7), (10, 8), (0, 13), (2, 16), (15, 10), (7, 9), (7, 6), (16, 18), (12, 5), (4, 4), (4, 16), (4, 19), (19, 1), (17, 16), (19, 7), (9, 12), (11, 12), (0, 12), (13, 6), (7, 2), (18, 2), (13, 15), (15, 12)}),
    frozenset({(8, 0), (5, 13), (0, 2), (19, 3), (10, 0), (9, 8), (2, 2), (9, 17), (11, 8), (0, 8), (10, 15), (7, 4), (7, 1), (16, 10), (15, 14), (6, 8), (15, 17), (18, 13), (12, 3), (3, 6), (17, 11), (4, 17), (9, 7), (5, 12), (0, 4), (11, 13), (0, 19), (15, 13), (16, 6), (18, 12), (6, 10), (16, 18), (12, 11), (7, 18), (17, 4), (3, 11), (3, 14), (4, 19), (0, 3), (17, 19), (13, 0), (5, 17), (2, 3), (11, 18), (9, 18), (15, 6), (1, 13), (1, 10), (0, 18), (16, 17)}),
    frozenset({(4, 6), (4, 12), (9, 2), (3, 10), (17, 6), (17, 12), (11, 2), (9, 8), (9, 14), (10, 3), (9, 17), (17, 18), (2, 11), (0, 11), (15, 8), (12, 6), (4, 5), (3, 6), (3, 12), (19, 11), (9, 10), (19, 14), (8, 17), (15, 4), (11, 13), (2, 10), (10, 17), (1, 14), (16, 6), (15, 10), (6, 13), (15, 19), (6, 16), (16, 18), (12, 5), (3, 2), (17, 4), (4, 16), (17, 1), (3, 8), (3, 17), (8, 7), (1, 1), (9, 12), (11, 9), (19, 10), (2, 0), (2, 6), (7, 11), (15, 18)}),
    frozenset({(4, 0), (12, 7), (3, 4), (14, 7), (19, 0), (19, 6), (4, 15), (3, 19), (10, 0), (14, 19), (9, 14), (13, 11), (18, 1), (1, 15), (12, 3), (14, 6), (4, 5), (4, 14), (3, 12), (19, 2), (9, 1), (11, 1), (8, 14), (19, 14), (2, 7), (0, 13), (0, 19), (11, 19), (1, 14), (13, 16), (13, 13), (16, 12), (15, 19), (6, 19), (5, 2), (3, 8), (5, 5), (19, 4), (8, 4), (3, 14), (19, 7), (19, 10), (1, 4), (8, 13), (16, 2), (13, 6), (7, 2), (0, 18), (6, 3), (16, 11)}),
    frozenset({(7, 17), (9, 5), (0, 2), (10, 0), (14, 13), (9, 14), (13, 2), (9, 11), (19, 18), (8, 18), (16, 4), (1, 9), (16, 7), (13, 8), (15, 11), (1, 18), (2, 17), (13, 17), (15, 14), (7, 13), (4, 2), (12, 15), (4, 11), (19, 11), (17, 17), (11, 10), (19, 17), (8, 17), (1, 11), (11, 13), (0, 19), (13, 16), (6, 7), (6, 13), (16, 18), (7, 18), (17, 4), (19, 4), (4, 13), (4, 19), (14, 17), (10, 4), (13, 3), (15, 6), (9, 18), (2, 6), (2, 15), (16, 14), (7, 11), (7, 8)}),
    frozenset({(6, 18), (7, 17), (14, 4), (7, 5), (14, 1), (5, 16), (10, 6), (0, 17), (10, 15), (16, 7), (13, 14), (6, 5), (16, 13), (18, 19), (14, 6), (4, 14), (17, 5), (8, 2), (8, 5), (5, 18), (5, 12), (19, 8), (11, 7), (13, 4), (0, 16), (13, 10), (15, 7), (18, 0), (16, 6), (16, 12), (15, 10), (6, 13), (16, 15), (15, 19), (16, 18), (14, 2), (12, 11), (9, 0), (17, 7), (19, 7), (17, 13), (0, 9), (5, 17), (15, 0), (2, 6), (16, 5), (1, 10), (18, 5), (16, 17), (7, 14)}),
    frozenset({(12, 7), (3, 1), (12, 19), (3, 10), (9, 5), (8, 3), (10, 0), (3, 19), (17, 6), (9, 14), (5, 19), (10, 3), (17, 18), (11, 14), (2, 11), (2, 8), (15, 11), (16, 16), (6, 14), (3, 0), (3, 3), (5, 6), (17, 5), (3, 12), (4, 17), (8, 8), (0, 7), (2, 4), (9, 16), (13, 1), (1, 11), (2, 10), (6, 4), (18, 3), (6, 16), (7, 15), (7, 18), (4, 10), (5, 5), (4, 13), (3, 17), (0, 9), (5, 17), (9, 15), (8, 19), (1, 7), (16, 5), (7, 2), (6, 6), (13, 15)})
]
#每个frozenset代表每一关的水果坐标

actual_snek = deque([(0,0)])
#下方为一些无关紧要的游戏操作逻辑
direction_facing = (1,0)
current_frozen_set = 0
fruits_eaten = []
while True:

    # generate map
    entire_map = ''
    for xcoord in range(SIZE):
        row = ''
        for ycoord in range(SIZE):

            # mark snek body
            if (xcoord,ycoord) in actual_snek:
                row+='#'
                continue

            # mark food
            if (xcoord,ycoord) in fruit[current_frozen_set]:
                row+='o'
                continue
            row+='.'
        entire_map+=row+'\n'
    print(entire_map,flush=True)

    inp = input('snek? ').strip().split()[0]


    if len(inp)>0:
        inp_val = inp#.popleft()
        if isinstance(inp_val,int) or inp_val.isdigit():
            inp_val = int(inp_val)
            #inp_val -= 1
            for _ in range(inp_val):
                snek16 = actual_snek[0]
                coords = (snek16[0] + direction_facing[0] ,snek16[1] + direction_facing[1])

                # off screen
                if coords[0]<0:
                    print('snek dead :(')
                    exit()
                if coords[0]>=SIZE:
                    print('snek dead :(')
                    exit()
                if coords[1]<0:
                    print('snek dead :(')
                    exit()
                if coords[1]>=SIZE:
                    print('snek dead :(')
                    exit()

                actual_snek.appendleft(coords)
                if coords in fruit[current_frozen_set]:
                    print(coords)
                    current_frozen_set+=1
                    actual_snek.append(coords)
                    fruits_eaten.append(coords)

                    # if through all 10 frozen sets
                    #重点在这里
                    if current_frozen_set == len(fruit):
                        total=0
                        for xcoord,ycoord in fruits_eaten:
                            total = total^1337
                            total *= SIZE**2
                            # at this point, total = 534800
                            total += xcoord*20 + ycoord
                        if key == total:
                            print('snek happy :D')
                            print(open('flag.txt','r').read().strip())
                        else:
                            print(total)
                            print('snek sad :(')
                            exit()
                    else:
                        actual_snek.pop()
                else:
                    actual_snek.pop()
        else:
            if inp_val == 'L':
                direction_facing = (-direction_facing[1],direction_facing[0])
            elif inp_val == 'R':
                direction_facing = (direction_facing[1],-direction_facing[0])
            else:
                print('snek confused :(')
                exit()
        time.sleep(0.1)
    else:
        ""
```

代码里的获胜判断逻辑告诉我们如何获得flag。每一关吃到的水果坐标x和y经过一系列运算后需要等于key。因为坐标不多，倒着来全部过一遍就好了。

```python
fruit = [
    [(6, 12), (3, 4), (4, 9), (19, 6), (9, 5), (14, 19), (5, 16), (19, 9), (10, 0), (8, 6), (8, 9), (10, 9), (17, 12), (8, 3), (1, 3), (16, 7), (7, 7), (14, 9), (17, 5), (14, 12), (4, 11), (5, 12), (8, 11), (19, 8), (8, 14), (19, 14), (9, 16), (0, 16), (11, 16), (16, 3), (18, 12), (16, 18), (7, 18), (4, 7), (4, 1), (4, 4), (4, 16), (5, 5), (8, 4), (17, 1), (19, 1), (11, 0), (14, 17), (0, 6), (16, 2), (1, 13), (2, 15), (18, 5), (15, 12), (16, 11)], 
    [(6, 18), (6, 15), (17, 3), (5, 1), (17, 9), (14, 13), (5, 10), (8, 9), (14, 19), (11, 5), (10, 9), (9, 11), (8, 15), (2, 5), (1, 18), (12, 3), (14, 6), (15, 9), (14, 9), (3, 9), (5, 3), (17, 11), (4, 11), (5, 15), (8, 14), (11, 10), (2, 7), (9, 19), (2, 13), (6, 7), (18, 6), (6, 3), (14, 2), (5, 2), (12, 17), (3, 8), (3, 17), (17, 10), (17, 16), (0, 3), (2, 0), (17, 19), (8, 13), (2, 9), (10, 16), (15, 0), (13, 3), (1, 16), (13, 15), (18, 11)],
    [(18, 17), (7, 17), (3, 1), (3, 10), (3, 16), (5, 13), (5, 1), (8, 3), (8, 18), (1, 12), (6, 2), (16, 16), (15, 17), (6, 17), (14, 0), (17, 2), (14, 9), (5, 3), (9, 1), (17, 14), (8, 11), (8, 5), (10, 5), (8, 17), (2, 7), (15, 4), (13, 1), (1, 5), (0, 13), (19, 17), (7, 9), (6, 13), (12, 8), (17, 7), (4, 13), (19, 1), (9, 9), (14, 17), (5, 14), (5, 17), (11, 9), (10, 7), (10, 1), (9, 15), (0, 12), (0, 15), (10, 19), (18, 2), (16, 11), (15, 15)],
    [(3, 4), (14, 4), (12, 10), (3, 7), (4, 6), (5, 7), (19, 6), (4, 15), (19, 3), (0, 5), (0, 8), (11, 17), (2, 8), (15, 17), (7, 13), (3, 0), (4, 5), (14, 3), (14, 18), (3, 18), (12, 18), (3, 15), (19, 5), (8, 11), (19, 11), (0, 10), (11, 10), (13, 7), (10, 8), (0, 13), (2, 16), (15, 10), (7, 9), (7, 6), (16, 18), (12, 5), (4, 4), (4, 16), (4, 19), (19, 1), (17, 16), (19, 7), (9, 12), (11, 12), (0, 12), (13, 6), (7, 2), (18, 2), (13, 15), (15, 12)],
    [(8, 0), (5, 13), (0, 2), (19, 3), (10, 0), (9, 8), (2, 2), (9, 17), (11, 8), (0, 8), (10, 15), (7, 4), (7, 1), (16, 10), (15, 14), (6, 8), (15, 17), (18, 13), (12, 3), (3, 6), (17, 11), (4, 17), (9, 7), (5, 12), (0, 4), (11, 13), (0, 19), (15, 13), (16, 6), (18, 12), (6, 10), (16, 18), (12, 11), (7, 18), (17, 4), (3, 11), (3, 14), (4, 19), (0, 3), (17, 19), (13, 0), (5, 17), (2, 3), (11, 18), (9, 18), (15, 6), (1, 13), (1, 10), (0, 18), (16, 17)],
    [(4, 6), (4, 12), (9, 2), (3, 10), (17, 6), (17, 12), (11, 2), (9, 8), (9, 14), (10, 3), (9, 17), (17, 18), (2, 11), (0, 11), (15, 8), (12, 6), (4, 5), (3, 6), (3, 12), (19, 11), (9, 10), (19, 14), (8, 17), (15, 4), (11, 13), (2, 10), (10, 17), (1, 14), (16, 6), (15, 10), (6, 13), (15, 19), (6, 16), (16, 18), (12, 5), (3, 2), (17, 4), (4, 16), (17, 1), (3, 8), (3, 17), (8, 7), (1, 1), (9, 12), (11, 9), (19, 10), (2, 0), (2, 6), (7, 11), (15, 18)],
    [(4, 0), (12, 7), (3, 4), (14, 7), (19, 0), (19, 6), (4, 15), (3, 19), (10, 0), (14, 19), (9, 14), (13, 11), (18, 1), (1, 15), (12, 3), (14, 6), (4, 5), (4, 14), (3, 12), (19, 2), (9, 1), (11, 1), (8, 14), (19, 14), (2, 7), (0, 13), (0, 19), (11, 19), (1, 14), (13, 16), (13, 13), (16, 12), (15, 19), (6, 19), (5, 2), (3, 8), (5, 5), (19, 4), (8, 4), (3, 14), (19, 7), (19, 10), (1, 4), (8, 13), (16, 2), (13, 6), (7, 2), (0, 18), (6, 3), (16, 11)],
    [(7, 17), (9, 5), (0, 2), (10, 0), (14, 13), (9, 14), (13, 2), (9, 11), (19, 18), (8, 18), (16, 4), (1, 9), (16, 7), (13, 8), (15, 11), (1, 18), (2, 17), (13, 17), (15, 14), (7, 13), (4, 2), (12, 15), (4, 11), (19, 11), (17, 17), (11, 10), (19, 17), (8, 17), (1, 11), (11, 13), (0, 19), (13, 16), (6, 7), (6, 13), (16, 18), (7, 18), (17, 4), (19, 4), (4, 13), (4, 19), (14, 17), (10, 4), (13, 3), (15, 6), (9, 18), (2, 6), (2, 15), (16, 14), (7, 11), (7, 8)],
    [(6, 18), (7, 17), (14, 4), (7, 5), (14, 1), (5, 16), (10, 6), (0, 17), (10, 15), (16, 7), (13, 14), (6, 5), (16, 13), (18, 19), (14, 6), (4, 14), (17, 5), (8, 2), (8, 5), (5, 18), (5, 12), (19, 8), (11, 7), (13, 4), (0, 16), (13, 10), (15, 7), (18, 0), (16, 6), (16, 12), (15, 10), (6, 13), (16, 15), (15, 19), (16, 18), (14, 2), (12, 11), (9, 0), (17, 7), (19, 7), (17, 13), (0, 9), (5, 17), (15, 0), (2, 6), (16, 5), (1, 10), (18, 5), (16, 17), (7, 14)],
    [(12, 7), (3, 1), (12, 19), (3, 10), (9, 5), (8, 3), (10, 0), (3, 19), (17, 6), (9, 14), (5, 19), (10, 3), (17, 18), (11, 14), (2, 11), (2, 8), (15, 11), (16, 16), (6, 14), (3, 0), (3, 3), (5, 6), (17, 5), (3, 12), (4, 17), (8, 8), (0, 7), (2, 4), (9, 16), (13, 1), (1, 11), (2, 10), (6, 4), (18, 3), (6, 16), (7, 15), (7, 18), (4, 10), (5, 5), (4, 13), (3, 17), (0, 9), (5, 17), (9, 15), (8, 19), (1, 7), (16, 5), (7, 2), (6, 6), (13, 15)]
]

SIZE = 20

key = 140447092963680462851258172325

picks = [None for i in range(10)]

total = 0
fruits_eaten = [u[0] for u in fruit]
for xcoord,ycoord in fruits_eaten:
    total = total^1337
    total *= SIZE**2
    total += xcoord*SIZE + ycoord

print(total)

for i in range(9, -1, -1):#倒着来
    l = fruit[i]
    curr = key
    for xcoord, ycoord in l:
        if (curr - xcoord*SIZE - ycoord) % SIZE**2 == 0:#如果当前的x和y是正确的，结果模SIZE**2应该没有余数
            #对应：
            #total *= SIZE**2
            #total += xcoord*20 + ycoord
            curr = (curr - xcoord*3 - ycoord) // SIZE**2#这里乘3不太明白是什么意思，按照加密代码
            #curr = (curr - xcoord*SIZE - ycoord) // SIZE**2  也是可以的
            curr ^= 1337
            picks[i] = (xcoord, ycoord)
            key = curr
            print(picks)
            break
```

最后连上服务器按照坐标吃水果就好了。第二个wp的思路则比较巧妙。运行文件，发现有一句"snek?"，说明内部一定有print函数。从[builtins](https://docs.python.org/3/library/builtins.html)中导入print函数，将其写为我们自己的print，内部调用[pdb](https://docs.python.org/3/library/pdb.html)的breakpoint函数插入断点。将下方代码放到snek.py的开头。

```python
import builtins
_print = print
def new_print(*args, **kwargs):
	breakpoint()
	return _print(*args, **kwargs)
builtins.print = new_print
```

进入调试界面后，可用[inspect](https://docs.python.org/3/library/inspect.html)检查当前栈帧：

```python
-> return _print(*args, **kwargs)
(Pdb) import inspect; inspect.currentframe()
<frame at 0x7fb65f211490, file '<stdin>', line 1, code <module>>
```

当前栈帧单纯是输入逻辑，我们需要回到print被调用的那个栈帧查看函数的主逻辑。

```python
(Pdb) frame = inspect.currentframe().f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back
(Pdb) frame
<frame at 0x5579fb06b6a0, file 'snek', line -1, code snek>
```

与第一种解法殊途同归，利用frame.f_code获取当前栈帧的code object，反编译后获取结果。

```python
(Pdb) import dis
(Pdb) dis.dis(frame.f_code)
```

这回不手译了，想办法用工具。当前python的反编译工具基本只支持反编译pyc文件，有没有办法把code object类型的文件写为pyc文件？答案是有，[这里](https://stackoverflow.com/questions/73439775/how-to-convert-marshall-code-object-to-pyc-file/73454818#73454818)有详细说明。不过在转换之前最好把变量名换一下。查看当前栈帧的变量名，全是一个名：

```python
(Pdb) frame.f_code.co_varnames
('snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek', 'snek')
```

重命名为别的后再写为pyc文件。

```python
(Pdb) codeobj = frame.f_code.replace(co_varnames=tuple('snek'+str(i) for i in range(21)))
(Pdb) import importlib; pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(codeobj)
(Pdb) with open("snek.pyc", "wb") as f: f.write(pyc_data)
```

然后取github搜一个[python 3.10 decompiler](https://github.com/greyblue9/unpyc37-3.10)就好了。这个能运行，不过结果有错误，需要人工稍微改正一下。还是比纯手译好。这个作者选择直接逆向：

```python
target = 140447092963680462851258172325
positions = []
for i in range(10):
    target, remainder = target//400, target%400 #target//400对应total *= SIZE**2；target%400对应total += xcoord*20 + ycoord
    positions.append([remainder//20, remainder%20])#remainder//20对应xcoord*20；remainder%20对应 + ycoord
    target ^= 1337
for i in positions[::-1]: print(i)#结果倒过来
```

## Flag
> lactf{h4h4_sn3k_g0_brrrrrrrr}