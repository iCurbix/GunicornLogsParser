from datetime import datetime, timezone
from typing import Optional

from guniparse.parser import OrderEnum, LogParser
from tests.constants import PATH_DESC, PATH_ASC
from tests.helpers import Paramizer, ParamizerItem

PARAMIZER = Paramizer(
    ParamizerItem(
        "without since, descending order",
        path=PATH_DESC,
        since=None,
        order=OrderEnum.desc,
        expected=b"""some kind of header that is not actual log
""",
    ),
    ParamizerItem(
        "without since, ascending order",
        path=PATH_ASC,
        since=None,
        order=OrderEnum.asc,
        expected=b"""some kind of header that is not actual log
""",
    ),
    ParamizerItem(
        "since later than all logs, descending order",
        path=PATH_DESC,
        since=datetime(2019, 12, 1, 10, 6, 6, tzinfo=timezone.utc),
        order=OrderEnum.desc,
        expected=b"""Dec 01 11:06:05 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:06:05 +0100] "GET /internal/user/38ca8008-fb70-44f0-a356-9bb9192ba15c/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 276202
""",
    ),
    ParamizerItem(
        "since later than all logs, ascending order",
        path=PATH_ASC,
        since=datetime(2019, 12, 1, 10, 6, 6, tzinfo=timezone.utc),
        order=OrderEnum.asc,
        expected=b"",
    ),
    ParamizerItem(
        "since earlier than all logs, descending order",
        path=PATH_DESC,
        since=datetime(2019, 12, 1, 10, 5, 6, tzinfo=timezone.utc),
        order=OrderEnum.desc,
        expected=b"",
    ),
    ParamizerItem(
        "since earlier than all logs, ascending order",
        path=PATH_ASC,
        since=datetime(2019, 12, 1, 10, 5, 6, tzinfo=timezone.utc),
        order=OrderEnum.asc,
        expected=b"""Dec 01 11:05:57 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:05:57 +0100] "GET /internal/user/ccba5351-810e-46d8-845b-912032060422/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 173208
""",
    ),
    ParamizerItem(
        "date somewhere in the middle of logs, descending order",
        path=PATH_DESC,
        since=datetime(2019, 12, 1, 10, 5, 59, tzinfo=timezone.utc),
        order=OrderEnum.desc,
        expected=b"""Dec 01 11:05:58 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:05:58 +0100] "GET /internal/user/8baa2b6c-8314-4252-a217-c6f50c41b7fe/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 69221
""",
    ),
    ParamizerItem(
        "date somewhere in the middle of logs, ascending order",
        path=PATH_ASC,
        since=datetime(2019, 12, 1, 10, 5, 59, tzinfo=timezone.utc),
        order=OrderEnum.asc,
        expected=b"""Dec 01 11:05:59 app3-test-vm1 gunicorn[53253]: 172.16.3.14 - - [01/Dec/2019:11:05:59 +0100] "GET /internal/user/74230293-6301-4832-a876-6033f6df585b/agenda/2019-12-01/2019-12-02 HTTP/1.1" 200 720 "-" "python-requests/2.22.0" 246558
""",
    ),
)


@PARAMIZER.paramize("path, since, order, expected")
def test_positive_open(path: str, since: Optional[datetime], order: OrderEnum, expected: str):
    parser = LogParser()
    f = parser._open(path, since, order)
    assert f.readline() == expected
