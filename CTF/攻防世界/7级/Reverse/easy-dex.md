# easy-dex

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d023a5b6-dcb0-4da2-8b46-0851c422cb0c_2&task_category_id=6)

easy才怪。

jadx打开apk，不是我的mainActivity哪去了？死在第一步，不想努力了，躺平看[wp](https://blog.csdn.net/qq_39736559/article/details/127321843)。原来这是纯native开发的app，通过资源文件文件夹下的AndroidManifest.xml的`android:hasCode="false"`能看出来。这种情况告诉我们该看so文件了。

发现找含main的函数基本没错，比如这题要找`android_main`。打开后，哇这都是些什么玩意，跟着wp勉强地模糊跟了一遍。

```c
```

双击`unk_7004`，提取出全部的数据，然后按照程序逻辑生成有flag的dex文件。程序逻辑是按照摇晃手机的次数逐渐解出dex文件。正常人肯定做不到10秒100下，还好程序将数据存在了里面，我们只要按照程序逻辑自己解密dex文件就行了。程序将加密的dex文件平均分成了10块，前8块对应9，19，29...，最后两块都是和89异或。借用大佬的脚本。

```python
import zlib

with open("./blog/out.dump", 'rb') as f:
    data = f.read()
    data_len = len(data)
    decode_bytes = [0]*data_len
    for i in range(0, 9):
        per_seg_len = int(len(data) // 10)
        print(i*per_seg_len, (i+1)*per_seg_len)
        print((i *10 + 9))
        start = i*per_seg_len
        while start < (i+1)*per_seg_len:
            decode_bytes[start] =  data[start] ^ (i *10 + 9)
            start += 1
    
    per_seg_len = int(len(data) // 10)
    start = 9*per_seg_len
    print(9*per_seg_len, data_len)
    while start < data_len:
        decode_bytes[start] =  data[start] ^ 89
        start += 1
    
with open("./blog/decode.dex", 'wb') as f:
    f.write(zlib.decompress(bytes(decode_bytes)))
```

直接把dex文件拖入jadx得到的信息有限，看大佬说可以反编译原apk文件，将其中的resources.arsc 文件和dex文件一起拖入jadx，则可以使jadx自动解析。没试过不知道行不行。或者按照题目里的wp的步骤：

```
将原来的apk解压缩
删除到libs 目录，拷贝out.dex文件到apk解压目录下，命名为classes.dex
修改AndroidManifest.xml
先使用zip工具压缩成apk
apktool解压apk
修改AndroidManifest.xml内容并重新打包
对apk签名并安装
修改AndroidManifest.xml主要关注去掉 android:hasCode="false" 属性，并指定启动
MainActivity。
修改前、修改后的对比如下。
<?xml version="1.0" encoding="utf-8" standalone="no"?><manifest
xmlns:android="http://schemas.android.com/apk/res/android"
package="com.a.sample.findmydex" platformBuildVersionCode="24"
platformBuildVersionName="7.0">
<application android:allowBackup="false" android:fullBackupContent="false"
android:hasCode="false" android:icon="@mipmap/ic_launcher"
android:label="@string/app_name" android:theme="@style/AppTheme">
<activity android:configChanges="keyboardHidden|orientation"
android:label="@string/app_name" android:name="android.app.NativeActivity">
<meta-data android:name="android.app.lib_name" android:value="native"/>
<intent-filter>
<action android:name="android.intent.action.MAIN"/>
<category android:name="android.intent.category.LAUNCHER"/>
</intent-filter>
</activity>
<activity android:name="com.a.sample.findmydex.MainActivity">
<intent-filter>
<action android:name="com.a.sample.findmydex.MAIN"/>
<category android:name="android.intent.category.DEFAULT"/>
</intent-filter>
</activity>
</application>
</manifest>
修改前
<?xml version="1.0" encoding="utf-8" standalone="no"?><manifest
xmlns:android="http://schemas.android.com/apk/res/android"
package="com.a.sample.findmydex" platformBuildVersionCode="24"
platformBuildVersionName="7.0">
<application android:allowBackup="false" android:fullBackupContent="false"
android:hasCode="false" android:icon="@mipmap/ic_launcher"
android:label="@string/app_name" android:theme="@style/AppTheme">
<activity android:configChanges="keyboardHidden|orientation"
android:label="@string/app_name" android:name="android.app.NativeActivity">
<meta-data android:name="android.app.lib_name" android:value="native"/>
<intent-filter>
<action android:name="android.intent.action.MAIN"/>
<category android:name="android.intent.category.LAUNCHER"/>
</intent-filter>
</activity>
<activity android:name="com.a.sample.findmydex.MainActivity">
<intent-filter>
<action android:name="com.a.sample.findmydex.MAIN"/>
<category android:name="android.intent.category.DEFAULT"/>
</intent-filter>
</activity>
</application>
</manifest>
```

最后是一个[twofish](https://xz.aliyun.com/t/5807)块加密算法。在反编译后的程序里找到密文和key`I have a male fish and a female fish.`。密文可以这么得到：

```python
import base64
a = [-120, 77, -14, -38, 17, 5, -42, 44, -32, 109, 85, 31, 24, -91, -112, -83, 64, -83, -128, 84, 5, -94, -98, -30, 18, 70, -26, 71, 5, -99, -62, -58, 117, 29, -44, 6, 112, -4, 81, 84, 9, 22, -51, 95, -34, 12, 47, 77]
a = [i&255 for i in a]
b = base64.b64encode(bytes(a))
print(b)
```

直接[网站](http://tool.chacuo.net/crypttwofish)一把梭。

## Flag
> qwb{TH3y_Io<e_EACh_OTh3r_FOrEUER}