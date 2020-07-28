# SA Tools Core

![](https://img.shields.io/pypi/status/sa-tools-core)
![](https://img.shields.io/pypi/v/sa-tools-core)
![](https://img.shields.io/pypi/pyversions/sa-tools-core)
![](https://img.shields.io/pypi/wheel/sa-tools-core)
![](https://img.shields.io/pypi/l/sa-tools-core)

SA Tools 顾名思义是 System Administrator 的工具集，包含一些实用工具，涉及 DNS 管理、远程批量执行脚本、日志分析查询、通知提醒等。

## Installation

```
pip install sa-tools-core
```

## Development Guide

Currently support python3.6+

### Quick start

```
# first clone this repo
cd sa-tools-core

make init
```

See Makefile for more details.

### Re-install after modify codes

```
make install
```

## Configuration

```
cp local_config.py.example local_config.py
# then edit local_config.py
vi local_config.py
```

You can use a system-wide configuration path as well, by default it is `/etc/sa-tools/config.py`.

Local configs will override [sa_tools_core/consts.py](sa_tools_core/consts.py).

For other third party service configs, see [examples/config](examples/config).

You can put third party service configs to `/etc/sa-tools/` directory.

## Command Line Tools

For all the CLI tools, you can type `-h` or `--help` to get help messages and examples.

### sa-notify

通知提醒工具，支持 wechat, wework(企业微信), email, sms, pushbullet, pushover, telegram 等多种通知类型。

```shell
sa-notify --wechat user1 --content 'xxx'
echo 'xxx' | sa-notify --wechat user1,user2 --email user1@example.com user3@example.com
```

### sa-dns

DNS 管理工具，目前仅支持 DNSPod。

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

远程命令执行工具，目前基于 ansible，需要事先配置好 ansible 环境(/etc/ansible/hosts)。

一些特点，

- 兼容 ansible host pattern
- 脚本可从 stdin 传入或指定文件路径，若都不指定则会调用 editor 进入编辑模式(类似 git commit 时的行为)。
- 批量执行，有进度条
- 执行完毕后会进入交互模式，可以对结果进行筛选，支持 shell 管道操作，支持再次发起执行

```shell
$ echo 'uptime && echo $HOSTNAME $(whoami)' | sa-script test_zk
Executing...
100%|######################################################|Elapsed Time: 0:00:09

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
sa-access query --term appname app1 -x count --by-script "def ip=doc['remote_addr'].value; ip.substring(0, ip.lastIndexOf('.')) + ' ' + doc['normalize_url'].value"
sa-access analyze --term host example.com -x sum bytes_sent --by nurl -a '2017-03-28 09:30' -d 15 -b '2017-03-28 10:30'
```

[see more](docs/sa-access.md)

### sa-icinga

一个 Icinga2 的 CLI 工具。

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

磁盘相关工具，利用 ncdu 快速扫盘，并可以保存、分析结果。

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

### sa-tc

`sa-tc` 是对腾讯云 API 的封装，支持黑石、CVM 等产品。

```shell
sa-tc bm devices
sa-tc bm devices -f yaml
sa-tc bm devices --alias host
```

### sa-github

`sa-github` 是对 Github API V3 的封装, 支持 github.com 和 ghe, 目前功能还在完善中, 只支持 collaborator api 

```shell
sa-github collaborator --org xxx --repo yyy add --username user_1 --permission admin
sa-github collaborator --org xxx --repo yyy remove --username user_1
```

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
