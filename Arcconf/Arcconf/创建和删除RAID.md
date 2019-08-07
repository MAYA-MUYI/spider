# 创建和删除RAID

## 命令功能
>创建、删除RAID。

## 命令格式
~~~
arcconf create controller_id logicaldrive stripesize stripesize name ld_name priority ld_priority method mode capacity raid_level channel_id1 slot_id1 channel_id2 slot_id2...channel_idN slot_idN [noprompt]
arcconf delete controller_id logicaldrive ld_id noprompt
~~~

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡ID | –|
| stripesize | 虚拟磁盘扇区大小 | –|
| ld_name | 虚拟磁盘名称 | –|
| ld_id | 虚拟磁盘ID | –|
| ld_priority | 创建虚拟磁盘任务的优先级 | high medium low|
| mode | 创建虚拟磁盘的后续动作 | 对于RAID 0/1和Volume，有“quick”和“skip”两个动作。前者用于对Array数据做快速初始化，后者用于恢复Array的情况，不清空数据直接建立RAID关系。 对于有冗余功能的Array，除“quick”和“skip”外，还增加了“Build/Verify”和“Clear”动作，可对RAID数据做初始化和清空Array数据。|
| capacity | 虚拟磁盘容量 | –|
| raid_level | 虚拟磁盘RAID级别 | –|
| channel_idN | 硬盘的Channel ID | –|
| slot_idN | 成员盘的槽位号 | –|

使用指南
- 无

使用实例
~~~
 创建RAID 5。& 删除ID为1的虚拟磁盘。
domino:# ./arcconf create 1 logicaldrive stripesize 64 name test01 priority high method quick 102400 5 0 0 0 1 0 2
Controllers found: 1 

For arrays with all SSD drives, caching is not recommended. Disable all cache settings?(Y/N) 

Are you sure you want to continue? 
Press y, then ENTER to continue or press ENTER to abort: y 

Do you want to add a logical device to the congirutaion? 
Press y, then ENTER to continue or press ENTER to abort: y 

Creating logical device: test01 

Command completed successfully.
domino:# ./arcconf delete 1 logicaldrive 1 nopromt
Controllers found: 1 
All data in logical device 1 will be lost: 
Deleting: logical device 1 ("LogicalDrv 1") 

Command completed successfully.     
~~~
