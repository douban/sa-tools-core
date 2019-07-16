# sa-disk

```shell
sa-disk usage
sa-disk usage -n 5 -d 3
sa-disk usage -r /data1/ncdu-export-%-20160513142844.gz
sa-disk usage -c /tmp
sa-disk usage -p /data
sa-disk usage --force-check

sa-disk clean
```

If you want to run it as root, you can call it like this

```
sudo sa-disk -usysadmin usage
```

Output examples,

```shell
(venv) user@host ~/projects/sa-tools-core $ sa-disk --debug usage -n 5 -d 3 -c . -p tmp/
2019-07-16 16:58:49,079 sa_tools_core.disk INFO Finding lastest ncdu exported data file from tmp/
2019-07-16 16:58:49,103 sa_tools_core.disk INFO Found ncdu exported data file tmp/ncdu-export-%home%user%projects%sa-tools-core-20190716161855.gz
2019-07-16 16:58:49,110 sa_tools_core.disk INFO About to calc top 5 huge items in depth 3.
2019-07-16 16:58:49,248 sa_tools_core.disk DEBUG calc top_huge_dirs_from_ncdu...
2019-07-16 16:58:49,416 sa_tools_core.disk DEBUG done top_huge_dirs_from_ncdu
Top 5 huge items in depth 3:
137.9 MiB  /home/user/projects/sa-tools-core/venv2/lib/python2.7
131.0 MiB  /home/user/projects/sa-tools-core/venv/lib/python3.7
23.6 MiB  /home/user/projects/sa-tools-core/tmp/ncdu-export-%-20160513142844.gz
23.6 MiB  /home/user/projects/sa-tools-core/tmp/ncdu-export-%-20160513155501.gz
23.6 MiB  /home/user/projects/sa-tools-core/tmp/ncdu-export-%-20160513160857.gz
```
