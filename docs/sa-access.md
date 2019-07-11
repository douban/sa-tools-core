# sa-access

access log 查询分析工具，支持简单查询，聚合查询，时段对比分析等

目前支持数据源为 Elasticsearch

## query

### normal query

```
$ sa-access query --term ip 1.1.1.1
$ sa-access query -q 2.2.2.2 --term appname app1 -n 20
$ sa-access query --term appname app1 remote_addr 2.2.2.2 -n 10
$ sa-access query -q 'remote_addr:[1.1.1.0 TO 1.1.1.254]' -n10
```

### aggs query

```
$ sa-access query -x bandwidth
$ sa-access query -x sum bytes_sent
$ sa-access query -t host movie.example.com -x bandwidth --by dt 30s
$ sa-access query -t host movie.example.com -x max bytes_sent --by dt 30s
$ sa-access query -q 'Baiduspider' -t host movie.example.com -x bandwidth --by nurl
$ sa-access query -t host movie.example.com -x bandwidth --by ip
$ sa-access query -x count --by ip
$ sa-access query -x unique_count browser_id --by ip
```

#### by multi field or script

```
$ sa-access query --term appname app1 -x count --by-multi remote_addr normalize_url
$ sa-access query --term appname app1 -x count \
        --by-script "doc['remote_addr'].value + ' ' + doc['normalize_url'].value"
```

##### by ip and nurl

```
$ sa-access query --term appname app1 -x count \
        --by-script "def ip=doc['remote_addr'].value;(ip >>24) \
        + '.' + ((ip >> 16) % 256) + '.' + ((ip >> 8) % 256) \
        + '.' + (ip % 256) + ' ' + doc['normalize_url'].value"
```

##### by ip section and nurl

```
$ sa-access query --term appname app1 -x count \
        --by-script "def ip=doc['remote_addr'].value>>8;(ip >>24) \
        + '.' + ((ip >> 16) % 256) + '.' + ((ip >> 8) % 256) \
        + '.' + (ip % 256) + ' ' + doc['normalize_url'].value"
```

## analyze

When qps is abnormal, we try to find which (ip, nurl) pair contribute to it.

```
$ sa-access analyze --term appname app1 -x count --by-multi remote_addr nurl

$ sa-access analyze --term appname app1 -x bandwidth --by-multi nurl

$ sa-access analyze --term host music.example.com -x count --by nurl \
        -a '2017-03-28 09:30' -d 15 -b '2017-03-28 10:30'
```

## explain

```
$ sa-access explain
$ sa-access explain -f remote_addr upstream_response_time
```
