# flag_universe

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=0c8faa09-dc38-4d99-bdf7-d105aa445671_2)

这题其实挺简单的，但是我中途被误导了好几次，还栽在不熟wireshark上。=(

首先附件是个pcapng，流量分析铁了。追踪tcp流发现是ftp，并且看到了flag.txt字样以及一些图片的数据流。在整个pcapng中没有发现flag.txt的内容，那就只能从图片入手了。

追踪每个png，并把下方的设置改成Show data as Raw，再保存。重复几次直到保存好所有的图片。这里会发现有两个png没有图片尾，不要理它，不重要，跟flag没有关系，如果说正常的3个图片中没有再从那2张图片里入手。

保存后用zsteg就可以直接在最后一张图片里找到flag。

- ### Flag
- > flag{Plate_err_klaus_Mail_Life}