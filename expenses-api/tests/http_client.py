import requests
import logging

logging.basicConfig(level=logging.INFO)


def post_aggregate(department, year=None, period=None, csv_path="test_expenses.csv"):
    base_url = "http://localhost:8000/api/aggregate"

    params = {"department": department}
    if year:
        params["year"] = year
    if period:
        params["period"] = period

    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_data = file.read()
    except FileNotFoundError:
        logging.error(f"CSV file not found at path: {csv_path}")
        return
    except Exception as e:
        logging.error(f"Unexpected error while reading CSV: {e}")
        return

    try:
        return requests.post(
            url=base_url,
            params=params,
            data=csv_data,
            headers={"Content-Type": "text/plain"},
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        print("Error:", e)
