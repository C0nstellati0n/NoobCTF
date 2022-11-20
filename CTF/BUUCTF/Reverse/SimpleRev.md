# SimpleRev

[题目地址](https://buuoj.cn/challenges#SimpleRev)

我的理解好像出了问题。

放进ida，main函数没啥东西，重点在Decry函数。

```c
unsigned __int64 Decry()

{

  char inputChar; // [rsp+Fh] [rbp-51h]

  int index; // [rsp+10h] [rbp-50h]

  int keyIndex; // [rsp+14h] [rbp-4Ch]

  int i; // [rsp+18h] [rbp-48h]

  int keyLength; // [rsp+1Ch] [rbp-44h]

  char src[8]; // [rsp+20h] [rbp-40h] BYREF

  __int64 v7; // [rsp+28h] [rbp-38h]

  int v8; // [rsp+30h] [rbp-30h]

  __int64 v9[2]; // [rsp+40h] [rbp-20h] BYREF

  int v10; // [rsp+50h] [rbp-10h]

  unsigned __int64 v11; // [rsp+58h] [rbp-8h]



  v11 = __readfsqword(0x28u);

  *(_QWORD *)src = 'SLCDN';

  v7 = 0LL;

  v8 = 0;

  v9[0] = 'wodah';

  v9[1] = 0LL;

  v10 = 0;

  text = join(key3, (const char *)v9);          // join函数将两个字符串连接

  strcpy(key, key1);                            // key1=ADSFK

  strcat(key, src);

  index = 0;

  keyIndex = 0;

  getchar();

  keyLength = strlen(key);

  for ( i = 0; i < keyLength; ++i )

  {

    if ( key[keyIndex % keyLength] > 64 && key[keyIndex % keyLength] <= 90 )

      key[i] = key[keyIndex % keyLength] + 32;  // key的大写字母转小写字母

    ++keyIndex;

  }

  printf("Please input your flag:");

  while ( 1 )

  {

    inputChar = getchar();

    if ( inputChar == '\n' )

      break;

    if ( inputChar == ' ' )

    {

      ++index;

    }

    else

    {

      if ( inputChar <= 96 || inputChar > 122 ) // 如果inputChar是字母或符号

      {

        if ( inputChar > 64 && inputChar <= 90 )// 如果是大写字母

        {

          str2[index] = (inputChar - 39 - key[keyIndex % keyLength] + 97) % 26 + 97;// key=adsfkndcls

          ++keyIndex;

        }

      }

      else

      {

        str2[index] = (inputChar - 39 - key[keyIndex % keyLength] + 97) % 26 + 97;

        ++keyIndex;

      }

      if ( !(keyIndex % keyLength) )

        putchar(' ');

      ++index;

    }

  }

  if ( !strcmp(text, str2) )                    // text=killshadow

    puts("Congratulation!\n");

  else

    puts("Try again!\n");

  return __readfsqword(0x28u) ^ v11;

}
```

要求最后text的内容等于str2，str2的值取决于我们的输入。看一下处理输入的地方，出现了模运算。这个不好逆向，直接爆破最好，毕竟字母也不多。我分析程序逻辑大概是，判断我们的输入是什么，如果是大写字母，`str2[index]`就等于那一串内容，如果不是并且不是小写字母和一些符号，`str2[index]`还是等于那一串内容。由于index每次都会自增，我们的输入不能有小写字母及一些符号，因为这样会导致`str2[index]`在当前index下没有赋值，不可能等于之后的text。直接在大写字母里爆破，不在大写字母里的情况先不管，看看出来的是什么。

```python
from string import ascii_uppercase
key='adsfkndcls'
text='killshadow'
for i in range(len(text)):
    for j in ascii_uppercase:
        c=ord(j)
        k=ord(key[i%len(key)])
        result=chr((c-39-k+97)%26+97)
        if result==text[i]:
            print(j,end='')
            break
```

直接就出来答案了。注意ida直接转字符串得到的`v9[0] = 'wodah';`需要反过来才是正确的，包括`*(_QWORD *)src = 'SLCDN';`。这些字符串本来是hex形式，右键转为char后由于端序问题是反过来的，需要手动转回来。总之就是，原本是hex的内容转为字符串后需要反过来才是正确的。

## Flag
> flag{KLDQCUDFZO}