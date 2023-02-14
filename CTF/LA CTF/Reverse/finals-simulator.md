# finals-simulator

[Problem](https://github.com/uclaacm/lactf-archive/tree/main/2023/rev/finals-simulator)

Use IDA to view the main function.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // [rsp+Ch] [rbp-114h] BYREF
  char s[264]; // [rsp+10h] [rbp-110h] BYREF
  char *i; // [rsp+118h] [rbp-8h]

  puts("Welcome to Finals Simulator 2023: Math Edition!");
  printf("Question #1: What is sin(x)/n? ");
  fflush(stdout);
  fgets(s, 256, stdin);
  s[strcspn(s, "\n")] = 0;
  if ( !strcmp(s, "six") )
  {
    printf("Question #2: What's the prettiest number? ");
    fflush(stdout);
    __isoc99_scanf("%d", &v4);
    if ( 42 * (v4 + 88) == 561599850 )
    {
      printf("Question #3: What's the integral of 1/cabin dcabin? ");
      fflush(stdout);
      getchar();
      fgets(s, 256, stdin);
      s[strcspn(s, "\n")] = 0;
      for ( i = s; *i; ++i )
        *i = 17 * *i % mod;
      putchar(10);
      if ( !strcmp(s, &enc) )
      {
        puts("Wow! A 100%! You must be really good at math! Here, have a flag as a reward.");
        print_flag();
      }
      else
      {
        puts("Wrong! You failed.");
      }
      result = 0;
    }
    else
    {
      puts("Wrong! You failed.");
      result = 0;
    }
  }
  else
  {
    puts("Wrong! You failed.");
    result = 0;
  }
  return result;
}
```

The first two questions are easy. The first if statement simply compares the input to "six", implying that the answer is "six". The second if statement requires the input number v4 to satisfy "42 \* (v4 + 88) == 561599850", and the answer can be obtained by doing a simple inverse operation.

42 \* (v4 + 88) = 561599850<br>
(v4 + 88) = 561599850//42<Br>
v4 = 561599850//42-88<br>
v4 = 13371337

The third problem involves modulo arithmetic, which is usually harder to reverse. However, we have the value of enc, and the flag must only contain printable characters, so we can directly get the flag in an exhaustive way.

```python
from string import printable
enc="0E C9 9D B8 26 83 26 41 74 E9 26 A5 83 94 0E 63 37 37 37".split(" ") #Double-click "enc" in IDA to enter "IDA View", select all the data of enc with the mouse, and click shift+e to extract the data.
for i in enc:
    for j in printable:
        if ord(j)*17%0xfd==int(i,16): #The value of "mod" can be found in IDA, which is 0xfd.
            print(j,end='')
```

The answer to the third question is "it's a log cabin!!!". Connect to the server, enter these three answers in sequence, and you will get the flag.

## Flag
> lactf{im_n0t_qu1t3_sur3_th4ts_h0w_m4th_w0rks_bu7_0k}