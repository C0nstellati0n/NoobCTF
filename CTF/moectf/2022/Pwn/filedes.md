# filedes

根本没用过c语言来读取文件的我直接懵逼。

给了一个程序，直接反编译。

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  puts("In UNIX, everything is a file.");
  puts("Your screen is a file, too.");
  puts("Do you know how to print flag on your screen file?");
  close(1);
  open("/flag.txt",0);
  __isoc99_scanf(&DAT_00400a45,&local_14);
  read(local_14,flag,0x40);
  __isoc99_scanf(&DAT_00400a45,&local_14);
  write(local_14,flag,0x40);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

第一次输入的local_14的值被用在read(local_14,flag,0x40);。c语言中read的第一个参数是文件描述符，打开的文件默认从3开始，因为0，1，2被系统占用了，0是stdin，1是stdout，2是stderr，也就是上面setvbuf的内容。理论上第一个输入应该填3。

write同理，第一个参数也是文件描述符。这回肯定打印到stdout我们才能看到，也就是1。但是我怎么试都不对，想要锤出题人的时候突然发现上面有一句话：close(1);。close的参数也是文件描述符，把1 close了意味着把stdout close了，下面还怎么玩？

学艺不精的我去搜了一下，偶然发现了[这个](https://www.runoob.com/cprogramming/c-input-output.html)。stderr中的内容会发送到我的屏幕，那发送flag也是可以的吧。之后又在本机上实验，发现在close(1)后再open文件，打开的文件的文件描述符就变成1了。果然还是要多调试多实验。只要这么输入就能得到flag了。

- In UNIX, everything is a file.
<br>Your screen is a file, too.
<br>Do you know how to print flag on your screen file?
<br>1
<br>2

- ### Flag
  > moectf{huh_s0_e4sy_fd_r1ght?}