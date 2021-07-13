import copy
import os

from guniparse.log_entry import RawLogEntry, LogEntry

RAW_LOG_ENTRY = RawLogEntry(
    h="172.16.3.14",
    l="-",
    u="-",
    t="01/Dec/2019:11:06:05 +0100",
    r="GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1",
    s="200",
    b="720",
    f="-",
    a="python-requests/2.22.0",
    D="72680",
)

LOG_ENTRY = LogEntry.from_raw(RAW_LOG_ENTRY)
LOG_ENTRY2 = copy.copy(LOG_ENTRY)
LOG_ENTRY2.b = None

PATH_ASC = os.path.dirname(os.path.abspath(__file__)) + "/data/10_logs_asc.log"
PATH_DESC = os.path.dirname(os.path.abspath(__file__)) + "/data/10_logs_desc.log"
