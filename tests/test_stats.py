from collections import Counter
from typing import List

from guniparse.log_entry import LogEntry
from guniparse.stats import Stats
from tests.constants import LOG_ENTRY, LOG_ENTRY2
from tests.helpers import Paramizer, ParamizerItem

PARAMIZER = Paramizer(
    ParamizerItem(
        "no logs",
        logs=[],
        requests=0,
        reqs_per_sec=0,
        statuses_counts=Counter(),
        avg_resp_size=0,
    ),
    ParamizerItem(
        "one log",
        logs=[LOG_ENTRY],
        requests=1,
        reqs_per_sec=1,
        statuses_counts=Counter({200: 1}),
        avg_resp_size=720,
    ),
    ParamizerItem(
        "one different log",
        logs=[LOG_ENTRY2],
        requests=1,
        reqs_per_sec=1,
        statuses_counts=Counter({200: 1}),
        avg_resp_size=0,
    ),
    ParamizerItem(
        "two logs with different resp size",
        logs=[LOG_ENTRY, LOG_ENTRY2],
        requests=2,
        reqs_per_sec=2,
        statuses_counts=Counter({200: 2}),
        avg_resp_size=360,
    ),
)


@PARAMIZER.paramize("logs, requests, reqs_per_sec, statuses_counts, avg_resp_size")
def test_positive_stats(
        logs: List[LogEntry], requests: int, reqs_per_sec: float, statuses_counts: Counter, avg_resp_size: float
):
    stats = Stats()
    for log in logs:
        stats.update(log)
    stats.end()
    assert stats.requests == requests
    assert stats.reqs_per_sec == reqs_per_sec
    assert stats.statuses_counts == statuses_counts
    assert stats.avg_resp_size == avg_resp_size
