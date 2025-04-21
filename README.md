## Expenses Analyser
A tool that can be used to calculate the money spent or earned by a specified department.

### Script usage

To run the script, user needs to run a following command:

```cat Expenses.csv | python3 expenses.py department year month | quarter```

Where:
- `Expenses.csv` is the comma delimited file, on which the script will conduct the analysis.
- `expenses.py` is the name of the script.
- `department` is a mandatory parameter and has to be passed always.
- `year` is an optional parameter of period modification.
- `month | quarter` is a set of optional parameters that can be used interchangeably (either month or quarter can be used).

### REST API

The second part of the repository contains a REST service with an endpoint performing the same actions and taking the same parameters as its script coounterpart.
To run the service the following command needs to be run in the command line, while in `/expenses-api` directory:

```uvicorn main:app --reload```

Then the app is started on port `8000`.


