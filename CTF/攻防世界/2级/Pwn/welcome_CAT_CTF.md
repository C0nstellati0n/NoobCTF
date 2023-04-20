# welcome_CAT_CTF

[题目](https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1681947596037)

这题给了两个elf，不过server对解题毫无用处，不用看。另外的一个client内部则是走迷宫的设计。

```c

/* WARNING: Unknown calling convention yet parameter storage is locked */
/* magic() */

void magic(void)

{
  int iVar1;
  long in_FS_OFFSET;
  undefined *apuStack184248 [99];
  undefined *apuStack183456 [101];
  undefined *apuStack182648 [12825];
  char y;
  char x;
  int i;
  int j;
  undefined *map [4];
  //这里省略了ghidra里的变量定义
  y = 40;
  x = 10;
  clock();
  do {
    printf("\x1b[H\x1b[2J");
    for (i = 0; i < 0x3b; i = i + 1) {
      for (j = 0; j < 0x22; j = j + 1) {
        printf("%s ",map[(long)i * 100 + (long)j]);
      }
      putchar(10);
    }
    scanf("%c",local_12);
    switch(local_12[0]) {
    case 'a':
      if (map[(long)(int)y * 100 + (long)(x + -1)] == &DAT_00109587) {
        map[(long)(int)y * 100 + (long)(int)x] = &DAT_00109587;
        x = x + -1;
        map[(long)(int)y * 100 + (long)(int)x] = &player;
      }
      break;
    case 'd':
      if (map[(long)(int)y * 100 + (long)(x + 1)] == &DAT_00109587) {
        map[(long)(int)y * 100 + (long)(int)x] = &DAT_00109587;
        x = x + 1;
        map[(long)(int)y * 100 + (long)(int)x] = &player;
      }
      break;
    case 'j':
      if (map[(long)(y + -1) * 100 + (long)(int)x] == &dollar) {
        if ((int)glod < 100) {
          glod = glod + 1;
        }
        puts(&DAT_00109650);
        printf(&DAT_0010967e,(ulong)glod);
        getchar();
      }
      if (map[(long)(y + -1) * 100 + (long)(int)x] == &DAT_00109629) {
        puts("miao~~~~~");
        getchar();
      }
      if ((map[(long)(y + -1) * 100 + (long)(int)x] == &player) && (0x5f5e100 < (int)glod)) { //player符号为@，这样要求我们在地图上走到固定的@符号的下面，并且glod要大于0x5f5e100
        puts("GET_FLAG!");
        iVar1 = get_nc();
        get_flag(iVar1);
        getchar();
      }
      break;
    case 's':
      if (map[(long)(y + 1) * 100 + (long)(int)x] == &DAT_00109587) {
        map[(long)(int)y * 100 + (long)(int)x] = &DAT_00109587;
        y = y + 1;
        map[(long)(int)y * 100 + (long)(int)x] = &player;
      }
      break;
    case 'w':
      if (map[(long)(y + -1) * 100 + (long)(int)x] == &DAT_00109587) {
        map[(long)(int)y * 100 + (long)(int)x] = &DAT_00109587;
        y = y + -1;
        map[(long)(int)y * 100 + (long)(int)x] = &player;
      }
    }
  } while( true );
}
```

flag的关键逻辑在case 'j'下面。寻找glod的引用，如果我们走到`$`符号下面就能将glod加一，然而只能加到100。这个地图只是障眼法，正常走是不可能拿到这么多的。既然client由我们控制，我们在程序一开始就把glod设为一个较大的数字就行了。

```
pwndbg> starti
pwndbg> info proc map
process 778
Mapped address spaces:
          Start Addr           End Addr       Size
      0x555555400000     0x55555540a000     0xa000
pwndbg> set *(0x555555400000+0x20a388)=0x6666666
```

省略了pwndbg里的一些回显，总之先starti让程序在一开始就停下，info proc map查看程序基址和映射，然后根据基址将glod的地址设为一个较大的数。注意这里设置的数我试过0xffffffff,0xaaaaaaa等，到最后都无法获取flag。可能是因为程序里比较时把glod强转为int，因此过大的数反而不行了。应该7位的数字不是特别大的16进制都行。

然后直接c继续程序，wasd控制自己走到`@`符号下就能获取flag了。这里不知道是不是我的环境的问题，我只能看见程序打印出的GET_FLAG!，却看不见flag内容，被printf打印出来的内容刷新掉了。我的解决办法是在get_flag返回处下个断点。

```
pwndbg> b *0x555555400000+0x1e02
```

## Flag
> cyberpeace{ed2021b3ef15707c4edec7c28539d846}