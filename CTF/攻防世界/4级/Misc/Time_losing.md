# Time_losing

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=6dda569a-1f8b-11ed-abf3-fa163e4fa609)

misc每次都能让我大开眼界。

附件是一堆空的txt。空的txt？这能隐写个啥？题目描述倒是有一句话。

- 2033-05-18 11:33:20似乎是个好时间。

查看第一个txt的简介，修改时间格外醒目。

- 2033年5月18日 上午11:34

排除出题人穿越的可能，这个修改时间一定隐藏着什么。可能是电脑设置的问题，我并没有发现怎么藏的，倒是看了[wp](https://blog.csdn.net/l2872253606/article/details/126807005)发现两个时间的差值是flag的ascii值（我的电脑只精确到分所以错过了这么重要的消息……）。大佬的脚本可以直接出flag。

```python
import time
from pathlib import Path

dirpath = r'./stego'
gtime = '2033-05-18 11:33:20'
timestamp = time.mktime(time.strptime(gtime, "%Y-%m-%d %H:%M:%S"))

p = Path(dirpath)
files = [i for i in p.glob('*')]
new_files = sorted(files, key=lambda f: int(f.name.replace('.txt', '')))
modified_files = [i.stat().st_mtime for i in new_files]
sub_times = list(map(lambda x: int(x-timestamp), modified_files))
flag = [chr(x) for x in sub_times]
print(''.join(flag))
```

注意此脚本可能会根据本机环境不同而效果不同。比如我的电脑就不是windows结果出来的东西就很诡异。前几行内容是为了把给的时间[转成时间戳](https://blog.csdn.net/google19890102/article/details/51355282)，使用的[Path](https://blog.csdn.net/kittyzc/article/details/106462397)是python下一个跨平台文件操作库。

### Flag
- XMan{seems_to_be_related_to_the_special_guests}