# coding: utf-8

from __future__ import print_function

import sys
import logging
import argparse
from pprint import pprint

import six

from sa_tools_core.libs.permission import require_sa, require_user  # NOQA
from sa_tools_core.libs.es import ESQuery
from sa_tools_core.libs.timeformat import timeformat
from sa_tools_core.consts import (SA_ES_HOSTS, SA_ES_VERSION,
                                  SA_ES_NGINX_ACCESS_INDEX_PREFIX,
                                  SA_ES_NGINX_ACCESS_INDEX_TIME_FORMAT,
                                  SA_ES_NGINX_ACCESS_TIMESTAMP_FIELD_NAME,
                                  SA_ES_NGINX_ACCESS_LOG_FIELD_NAME)
try:
    from sa_tools_core.consts import (SA_ES_USER, SA_ES_PASSWD)
except Exception as e:
    SA_ES_USER = ''
    SA_ES_PASSWD = ''
from sa_tools_core.utils import get_os_username, props, i2ip

logger = logging.getLogger(__name__)
VERBOSE_LEVEL = (
    (0, logging.WARN),
    (1, logging.INFO),
    (2, logging.DEBUG),
)

N_DOC_DEFAULT = 10


class NginxAccessESQuery(ESQuery):
    def __init__(self,
                 es_hosts=SA_ES_HOSTS,
                 index_prefix=SA_ES_NGINX_ACCESS_INDEX_PREFIX,
                 timestamp_field=SA_ES_NGINX_ACCESS_TIMESTAMP_FIELD_NAME,
                 index_time_format=SA_ES_NGINX_ACCESS_INDEX_TIME_FORMAT,
                 es_user=SA_ES_USER,
                 es_passwd=SA_ES_PASSWD):
        super(NginxAccessESQuery, self).__init__(es_hosts=es_hosts, index_prefix=index_prefix,
                                                 timestamp_field=timestamp_field,
                                                 index_time_format=index_time_format,
                                                 es_user=es_user, es_passwd=es_passwd)

    def make_body(self, time_range=None, query_string=None, term_dict=None,
                  aggregations=None, sort=None,
                  **kw):
        must_list = [{"range": time_range}]
        if term_dict:
            must_list += [{"term": {k: v}} for k, v in term_dict.items()]
        body = {
            "query": {
                "bool": {
                    "must": {
                        "query_string": query_string,
                    },
                    "filter": {
                        "bool": {
                            "must": must_list,
                            # "must_not": [],
                        }
                    }
                }
            },
            "aggs": aggregations,
            "sort": sort,
        }
        logger.debug('make_body: %s' % body)
        return body

    def query(self, lucene_query_string="*", term_dict=None, aggregations=None, sort=None,
              start=-15, duration=15, size=0):
        return super(NginxAccessESQuery, self).query(lucene_query_string=lucene_query_string,
                                                     term_dict=term_dict,
                                                     aggregations=aggregations, sort=sort,
                                                     start=start, duration=duration, size=size)


class AggregationsUtils(object):
    @staticmethod
    def by(x, y=None, y_script=None, size=20):
        """ x by y. e.g. by(bandwidth, 'remote_addr') """
        aggs_name = 'my_aggs'
        if not y and not y_script:
            return {aggs_name: x} if x != '_count' else {}
        order_dir = 'desc'
        x_name = str(x) if isinstance(x, str) else 'sub_aggs'
        order_name = x_name
        if isinstance(x, dict) and 'percentiles' in x:
            order_name = '%s.%s' % (x_name, x['percentiles']['percents'][0])
        if isinstance(y, str):
            aggs = dict(terms=dict(field=y,
                                   size=size,
                                   order={order_name: order_dir}))
        elif y_script:
            aggs = dict(terms=dict(script=y_script,
                                   size=size,
                                   order={order_name: order_dir}))
        else:  # dictify
            aggs = y
        if x != '_count':
            aggs['aggs'] = {x_name: x}
        return {aggs_name: aggs}

    # x
    class X(object):
        @staticmethod
        def _parse(*a):
            if a[0] in builtin_x:
                x = getattr(A.X, a[0])
                # Get the function out of unbound method.
                # In Python 3, unbound methods don't exist, so this function
                # just returns the function object unchanged.
                return six.get_unbound_function(x)(*[A.Y._alias_field(f) for f in a[1:]]) if callable(x) else x
            else:
                return six.get_unbound_function(A.X._)(*a)

        _ = lambda agg_func, field: {agg_func: dict(field=field)}  # NOQA
        qps = count = '_count'
        bandwidth = _('sum', 'bytes_sent')
        sum_response_time = _('sum', 'upstream_response_time')
        avg_response_time = _('avg', 'upstream_response_time')
        percentiles = lambda field_name, percents: {'percentiles': dict(field=field_name, percents=percents)}  # NOQA
        mean_response_time = percentiles('upstream_response_time', [50])
        unique_count = lambda field: {'cardinality': dict(field=field)}  # NOQA
        unique_ip_count = unique_count('remote_addr')
        unique_bid_count = unique_count('browser_id')

    # y
    class Y(object):
        @staticmethod
        def _parse(*a):
            if a[0] in builtin_y:
                y = getattr(A.Y, a[0])
                return six.get_unbound_function(y)(*a[1:]) if callable(y) else y
            else:
                return a[0]

        @staticmethod
        def _alias_field(alias):
            if alias in builtin_y and isinstance(getattr(A.Y, alias), str):
                return getattr(A.Y, alias)
            return alias

        ip = 'remote_addr'
        ua = 'http_user_agent'
        uid = 'user_id'
        bid = 'browser_id'
        nurl = 'normalize_url'
        dt = date_histogram = lambda interval: \
            {'date_histogram': dict(field=SA_ES_NGINX_ACCESS_TIMESTAMP_FIELD_NAME,
                                    interval=interval, time_zone="Asia/Shanghai")}
        date_histogram_1s = date_histogram('1s')


A = AggregationsUtils
builtin_x = props(A.X)
builtin_y = props(A.Y)


def _query(args, es, start, doc_number=None):
    if args.term:
        term_dict = {A.Y._alias_field(args.term[i << 1]): args.term[i << 1 | 1]
                     for i in range(len(args.term) >> 1)}
    else:
        term_dict = None

    if args.agg_x:
        aggs_params = {'x': A.X._parse(*args.agg_x), 'size': args.agg_number}
        if args.agg_y:
            aggs_params['y'] = A.Y._parse(*args.agg_y)
        elif args.agg_multi_y:
            aggs_params['y_script'] = " + ' ' + ".join("doc['%s'].value" % A.Y._alias_field(field)
                                                       for field in args.agg_multi_y)
        elif args.agg_script_y:
            aggs_params['y_script'] = args.agg_script_y
        aggs = A.by(**aggs_params)
        doc_number = 0 if doc_number is None else doc_number
        sort = None
    else:
        aggs = None
        doc_number = N_DOC_DEFAULT if doc_number is None else doc_number
        sort = [{SA_ES_NGINX_ACCESS_TIMESTAMP_FIELD_NAME: {'order': "desc",
                                                           'unmapped_type': "boolean"}}]

    res = es.query(term_dict=term_dict,
                   aggregations=aggs,
                   # aggregations=A.by(A.X.bandwidth, A.Y.ip),
                   # aggregations=A.by(A.X.unique_bid_count, A.Y.ip, size=args.agg_number),
                   # aggregations=A.by(A.X.unique_bid_count),
                   # aggregations=A.by(A.X.qps, A.Y.date_histogram_1s),
                   sort=sort,
                   start=start,
                   duration=args.duration,
                   size=doc_number,
                   lucene_query_string=args.query_string)

    return res


def parse_es_result(args, res):
    def as_string(s):
        if SA_ES_VERSION < (3, 0, 0):
            # the following code is for old elasticsearch, to translate ip format
            if args.agg_multi_y:
                remote_addr_indexes = {i for i, field in enumerate(args.agg_multi_y)
                                       if A.Y._alias_field(field) == 'remote_addr'}
                sep = ' '
                parts = s.split(sep)
                s = sep.join(i2ip(p) if i in remote_addr_indexes else p for i, p in enumerate(parts))
        return s

    ret = {}
    if 'hits' in res.get('hits', {}):
        ret['docs'] = [doc.get('_source', {}).get(SA_ES_NGINX_ACCESS_LOG_FIELD_NAME) for doc in res['hits']['hits']]
    if 'aggregations' in res:
        my_aggs = res['aggregations'].get('my_aggs', {})
        buckets = my_aggs.get('buckets', [])
        if buckets:
            possible_x_names = [k for k, v in buckets[0].items()
                                if isinstance(v, dict) and 'value' in v]
            x_name = possible_x_names[0] if possible_x_names else 'doc_count'
            ret['aggs'] = [(as_string(b.get('key_as_string') or b.get('key')),
                            b['doc_count'] if x_name == 'doc_count'
                            else b.get(x_name).get('value'))
                           for b in buckets]
        elif 'value' in my_aggs:
            ret['aggs'] = [('', my_aggs['value'])]

    return ret


@require_user
def query(args):
    es = NginxAccessESQuery()

    res = _query(args, es, args.start, doc_number=args.number)

    if args.raw:
        pprint(res.pop(u'aggregations', None))
        pprint(res)
    else:
        ret = parse_es_result(args, res)
        if 'docs' in ret and ret['docs']:
            print('>>', 'docs')
            for i in ret['docs']:
                print(i)
        if 'aggs' in ret:
            print('>>', 'aggs')
            for k, v in ret['aggs']:
                if args.min_value is None or float(v) >= float(args.min_value):
                    print(k, v)


@require_user
def analyze(args):
    es = NginxAccessESQuery()
    res = (_query(args, es, args.start_normal), _query(args, es, args.start_abnormal))
    if args.raw:
        pprint(res)
        return 0

    ret = [parse_es_result(args, r).get('aggs', {}) for r in res]
    dicts = [dict(rt) for rt in ret]

    for k, v in ret[1]:
        if k in dicts[0]:
            print(k, 'before', dicts[0][k], 'now', v)
        else:
            print(k, v, 'new')
    for k, v in ret[0]:
        if k not in dicts[1]:
            print(k, v, 'disappear')


@require_user
def explain(args):
    es = NginxAccessESQuery()
    res = es.get_mapping(fields=args.field)
    pprint(res)


def main():
    """
    e.g.

    ## query

    ### normal query
    $ sa-access query --term ip 1.1.1.1
    $ sa-access query -q 2.2.2.2 --term appname app1 -n 20
    $ sa-access query --term appname app1 remote_addr 2.2.2.2 -n 10
    $ sa-access query -q 'remote_addr:[1.1.1.0 TO 1.1.1.254]' -n10
    $ sa-access query -q 'remote_addr:"1.1.1.0/24"' -n10

    ### aggs query
    $ sa-access query -x bandwidth
    $ sa-access query -x sum bytes_sent
    $ sa-access query -t host movie.example.com -x bandwidth --by dt 30s
    $ sa-access query -t host movie.example.com -x max bytes_sent --by dt 30s
    $ sa-access query -q 'Baiduspider' -t host movie.example.com -x bandwidth --by nurl
    $ sa-access query -t host movie.example.com -x bandwidth --by ip
    $ sa-access query -x count --by ip
    $ sa-access query -x unique_count browser_id --by ip

    #### by multi field or script
    $ sa-access query --term appname app1 -x count --by-multi remote_addr normalize_url
    $ sa-access query --term appname app1 -x count \
            --by-script "doc['remote_addr'].value + ' ' + doc['normalize_url'].value"
    ##### by ip and nurl
    $ sa-access query --term appname app1 -x count \
            --by-script "def ip=doc['remote_addr'].value; \
            ip + ' ' + doc['normalize_url'].value"
    ###### If you use old version elasticsearch, you will get ip in long integer, then you can do the following:
    $ sa-access query --term appname app1 -x count \
            --by-script "def ip=doc['remote_addr'].value;(ip >>24) \
            + '.' + ((ip >> 16) % 256) + '.' + ((ip >> 8) % 256) \
            + '.' + (ip % 256) + ' ' + doc['normalize_url'].value"
    ##### by ip section and nurl
    $ sa-access query --term appname app1 -x count \
            --by-script "def ip=doc['remote_addr'].value; \
            ip.substring(0, ip.lastIndexOf('.')) + ' ' + doc['normalize_url'].value"

    ## analyze

    ### qps is abnormal, we try to find which (ip, nurl) pair contribute to it.
    $ sa-access analyze --term appname app1 -x count --by-multi remote_addr nurl

    $ sa-access analyze --term appname app1 -x bandwidth --by-multi nurl

    $ sa-access analyze --term host music.example.com -x count --by nurl \
            -a '2017-03-28 09:30' -d 15 -b '2017-03-28 10:30'

    ## explain

    $ sa-access explain
    $ sa-access explain -f remote_addr upstream_response_time

    """
    parser = argparse.ArgumentParser(epilog=main.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose.')

    # compatible with py2 & 3
    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    explain_parser = subparsers.add_parser('explain', help='show the explanation of fields')
    explain_parser.add_argument('-f', '--field', nargs='*', help='es doc field')
    explain_parser.set_defaults(func=explain)

    # TODO: support more time format

    # sub command, diff tops
    analyze_parser = subparsers.add_parser('analyze', help='analyze access log to find '
                                                           'abnormal IP, UA, UID, NURL, etc.')
    analyze_parser.add_argument('-r', '--raw', action='store_true',
                                help='Whether to use raw json output.')
    analyze_parser.add_argument('-q', '--query-string', help='Lucene query string.')
    analyze_parser.add_argument('-t', '--term', nargs='*',
                                metavar='<term name> <term value>',
                                help='term query.')
    # time
    analyze_parser.add_argument('-a', '--start-normal', type=timeformat, default=timeformat(-30),
                                help='start time of the normal period(default: %(default)s '
                                     'means %(default)s mins before, or specify datetime string).')
    analyze_parser.add_argument('-b', '--start-abnormal', type=timeformat, default=timeformat(-15),
                                help='start time of the abnormal period(default: %(default)s '
                                     'means %(default)s mins before, or specify datetime string).')
    analyze_parser.add_argument('-d', '--duration', type=int, default=15,
                                help='time duration(default: %(default)s '
                                     'means a duration of %(default)s mins).')
    # aggs
    analyze_parser.add_argument('-N', '--agg-number', type=int, default=20,
                                help='size of agg y(default: %(default)s).')
    analyze_parser.add_argument('-x', '--agg-x', nargs='*', required=True,
                                help='x of the aggregation(built-in: %s, '
                                     'or custom: `<agg_func> <field>`).' % builtin_x)
    analyze_parser.add_argument('-y', '--agg-y', '--by', nargs='*',
                                help='y of the aggregation(built-in: %s, '
                                     'or custom: `<field>`).' % builtin_y)
    analyze_parser.add_argument('-m', '--agg-multi-y', '--by-multi', nargs='*',
                                help='y of the aggregation, multi field')
    analyze_parser.add_argument('-S', '--agg-script-y', '--by-script',
                                help='y of the aggregation, script')
    analyze_parser.set_defaults(func=analyze)

    query_parser = subparsers.add_parser('query', help='query nginx access')
    query_parser.add_argument('-r', '--raw', action='store_true',
                              help='Whether to use raw json output.')
    query_parser.add_argument('-q', '--query-string', help='Lucene query string.')
    query_parser.add_argument('-s', '--start', type=timeformat, default=timeformat(-15),
                              help='start time(default: %(default)s '
                                   'means %(default)s mins before, or specify datetime string).')
    query_parser.add_argument('-d', '--duration', type=int, default=15,
                              help='time duration(default: %(default)s '
                                   'means a duration of %(default)s mins).')
    query_parser.add_argument('-n', '--number', type=int,
                              help='number of documents(default: 0 for aggs query, '
                                   '{doc_query_default} for only-docs query).'
                                   .format(doc_query_default=N_DOC_DEFAULT))
    query_parser.add_argument('-t', '--term', nargs='*',
                              metavar='<term name> <term value>',
                              help='term query.')
    # aggs
    query_parser.add_argument('-N', '--agg-number', type=int, default=20,
                              help='size of agg y(default: %(default)s).')
    query_parser.add_argument('-x', '--agg-x', nargs='*',
                              help='x of the aggregation(built-in: %s, '
                                   'or custom: `<agg_func> <field>`).' % builtin_x)
    query_parser.add_argument('-y', '--agg-y', '--by', nargs='*',
                              help='y of the aggregation(built-in: %s, '
                                   'or custom: `<field>`).' % builtin_y)
    query_parser.add_argument('-m', '--agg-multi-y', '--by-multi', nargs='*',
                              help='y of the aggregation, multi field')
    query_parser.add_argument('-S', '--agg-script-y', '--by-script',
                              help='y of the aggregation, script')
    query_parser.add_argument('--min-value', '--min',
                              help='filter result entires with the min value')
    query_parser.set_defaults(func=query)

    args = parser.parse_args()
    args.user = args.user or get_os_username()

    if args.func == query:
        if args.term and len(args.term) % 2:
            parser.error('-t/--term should accept name/value pairs.')
        if not args.agg_x and (args.agg_y or args.agg_multi_y or args.agg_script_y):
            parser.error('-x/--agg-x should be provided.')
        if args.start is None:
            parser.error('-s/--start invalid, must be negative integer, or datetime string')

    if args.func == analyze:
        if args.term and len(args.term) % 2:
            parser.error('-t/--term should accept name/value pairs.')
        if not args.agg_y and not args.agg_multi_y and not args.agg_script_y:
            parser.error('aggs y should be provided.')
        if args.start_abnormal is None or args.start_normal is None:
            parser.error('-a, -b invalid, must be negative integer, or datetime string')

    levels = [level for v, level in VERBOSE_LEVEL if args.verbose >= v]
    level = min(levels)
    logging.getLogger("requests").setLevel(level)
    logging.getLogger("elasticsearch").setLevel(level)
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    sys.exit(args.func(args))
