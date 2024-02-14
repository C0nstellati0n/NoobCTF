# Pwn学习笔记

这里记录一些平时看的和pwn有关的教程里的知识点

## [教程一](https://www.youtube.com/watch?v=CgGha_zLqlo&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN)

1. Reversing Statically-Linked Binaries with Function Signatures
- 当elf文件静态包含libc并stripped时，一些libc内的函数名无法被识别。这时可以利用插件+函数签名的方式还原函数名。ida pro可以用[F.L.I.R.T.](https://hex-rays.com/products/ida/tech/flirt/)，放到ghidra可以用[ApplySig](https://github.com/NWMonster/ApplySig),签名文件可以在[sig-database](https://github.com/push0ebp/sig-database)里找到
2. Exploit Dev Pitfall Corrupted Shellcode
- 运行栈上的shellcode时，一定要注意将shellcode和rip隔离（利用nop多滑几段栈）。否则当shellcode内部执行到push时，push进来的内容有可能会覆盖原本的shellcode，导致执行失败