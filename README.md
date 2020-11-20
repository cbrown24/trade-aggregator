# Python assignment



## Assignment
```
Tool which Accepts or Rejects trades grouped by CorrelationID based on a limit.

**Assumptions and edge cases:**

-   Groups that contain only 1 trade are to be expected (e.g. CorrelationID 222). This will be a simple case of an inline comparison and output.
-   Incomplete Groups need to be outputted as Pending (e.g. CorrelationID 200 where the second trade never arrived).
-   ID fields are strings, all other fields are integers (positive and negative).
-   Memory consumption and Big O notation are important. Your solution will be profiled withy several input files.
```

additional:
-	duplicate tradeId's are skipped
-	finding a higher number of trades than expected causes the group to be rejected

## Solution
Developed in Python3.8.1


## Installing
 create a venv
```
Christophers-MacBook-Pro:rabo christopherbrown$ python3 -m venv trade_agregator
```
change to the trade_agregator directory, unzip the files and activate venv
```
Christophers-MacBook-Pro-2:testing-trade_agregator christopherbrown$ cd trade_agregator
...git clone...

Christophers-MacBook-Pro-2:trade_agregator christopherbrown$ source bin/activate
(trade_agregator) Christophers-MacBook-Pro-2:trade_agregator christopherbrown$
```

pip install
```
(trade_agregator) Christophers-MacBook-Pro-2:trade_agregator christopherbrown$ cd src/
(trade_agregator) Christophers-MacBook-Pro-2:trade_agregator christopherbrown$ pip install -r requirements.txt
Collecting attrs==19.3.0 (from -r requirements.txt (line 1))
Using cached https://files.pythonhosted.org/packages/a2/db/4313ab3be961f7a763066401fb77f7748373b6094076ae2bda2806988af6/attrs-19.3.0-py2.py3-none-any.whl
... snip ...
```

## Demo
run against provided input file
```
(trade_agregator) Christophers-MacBook-Pro-2:trade_agregator christopherbrown$ python trade_agregator-test.py input.xml
2020-02-09 22:12:16,071 - __main__ - INFO - * starting - inputfile: input.xml
2020-02-09 22:12:16,071 - __main__ - INFO - writing output file: results.csv
2020-02-09 22:12:16,072 - __main__ - INFO - * exiting - error=0
```

check results
```
(trade_agregator) Christophers-MacBook-Pro-2:trade_agregator christopherbrown$ cat results.csv
200, 2, Pending
222, 1, Rejected
234, 3, Accepted
```

## Tests
```
trade_agregator2) Christophers-MacBook-Pro-2:src christopherbrown$ pytest -v
=========================================================================== test session starts ===========================================================================
platform darwin -- Python 3.8.1, pytest-5.3.5, py-1.8.1, pluggy-0.13.1 -- /Users/christopherbrown/Documents/trade_agregator2/bin/python3
cachedir: .pytest_cache
rootdir: /Users/christopherbrown/Documents/trade_agregator2/src
collected 8 items                                                                                                                                                         

test/test_01_unit.py::Test::test_01_iterfile PASSED                                                                                                                 [ 12%]
test/test_01_unit.py::Test::test_02_iterfile_bad_name PASSED                                                                                                        [ 25%]
test/test_01_unit.py::Test::test_03_create_trade_from_elem PASSED                                                                                                   [ 37%]
test/test_01_unit.py::Test::test_04_add_trade_to_summary PASSED                                                                                                     [ 50%]
test/test_01_unit.py::Test::test_05_aggregation PASSED                                                                                                              [ 62%]
test/test_01_unit.py::Test::test_06_duplicate PASSED                                                                                                                [ 75%]
test/test_01_unit.py::Test::test_07_too_many_trades PASSED                                                                                                          [ 87%]
test/test_01_unit.py::Test::test_08_bad_xml PASSED                                                                                                                  [100%]

============================================================================ 8 passed in 0.05s ============================================================================
(trade_agregator2) Christophers-MacBook-Pro-2:src christopherbrown$ 
```
