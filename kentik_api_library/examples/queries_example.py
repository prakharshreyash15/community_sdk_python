# pylint: disable=redefined-outer-name
"""
Examples of using the typed Query API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI
from kentik_api.public.query_object import (
    QueryObject,
    QueryArrayItem,
    Query,
    Aggregate,
    AggregateFunctionType,
    FastDataType,
    MetricType,
    DimensionType,
)

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_query_data() -> None:
    """
    Expected response is like:

    Sending data query...

    Results:
    [subsequent result items]
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    agg1 = Aggregate(name="avg_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.average, raw=True)
    agg2 = Aggregate(name="p95th_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.percentile, rank=95)
    agg3 = Aggregate(name="max_bits_per_sec", column="f_sum_both_bytes", fn=AggregateFunctionType.max)
    query = Query(
        dimension=[DimensionType.Traffic],
        cidr=32,
        cidr6=128,
        metric=MetricType.bytes,
        topx=8,
        depth=75,
        fastData=FastDataType.auto,
        outsort="avg_bits_per_sec",
        lookback_seconds=3600,
        hostname_lookup=True,
        device_name=[],
        all_selected=True,
        filters_obj=None,
        descriptor="",
        aggregates=[agg1, agg2, agg3],
    )
    query_item = QueryArrayItem(query=query, bucket="Left +Y Axis")
    query_object = QueryObject(queries=[query_item])

    print("Sending data query...")
    result = client.query.data(query_object)

    print("Results:")
    for item in result.results:
        print(item.__dict__)


if __name__ == "__main__":
    run_query_data()