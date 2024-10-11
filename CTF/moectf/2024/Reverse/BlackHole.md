# BlackHole

提示都说了bruteforce，那还等什么？
```c
#include <windows.h>
#include <string.h>
#include <stdio.h>
int main()
{
    HMODULE h = NULL;
    h = LoadLibraryA("you_cannot_crack_me.vmp.dll");
    if (!h)
    {
        printf("failed to load dll...\n");
        return -1;
    }
    typedef int(*checkFlag)(char *, size_t);
    checkFlag check = (checkFlag)GetProcAddress(h, "checkMyFlag");
    char digits[] = "0123456789";
    char letters[]="abcdefghijklmnopqrstuvwxyz";
    char flag[]="moectf{cxxxxmx}";
    size_t len = strlen(flag);
    for(int i=0;i<strlen(digits);i++){
        for(int j=0;j<strlen(digits);j++){
            for(int k=0;k<strlen(letters);k++){
                for(int m=0;m<strlen(letters);m++){
                    for(int n=0;n<strlen(letters);n++){
                        flag[9]=digits[i];
                        flag[13]=digits[j];
                        flag[8]=letters[k];
                        flag[10]=letters[m];
                        flag[11]=letters[n];
                        if (check(flag, len))
                        {
                            printf("%s",flag);
                            CloseHandle(h);
                            return 0;
                        }
                    }
                }
            }
        }
    }
    printf("failed!");
    CloseHandle(h);
    return 0;
}
```
如何在linux上编译c文件到exe：首先安装mingw-w64：`sudo apt install mingw-w64`，然后`x86_64-w64-mingw32-gcc -o test.exe test.c`即可。不知道为什么，纸条里的源码是`#include <Windows.h>`，换成linux上就是`#include <windows.h>`。我还以为是mingw-w64没装完全少了个header文件，没想到`ls /usr/x86_64-w64-mingw32/include`后发现里面的header文件开头全是小写

另外不推荐搞c++版本，不知道为啥编译出来的exe需要`libstdc++-6.dll`。直接编译c文件就没这么多问题