from typing import Any

import pytest

from guniparse.log_entry import RawLogEntry, LogEntry
from tests.constants import RAW_LOG_ENTRY, LOG_ENTRY, LOG_ENTRY2
from tests.helpers import Paramizer, ParamizerItem

PARAMIZER = Paramizer(
    ParamizerItem(
        "default log format",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        expected=r'^(?P<prefix>.*) (?P<log>(?P<h>.*) (?P<l>.*) (?P<u>.*) \[(?P<t>.*)\] "(?P<r>.*)" (?P<s>.*) (?P<b>.*) "(?P<f>.*)" "(?P<a>.*)" (?P<D>.*))$',
    ),
    ParamizerItem(
        "rearranged log format",
        log_format="""%(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s %(h)s %(l)s %(u)s""",
        expected=r'^(?P<prefix>.*) (?P<log>\[(?P<t>.*)\] "(?P<r>.*)" (?P<s>.*) (?P<b>.*) "(?P<f>.*)" "(?P<a>.*)" (?P<D>.*) (?P<h>.*) (?P<l>.*) (?P<u>.*))$',
    ),
    ParamizerItem(
        "format with headers and environmental variable",
        log_format="""%(h)s %({x-header-in}i)s %({x-header-out}o)s %({VARIABLE}e)s""",
        expected=r'^(?P<prefix>.*) (?P<log>(?P<h>.*) (?P<x_header_ini>.*) (?P<x_header_outo>.*) (?P<VARIABLEe>.*))$',
    ),
    ParamizerItem(
        "some things in between",
        log_format="""%(h)s ASDF %(l)s 1234 %(u)s "ASDF" %(t)s [ASDF] "%(r)s" %(s)s""",
        expected=r'^(?P<prefix>.*) (?P<log>(?P<h>.*) ASDF (?P<l>.*) 1234 (?P<u>.*) "ASDF" \[(?P<t>.*)\] [ASDF] "(?P<r>.*)" (?P<s>.*))$',
    ),
)


@PARAMIZER.paramize("log_format, expected")
def test_positive_line_exp(log_line_parser, log_format: str, expected: str) -> None:
    parser = log_line_parser(log_format)
    assert parser.line_exp.pattern == expected


PARAMIZER = Paramizer(
    ParamizerItem(
        "default log format",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680
""",
        expected=RAW_LOG_ENTRY,
    ),
    ParamizerItem(
        "rearranged log format",
        log_format="""%(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s %(h)s %(l)s %(u)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680 172.16.3.14 - -
""",
        expected=RAW_LOG_ENTRY,
    ),
)


@PARAMIZER.paramize("log_format, line, expected")
def test_positive_raw_parse_line(log_line_parser, log_format: str, line: str, expected: RawLogEntry) -> None:
    parser = log_line_parser(log_format)
    parsed = parser._raw_parse_line(line)
    assert parsed == expected


PARAMIZER = Paramizer(
    ParamizerItem(
        "missing required field in RawLogEntry",
        log_format="""%(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680
""",
        exception=TypeError,
    ),
)


@PARAMIZER.paramize("log_format, line, exception")
def test_negative_raw_parse_line(log_line_parser, log_format: str, line: str, exception: Any) -> None:
    parser = log_line_parser(log_format)
    with pytest.raises(exception):
        parser._raw_parse_line(line)


PARAMIZER = Paramizer(
    ParamizerItem(
        "default log format",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680
""",
        expected=LOG_ENTRY,
    ),
    ParamizerItem(
        "rearranged log format",
        log_format="""%(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s %(h)s %(l)s %(u)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680 172.16.3.14 - -
""",
        expected=LOG_ENTRY,
    ),
    ParamizerItem(
        "'-' as response length",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 - "-" "python-requests/2.22.0" 72680
""",
        expected=LOG_ENTRY2,
    ),
)


@PARAMIZER.paramize("log_format, line, expected")
def test_positive_parse_line(log_line_parser, log_format: str, line: str, expected: LogEntry) -> None:
    parser = log_line_parser(log_format)
    parsed = parser.parse_line(line)
    assert parsed == expected


PARAMIZER = Paramizer(
    ParamizerItem(
        "bad datetime format",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01-Dec-2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 72680
""",
        exception=ValueError,
    ),
    ParamizerItem(
        "status not int",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" bad_status_code 720 "-" "python-requests/2.22.0" 72680
""",
        exception=ValueError,
    ),
    ParamizerItem(
        "response length not Optional[int]",
        log_format="""%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s""",
        line="""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/5fdbb021-eebd-4156-a8a7-132289cef8a4/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" bad_resp_len
""",
        exception=ValueError,
    ),
)


@PARAMIZER.paramize("log_format, line, exception")
def test_negative_parse_line(log_line_parser, log_format: str, line: str, exception: Any) -> None:
    parser = log_line_parser(log_format)
    with pytest.raises(exception):
        parser.parse_line(line)
