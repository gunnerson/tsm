from django.db import models
from django.contrib.postgres.search import (
    SearchRank,
    SearchVector,
    SearchQuery,
)


def db_search(queryset, query, config, *args):
    vector = SearchVector(*args, config='english')

    if config == "A":
        query = SearchQuery(query, search_type="raw")
        qs = queryset.annotate(
            search=vector,
            rank=SearchRank(vector, query)).filter(
            search=query).order_by('-rank')

    if config == "B":
        query_terms = query.split()
        query_terms = ['{0}:*'.format(query_term)
                       for query_term in query_terms]
        tsquery = " & ".join(query_terms)
        query = SearchQuery(tsquery, search_type="raw")
        qs = queryset.annotate(
            search=vector,
            rank=SearchRank(vector, query)).filter(
            search=query).order_by('-rank')

    if config == "C":
        query_terms = query.split()
        tsquery = " & ".join(query_terms)
        tsquery += ":*"
        query = SearchQuery(tsquery, search_type="raw")
        qs = queryset.annotate(
            search=vector,
            rank=SearchRank(vector, query)).filter(
            search=query).order_by('-rank')

    return qs


class TruckSearch(models.Manager):
    def search(self, query, account):
        qs = self.get_queryset().filter(account=account)
        if query:
            qs = db_search(qs, query, 'B',
                           'fleet_number', 'vin', 'license_plate')
        return qs
