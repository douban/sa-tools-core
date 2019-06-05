# coding: utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = '/etc/sa-tools/'

NODE_IRC_CHANNEL = '#sysadmin'
NODE_SLACK_CHANNEL = '#sa'
NODE_MAIL_TO = 'sa@example.com'

SYSADMIN_EMAIL = 'sysadmin@example.com'
ICINGA_EMAIL = 'icinga@example.com'

IPMI_TIMEOUT = 2
IPMI_RETRIES = 1

SMTP_SERVER = ''

NCDU_EXPORT_DATA_PATH = "/data1"
NCDU_JOB_LOCK_PREFIX = "/tmp/sa-disk-ncdu-lock"

NOTIFICATION_GATEWAY_API = ''
NOTIFICATION_GATEWAY_TIMEOUT = 10  # 10s

SA_ES_HOSTS = ['es.svc:8080']
SA_ES_NGINX_ACCESS_INDEX_PREFIX = 'heka-nginx.access-'
SA_ES_NGINX_ACCESS_DOC_TYPE = 'nginx.access'

PROXIES = {
    "http": "http://gfw:2333",
    "https": "http://gfw:2333",
}

try:
    exec(open(os.path.join(CONFIG_DIR, "config.py")).read())
except Exception:
    pass
