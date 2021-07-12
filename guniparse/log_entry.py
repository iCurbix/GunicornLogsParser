from dataclasses import dataclass, make_dataclass
from datetime import datetime
from typing import Dict, Optional


DATETIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


class _RawLogEntry:
    @classmethod
    def from_dict(cls, d: Dict) -> "_RawLogEntry":
        return cls(**{k: v for k, v in d.items() if k in cls.__annotations__})  # type: ignore


@dataclass
class LogEntry:
    # I wish I could use pydantic with its field aliases...
    h: str  # remote address
    l: str  # '-'
    u: str  # user name
    t: datetime  # date of the request
    r: str  # status line  ...I dont need to parse it so I'll just leave it as str
    s: int  # status
    b: Optional[int]  # response length or '-' (CLF format)
    f: str  # referer
    a: str  # user agent
    D: int  # request time in microseconds

    @classmethod
    def from_raw(cls, raw: _RawLogEntry) -> "LogEntry":
        fields = raw.__dict__.copy()
        for k, v in cls.__annotations__.items():
            # I wish I could use python 3.10 pattern matching ;)
            if v is int:
                fields[k] = int(fields[k])
            elif v is Optional[int]:
                try:
                    fields[k] = int(fields[k])
                except ValueError:
                    fields[k] = None
            elif v is datetime:
                fields[k] = datetime.strptime(fields[k], DATETIME_FORMAT)
        return cls(**fields)


# I just want to have strings here
RawLogEntry = make_dataclass("RawLogEntry", [(k, str) for k in LogEntry.__annotations__.keys()], bases=(_RawLogEntry,))
