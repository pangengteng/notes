# TCP

## 定义
全称 Transmission Control Protocol，中文翻译为传输控制协议，一种面向链接，可靠的传输协议

## 包头格式
![格式](https://static001.geekbang.org/resource/image/64/bf/642947c94d6682a042ad981bfba39fbf.jpg)

> 序号：

> 确认序号：

> 状态位  
> 1. URG:
> 2. ACK:
> 3. PSH:
> 3. RST:
> 4. SYN:
> 5. FIN:

## 三次握手
> 为什么是三次

> 状态时序图
![三次握手](https://static001.geekbang.org/resource/image/c0/08/c067fe62f49e8152368c7be9d91adc08.jpg)

> 过程详解

> 第一次握手，SYN = 1，seq=3193042259
![第一次握手](./images/first_handshake.png)

> 第二次握手，SYN, ACK = 1，seq=2807733674，ack=3193042260
![第二次握手](./images/second_handshake.png)

> 第三次握手，ACK = 1，seq=3193042260，ack=2807733675
![第二次握手](./images/third_handshake.png)

## 四次挥手

> 状态时序图
![四次挥手](https://static001.geekbang.org/resource/image/bf/13/bf1254f85d527c77cc4088a35ac11d13.jpg)

> 过程详解
> 

## 问题
1. 发送方传输数据为什么 ACK = 1
![传输数据](./images/transfer_data_1.png)