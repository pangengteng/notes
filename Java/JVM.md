# JVM

## 环境
> JDK, JRE, JVM 的关系
>
> 就范围来说，JDK > JRE > JVM
> JDK = JRE + 开发工具
> JRE = JVM + 类库

![](images/jdk&jre&jvm.png)

## 字节码

> javac 和 javap 命令 
> 常量池 
> 方法体
> 非静态方法隐藏this参数
> 局部变量表
> JDK1.7 invokeDynamic 指令和 JDK8 lambda 表达式
> 通过字节码可以了解枚举类的实现

## 类加载

### 类的生命周期和加载过程
![](images/class_loading.png)

> 1. 加载：找到文件系统中的class文件，找不到报NoClassDefFoundError
> 2. 校验：校验class字节码的合法性
> 3. 准备：创建静态字段并赋默认值，如果静态字段被final修饰，则初始化
> 4. 解析：将符号引用解析成直接引用
> 5. 初始化：执行类构造器方法、静态变量赋值语句、静态代码块

> 用Class.forname动态加载类时，找不到class文件报ClassNotFoundException