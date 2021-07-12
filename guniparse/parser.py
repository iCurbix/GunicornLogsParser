import os
import re
from datetime import datetime, timezone
from enum import Enum
from re import Pattern
from typing import List, Tuple, Optional, Iterable

from guniparse.log_entry import RawLogEntry, LogEntry
from guniparse.stats import Stats


class LogLineParser:

    LOG_FORMAT = """%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s"""

    sub_pipeline: List[Tuple[Pattern, str]] = [
        (re.compile(r"%\(t\)s"), r"\[%(t)s\]"),  # the groups would not match as expected otherwise
    ]
    field_exp = re.compile(r"%\({?\w+}?\w?\)s")

    def __init__(self):
        self.line_exp = re.compile(self._prepare_line_exp(self.LOG_FORMAT))

    def _prepare_line_exp(self, log_format: str) -> str:
        # eventually there is only one thing in pipeline but yeah...whatever
        for e, sub in self.sub_pipeline:
            log_format = e.sub(sub, log_format)

        exp = ""
        old_end = 0
        for match in self.field_exp.finditer(log_format):
            start, end = match.span()
            exp += log_format[old_end:start]
            inside = log_format[start+2:end-2]  # get rid of %( and )s
            exp += f"(?P<{inside}>.*)"  # named groups to easily extract with .groupdict()
            old_end = end

        exp += log_format[old_end:]
        return f"^(?P<prefix>.*) (?P<log>{exp})$"  # we need to assume that there is a space separating groups

    def _raw_parse_line(self, line: str) -> RawLogEntry:
        m = self.line_exp.match(line)
        return RawLogEntry.from_dict(m.groupdict())

    def parse_line(self, line: str) -> LogEntry:
        return LogEntry.from_raw(self._raw_parse_line(line))


class OrderEnum(Enum):
    asc = "ascending"
    desc = "descending"


class LogParser:
    def __init__(self):
        self._line_parser = LogLineParser()

    @staticmethod
    def _get_next_place(curr: int, start: int, end: int, too_far: bool) -> int:
        if too_far:
            return start + (curr - start) // 2
        return curr + (end - curr) // 2

    def _open(self, path: str, since: Optional[datetime], order: OrderEnum):
        """
        Opens log file and sets descriptor at the right place
        :param path: path to the log file.
        :param since: since when the log file should be read. if no tzinfo provided then assumes utc
        :param order: order of logs in the log file. If newest logs at the top of the file then should be OrderEnum.desc
        :return: file descriptor
        """
        f = open(path, "rb")
        if not since:
            return f

        while True:
            try:
                line_place = f.tell()
                line_datetime = self._line_parser.parse_line(f.readline().decode()).t
            except:
                pass
            else:
                break

        if order == order.desc:
            if line_datetime < since:
                f.seek(line_place)
                return f
        else:
            if line_datetime >= since:
                f.seek(line_place)
                return f

        f.seek(0, os.SEEK_END)
        start = 0
        end = f.tell()
        where = end // 2
        line_place = -1
        old_line_place = 0
        while old_line_place != line_place:
            f.seek(where)
            while f.read(1) != b"\n":
                where -= 1
                # seek to -1 is not possible as first log was already checked
                f.seek(where)
            old_line_place = line_place
            line_place = f.tell()
            line_datetime = self._line_parser.parse_line(f.readline().decode()).t

            too_far = False
            if order == OrderEnum.desc and line_datetime < since:
                too_far = True
            elif order == OrderEnum.asc and line_datetime >= since:
                too_far = True

            where = self._get_next_place(line_place, start, end, too_far)
            if too_far:
                end = line_place
            else:
                start = line_place
        return f

    def _parsed_lines(
            self, path: str, _from: Optional[datetime], to: Optional[datetime], order: OrderEnum
    ) -> Iterable[LogEntry]:
        since = None
        if to:
            if not to.tzinfo:
                to = to.replace(tzinfo=timezone.utc)
            if order == OrderEnum.desc:
                since = to
        if _from:
            if not _from.tzinfo:
                _from = _from.replace(tzinfo=timezone.utc)
            if order == OrderEnum.asc:
                since = _from

        f = self._open(path, since, order)
        while line := f.readline():
            try:
                parsed = self._line_parser.parse_line(line.decode())
            except:
                continue
            if order == OrderEnum.desc and _from and parsed.t < _from:
                break
            if order == OrderEnum.asc and to and parsed.t >= to:
                break
            yield parsed
        f.close()

    def stats(
            self,
            path: str,
            _from: Optional[datetime] = None,
            to: Optional[datetime] = None,
            order: OrderEnum = OrderEnum.desc
    ) -> Stats:
        stats_obj = Stats()
        for log in self._parsed_lines(path, _from, to, order):
            if stats_obj.requests % 1000 == 0:
                print(f"\rrequests: {stats_obj.requests}", end="")
            stats_obj.update(log)
        stats_obj.end()
        return stats_obj
