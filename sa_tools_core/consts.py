# coding: utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

IPMI_TIMEOUT = 2
IPMI_RETRIES = 1

# CONFIGURATION SECTION

CONFIG_DIR = '/etc/sa-tools/'
EXTERNAL_DOMAINS_CONFIG_FILE = CONFIG_DIR + '/external_domains'

NODE_IRC_CHANNEL = '#sysadmin'
NODE_SLACK_CHANNEL = '#sa'
NODE_MAIL_TO = 'sa@example.com'

SYSADMIN_EMAIL = 'sysadmin@example.com'
ICINGA_EMAIL = 'icinga@example.com'

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

# # DNS

# can be a string pattern which contains {cb_token}
DNS_MONITOR_CALLBACK_URL = 'http://example.com/api/callback/dnsmonitor/{cb_token}'
DEFAULT_DNS_DOMAIN = 'example.com'

# # Scripts

ENABLE_DOA = False

try:
    from local_config import *  # NOQA
    exec(open(os.path.join(CONFIG_DIR, "config.py")).read())
except Exception:
    pass
