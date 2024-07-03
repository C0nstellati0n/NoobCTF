# [POSTVIEWER V3](https://blog.huli.tw/2024/06/28/google-ctf-2024-writeup)

去年的v2看懵了，今年的v3也看懵了。何尝不是一种传承？

看了这篇wp加上[官方wp](https://github.com/google/google-ctf/tree/main/2024/quals/web-postviewer3)都没懂。xss在哪？于是我决定先搞清楚这个app是怎么运作的

首先这个app只有一个页面，`src/views/index.ejs`。不赘述传文件等不重要的功能，总之传完文件后，文件名会显示在页面上，点击文件名会更新当前页面url的hash（sha1(filename)）。根据`index.ejs`的源码，当前window的hashchange事件绑定了processHash函数，所以每次点击不同文件都会调用这个函数。processHash里调用了一个previewFile函数，用来展示文件内容，其定义在`src/static/util.js`。previewFile内部调用了safeFrameRender函数，其定义在`src/static/safe-frame.js`。这个函数内部产生了一个sandbox domain，名称取决于`calculateHash(body,product,window.origin,location.href)`。从previewFile里知道，body是一个固定的html，product的值也是一个固定的字符串。紧接着这个函数创建了一个iframe，src为刚才产生的sandbox domain url+`/shim.html`，顺便设置一个get参数o的值为window.origin。长话短说，目前有一个iframe，内部内容为`sandbox.domain/shim.html?o=xxx`。shim.html位于`src/sandbox/shim.html`。内部会等待message，若message的origin等于参数o传的origin，且message传入的body和salt经过calculateHash后等同于当前url host名，就把传入的body变成blob，然后载入blob。等内容为shim.html的iframe加载完成后，safeFrameRender函数会给这个iframe postMessage，salf为location.href，body为evaluatorHtml，定义在`src/static/util.js`。等于说shim.html这个iframe加载完成后，iframe的内容就变成evaluatorHtml了。evaluatorHtml说白了就一句话，eval接收到的message

现在我们回到previewFile函数。等内容为evaluatorHtml的iframe加载完成后，previewFile函数会给里面的evaluatorHtml postMessage，eval的内容为iframeInserterHtml，也定义在`src/static/util.js`。这个iframeInserterHtml内部又创建了一个sandboxed iframe，为展示的文件内容。结束。整体是main domain->main domain creates sandbox domain->sandbox domain creates iframe A with shim.html->iframe A loads evaluatorHtml->evaluatorHtml evals iframeInserterHtml->iframeInserterHtml creates iframe B with file content。我们web有自己的俄罗斯套娃

所以怎么在有flag的sandbox domain下拿到xss？产生hash的四个参数有三个已知，但是第四个参数是location.href。location.href包含hash，而hash又是文件内容的sha1值。不知道flag文件内容因此不知道hash，最后不知道有flag的sandbox domain。还有个问题，存有flag的sandbox domain只相信某个origin的代码。虽然origin以get参数形式传入，但我们也不能随意修改origin的值，因为这样的话算出来的hash就不等同于sandbox domain的host名了，就算得到xss也不在flag所在的sandbox domain下。所以有没有什么办法可以让我们在改动get参数origin的情况下还让算出来的hash等同于flag所在的sandbox domain？答案是有，因为calculateHash函数计算hash时直接将4个参数拼了起来，中间没加分隔符。那我们就可以动动手脚了，稍微shift一下各个参数的内容。两篇wp分别用了不同的方法来构造相同的hash，这边拿官方wp来看（相比第一篇wp这块讲的比较详细）

在processHash里发现当前app提供了一个功能，可以用`#id`来指代某个文件，app会自动将其转为该文件对应的hash。虽然我们不知道admin的flag文件的hash，但是可以用`#0`让app自己把hash写上url。这个函数又有个`await sleep(0)`让后面的操作变成非同步，就有了race condition。我们先`#0`让app自动解析hash然后return，但是hash改变了于是又进到了processHash。此时当前url的hash已经是flag文件的hash而不是`#0`了。processHash拿到flag文件的fileDiv后，我们卡个race condition，在previewFile的safeFrameRender之前将url hash改为任意我们自己控制的hash，就解决了flag文件hash不知道的问题。配合calculateHash里的漏洞，成功在flag sandbox domain下拿到xss

对了，官方wp还提供了一个在`storage.googleapis.com`下拿到xss的方法