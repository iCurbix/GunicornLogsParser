import os.path
import sys
from datetime import datetime
from typing import List, Any, Dict, Callable

from guniparse.parser import OrderEnum

DATETIME_FORMATS = ["%d/%m/%Y:%H:%M:%S%z", "%d/%m/%Y:%H:%M:%S"]
HELP_MSG = """
usage: guniparse [--help] [--from FROM] [--to TO] [--order ORDER]

  --help        prints this message
  --from FROM   from when should logs be parsed (format 12.07.2021:22:40:13+0100 or 12.07.2021:21:40:13)
  --to TO       to when should logs be parsed (format 12.07.2021:22:40:13+0100 or 12.07.2021:21:40:13)
  --order ORDER specify if newest logs are at the beginning of the file (descending) or at the end (ascending)
                can be one of ["ascending", "descending"], default: "descending"
"""


class Cli:
    # real quick and dirty

    def __init__(self):
        self.args = ["--from", "--to", "--order", "help", "--help"]
        self.needs_value = ["--from", "--to", "--order"]
        self.option2func: Dict[str, Callable] = {
            "--from": self.to_from,
            "--to": self.to_from,
            "--order": self.order,
            "help": self.help,
            "--help": self.help,
        }
        self.option2names = {
            "--from": "_from",
            "--to": "to",
            "--order": "order",
        }

    def parse(self, argv: List[str]) -> Dict[str, Any]:
        i = 1
        if len(argv) < 2:
            self.help()
        kwargs = {}
        while i < len(argv):
            option = argv[i]
            if option not in self.args:
                if i == len(argv) - 1:
                    break
                sys.exit("Option not recognized. Try `guniparse help`")
            val = None
            if argv[i] in self.needs_value:
                if len(argv) <= i + 2:
                    sys.exit("You forgot to add value to option or path to a log file")
                i += 1
                val = argv[i]
            val = self.option2func[option](val)
            kwargs[self.option2names[option]] = val
            i += 1

        kwargs["path"] = self.path(argv[-1])
        return kwargs

    @staticmethod
    def to_from(arg: str) -> datetime:
        for dt_format in DATETIME_FORMATS:
            try:
                return datetime.strptime(arg, dt_format)
            except ValueError:
                continue
        sys.exit("Invalid date")

    @staticmethod
    def order(arg: str) -> OrderEnum:
        try:
            return OrderEnum(arg)
        except ValueError:
            sys.exit("Invalid order. Should be either 'ascending' or 'descending'")

    @staticmethod
    def path(arg: str) -> str:
        if os.path.isfile(arg):
            return arg
        sys.exit("Invalid path to a log file")

    @staticmethod
    def help(_: None = None) -> None:
        print(HELP_MSG)
        sys.exit()
