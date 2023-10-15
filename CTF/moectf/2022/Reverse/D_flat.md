# D_flat

这题其实还挺简单的，压根就没有算法要逆向，关键点在于不要逆错文件了。

两个压缩包我都下载了。区别应该是一个压缩包里的可执行文件是exe，另一个是elf。仔细看pdf附件的介绍，透露了这道题的一个关键点——在可执行文件里是找不到解法的。

我也尝试用ghidra逆向了一下elf，函数很多很乱。还是跟着出题人思路走，不要在elf上浪费时间了，转而看看其他的附件。

一个是D_flat.runtimeconfig.json

```json
{
  "runtimeOptions": {
    "tfm": "netcoreapp3.1",
    "framework": {
      "name": "Microsoft.NETCore.App",
      "version": "3.1.0"
    }
  }
}
```

另一个是D_flat.deps.json

```json
{
  "runtimeTarget": {
    "name": ".NETCoreApp,Version=v3.1",
    "signature": ""
  },
  "compilationOptions": {},
  "targets": {
    ".NETCoreApp,Version=v3.1": {
      "D_flat/1.0.0": {
        "runtime": {
          "D_flat.dll": {}
        }
      }
    }
  },
  "libraries": {
    "D_flat/1.0.0": {
      "type": "project",
      "serviceable": false,
      "sha512": ""
    }
  }
}
```

另外还有pdb和dll文件。看来这次逆向的目标是.NET。但是我根本不知道这两个json有什么用，搜了一下在[这个问题](https://stackoverflow.com/questions/40849745/what-is-deps-json-and-how-do-i-make-it-use-relative-paths)的回答里找到了答案。

- .deps.json is a list of dependencies, as well as compilation context data and compilation dependencies. Not technically required, but required to use the servicing or package cache/shared package install features.

大概就是个依赖项列表。没有详细解释里面每一项的含义，但我们的deps.json中的配置有D_flat.dll。[dll文件](https://zhuanlan.zhihu.com/p/406236763)是动态链接文件，里面存放着可共享的代码和数据。既然elf链接了dll，那么dll里肯定有好东西。

ghidra进来没有函数，不知道ida是不是这样。点击defined strings看到了TTTTQQQQQLLLL……应该是一个字符串的头。点击到这串字符串所在的栈上，周围还有更多的提示语，但是没看见flag。再往下翻翻，flag赫然出现在栈上。就这么……解决了？

[pdb](https://blog.csdn.net/feihe0755/article/details/54233714)是程序的基本数据，此处没用到。挺好，白捡100分。

- ### Flag
  > moectf{D_flate_is_C_sharp!}