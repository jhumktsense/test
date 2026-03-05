import pandas as pd
from pathlib import Path

# Base directory for this script.
PROJECT_ROOT = Path(__file__).resolve().parent

# If you change the folder or file name, update these variables.
DATA_DIR = PROJECT_ROOT
EXCEL_PATH = DATA_DIR / "MarSci_Assessment_Sample_Data.xlsx"


def check_ad_platforms(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the Ad Platforms sheet.
    """
    print("=== Ad Platforms ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Check for duplicates at the (Date, Platform) level.
    dup_mask = df.duplicated(subset=["Date", "Platform"])
    print("Any duplicated (Date, Platform) rows?:", bool(dup_mask.any()))
    print()

    # Check date coverage and gaps per platform.
    platforms = df["Platform"].unique()
    for platform in platforms:
        sub = df[df["Platform"] == platform].copy()
        full_range = pd.date_range(sub["Date"].min(), sub["Date"].max(), freq="D")
        missing = set(full_range) - set(sub["Date"])
        print(
            "Platform {}: rows={}, date_min={}, date_max={}, missing_dates={}".format(
                platform,
                len(sub),
                sub["Date"].min().date(),
                sub["Date"].max().date(),
                len(missing),
            )
        )
    print()


def check_sales(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the Sales sheet.
    """
    print("=== Sales ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # One row per calendar date is expected.
    print("Unique Date count:", df["Date"].nunique())
    print("Any duplicated Date rows?:", bool(df.duplicated(subset=["Date"]).any()))

    full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    missing = set(full_range) - set(df["Date"])
    print("Date range:", df["Date"].min(), "->", df["Date"].max())
    print("Missing dates inside range:", len(missing))
    print()


def check_ga4_sessions(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the GA4 Sessions sheet.
    """
    print("=== GA4 Sessions ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Check uniqueness at the (Date, GA4_Channel) level.
    dup_mask = df.duplicated(subset=["Date", "GA4_Channel"])
    print("Any duplicated (Date, GA4_Channel) rows?:", bool(dup_mask.any()))

    print(
        "Unique (Date, GA4_Channel) pairs:",
        df[["Date", "GA4_Channel"]].drop_duplicates().shape[0],
    )
    print("Date range:", df["Date"].min(), "->", df["Date"].max())

    # How many GA4 channels do we see per day?
    channels_per_date = df.groupby("Date")["GA4_Channel"].nunique()
    print()
    print("GA4 channels per date (summary):")
    print(channels_per_date.describe())

    full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    missing = set(full_range) - set(df["Date"])
    print("Missing GA4 dates inside range:", len(missing))
    print()


def main() -> None:
    """
    Run a set of lightweight data quality checks on the three raw sheets
    before building the weekly modeling dataset.
    """
    print("Loading raw Excel from:", EXCEL_PATH)
    excel = pd.ExcelFile(EXCEL_PATH)

    ad = excel.parse("Ad Platforms")
    sales = excel.parse("Sales")
    ga4 = excel.parse("GA4 Sessions")

    check_ad_platforms(ad)
    check_sales(sales)
    check_ga4_sessions(ga4)


if __name__ == "__main__":
    main()

import pandas as pd
from pathlib import Path

# Base directory for this script.
PROJECT_ROOT = Path(__file__).resolve().parent

# If you change the folder or file name, update these variables.
DATA_DIR = PROJECT_ROOT
EXCEL_PATH = DATA_DIR / "MarSci_Assessment_Sample_Data.xlsx"


def check_ad_platforms(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the Ad Platforms sheet.
    """
    print("=== Ad Platforms ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Check for duplicates at the (Date, Platform) level.
    dup_mask = df.duplicated(subset=["Date", "Platform"])
    print("Any duplicated (Date, Platform) rows?:", bool(dup_mask.any()))
    print()

    # Check date coverage and gaps per platform.
    platforms = df["Platform"].unique()
    for platform in platforms:
        sub = df[df["Platform"] == platform].copy()
        full_range = pd.date_range(sub["Date"].min(), sub["Date"].max(), freq="D")
        missing = set(full_range) - set(sub["Date"])
        print(
            "Platform {}: rows={}, date_min={}, date_max={}, missing_dates={}".format(
                platform,
                len(sub),
                sub["Date"].min().date(),
                sub["Date"].max().date(),
                len(missing),
            )
        )
    print()


def check_sales(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the Sales sheet.
    """
    print("=== Sales ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # One row per calendar date is expected.
    print("Unique Date count:", df["Date"].nunique())
    print("Any duplicated Date rows?:", bool(df.duplicated(subset=["Date"]).any()))

    full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    missing = set(full_range) - set(df["Date"])
    print("Date range:", df["Date"].min(), "->", df["Date"].max())
    print("Missing dates inside range:", len(missing))
    print()


def check_ga4_sessions(df: pd.DataFrame) -> None:
    """
    Basic sanity checks for the GA4 Sessions sheet.
    """
    print("=== GA4 Sessions ===")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Nulls per column:")
    print(df.isna().sum())
    print()

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Check uniqueness at the (Date, GA4_Channel) level.
    dup_mask = df.duplicated(subset=["Date", "GA4_Channel"])
    print("Any duplicated (Date, GA4_Channel) rows?:", bool(dup_mask.any()))

    print(
        "Unique (Date, GA4_Channel) pairs:",
        df[["Date", "GA4_Channel"]].drop_duplicates().shape[0],
    )
    print("Date range:", df["Date"].min(), "->", df["Date"].max())

    # How many GA4 channels do we see per day?
    channels_per_date = df.groupby("Date")["GA4_Channel"].nunique()
    print()
    print("GA4 channels per date (summary):")
    print(channels_per_date.describe())

    full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    missing = set(full_range) - set(df["Date"])
    print("Missing GA4 dates inside range:", len(missing))
    print()


def main() -> None:
    """
    Run a set of lightweight data quality checks on the three raw sheets
    before building the weekly modeling dataset.
    """
    print("Loading raw Excel from:", EXCEL_PATH)
    excel = pd.ExcelFile(EXCEL_PATH)

    ad = excel.parse("Ad Platforms")
    sales = excel.parse("Sales")
    ga4 = excel.parse("GA4 Sessions")

    check_ad_platforms(ad)
    check_sales(sales)
    check_ga4_sessions(ga4)


if __name__ == "__main__":
    main()

