# string-cheese

[Problem](https://github.com/uclaacm/lactf-archive/tree/main/2023/rev/string-cheese)

Open the ELF file directly with IDA to see the correct answer.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s[256]; // [rsp+0h] [rbp-100h] BYREF

  printf("What's my favorite flavor of string cheese? ");
  fflush(_bss_start);
  fgets(s, 256, stdin);
  s[strcspn(s, "\n")] = 0;
  if ( !strcmp(s, "blueberry") )
  {
    puts("...how did you know? That isn't even a real flavor...");
    puts("Well I guess I should give you the flag now...");
    print_flag();
  }
  else
  {
    puts("Hmm... I don't think that's quite it. Better luck next time!");
  }
  return 0;
}
```

If we enter "blueberry", the server will print out the flag.

## Flag
> lactf{d0n7_m4k3_fun_0f_my_t4st3_1n_ch33s3}