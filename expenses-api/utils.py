import pandas as pd
import re

from io import StringIO


MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def clean_amount(value):
    try:
        value = (
            str(value)
            .strip()
            .replace("$", "")
            .replace(",", "")
            .replace("(", "-")
            .replace(")", "")
        )
        return float(value)
    except Exception:
        return 0.0


def prepare_dataframe(csv_text):
    df = pd.read_csv(StringIO(csv_text), sep=";")

    df_melted = df.melt(
        id_vars=["Department", "Expense Type", "Year"],
        value_vars=list(MONTHS.keys()),
        var_name="Month",
        value_name="Amount",
    )

    df_melted["Month Number"] = df_melted["Month"].map(MONTHS)
    df_melted["Quarter"] = ((df_melted["Month Number"] - 1) // 3) + 1
    df_melted["Amount"] = df_melted["Amount"].apply(clean_amount)

    return df_melted


def filter_dataframe(
    df_melted, department, year=None, period_type=None, period_value=None
):
    df = df_melted[df_melted["Department"].str.lower() == department.lower()]

    if year:
        df = df[df["Year"] == year]

    if period_type and period_value:
        if period_type == "quarter":
            df = df[df["Quarter"] == period_value]
        elif period_type == "month":
            month_number = MONTHS[period_value]
            df = df[df["Month Number"] == month_number]

    return df


def process_expenses(
    csv_text, department, year=None, period_type=None, period_value=None
):
    df_melted = prepare_dataframe(csv_text)
    df_filtered = filter_dataframe(
        df_melted, department, year, period_type, period_value
    )

    total = df_filtered["Amount"].sum()
    formatted = "${:,.2f}".format(total)
    return formatted
