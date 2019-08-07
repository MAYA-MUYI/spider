# 设置Spinup参数

## 命令功能
>设置上电时允许同时起转的硬盘数量。

## 命令格式
`arcconf setpower controller_id spinup internal external`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | 硬盘所在RAID卡的ID | –|
| internal | 上电时允许同时起转的内部硬盘数量 | –|
| external | 上电时允许同时起转的外部硬盘（如外接JBOD）数量 | –|

使用指南
- 无

使用实例
~~~
 设置硬盘spinup参数。& 查询spinup配置。
domino:# ./arcconf setpower 1 spinup 4 0
Controllers found: 1 


Command completed successfully.
domino:# ./arcconf getconfig 1 | grep Spinup
   Spinup limit internal drives             : 4 
   Spinup limit external drives             : 0
~~~
