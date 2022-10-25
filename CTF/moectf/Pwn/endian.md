# endian

Mikato到底是谁？？？

这题我真的服了我自己了，做了几个小时才发现自己的方法有问题。main函数很简单，但是有个混淆项。

```c
undefined8 main(void)
{
  int iVar1;
  long in_FS_OFFSET;
  char local_18 [4];
  undefined auStack20 [4];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  __isoc99_scanf(&DAT_004008a4,local_18,auStack20);
  iVar1 = strncmp("MikatoNB",local_18,8);
  if (iVar1 == 0) {
    system("/bin/sh");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

DAT_004008a4是格式化字符串的格式，内容为%d%d。如果它是%s%s，这题将非常简单，关键就在于它是%d。%d%d表示以int方式将接收到的内容放到local_18和auStack20中，但后面的strncmp是比较字符串的。local_18长度为4却比较了8位不用管，因为local_18和auStack20是挨着的，local_18不够了就会去比较auStack20的。

再无数次尝试输入数字但是都不对后我决定自己写个差不多的程序进行调试。

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
int main(void)
{
    char a[4];
    char b[4];
    scanf("%d%d",a,b);
    int result=strncmp("MikatoNB",a,8);
    if(result==0){
        printf("Sucess!\n");
    }
    else{
        printf("Nope!At %d\n",result);
    }
}
```

- gcc s.c -o s.o

写完编译后打开gdb进行调试。其实直接调试附件给的程序也可以，我加了个反馈，有点用但用处不大。gdb设个断点在strncmp处。

- (gdb) b strncmp

因为是64位程序，所以在strncmp断开时两个参数会被存在rdi和rsi中。提供几个有用的gdb检查内存的命令。

- 检查指定寄存器地址中存储的字符串
  > (gdb) x/s $rsi<br>(gdb) x/s $rdi

x表示examine，s表示以字符串形式。$我个人理解是取寄存器的地址。

- 检查指定寄存器地址中存储的n个无符号数字
  > (gdb) x/8u $rsi<br>(gdb) x/8u $rdi

d表示以无符号数字形式，8表示从指定地址往后取8个。这个数字可以根据需求改变。

这题的思路和ezTea的一个知识点完全一致。我先放出来找到答案的脚本。

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
int main() {
    char input[8] = "MikatoNB";
    int v[2] = {*(int *)&input[0],*(int *)&input[4]};
    printf("%u\n%u\n",v[0],v[1]);
    return 0;
}
```

有点眼熟吧？这个指针转换我是直接从ezTea的脚本中抄的，改动了一点我想要的内容。题目要求我们输入数字，然后用char指针一点一点读取我们输入的数字进行比对（strncmp是一个字符一个字符比较的，相等返回0，不相等返回字符串1在不相等处的字符的ascii值减去字符串2在不相等处的字符的ascii值），也就是整形指针强行转换为字符指针。所以我们可以反过来，把目标字符串指针强行转换为整型指针，接着读取里面的值就是答案。分成两半是因为题目同样也把输入的数字分成了两半。运行程序即可得到答案。

- 1634429261
<br>1112436596

手动连接nc然后输入这两个数字就可以得到shell了。

- ### Flag
  > moectf{I_sta2t_p33ling_e99s_fr0m_7he_m1ddle}