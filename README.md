# GunicornLogsParser

### Example usage
```shell
cd GunicornLogsParser
python -m guniparse ./logfile.log
```
or
```shell
pip install GunicornLogsParser
guniparse ./logfile.log
```

### All available command line arguments
| Argument                | Description                             |
|:------------------------|:----------------------------------------|
| --help                  | prints help message                     |
|--from FROM              | from when should logs be parsed         |
|--to TO                  | to when should logs be parsed           |
|--order ORDER            | specify logs order (default=descending) |

### If you need more details about usage
```shell
guniparse --help
```

## Tests
Tests unfortunately are not as neatly written and do not cover as many test cases
as I would like, but I just did not really have much free time :/

Anyway...
### Running tests
To run tests write while in project root directory
```shell
python setup.py test 
```

or

first install pytest
```shell
pip install -U pytest
```
and then while being in project root directory you can run tests with
```shell
pytest
```
