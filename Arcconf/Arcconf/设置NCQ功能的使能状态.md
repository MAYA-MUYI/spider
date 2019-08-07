# 设置NCQ功能的使能状态

## 命令功能
>使能和禁用读写指令优化处理功能。

## 命令格式
`arcconf setncqcontroller_id state`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | 硬盘所在RAID卡的ID | –|
| state | NCQ功能的状态 | enable disable|

使用指南
- 无

使用实例
~~~
# 打开NCQ功能。
domino:# ./arcconf setncq 1 enable
Controllers found: 1 

WARNING : NCQ setting changes will be reflected only after next power cycle. 

Command completed successfully.
~~~
