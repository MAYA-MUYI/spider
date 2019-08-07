# 更改RAID条带大小/容量/级别

## 命令功能
>可以同时调整RAID中硬盘条带大小、RAID容量，并变更RAID级别。

## 命令格式
`arcconf modify controller_id from ld_id to [stripesize size] capacity raid_level channel_id1 slot_id1 ... channel_idN slot_idN [noprompt]`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡ID | –|
| ld_id | 待操作的虚拟磁盘ID | –|
| size | 待设置的条带大小 | –|
| capacity | 待设置的虚拟磁盘的大小 | –|
| raid_level | 待设置的虚拟磁盘的RAID级别 | –|
| channel_id1...channel_idN | 硬盘Channel ID | –|
| slot_id1...slot_idN | 硬盘槽位号 | –|

使用指南
- 带noprompt参数，表示强制执行。

使用实例
~~~
 不增加硬盘更改条带大小为“1024”。& 将VD 0的RAID级别迁移至RAID 5。
domino:# ./arcconf modify 1 from 0 to stripesize 1024 1525760 0 0 0 0 1
Controllers found: 1 
Reconfiguration of a logical device is a long process. Are you sure you want to continue? 
Press y, then ENTER to continue or press ENTER to abort: y 

Reconfiguring logical device: LogicalDrv 0 

Command completed successfully.
domino:# ./arcconf modify 1 from 0 to 1024 5 0 0 0 1 0 2 noprompt
Controllers found: 1 
Reconfiguring logical device: LogicalDrv 0 

Command completed successfully.
~~~
