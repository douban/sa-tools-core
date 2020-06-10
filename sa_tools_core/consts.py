# coding: utf-8

from __future__ import print_function

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

IPMI_TIMEOUT = 2
IPMI_RETRIES = 1

########################
# CONFIGURATION SECTION
########################

CONFIG_DIR = '/etc/sa-tools/'
EXTERNAL_DOMAINS_CONFIG_FILE = CONFIG_DIR + '/external_domains'

#######################################
# # Notification (sa-notify related)
#######################################

# sa-node related, not used yet
NODE_IRC_CHANNEL = '#sysadmin'
NODE_SLACK_CHANNEL = '#sa'
NODE_MAIL_TO = 'sa@example.com'

# default mail from addr
SYSADMIN_EMAIL = 'sysadmin@example.com'

# SMTP server related
SMTP_SERVER = ''
# If port is zero, the standard port is used.
SMTP_SERVER_PORT = 0
# Indicate the config file name for SMTP credentials, e.g. /etc/sa-tools/email
# SMTP_CREDENTIALS_CONFIG = 'email'
SMTP_CREDENTIALS_CONFIG = ''
SMTP_SSL = False

# proxies for slack, etc.
PROXIES = {
    "http": "http://gfw:2333",
    "https": "http://gfw:2333",
}

########################
# # Elasticsearch
########################

SA_ES_HOSTS = ['es.svc:8080']
SA_ES_VERSION = (7, 5, 1)
SA_ES_USER = ''
SA_ES_PASSWD = ''
SA_ES_NGINX_ACCESS_INDEX_PREFIX = 'heka-nginx.access-'
SA_ES_NGINX_ACCESS_INDEX_TIME_FORMAT = '%Y.%m.%d'
SA_ES_NGINX_ACCESS_TIMESTAMP_FIELD_NAME = "Timestamp"
SA_ES_NGINX_ACCESS_LOG_FIELD_NAME = "Payload"

########################
# # DNS
########################

# can be a string pattern which contains {cb_token}
DNS_MONITOR_CALLBACK_URL = 'http://example.com/api/callback/dnsmonitor/{cb_token}'
DEFAULT_DNS_DOMAIN = 'example.com'

########################
# # Scripts
########################

ANSIBLE_INVENTORY_CONFIG_PATH = ['/etc/ansible/hosts']
ANSIBLE_MODULE_PATH = []

########################
# # Disk
########################

NCDU_EXPORT_DATA_PATH = "/data1"
NCDU_JOB_LOCK_PREFIX = "/tmp/sa-disk-ncdu-lock"

########################
# # Icinga2
########################

ICINGA_EMAIL = 'icinga@example.com'
# see https://docs.sentry.io/error-reporting/configuration/?platform=python for more details
# SENTRY_DSN = 'https://<key>@sentry.io/<project>'
SENTRY_DSN = ''

# icinga alert page base url, every notify sent by sa-icinga will be attrtched with a wiki link
# For example : http://yourwiki.com/alerts/sshd_down
# Set to '' if you don't want it.
ALERT_WIKI_BASE_URL = ''

# notification gateway is a web service that stores and analyizes notifications. We have one in douban, you can build
# your own.
NOTIFICATION_GATEWAY_API = ''
NOTIFICATION_GATEWAY_TIMEOUT = 10  # 10s

ICINGA_CACERT = '/etc/icinga2/ssl/certs/ca.pem'
# you need to inhert IcingaClusterConfig and impl your own config class
# see sa_tools_core.libs.icinga for more details
ICINGA_CLUSTER_CONFIG_CLASS = 'sa_tools_core.libs.icinga:IcingaClusterConfig'

########################
# # BS(Black Stone)
########################

BS_CMD_PATTERN = 'qcloudcli "{module}" "{action}" {params}'
BS_DEFAULT_ATTRS = (
    'alias',
    'eipName',
    'subnetName',
    # 'vpcName', 'natName', 'instanceAlias',
    # 'instanceId', 'vlanId', 'natUid', 'unInstanceId', 'subnetId',
    'lanIp',
    'vpcIp',
    'eip',
    'cidrBlock',
    'cidr',
)
BS_DEFAULT_PARAMS = {
    'limit': 100,
}
BS_DEFAULT_PARAMS_BM = {
    'vpcId': 1001,
    'unVpcId': 'vpc-xxxxxxxx',
    'zoneId': 1000800001,  # 可用区ID。可通过 DescribeRegions 接口用来获取黑石物理机可用区。
}
BS_PLURAL_SUFFIX = ['s', 'List', 'Set']

########################
# # TC(Tencent CLI)
########################

TENCENT_DEFAULT_REGIN = 'ap-beijing'
TENCENT_DEFAULT_PARAMS = {
    'limit': 10,
    'offset': 0,
    'enhanced_service_security_service_enabled': False,
    'enhanced_service_monitor_service_enabled': False,
}

########################
# # Others
########################

GITHUB_API_ENTRYPOINT = 'https://ghe.yourdomain.com/api/v3'

try:
    from local_config import *  # NOQA
except Exception:
    pass

try:
    from io import open
    config_path = os.path.join(CONFIG_DIR, "config.py")
    exec(open(config_path, encoding='utf-8').read())
except Exception:
    print('WARNING: failed to load config %s.' % config_path)
