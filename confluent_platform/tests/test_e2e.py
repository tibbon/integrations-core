# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest
from six import iteritems

from datadog_checks.base.stubs.aggregator import AggregatorStub
from .metrics import build_metrics

# https://docs.confluent.io/current/kafka/monitoring.html#broker-metrics

BROKER_METRICS = [
    'kafka.server.replica_manager.under_min_isr_partition_count',
]

ALL_METRICS = BROKER_METRICS


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance, rate=True)  # type: AggregatorStub

    # Mark jvm. metrics as asserted
    for metric_name in aggregator._metrics:
        if metric_name.startswith('jvm.'):
            aggregator.assert_metric(metric_name)

    for metric in build_metrics(checked_only=True):
        metric_name = metric['metric_name']
        aggregator.assert_metric(metric_name)

    # aggregator.assert_all_metrics_covered()

    # for metric_name, metrics in iteritems(aggregator._metrics):
    #     # print("{} => {}".format(metric_name, metrics))
    #     print(metric_name)
    # # for metric in ACTIVEMQ_E2E_METRICS:
    #     aggregator.assert_metric(metric)
