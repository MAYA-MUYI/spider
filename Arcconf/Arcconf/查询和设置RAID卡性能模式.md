# 查询和设置RAID卡性能模式

## 命令功能
>查询和设置RAID卡性能模式。

## 命令格式
~~~
arcconf setperform controller_id mode
arcconf getperform controller_id
~~~

## 参数说明
| 参数| 参数说明| 取值|
| ---- | ---- | ----|
| controller_id | RAID卡的ID | –|
| mode | RAID卡性能模式 | 1：Dynamic 2：OLTP/Database 3：Big Block Bypass mode 4：User defined mode|

使用指南
- 无

使用实例
~~~
 设置RAID卡性能模式为Dymatic。& 查询RAID卡性能模式。
domino:# ./arcconf setperform 1 1
Controllers found: 1 

Command completed successfully.
domino:# ./arcconf getperform 1
Controllers found: 1 

   Performance Mode                        : Default/Dymatic 

   CACHE_REPRESSPREFETCHING                : DISABLE 
   CACHE_IO_SORTING                        : ENABLE 
   CACHE_INSERT_LRU                        : DISABLE 
   CACHE_DYNAMIC_SHARING                   : ENABLE 
   CACHE_READ_LOAD_BYPASS_VALID            : ENABLE 
   CACHE_WRITE_LOAD_BYPASS_VALID           : ENABLE 
   CACHE_LARGE_WRITE_BYPASS                : DISABLE 
   IO_COALESCING                           : ENABLE 
   CACHE_MAX_DIRTY                         : 75 percent 
   CACHE_DEMAND_FLUSH_THRESHOLD            : 75 percent 
   CACHE_PAGE_SIZE                         : 256 KB 
   CACHE_RESERVED_FOR_INACTIVE             : 10 
   CACHE_ADDITIONAL_WRITES                 : 4 
   CACHE_MIN_FLUSH_STRIPE                  : 64 KB 
   CACHE_BYPASS_WRITE_IO_SIZE              : 128 KB 
   IO_LIMIT_SATA_HDD                       : 32 
   IO_LIMIT_SATA_SSD                       : 32 
   IO_LIMIT_SAS_HDD                        : 64 
   IO_LIMIT_SAS_SSD                        : 64 
   R1_SEQ_READ_LOW_QW_THRESHOLD            : 4 
   R1_SEQ_DETECTION_THRESHOLD              : 4 

Command completed successfully.
~~~
