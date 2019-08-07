# 设置SATA硬盘密码

## 命令功能
>为防止SATA硬盘被安全擦除，可设置SATA硬盘的密码。

## 命令格式
~~~
arcconf atapassword controller_id set new_password channel_id slot_id
arcconf atapassword controller_id clear current_password channel_id slot_id
~~~

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡ID | –|
| channel_id | 硬盘的Channel ID | –|
| slot_id | 硬盘的槽位号 | –|
| new_password | 待设置的密码 | –|
| current_password | SATA硬盘当前密码 | –|

使用指南
- 无

使用实例
~~~
 设置slot 0的SATA硬盘的密码为“huawei”。& 清除slot 0的SATA硬盘密码。
domino:# ./arcconf atapassword 1 set huawei 0 0
Controllers found: 1 
Setting the ATA security password on the SATA harddrive 

Are you sure you want to continue? 
Press y, then ENTER to continue or press ENTER to abort: y 

Command completed successfully.
domino:# ./arcconf atapassword 1 clear huawei 0 0
Controllers found: 1 
Clearing the ATA security password on the SATA harddrive 

Are you sure you want to continue? 
Press y, then ENTER to continue or press ENTER to abort: y 

Command completed successfully.
~~~
