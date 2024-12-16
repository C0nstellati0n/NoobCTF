# CatFly

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=a47b5186-8d9a-11ed-ab28-000c29bc20bf&task_category_id=4)

这次的题目文件不一般，运行竟然能得到动画。注意到中间有一长串不断变化的文字，就从这里入手。ida打开main函数。

```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  //这里省去用不着的部分
  time(&timer);
  v15 = 1;
  v26 = 0LL;
  v25 = 0;
  v24 = 0;
  v14 = off_FA88;
  while ( v15 )
  {
    if ( dword_E104 )
      printf("\x1B[H");
    else
      printf("\x1B[u");
    for ( k = dword_E1EC; k < dword_E1F0; ++k )
    {
      for ( l = dword_E1F4; l < dword_E1F8; ++l )
      {
        if ( k <= 23 || k > 42 || l >= 0 )
        {
          if ( l >= 0 && k >= 0 && k <= 63 && l <= 63 )
          {
            v21 = off_FA20[v26][k][l];
            off_FA88 = (char *)sub_6314((unsigned int)v26, (unsigned int)k, (unsigned int)l, v14);// 最近的写入引用
          }
          else
          {
            v21 = 44;
          }
        }
        else
        {
          v20 = (2 - l) % 16 / 8;
          if ( ((v26 >> 1) & 1) != 0 )
            v20 = 1 - v20;
          v11 = ",,>>&&&+++###==;;;,,";
          v21 = asc_BFE3[v20 - 23 + k];
          if ( !v21 )
            v21 = 44;
        }
        if ( v27 )
        {
          printf("%s", *((const char **)&unk_FCC0 + v21));
        }
        else if ( v21 == v24 || !*((_QWORD *)&unk_FCC0 + v21) )
        {
          printf("%s", off_FA88);
        }
        else
        {
          v24 = v21;
          printf("%s%s", *((const char **)&unk_FCC0 + v21), off_FA88);
        }
      }
      sub_65E2(1LL);
    }
    if ( dword_E100 )
    {
      time(&time1);
      v13 = difftime(time1, timer);
      v12 = sub_63FF((unsigned int)(int)v13);
      for ( m = (dword_E1FC - 29 - v12) / 2; m > 0; --m )
        putchar(32);
      dword_E1E8 += printf("\x1B[1;37mYou have nyaned for %d times!\x1B[J\x1B[0m", (unsigned int)++dword_108E0);
    }
    v24 = 0;
    ++v25;
    if ( dword_104C4 && v25 == dword_104C4 )
      sub_6471();
    if ( !off_FA20[++v26] )
      v26 = 0LL;
    usleep(1000 * v29);
  }
  return 0LL;
}
```

看了一下感觉`off_FA88`最有可能是那行文字，其他printf函数输出的内容基本都是定值，不会变化。查找交叉引用，只需要看离printf最近的写入引用就行了，更早的写入引用或者其他无关读取引用不用看。那就是注释标注的地方了，值由`sub_6314`得出。

```c
char *__fastcall sub_6314(__int64 a1, int a2, int a3, __int64 a4)
{
  if ( a2 != 18 )
    return (char *)a4;
  if ( a3 <= 4 || a3 > 54 )
    return (char *)a4;
  byte_104C9 = 32;
  dword_E120[a3 - 5] ^= sub_62B5();
  if ( (unsigned __int8)sub_62E3(dword_E120[a3 - 5]) )
    byte_104C8 = dword_E120[a3 - 5] & 0x7F;
  else
    byte_104C8 = 32;
  return &byte_104C8;
}
```

函数不难，返回值是`byte_104C8`。`byte_104C8`的值又由`dword_E120`得出。而`dword_E120`等于自身异或函数`sub_62B5`的返回值。

```c
__int64 sub_62B5()
{
  dword_E1E8 = 1103515245 * dword_E1E8 + 12345;
  return (dword_E1E8 >> 10) & 0x7FFF;
}
```

`sub_62B5`返回的内容与`dword_E1E8`有关。查交叉引用，在main函数里查到了这么一句：`dword_E1E8 += printf("\x1B[1;37mYou have nyaned for %d times!\x1B[J\x1B[0m", (unsigned int)++dword_108E0);`，和printf函数的返回值密切相关。printf的返回值是写入的字符总数，那就间接和`dword_108E0`有关，又要去找`dword_108E0`的引用了。还好只有此处的自增。收集好相关的数据就能自己算出flag了，此处借用wp的脚本，自己做了点注释。

```c
#include<stdio.h>
#include<string.h>
//在ida里面点开dword_E1E8会发现初始值为0x1106
//感谢一位好心大佬指出这里原有的错误，不然我这辈子都不会发现了(._.)
int dword_E1E8 = 0x1106;
//同理，ida里也能看到dword_E120的初始值
int dword_E120[50]={0x27fb, 0x27a4, 0x464e, 0x0e36, 0x7b70, 0x5e7a, 0x1a4a, 0x45c1, 0x2bdf, 0x23bd, 0x3a15, 0x5b83, 0x1e15, 0x5367, 0x50b8, 0x20ca, 0x41f5, 0x57d1, 0x7750, 0x2adf, 0x11f8, 0x09bb, 0x5724, 0x7374, 0x3ce6, 0x646e, 0x010c, 0x6e10, 0x64f4, 0x3263, 0x3137, 0x00b8, 0x229c, 0x7bcd, 0x73bd, 0x480c, 0x14db, 0x68b9, 0x5c8a, 0x1b61, 0x6c59, 0x5707, 0x09e6, 0x1fb9, 0x2ad3, 0x76d4, 0x3113, 0x7c7e, 0x11e0, 0x6c70};
//原封不动抄下来就好了
int sub_62B5()
{
  dword_E1E8 = 1103515245 * dword_E1E8 + 12345;
  return (dword_E1E8 >> 10) & 0x7FFF;
}
//这块是拿来算输出数字n需要多少个字符的。个位数0，十位数1，百位数2……以此类推。至于为什么和一般理解的不一样，我也不太清楚，自己做了个实验发现的
int llog(int n){
    int a = 0;
    while(n /= 10)a++;
    return a;
}
//这个函数我没有特别放出来，反正这里也是照抄的
int sub_62E3(char a1)
{
  int result; // rax

  if ( (a1 & 0x7Fu) <= 0x7E )
    result = (a1 & 0x7Fu) > 0x20;
  else
    result = 0LL;
  return result;
}

int main(){
    //count代表那个不停自增的dword_108E0
    int count = 0;
    while(1){
        //这里结合 函数，本来应该是dword_E120[a3-5]。a3对应到main函数的调用是循环索引l，还挺麻烦的。其实只需要把鼠标悬停在dword_E120上，就能发现它的大小是50，直接这么设定就好了。一个偷懒的方法，很多情况还是要动调确定
        for(int i = 0; i < 50; i++){
            dword_E120[i]^=sub_62B5();
        }
        count++;
        //计算printf的返回值，更改dword_E1E8,每10倍增加一个位数
        dword_E1E8+=42+llog(count);
        if(count % 1000000 == 0 ){
            printf("Count:%d\n",count);
        }
        //flag代表off_FA88
        unsigned char flag[51]={0};
        for(int i = 0; i < 50; i++){
            //根据出题人所说，出题时循环次数为705980581，但是线性同余随机数算法出现了循环导致在100427942就出现了flag，若只考虑数组的最低字节，能在100001958得到flag
            // Loop: 100427942
            // if((dword_E120[i] & 0xff00)){
            //     break;
            // }
            // Loop: 100001958
            if(!sub_62E3(dword_E120[i])){
                break;
            }
            flag[i]=dword_E120[i]&0xff;
        }
        if(memcmp("CatCTF",flag,6) == 0){
            puts(flag);
            printf("Count:%d\n",count);
            break;
        }
    }
}
```

提到的实验指下面这句话：

```c
printf("\n%d",printf("\x1B[1;37mYou have nyaned for %d times!\x1B[J\x1B[0m",1));
```

发现这样是42，再多试几个就试出来规律了。最后总结一下，main函数所有相关值的修改顺序是`off_FA88->dword_108E0->dword_E1E8`。解题exp也遵循这个规律，先处理dword_E120（flag，off_FA88），再是dword_E1E8（count），最后dword_E1E8。后面的for循环只不过是将稍微修正一下flag的值而已，总体完全等同于题目逻辑。

## Flag
> CatCTF{Fly1NG_NyAnC4t_Cha5eS_the_FL4G_in_The_Sky}