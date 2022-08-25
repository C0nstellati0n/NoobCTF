# MISCall

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e4eaa969-2310-49ca-a9b1-927e45cab8b5_2)

这道题考的就是git命令的使用了。太棒了我不会（用Github却不会git命令真的是屑(._.)）

附件是bzip2文件，可以用【bzip2 -d 文件名】命令来解压。如果跟我的电脑一样没有安装这个命令，也可以在[网上](https://extract.me/)提取。提取出来的文件是个tar，解压后是一个名叫ctf的仓库。

![ctf](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/ctf.png)

能看见第一个文件就是flag.txt，难道是送分题？事实证明没那么好的事。

> Nothing to see here, moving along...

ls -a命令来看看里面都有些啥。（-a参数一定要加，表示展示所有文件和文件夹，不加就只有一个孤单的假flag文件）可以发现有一个.git文件夹。再进到里面。

> COMMIT_EDITMSG	HEAD		ORIG_HEAD	branches	config		description	hooks		index		info		log
> objects		refs

这里介绍一下这个挑战需要用到的重要文件和命令

> #### log 
> - 这个文件记录了整个仓库的提交记录
> #### git log
> - 查看指定文件的提交记录
> ### git stash list
> - 查看stash中的存储内容
> #### git stash show
> - 显示文件所做的改动
> #### git stash apply
> - 应用指定存储（可以理解为恢复stash中的文件）

有了这些命令，这个挑战就很简单了。首先git log，看看提交记录。

> commit bea99b953bef6cc2f98ab59b10822bc42afe5abc (HEAD -> master)

但是你会发现没有这个文件。可以用find命令查找当前目录下是否有这个文件。

> #### find
> - find 当前文件夹路径 -name 要查找的文件名

那就用git stash list看看最近修改了啥。

> stash@{0}: WIP on master: bea99b9 Initial commit

有修改，那么这个修改很可能有我没想要的东西。用git stash show看看存储了什么改动文件

>  flag.txt | 25 ++++++++++++++++++++++++-
>  s.py     |  4 ++++
>  2 files changed, 28 insertions(+), 1 deletion(-)

flag！赶紧用git stash apply恢复文件。记得把刚才的假flag先删了，否则操作会被终止。

> On branch master
>Changes to be committed:
> (use "git restore --staged <file>..." to unstage)
>	new file:   s.py

>Changes not staged for commit:
>  (use "git add <file>..." to update what will be committed)
>  (use "git restore <file>..." to discard changes in working directory)
>	modified:   flag.txt

但flag.txt里并不直接是flag，需要运行s.py才能得到flag。

```python
#!/usr/bin/env python
from hashlib import sha1
with open("你的flag.txt文件地址", "rb") as fd:
    print("NCN" + sha1(fd.read()).hexdigest())
```

> ### Flag
> - NCN4dd992213ae6b76f27d7340f0dde1222888df4d3