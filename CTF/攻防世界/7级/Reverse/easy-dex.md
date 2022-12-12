# easy-dex

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d023a5b6-dcb0-4da2-8b46-0851c422cb0c_2&task_category_id=6)

easy才怪。

jadx打开apk，不是我的mainActivity哪去了？死在第一步，不想努力了，躺平看[wp](https://blog.csdn.net/qq_39736559/article/details/127321843)。原来这是纯native开发的app，通过资源文件文件夹下的AndroidManifest.xml的`android:hasCode="false"`能看出来。这种情况告诉我们该看so文件了。

发现找含main的函数基本没错，比如这题要找`android_main`。打开后，哇这都是些什么玩意，跟着wp勉强地模糊跟了一遍。

```c
int __fastcall android_main(_DWORD *a1)
{
  void *v2; // r5
  char *v3; // r10
  int v4; // r2
  int v5; // r1
  time_t v6; // r8
  int *v7; // r0
  int v8; // r3
  int v9; // r6
  int shake_times; // r4
  float v11; // s0
  int v12; // r0
  int v13; // r5
  int v14; // r5
  int v15; // r3
  void *v16; // r0
  int v17; // r2
  int v18; // r1
  char *v19; // r3
  time_t v20; // r5
  int v21; // r8
  Bytef *dest; // [sp+8h] [bp-158h]
  int v24; // [sp+10h] [bp-150h] BYREF
  char v25[4]; // [sp+14h] [bp-14Ch] BYREF
  int v26[13]; // [sp+18h] [bp-148h] BYREF
  uLongf destLen; // [sp+4Ch] [bp-114h] BYREF
  char v28[8]; // [sp+50h] [bp-110h] BYREF
  int v29; // [sp+58h] [bp-108h]
  float shake_degree; // [sp+70h] [bp-F0h]
  char name[4]; // [sp+B8h] [bp-A8h] BYREF
  int v32; // [sp+BCh] [bp-A4h]
  int v33; // [sp+C0h] [bp-A0h]
  int v34; // [sp+C4h] [bp-9Ch]
  int v35; // [sp+C8h] [bp-98h]
  int v36; // [sp+CCh] [bp-94h]
  int v37; // [sp+D0h] [bp-90h]
  int v38; // [sp+D4h] [bp-8Ch]
  int v39; // [sp+D8h] [bp-88h]
  int v40; // [sp+DCh] [bp-84h]
  int v41; // [sp+E0h] [bp-80h]
  __int16 v42; // [sp+E4h] [bp-7Ch]
  char v43; // [sp+E6h] [bp-7Ah]
  char filename[4]; // [sp+E8h] [bp-78h] BYREF
  int v45; // [sp+ECh] [bp-74h]
  int v46; // [sp+F0h] [bp-70h]
  int v47; // [sp+F4h] [bp-6Ch]
  int v48; // [sp+F8h] [bp-68h]
  int v49; // [sp+FCh] [bp-64h]
  int v50; // [sp+100h] [bp-60h]
  int v51; // [sp+104h] [bp-5Ch]
  int v52; // [sp+108h] [bp-58h]
  int v53; // [sp+10Ch] [bp-54h]
  int v54; // [sp+110h] [bp-50h]
  int v55; // [sp+114h] [bp-4Ch]
  int v56; // [sp+118h] [bp-48h]
  char v57; // [sp+11Ch] [bp-44h]
  int v58; // [sp+124h] [bp-3Ch]

  destLen = 0x100000;
  dest = (Bytef *)malloc(0x100000u);
  v2 = off_43A18;
  v3 = (char *)malloc((size_t)off_43A18);       // v3的长度为off_43A18
  qmemcpy(v3, &unk_7004, (size_t)v2);           // v3的值等同于unk_7004
  *(_DWORD *)filename = -1651995345;
  v45 = -2003974520;
  v46 = -1966700387;
  v47 = -2000190330;
  v48 = -2071422265;
  v49 = -947092071;
  v50 = -1920499569;
  v51 = -1936879484;
  v52 = -2138061167;
  v53 = -962950011;
  v54 = -1702328950;
  v55 = -946172774;
  v56 = -376337267;
  v57 = 0;
  *(_DWORD *)name = -1651995194;
  v32 = -2003974520;
  v33 = -1966700387;
  v34 = -2000190330;
  v35 = -2071422265;
  v36 = -947092071;
  v37 = -1920499569;
  v38 = -1936879484;
  v39 = -2138061167;
  v40 = -962950011;
  v41 = -1853059706;
  v43 = 0;
  v4 = 1;
  v42 = -5690;
  do
    filename[v4++] ^= 0xE9u;
  while ( v4 != 53 );
  v5 = 1;
  name[0] = 47;
  do
    name[v5++] ^= 0xE9u;
  while ( v5 != 47 );
  j_app_dummy();
  memset(v26, 0, sizeof(v26));
  *a1 = v26;
  a1[1] = sub_29B8;
  a1[2] = sub_2B90;
  v26[0] = (int)a1;
  v26[1] = ASensorManager_getInstance();
  v26[2] = ASensorManager_getDefaultSensor(v26[1], 1);
  v6 = 0;
  v26[3] = ASensorManager_createEventQueue(v26[1], a1[7], 3, 0, 0);
  v7 = (int *)a1[5];
  if ( v7 )
  {
    v8 = v7[1];
    v9 = v7[2];
    v26[10] = *v7;
    v26[11] = v8;
    v26[12] = v9;
  }
  _android_log_print(4, "FindMyDex", "Can you shake your phone 100 times in 10 seconds?");
  shake_times = 0;
  do
  {
    while ( 1 )
    {
      v12 = 0;
      if ( !v26[4] )
        v12 = -1;
      v13 = ALooper_pollAll(v12, 0, v25, &v24);
      if ( v13 >= 0 )
        break;
      if ( v26[4] )
      {
        v11 = *(float *)&v26[10] + 0.01;
        if ( (float)(*(float *)&v26[10] + 0.01) > 1.0 )
          v11 = 0.0;
        *(float *)&v26[10] = v11;
        sub_2C14(v26);
      }
    }
    if ( v24 )
      (*(void (__fastcall **)(_DWORD *))(v24 + 8))(a1);
    if ( v13 == 3 && v26[2] )
    {
      while ( 1 )
      {
        do
        {
          if ( ASensorEventQueue_getEvents(v26[3], v28, 1) < 1 )
            goto LABEL_51;
        }
        while ( v29 != 1 );
        if ( (shake_times & 1) != 0 )
        {
          if ( shake_degree >= -15.0 )
          {
LABEL_30:
            v14 = shake_times;
            goto LABEL_31;
          }
          if ( shake_times == 1 )
            v6 = time(0);
          v14 = shake_times + 1;
        }
        else
        {
          if ( shake_degree <= 15.0 )
            goto LABEL_30;
          v14 = shake_times + 1;
          if ( shake_times >= 0 )
            _android_log_print(4, "FindMyDex", "Oh yeah~ You Got it~ %d times to go~", 99 - shake_times);
        }
LABEL_31:
        shake_times = v14;                      // shake_times和v14表示的值应该是一致的，都是用户摇手机的次数
        if ( (unsigned int)(v14 - 1) <= 88 )
        {
          shake_times = v14;
          v15 = v14 / 10;
          if ( v14 % 10 == 9 )                  // v14的可能值个位数为9，结合要求摇的次数不超过100，是9，19，29，39，49，59，69，79，89
          {
            v16 = off_43A18;                    // 上面知道，off_43A18是v3的长度，v3的内容又完全等于加密的dex数据，说明off_43A18就是加密数据的长度
            v17 = (int)off_43A18 / 10;          // 分成10份
            v18 = (v15 + 1) * ((int)off_43A18 / 10);// v15是v14/10，即摇晃次数/10。根据摇晃次数获取平均分的10份里的某一份
            if ( (int)off_43A18 / 10 * v15 < v18 )// 这种情况可以自己手动算几个值，会发现恒等为真
            {
              v19 = &v3[v17 * v15];             // 根据上面的规则取出一份
              do
              {
                --v17;
                *v19++ ^= v14;                  // 与v14异或
              }
              while ( v17 );
            }
            if ( v14 == 89 )
            {
              while ( v18 < (int)v16 )
                v3[v18++] ^= 89u;               // 如果v14达到了89，接下来的内容全部与v4异或
            }
            shake_times = v14 + 1;
          }
        }
        if ( v14 == 100 )
        {
          if ( (int)(time(0) - v6) > 9 )
          {
            _android_log_print(4, "FindMyDex", "OH~ You are too slow. Please try again");
            qmemcpy(v3, &unk_7004, (size_t)off_43A18);
            shake_times = 0;
          }
          else
          {
            v20 = v6;
            if ( uncompress(dest, &destLen, (const Bytef *)v3, (uLong)off_43A18) )
              _android_log_print(5, "FindMyDex", "Dangerous operation detected.");
            v21 = open(filename, 577, 511);
            if ( !v21 )
              _android_log_print(5, "FindMyDex", "Something wrong with the permission.");
            write(v21, dest, destLen);          // 写入结果dex文件
            close(v21);
            free(dest);
            free(v3);
            if ( access(name, 0) && mkdir(name, 0x1FFu) )
              _android_log_print(5, "FindMyDex", "Something wrong with the permission..");
            sub_2368(a1);
            remove(filename);
            _android_log_print(4, "FindMyDex", "Congratulations!! You made it!");
            sub_2250((int)a1);
            shake_times = 0x80000000;
            v6 = v20;
          }
        }
      }
    }
LABEL_51:
    ;
  }
  while ( !a1[15] );
  sub_2BDA(v26);
  return _stack_chk_guard - v58;
}
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