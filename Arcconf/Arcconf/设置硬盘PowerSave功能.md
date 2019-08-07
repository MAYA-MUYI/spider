# 设置硬盘PowerSave功能

## 命令功能
>设置虚拟磁盘的省电参数。

## 命令格式
`arcconf setpower controller_id ld ld_id slowdown timer1 poweroff timer2`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡的ID。 | –|
| ld_id | 虚拟磁盘的ID。 | –|
| timer1 | 减速定时器。 | 单位为minutes。|
| timer2 | 下电定时器。 | 单位为minutes。|

使用指南
- 无

使用实例
~~~
# 设置Powersave参数。
domino:# ./arcconf setpower 1 ld 0 slowdown 3 poweroff 5
Controllers found: 1 

Command completed successfully.
~~~
