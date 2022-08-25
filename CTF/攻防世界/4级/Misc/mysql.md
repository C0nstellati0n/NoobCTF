# mysql

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=c04b2fff-92d9-492d-b6e1-2e7f37b1a34c_2)

你永远可以相信strings。

mysql都出来了？根据题目描述，应该是要恢复被删除的数据。我可没有类似的工具，不过根据上次git恢复的经验，我感觉应该有个文件用于记录被删除的数据。

- ### ibdata1
  > ibdata1是一个用来构建innodb系统表空间的文件，这个文件包含了innodb表的元数据、撤销记录、修改buffer和双写buffer。

strings一下ibdata1，然后就出现flag了。这是我没想到的。

当然如果没有思路的话，可以像这位大佬一样熟练使用shell命令。（来自题目wp区）

- find . -type f -exec strings {} \; |grep -i 

这题的正经做法应该是使用Undrop for InnoDB工具，官方wp有提到。但是反正已经做出来谁还管你正经不正经呢？

- ### Flag
  > 71e55075163d5c6410c0d9eae499c977