from collections import Counter
from dataclasses import field, dataclass
from datetime import datetime
from typing import Optional

from guniparse.log_entry import LogEntry
from guniparse.utils import size_fmt


@dataclass
class Stats:
    requests: int = 0  # total number of requests
    reqs_per_sec: float = 0
    statuses_counts: Counter = field(default_factory=Counter)
    avg_resp_size: int = 0  # for status 2xx
    ok_resps: int = field(default=0, repr=False)
    _first_date: Optional[datetime] = field(default=None, repr=False)
    _last_date: Optional[datetime] = field(default=None, repr=False)

    def _update_first(self, log: LogEntry) -> None:
        self._update(log)
        self._first_date = log.t
        self.update = self._update

    def _update(self, log: LogEntry) -> None:
        self.requests += 1
        self.statuses_counts[log.s] += 1
        if log.s // 100 == 2:
            size = log.b if log.b else 0
            self.avg_resp_size = int((self.avg_resp_size * self.ok_resps + size) / (self.ok_resps + 1))
            self.ok_resps += 1
        self._last_date = log.t

    def end(self) -> None:
        if self._first_date and self._last_date:
            seconds = abs((self._first_date - self._last_date).total_seconds()) + 1
            self.reqs_per_sec = self.requests / seconds

    def print(self) -> None:
        print(
            f"\rrequests: {self.requests}\n"
            f"requests/sec: {self.reqs_per_sec}\n"
            f"responses: {dict(self.statuses_counts)}\n"
            f"avg size of 2xx responses: {size_fmt(self.avg_resp_size)}\n"
        )

    update = _update_first
