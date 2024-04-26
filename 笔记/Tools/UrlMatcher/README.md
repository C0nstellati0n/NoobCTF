# UrlMatcher

每次CTF结束后，都要手动在discord server里的每个channel找大家发的writeup。就这样找了一年，终于想着要不写个脚本吧？不过discord的api只有bot才能用，而使用bot又需要在当前服务器有权限。于是想了个笨方法，从chrome下载了个可以导出聊天记录的插件[Discrub](https://chromewebstore.google.com/detail/discrub/plhdclenpaecffbcefjmpkkbdpkmhhbj)，导出记录为json后再用正则匹配可能的url

没做任何处理错误的逻辑，而且不智能，容易匹配出一堆没用的url。能用就行，能用就行(･_･;

加了个导出为bookmark文件的功能。可以直接将writeup的url以bookmark的形式导入chrome，方便管理