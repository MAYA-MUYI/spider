# 设置RAID组的Cache读写属性

## 命令功能
>设置RAID组的Cache读写属性。

## 命令格式
`arcconf setcache controller_id logicaldrive ld_id mode`

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡ID | –|
| ld_id | 虚拟磁盘ID | –|
| mode | RAID的Cache读写策略 | 读策略包括：ron：使能读Cache功能 roff：关闭读Cache功能 写策略包括：wb：在没有电容保护时，仍会打开RAID组写Cache，可能会导致异常掉电后的数据丢失。说明：请谨慎选择将写策略设置为“wb”。wbb：在没有电容或电容还没有Ready时自动将RAID组写Cache关闭，为推荐配置。wt：始终关闭写Cache功能。|

使用指南
- 无

使用实例
~~~
# 使能RAID的读Cache功能。
domino:# ./arcconf setcache 1 logicaldrive 0 ron
Controllers found: 1 

Command completed successfully.
~~~
