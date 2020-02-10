# Python assignment BNP



## Assignment
```
The purpose of this exercise is to Accept or Reject trades **grouped by CorrelationID based** on a limit.

**Assumptions and edge cases:**

-   Groups that contain only 1 trade are to be expected (e.g. CorrelationID 222). This will be a simple case of an inline comparison and output.
-   Incomplete Groups need to be outputted as Pending (e.g. CorrelationID 200 where the second trade never arrived).
-   ID fields are strings, all other fields are integers (positive and negative).
-   Memory consumption and Big O notation are important. Your solution will be profiled withy several input files.
```

I have also assumed that:
-	duplicate tradeId's should be skipped
-	finding a higher number of trades than expected should cause the group to be rejected

## Solution
Developed in Python3.8.1


## Installing
 create a venv
```
Christophers-MacBook-Pro:rabo christopherbrown$ python3 -m venv bnp
```
change to the bnp directory, unzip the files and activate venv
```
Christophers-MacBook-Pro-2:testing-bnp christopherbrown$ cd bnp
Christophers-MacBook-Pro-2:bnp christopherbrown$ unzip ~/Documents/bnp-submission/bnp.zip

Archive:  /Users/christopherbrown/Documents/bnp-submission/bnp.zip
creating: src/
inflating: src/requirements.txt
creating: src/test/
extracting: src/test/__init__.py
inflating: src/test/test_01_unit.py
inflating: src/README.md
inflating: src/bnp-test.py
inflating: src/input.xml
creating: __MACOSX/
creating: __MACOSX/src/
inflating: __MACOSX/src/._input.xml
Christophers-MacBook-Pro-2:bnp christopherbrown$

Christophers-MacBook-Pro-2:bnp christopherbrown$ source bin/activate
(bnp) Christophers-MacBook-Pro-2:bnp christopherbrown$
```

pip install
```
(bnp) Christophers-MacBook-Pro-2:bnp christopherbrown$ cd src/
(bnp) Christophers-MacBook-Pro-2:bnp christopherbrown$ pip install -r requirements.txt
Collecting attrs==19.3.0 (from -r requirements.txt (line 1))
Using cached https://files.pythonhosted.org/packages/a2/db/4313ab3be961f7a763066401fb77f7748373b6094076ae2bda2806988af6/attrs-19.3.0-py2.py3-none-any.whl
... snip ...
```

## Demo
run against provided input file
```
(bnp) Christophers-MacBook-Pro-2:bnp christopherbrown$ python bnp-test.py input.xml
2020-02-09 22:12:16,071 - __main__ - INFO - * starting - inputfile: input.xml
2020-02-09 22:12:16,071 - __main__ - INFO - writing output file: results.csv
2020-02-09 22:12:16,072 - __main__ - INFO - * exiting - error=0
```

check results
```
(bnp) Christophers-MacBook-Pro-2:bnp christopherbrown$ cat results.csv
200, 2, Pending
222, 1, Rejected
234, 3, Accepted
```

## Tests
```
bnp2) Christophers-MacBook-Pro-2:src christopherbrown$ pytest -v
=========================================================================== test session starts ===========================================================================
platform darwin -- Python 3.8.1, pytest-5.3.5, py-1.8.1, pluggy-0.13.1 -- /Users/christopherbrown/Documents/bnp2/bin/python3
cachedir: .pytest_cache
rootdir: /Users/christopherbrown/Documents/bnp2/src
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
(bnp2) Christophers-MacBook-Pro-2:src christopherbrown$ 
```