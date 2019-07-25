# sa-dns

## Usage

```
sa-dns -h
```

Examples,

```shell
# 切 A 记录
sa-dns ensure main --type A --value 1.1.1.1 --enable
# dry-run
sa-dns ensure main --type A --value 1.1.1.1 --enable --dry-run
# 切 A 记录，独占
sa-dns ensure main --type A --value 1.1.1.1 --enable --excl
# 调整 ttl
sa-dns ensure main --type A --value 1.1.1.1 --ttl 100 --enable
# 批量切 CNAME 记录，常用于 CNAME 到 CDN 等操作
sa-dns ensure main --type CNAME --value {domain}.h1.aqb.so. --enable

# 查找子域记录
sa-dns list -S music
# 查找 aqb 相关记录（只返回符合该关键字的记录）
sa-dns list -s aqb
# 按正则查找子域（查看 aqb 的测试域名）
sa-dns list | grep -E '^.*aqb\s'

# 支持通过 -d,--domain 指定其他域名
sa-dns -d dou.bz list
```

### ensure

Add or modified, ensure the dns records that demanded to present.

有几种用法，

1. 无记录时，添加记录
2. 有记录时，disable 或 enable 记录

由于一个子域名的 CNAME 跟 A 记录是互斥的，必须先 disable 再 enable 另一个，所以 ensure 一条记录可能会产生很多修改请求。

#### excl

为了方便操作，支持 `--excl` 选项，意为独占、排他（exclusive），会 disable 掉该域名的其他同类型记录。

#### dry run

没把握的可以先使用 `--dry-run`，会输出比较详细的信息。

#### 批量操作一组域名

如，

`sa-dns ensure main --type CNAME --value {domain}.h1.aqb.so. --enable`

是将主要域名（在 `external_domains` 这个 ini file 中配置 main 段落）都 CNAME 到对应的 aqb 域名。

`sa-dns ensure main --type A --value 1.1.1.1 --enable --excl`

是将主要域名都解析到 1.1.1.1，同时停止其他 A 记录。

### list

List dns records.

### dump

Dump dns records.

### show

Show information.

### remove

Remove dns records.

### monitor

DNSPod Monitor.
