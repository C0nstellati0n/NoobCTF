# usb

流量分析题，还好数据包不多。稍微看了一下，发现当数据包的source- destination为2.2.2-host时会有个HID Data字段，其他都没有。

不知道为什么，这题的键盘数据并没有跟[ctf wiki](https://ctf-wiki.org/misc/traffic/protocols/usb/)里介绍的常见usb流量包一样在leftover capture data里，而是在上面提到的HID Data中。

第13个包的HID data为0x10，对比在ctf wiki看到的对照表，正好是字母m。往后多看几个，依次发现了oe，数据间隔了一个空数据。把HID data提取出来，然后借用大佬的[脚本](https://github.com/WangYihang/UsbKeyboardDataHacker)，直接得到flag。

```python
import json
hiddata=[]
with open("userdata.json") as f:
    data=f.read()
data=json.loads(data)
for i in data:
    try:
        hiddata.append(i["_source"]["layers"]["usbhid.data"])
    except:
        pass
normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":":","34":"\"","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

def main():
    result = ""
    for press in hiddata:
        if press == '':
            continue
        if ':' in press:
            Bytes = press.split(":")
        else:
            Bytes = [press[i:i+2] for i in range(0, len(press), 2)]
        if Bytes[0] == "00":
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += normalKeys[Bytes[2]]
        elif int(Bytes[0],16) & 0b10 or int(Bytes[0],16) & 0b100000: # shift key is pressed.
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += shiftKeys[Bytes[2]]
        else:
            print("[-] Unknow Key : %s" % (Bytes[0]))
    print("[+] Found : %s" % (result))
if __name__ == "__main__":
    main()
```

userdata.json是在wireshark中提取出来的流量包json信息。菜单file->export packet dissections->as json即可得到。输出结果如下。

- [+] Found : moectf{\<CAP>l\<CAP>earnee\<DEL>d_a6ou7_\<CAP>usb\<CAP>_tr@ffic}

\<CAP>\<CAP>包裹起来的字母表示要大写，比如\<CAP>usb\<CAP>代表USB。\<DEL>前面的字母不算，比如earnee\<DEL>d表示earned。由此得到正确的flag。

- ### Flag
  > moectf{Learned_a6ou7_USB_tr@ffic}