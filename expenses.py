import sys
import pandas as pd
import re


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


def extract_arguments():
    department = sys.argv[1]
    year = int(sys.argv[2]) if len(sys.argv) >= 3 else None
    period = sys.argv[3] if len(sys.argv) == 4 else None

    return department, year, period


def read_and_prepare_dataframe():
    df = pd.read_csv(sys.stdin, sep=";")

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


def filter_dataframe(df_melted, department, year, period):
    df_filtered = df_melted[df_melted["Department"].str.lower() == department.lower()]

    if year:
        df_filtered = df_filtered[df_filtered["Year"] == year]

    if period:
        if re.match(r"^[1-4]$", period):
            quarter = int(period)
            df_filtered = df_filtered[df_filtered["Quarter"] == quarter]
        elif period.capitalize() in MONTHS:
            month_number = MONTHS[period.capitalize()]
            df_filtered = df_filtered[df_filtered["Month Number"] == month_number]
        else:
            print("Invalid quarter or month format.", file=sys.stderr)
            sys.exit(1)

    return df_filtered


def process_expenses():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 expenses.py department [year] [quarter|month]",
            file=sys.stderr,
        )
        sys.exit(1)

    department, year, period = extract_arguments()
    df_melted = read_and_prepare_dataframe()
    df_filtered = filter_dataframe(df_melted, department, year, period)

    total = df_filtered["Amount"].sum()
    formatted = "${:,.2f}".format(total)
    print(formatted)


if __name__ == "__main__":
    process_expenses()
