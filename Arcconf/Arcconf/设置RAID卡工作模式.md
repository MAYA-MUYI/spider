# 设置RAID卡工作模式

## 命令功能
>设置RAID卡工作模式。

## 命令格式
`arcconf setpcontrollermode controller_id mode`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡的ID | –|
| mode | RAID卡工作模式 | 0：表示“RAID：expose RAW”，为默认值，若硬盘本身没有RAID配置信息，则会以RAW盘的方式上报给OS，OS可以直接操作硬盘。 1：表示“RAID：hide RAW”，RAID卡只上报创建了RAID的盘。 2：表示“HBA”，该模式不允许创建RAID，所有盘以裸盘形式上报OS。 3：表示“Auto Volume”，若硬盘本身没有RAID配置信息，但是含有OS分区，则会以RAW盘上报OS，若硬盘本身既没有RAID配置信息，也不含OS分区，则RAID卡将该盘创建一个Volume上报OS。|

使用指南
- 无

使用实例
~~~
 设置RAID卡工作模式为“RAID：expose RAW”。& 查询RAID卡工作模式。
domino:# ./arcconf setcontrollermode 1 0
Controllers found: 1 

Command completed successfully.
domino:# ./arcconf getconfig 1
Controllers found: 1 
-------------------------------------------------------------- 
Controller information 
-------------------------------------------------------------- 
   Controller Status                       : Optimal 
   Controller Mode                         : RAID (Expose RAW)
   Channel description                     : SAS/SATA 
......
~~~
