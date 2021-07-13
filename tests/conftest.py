import pytest


@pytest.fixture
def log_line_parser():
    def make_log_line_parser(log_format: str):
        from guniparse.parser import LogLineParser
        LogLineParser.LOG_FORMAT = log_format
        return LogLineParser()
    return make_log_line_parser
