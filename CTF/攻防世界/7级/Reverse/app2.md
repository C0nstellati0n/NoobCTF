# app2

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=8949c6aa-fae8-47ee-8897-bbbccd3d4437_2&task_category_id=6)

有了jadx后就能正式进军安卓逆向题了。

直接看MainActivity。

```java
public void onClick(View view) {

        switch (view.getId()) {

            case R.id.button1 /* 2131165187 */:

                if (this.c.getText().length() == 0 || this.d.getText().length() == 0) {

                    Toast.makeText(this, "不能为空", 1).show();

                    return;

                }

                String obj = this.c.getText().toString();

                String obj2 = this.d.getText().toString();

                Log.e("test", obj + " test2 = " + obj2);

                Intent intent = new Intent(this, SecondActivity.class);

                intent.putExtra("ili", obj);

                intent.putExtra("lil", obj2);

                startActivity(intent);

                return;

            default:

                return;

        }

    }
```

看见onClick函数中调用了SecondActivity，跟进看看。

```java
public void onCreate(Bundle bundle) {

        super.onCreate(bundle);

        setContentView(R.layout.activity_main2);

        Intent intent = getIntent();

        String stringExtra = intent.getStringExtra("ili");

        String stringExtra2 = intent.getStringExtra("lil");

        if (Encryto.doRawData(this, stringExtra + stringExtra2).equals("VEIzd/V2UPYNdn/bxH3Xig==")) {

            intent.setAction("android.test.action.MoniterInstallService");

            intent.setClass(this, MoniterInstallService.class);

            intent.putExtra("company", "tencent");

            intent.putExtra("name", "hacker");

            intent.putExtra("age", 18);

            startActivity(intent);

            startService(intent);

        }

        SharedPreferences.Editor edit = getSharedPreferences("test", 0).edit();

        edit.putString("ilil", stringExtra);

        edit.putString("lili", stringExtra2);

        edit.commit();

    }
```

其中的onCreate函数调用了Encrypto的doRawData函数。

```java
public class Encryto {

    public static native int checkSignature(Object obj);



    public static native String decode(Object obj, String str);



    public static native String doRawData(Object obj, String str);



    public static native String encode(Object obj, String str);



    public native String HelloLoad();



    static {

        System.loadLibrary("JNIEncrypt");

    }

}
```

然而Encrypto本身是在外部链接库中的。把题目的apk改为zip后缀解压后找到名为`JNIEncrypt`的so文件，放入ghidra或ida中进行反编译并找到doRawData函数。

```c
void doRawData(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  char *__s;
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  size_t sVar4;
  int in_GS_OFFSET;
  undefined4 uVar5;
  code *pcVar6;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined local_1c;
  int local_18;
  
  uVar5 = 0x127f1;
  local_18 = *(int *)(in_GS_OFFSET + 0x14);
  iVar1 = checkSignature(param_1,param_2,param_3);
  if (iVar1 == 1) {
    local_1c = 0;
    local_20 = 0x3d3d7965;
    local_24 = 0x6b747365;
    local_28 = 0x74617369;
    local_2c = 0x73696874;
    uVar2 = (**(code **)(*param_1 + 0x2a4))(param_1,param_4,0);
    uVar3 = AES_128_ECB_PKCS5Padding_Encrypt(uVar2,&local_2c);
    (**(code **)(*param_1 + 0x2a8))(param_1,param_4,uVar2,uVar5,uVar3);
    (**(code **)(*param_1 + 0x29c))(param_1,uVar3);
  }
  else {
    __s = *(char **)PTR_UNSIGNATURE_00014f90;
    pcVar6 = *(code **)(*param_1 + 0x28c);
    sVar4 = strlen(__s);
    (*pcVar6)(param_1,__s,sVar4);
  }
  if (*(int *)(in_GS_OFFSET + 0x14) == local_18) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

local_2c那部分一看就是个字符串，转为字符后再反过来得到key`thisisatestkey==`。回到SecondActivity地onCreate函数中找到比对的密文字符串`VEIzd/V2UPYNdn/bxH3Xig==`，aes的ecb模式解密后得到`aimagetencent`（如果使用cyberchef解密，需要先from base64，aes的key和iv都是`thisisatestkey==`），却不是flag。因为没有模拟器无法运行题目，只能继续在程序中看看有什么漏掉的函数。发现有个`FileDataActivity`很可疑。里面也有串密文，不知道是啥，赌了一把拿相同的key去aes解密，直接就得到了flag。

## Flag
> Cas3_0f_A_CAK3