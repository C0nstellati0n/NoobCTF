# gas

这题本来就是个脚本题，但是某些细节上的处理卡了我很久。而且不知道为啥，最后脚本也不是100%成功，还有概率。奇了怪了，难道是我的网太卡了？
```py
import requests
import zlib
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode
import json
session = requests.Session()
def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)
    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True
    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                        'an exception')
    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                            'decoding the payload')
    return session_json_serializer.loads(payload)
data = {
  'driver':'a',
  'steering_control':"-1",
  "throttle":"2"
}
first = session.post('http://localhost:53846/',data=data)
cookies = json.loads(json.dumps(requests.utils.dict_from_cookiejar(first.cookies)))
json_cookie=decryption(cookies["session"].encode())
for i in range(100):
    data = {
        'driver':'a',
        'steering_control':-json_cookie['next_control'][0],
        "throttle":json_cookie['next_control'][1]
    }
    response = session.post('http://localhost:53846/',data=data,cookies=cookies)
    cookies = json.loads(json.dumps(requests.utils.dict_from_cookiejar(response.cookies)))
    json_cookie=decryption(cookies["session"].encode())
    if json_cookie['round']==5:
        print(response.text)
```