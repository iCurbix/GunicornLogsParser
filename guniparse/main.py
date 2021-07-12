import signal
import sys
from datetime import datetime
from types import FrameType
from typing import Optional

from guniparse.cli import Cli
from guniparse.parser import LogParser, OrderEnum


def main():
    def signal_handler(sig: int, frame: FrameType) -> None:
        sys.exit("Cancelled")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        cli = Cli()
        kwargs = cli.parse(sys.argv)
        guniparse_start(**kwargs)
    except Exception:
        sys.exit("Something went wrong. Check your options and if log file is of valid format")
    except SystemExit as e:
        print(e)


def guniparse_start(
        path: str,
        _from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        order: OrderEnum = OrderEnum.desc
) -> None:
    parser = LogParser()
    stats = parser.stats(path, _from, to, order)
    stats.print()


if __name__ == "__main__":
    main()
