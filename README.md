# GunicornLogsParser

###Example usage
```shell
cd GunicornLogsParser
python -m guniparse ./logfile.log
```
or
```shell
pip install GunicornLogsParser
guniparse ./logfile.log
```

###All available command line arguments
| Argument                | Description                             |
|:------------------------|:----------------------------------------|
| --help                  | prints help message                     |
|--from FROM              | from when should logs be parsed         |
|--to TO                  | to when should logs be parsed           |
|--order ORDER            | specify logs order (default=descending) |

###If you need more details about usage
```shell
guniparse --help
```
