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

For all the CLI tools, you can type `-h` or `--help` to get help messages and examples.

### sa-notify

```shell
sa-notify --wechat user1 --content 'xxx'
echo 'xxx' | sa-notify --wechat user1,user2 --email user1@douban.com user3@douban.com
```

### sa-dns

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

[see more](docs/sa-dns.md)

### sa-script

A remote script runner tool based on ansible. To use it, you need to prepare your ansible environment first.

```shell
$ echo 'uptime && echo $HOSTNAME $(whoami)' | sa-script test_zk
Executing...
100%|##################################################################################################################################################|Elapsed Time: 0:00:09

+----------+----+-------------------------------------------------------+--------+
| host     | rc | stdout                                                | stderr |
+----------+----+-------------------------------------------------------+--------+
| test-zk3 | 0  |  11:40:15 up 384 days, 19:00,  1 user,  load average: |        |
|          |    | 0.16, 0.20, 0.26 test-zk3 user1                       |        |
| test-zk2 | 0  |  11:40:15 up 392 days, 20:00,  1 user,  load average: |        |
|          |    | 0.25, 0.22, 0.30 test-zk2 user1                       |        |
| test-zk1 | 0  |  11:40:15 up 392 days, 23:53,  1 user,  load average: |        |
|          |    | 0.30, 0.22, 0.25 test-zk1 user1                       |        |
+----------+----+-------------------------------------------------------+--------+
```

See `sa-script -h` for more details.

TODO: add a gif to demonstrate.

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

```shell
# try test
sa-icinga notify --wechat user1 --email user1@example.com --test

sa-icinga notify --wechat user1 --email user1@example.com  # need icinga pass os environment vars

sa-icinga ack --host sa --service check-puppet --comment 'hehe'
sa-icinga ack --host 'sa*' --service 'check-puppet'
sa-icinga ack --host 'sa*' --service 'check-puppet' --remove

sa-icinga show --filter 'host.name == "sa" && service.name == "check-puppet"'
sa-icinga show --type host --filter 'match("sa*", host.name)' | less
sa-icinga show --type service --filter 'regex("check_[a-z]*", service.name)' | less
sa-icinga show --type notification --filter 'notification.host_name == "sa"' | less
sa-icinga show --type user | grep user1
sa-icinga show --filter 'service.name == "check-puppet"' --attrs acknowledgement
```

[see more](docs/sa-icinga.md)

### sa-disk

```shell
sa-disk usage
sa-disk usage -n 5 -d 3
sa-disk usage -r /data1/ncdu-export-%-20160513142844.gz
sa-disk usage -c /tmp
sa-disk usage -p /data
sa-disk usage --force-check

sa-disk clean
```

[see more](docs/sa-disk.md)

### sa-bs

TODO

## Client

Tools can be called from client as well.

```python
from sa_tools_core.client import Client

c = Client()
c.notify(wework='user1', content='hehe')
c.uptime()
c.dns.list(S='@')
```

See [sa_tools_core/client.py](sa_tools_core/client.py) for more details.
