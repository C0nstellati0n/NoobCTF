# easyEZbaby_app

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f083ba70-56a2-11ed-ab28-000c29bc20bf&task_category_id=4)

确实baby题，终于来了个不骗人的出题人。查看AndroidManifest.xml，在activity那一栏找到逆向目标——`com.example.activitytest.FirstActivity`。

```java
public void onClick(View view) {
        String obj = this.username.getText().toString();
        String obj2 = this.password.getText().toString();
        if (checkUsername(obj) && checkPass(obj2)) {
            Toast.makeText(this, "登录成功", 0).show();
            Toast.makeText(this, "flag{" + obj + obj2 + "}", 0).show();
            return;
        }
        Toast.makeText(this, "登录失败", 0).show();
    }
```

两个函数，`checkUsername`和`checkPass`，一个用户名一个密码，flag是`flag{用户名+密码}`。先看`checkUsername`。

```java
  public boolean checkUsername(String str) {
        if (str != null) {
            try {
                if (str.length() != 0 && str != null) {
                    MessageDigest messageDigest = MessageDigest.getInstance("MD5");
                    messageDigest.reset();
                    messageDigest.update("zhishixuebao".getBytes());
                    String hexString = toHexString(messageDigest.digest(), "");
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0; i < hexString.length(); i += 2) {
                        sb.append(hexString.charAt(i));
                    }
                    String sb2 = sb.toString();
                    return (sb2).equals(str);
                }
                return false;
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            }
        }
        return false;
    }
```

我完全没学过java，碰都没碰过，所以最开始那个md5加密我是拿去外面做的。兴冲冲地去加密`zhishixuebao`，然后放入函数，来一句`System.out.println(sb2);`就能直接秒username。然而第一次没成功，外面加密得到的md5和java里面的不一样。好吧只能搞java原生的了。这里标注几个成功运行的点。

1. 不要忘了引入必要的包,`import java.security.MessageDigest;`和`import java.security.NoSuchAlgorithmException;`。前者md5加密需要，后者`NoSuchAlgorithmException`需要。
1. 使用`MessageDigest`时，必须要有一个try-catch语句，否则编译时会报错。catch的exception正是上面所引入的，不引入又报错。

至于密码就很简单了。

```java
    public boolean checkPass(String str) {
        if (str != null) {
            char[] charArray = str.toCharArray();
            if (charArray.length != 15) {
                return false;
            }
            for (int i = 0; i < charArray.length; i++) {
                charArray[i] = (char) ((((255 - i) + 2) - 98) - charArray[i]);
                if (charArray[i] != '0' || i >= 15) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
```

注意最后是`!='0'`而不是`!=0`，是字符不是数字。也就是说加密后的结果是`ord('0')=48`。

```python
for i in range(15):
    print(chr((255-i)+2-98-48),end='')
```

最后放完整检查脚本。

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Main
{
        static boolean checkPass(String str) {
        if (str != null) {
            char[] charArray = str.toCharArray();
            if (charArray.length != 15) {
                return false;
            }
            for (int i = 0; i < charArray.length; i++) {
                charArray[i] = (char) ((((255 - i) + 2) - 98) - charArray[i]);
                if (charArray[i] != '0' || i >= 15) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }

        static String toHexString(byte[] bArr, String str) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bArr) {
            String hexString = Integer.toHexString(b & 255);
            if (hexString.length() == 1) {
                sb.append('0');
            }
            sb.append(hexString);
            sb.append(str);
        }
        System.out.println(sb.toString());
        return sb.toString();
    }

    static boolean checkUsername(String str) {
        if (str != null) {
            try {
                if (str.length() != 0 && str != null) {
                    MessageDigest messageDigest = MessageDigest.getInstance("MD5");
                    messageDigest.reset();
                    messageDigest.update("zhishixuebao".getBytes());
                    String hexString = toHexString(messageDigest.digest(), "");
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0; i < hexString.length(); i += 2) {
                        sb.append(hexString.charAt(i));
                    }
                    String sb2 = sb.toString();
                    System.out.println(sb2);
                    return (sb2).equals(str);
                }
                return false;
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            }
        }
        return false;

    }
    public static void main(String[] args) {
        System.out.println(checkUsername("7afc4fcefc616ebd"));
        System.out.println(checkPass("onmlkjihgfedcba"));
    }
}
```

## Flag
> flag{7afc4fcefc616ebdonmlkjihgfedcba}