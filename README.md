# SA Tools Core


## Development guide

Currently support python2.7 ~ python3.7

### quick start

```
make init
```

### re-install after modify codes

```
make install
```

## Command Line Tools

### sa-notify

TODO

### sa-dns

```shell
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

[see more](docs/sa-dns.md)

### sa-script

TODO

### sa-access

access log 查询分析工具，支持简单查询，聚合查询，时段对比分析等

```shell
sa-access query
sa-access query --term ip 1.1.1.1
sa-access query -t host example.com -x bandwidth --by ip
sa-access query --term appname app1 -x count --by-script "doc['remote_addr'].value + ' ' + doc['normalize_url'].value"
sa-access query --term appname app1 -x count --by-script "def ip=doc['remote_addr'].value;(ip >>24) + '.' + ((ip >> 16) % 256) + '.' + ((ip >> 8) % 256) + '.' + (ip % 256) + ' ' + doc['normalize_url'].value"
sa-access analyze --term host example.com -x sum bytes_sent --by nurl -a '2017-03-28 09:30' -d 15 -b '2017-03-28 10:30'
```

[see more](docs/sa-access.md)

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

### sa-disk

TODO

### sa-bs

TODO
