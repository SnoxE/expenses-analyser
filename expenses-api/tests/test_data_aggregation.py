import pytest
import requests

from http_client import post_aggregate

CSV_PATH = "test_expenses.csv"


def test_total_for_department():
    # when
    result = post_aggregate(department="Sales", csv_path=CSV_PATH)

    # then
    assert result.status_code == requests.codes.ok
    body = result.json()
    assert body["total"] == "$36.00"


@pytest.mark.parametrize(
    ("department", "year", "expected_total"),
    [("Sales", 2020, "$12.00"), ("Sales", 2021, "$24.00")],
)
def test_total_for_department_and_year(department: str, year: int, expected_total: str):
    # when
    result = post_aggregate(department=department, year=year, csv_path=CSV_PATH)

    # then
    assert result.status_code == requests.codes.ok
    body = result.json()
    assert body["total"] == expected_total
