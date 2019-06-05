# SA Tools Core


## Development guide

Currently support python2.7

### quick start

```
make init
```

### re-install after modify codes

```
make install
```

## Usage

### sa-dns

```
# 切 aqb
sa-dns ensure main --type CNAME --value {domain}.h1.aqb.so. --enable
# 切 A 记录
sa-dns ensure main --type A --value 1.1.1.1 --enable
# dry-run
sa-dns ensure main --type A --value 1.1.1.1 --enable --dry-run
# 切 A 记录，独占
sa-dns ensure main --type A --value 1.1.1.1 --enable --excl
# 调整 ttl
sa-dns ensure main --type A --value 1.1.1.1 --ttl 100 --enable

# 查找子域记录
sa-dns list -S music
# 查找 aqb 相关记录（只返回符合该关键字的记录）
sa-dns list -s aqb
# 按正则查找子域（查看 aqb 的测试域名）
sa-dns list | grep -E '^.*aqb\s'

# 测试 aqb 测试域名
sa-dns ensure aqb --type A --value 1.1.1.1 --enable --excl
sa-dns ensure aqb --type CNAME --value {domain}.h1.aqb.so. --enable

# 支持 -d,--domain 参数
sa-dns -d dou.bz list
```

#### ensure

有几种用法，

1. 无记录时，添加记录
2. 有记录时，disable 或 enable 记录

由于一个子域名的 CNAME 跟 A 记录是互斥的，必须先 disable 再 enable 另一个，所以 ensure 一条记录可能会产生很多修改请求。

##### excl

为了方便操作，支持 `--excl` 选项，意为独占、排他（exclusive），会 disable 掉该域名的其他同类型记录。

##### dry run

没把握的可以先使用 `--dry-run`，会输出比较详细的信息。

##### 批量操作一组域名

如，

`sa-dns ensure main --type CNAME --value {domain}.h1.aqb.so. --enable`

是将主要域名（在 `external_domains` 这个 ini file 中配置 main 段落）都 CNAME 到对应的 aqb 域名。

`sa-dns ensure main --type A --value 1.1.1.1 --enable --excl`

是将主要域名都解析到 1.1.1.1，同时停止其他 A 记录。

### sa-icinga

icinga2 doc: <http://docs.icinga.org/icinga2/latest/doc/module/icinga2/toc>

```
$ sa-icinga notify --wechat user1 --email user1@douban.com  # need icinga pass os environment vars

$ sa-icinga ack --host sa --service check-puppet --comment 'hehe'
$ sa-icinga ack --host 'sa*' --service 'check-puppet'
$ sa-icinga ack --host 'sa*' --service 'check-puppet' --remove

$ sa-icinga show --filter 'host.name == "sa" && service.name == "check-puppet"'
$ sa-icinga show --type host --filter 'match("sa*", host.name)' | less
$ sa-icinga show --type service --filter 'regex("check_[a-z]*", service.name)' | less
$ sa-icinga show --type notification --filter 'notification.host_name == "sa"' | less
$ sa-icinga show --type user | grep user1
$ sa-icinga show --filter 'service.name == "check-puppet"' --attrs acknowledgement
```

### sa-notify

TODO
