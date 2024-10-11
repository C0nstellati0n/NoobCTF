# Re: 从零开始的 XDU 教书生活

```py
from requests import *
import json
url="http://127.0.0.1:53776"
data=json.load(open("showSignInfo1",'r'))
sign_code="3262820235251"
enc="441840C9029E1BAC581B8FBE1DEA0FB2"
r=Session()
def login(name):
    r.post(f"{url}/fanyalogin",data={"uname":name,"password":name,"t":"false"})
def refresh():
    global sign_code
    global enc
    info=json.loads(r.get(f"{url}/v2/apis/sign/refreshQRCode").text)
    sign_code=info['data']["signCode"]
    enc=info['data']['enc']
def checkin():
    return r.get(f"{url}/widget/sign/e?id=4000000000000&c={sign_code}&enc={enc}&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=id").text
for student in data['data']['changeUnSignList']:
    name=student['uid']
    login(name)
    if "已过期" in checkin():
        refresh()
        checkin()
```
读取签到的二维码的内容就能知道签到操作要访问的url和相关逻辑了。`/widget/sign/pcTeaSignController/showSignInfo1`路径记录了全部学生的uid，这里我提前缓存下来了。遍历全部学生的uid一一登录再签到即可，二维码过期就自己手动刷新