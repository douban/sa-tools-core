# coding: utf-8

from __future__ import print_function

import time
from datetime import datetime

from elasticsearch import Elasticsearch, __version__ as es_client_version


class ESQuery(object):
    def __init__(self, es_hosts, index_prefix, timestamp_field, index_time_format='%Y.%m.%d', es_user='', es_passwd=''):
        self.client = Elasticsearch(hosts=es_hosts, http_auth=(es_user, es_passwd)) if es_user and es_passwd else Elasticsearch(hosts=es_hosts)
        self.index_prefix = index_prefix
        self.timestamp_field = timestamp_field
        self.index_time_format = index_time_format

    def get_mapping(self, fields=None):
        """Retrieve mapping definition of index or specific field.
        http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-mapping.html"""
        indexes = self.compute_indexes(*self.compute_start_end_timestamp(0, 0))
        if fields:
            res = self.client.indices.get_field_mapping(index=indexes,
                                                        fields=fields)
        else:
            res = self.client.indices.get_mapping(index=indexes)
        return res

    def compute_start_end_timestamp(self, start, duration):
        if isinstance(start, int):
            now_timestamp = int(time.time())
            start_timestamp = now_timestamp + start * 60
        else:
            start_timestamp = int(time.mktime(start.timetuple()))
        end_timestamp = start_timestamp + duration * 60
        return start_timestamp, end_timestamp

    def compute_time_range(self, start_timestamp, end_timestamp):
        time_range = {self.timestamp_field: {'gte': start_timestamp,
                                             'lte': end_timestamp,
                                             'format': "epoch_second"}}
        return time_range

    def compute_indexes(self, start_timestamp, end_timestamp):
        start_utc_datetime = datetime.utcfromtimestamp(start_timestamp)
        end_utc_datetime = datetime.utcfromtimestamp(end_timestamp)
        ordinal_range = range(start_utc_datetime.toordinal(), end_utc_datetime.toordinal() + 1)
        indexes = ','.join('%s%s' % (self.index_prefix,
                                     datetime.fromordinal(i).strftime(self.index_time_format))
                           for i in ordinal_range)
        return indexes

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
        return body

    @staticmethod
    def _filter_None(obj):
        if obj is None or isinstance(obj, (int, str)):
            return obj
        if isinstance(obj, list):
            return [ESQuery._filter_None(i) for i in obj if ESQuery._filter_None(i)]
        return {k: ESQuery._filter_None(v) for k, v in obj.items() if ESQuery._filter_None(v)}

    def query(self, lucene_query_string="*", term_dict=None, aggregations=None, sort=None,
              start=-15, duration=15, size=0):
        start_timestamp, end_timestamp = self.compute_start_end_timestamp(start, duration)
        time_range = self.compute_time_range(start_timestamp, end_timestamp)
        indexes = self.compute_indexes(start_timestamp, end_timestamp)

        if lucene_query_string and lucene_query_string != '*':
            query_string = dict(query=lucene_query_string,
                                analyze_wildcard=True)
        else:
            query_string = None

        body = self.make_body(time_range=time_range, query_string=query_string,
                              term_dict=term_dict,
                              aggregations=aggregations, sort=sort)
        body = ESQuery._filter_None(body)

        params = dict(index=indexes,
                      size=size,
                      body=body)

        res = self.client.search(**params)
        return res


if __name__ == '__main__':
    body = {
        "query": {
            "bool": {
                "must": {
                    "query_string": 'test',
                },
                "filter": {
                    "bool": {
                        "must": [
                            {"range": 'yes'},
                            {"term": None},
                        ],
                        "must_not": [],
                    }
                }
            }
        },
        "aggs": None,
    }
    print(ESQuery._filter_None(body))
