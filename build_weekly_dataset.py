import pandas as pd
from pathlib import Path

# Base directory for this project.
# When you move this script, PROJECT_ROOT will follow the script location.
PROJECT_ROOT = Path(__file__).resolve().parent

# If you prefer a different folder structure, update these variables.
# For this assessment the CSVs and Excel live in this same folder.
DATA_DIR = PROJECT_ROOT
EXCEL_PATH = DATA_DIR / "MarSci_Assessment_Sample_Data.xlsx"
OUTPUT_CSV = DATA_DIR / "weekly_mmm_dataset.csv"


def add_week_start(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    """
    Add a 'week_start' column representing the Monday of each calendar week.

    We use this to aggregate daily data into weekly data in a consistent way
    across all three source tables.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    # Monday is weekday 0, so we subtract the weekday offset in days
    df["week_start"] = df[date_col] - pd.to_timedelta(df[date_col].dt.weekday, unit="D")
    return df


def normalize_platform_name(name: str) -> str:
    """
    Turn a platform name like 'Google Ads' into a safe, readable identifier
    like 'google_ads' that we can use in column names.
    """
    return name.strip().lower().replace(" ", "_")


def normalize_channel_name(name: str) -> str:
    """
    Turn a GA4 channel name like 'Paid Search' or 'Cross-network'
    into 'paid_search' or 'cross_network' for column naming.
    """
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def main() -> None:
    # 1. Load the three input sheets from the Excel file
    ad = pd.read_excel(EXCEL_PATH, sheet_name="Ad Platforms")
    sales = pd.read_excel(EXCEL_PATH, sheet_name="Sales")
    ga4 = pd.read_excel(EXCEL_PATH, sheet_name="GA4 Sessions")

    # 2. Ad Platforms: weekly spend and impressions by platform
    ad = add_week_start(ad, "Date")

    # Aggregate daily rows into weekly totals per platform
    ad_weekly = (
        ad.groupby(["week_start", "Platform"], as_index=False)
        .agg(
            weekly_cost=("Cost", "sum"),
            weekly_impressions=("Impressions", "sum"),
        )
    )

    # Create a clean platform identifier to use in column names
    ad_weekly["platform_clean"] = ad_weekly["Platform"].apply(normalize_platform_name)

    # Pivot to wide format: one row per week, one column per platform
    cost_pivot = ad_weekly.pivot_table(
        index="week_start",
        columns="platform_clean",
        values="weekly_cost",
        aggfunc="sum",
        fill_value=0.0,
    )

    imps_pivot = ad_weekly.pivot_table(
        index="week_start",
        columns="platform_clean",
        values="weekly_impressions",
        aggfunc="sum",
        fill_value=0.0,
    )

    # Prefix columns to make their meaning obvious
    cost_pivot.columns = [f"cost_{c}" for c in cost_pivot.columns]
    imps_pivot.columns = [f"imps_{c}" for c in imps_pivot.columns]

    ad_weekly_wide = pd.concat([cost_pivot, imps_pivot], axis=1).reset_index()

    # 3. Sales: weekly KPI (net sales)
    sales = add_week_start(sales, "Date")

    # Sum daily net sales into weekly net sales
    sales_weekly = (
        sales.groupby("week_start", as_index=False)
        .agg(net_sales=("Net_Sales", "sum"))
    )

    # 4. GA4 Sessions: weekly sessions by channel
    ga4 = add_week_start(ga4, "Date")

    # Aggregate daily sessions into weekly sessions per GA4 channel
    ga4_weekly = (
        ga4.groupby(["week_start", "GA4_Channel"], as_index=False)
        .agg(weekly_sessions=("Sessions", "sum"))
    )

    # Create a clean channel identifier for column names
    ga4_weekly["channel_clean"] = ga4_weekly["GA4_Channel"].apply(
        normalize_channel_name
    )

    # Pivot to wide format: one row per week, one column per GA4 channel
    ga4_pivot = ga4_weekly.pivot_table(
        index="week_start",
        columns="channel_clean",
        values="weekly_sessions",
        aggfunc="sum",
        fill_value=0.0,
    )

    ga4_pivot.columns = [f"sessions_{c}" for c in ga4_pivot.columns]
    ga4_weekly_wide = ga4_pivot.reset_index()

    # 5. Build the full weekly calendar over the sales date range
    # We use the sales table to define the overall time window
    min_week = sales_weekly["week_start"].min()
    max_week = sales_weekly["week_start"].max()

    # Create a continuous weekly index from min to max (Mondays only)
    all_weeks = pd.DataFrame(
        {"week_start": pd.date_range(start=min_week, end=max_week, freq="W-MON")}
    )

    # 6. Join everything into a single weekly modeling dataset
    weekly = all_weeks.merge(sales_weekly, on="week_start", how="left")
    weekly = weekly.merge(ad_weekly_wide, on="week_start", how="left")
    weekly = weekly.merge(ga4_weekly_wide, on="week_start", how="left")

    # For modeling, weeks with no spend or sessions are better treated as zeros
    # than as missing values. We keep 'week_start' as a proper datetime column.
    value_cols = [c for c in weekly.columns if c != "week_start"]
    weekly[value_cols] = weekly[value_cols].fillna(0.0)

    weekly = weekly.sort_values("week_start").reset_index(drop=True)

    # 7. Save the weekly dataset to CSV
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    weekly.to_csv(OUTPUT_CSV, index=False)

    print(f"Weekly MMM dataset saved to: {OUTPUT_CSV}")
    print("Shape:", weekly.shape)
    print("Columns:", list(weekly.columns))


if __name__ == "__main__":
    main()

import pandas as pd
from pathlib import Path

# Base directory for this project.
# When you move this script, PROJECT_ROOT will follow the script location.
PROJECT_ROOT = Path(__file__).resolve().parent

# If you prefer a different folder structure, update these variables.
# For example, you can change "marsei_assessment" to another folder name.
DATA_DIR = PROJECT_ROOT  # write your data folder here if needed
EXCEL_PATH = DATA_DIR / "MarSci_Assessment_Sample_Data.xlsx"  # write your Excel file name here
OUTPUT_CSV = DATA_DIR / "weekly_mmm_dataset.csv"


def add_week_start(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    """
    Add a 'week_start' column representing the Monday of each calendar week.

    We use this to aggregate daily data into weekly data in a consistent way
    across all three source tables.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    # Monday is weekday 0, so we subtract the weekday offset in days
    df["week_start"] = df[date_col] - pd.to_timedelta(df[date_col].dt.weekday, unit="D")
    return df


def normalize_platform_name(name: str) -> str:
    """
    Turn a platform name like 'Google Ads' into a safe, readable identifier
    like 'google_ads' that we can use in column names.
    """
    return name.strip().lower().replace(" ", "_")


def normalize_channel_name(name: str) -> str:
    """
    Turn a GA4 channel name like 'Paid Search' or 'Cross-network'
    into 'paid_search' or 'cross_network' for column naming.
    """
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def main() -> None:
    # 1. Load the three input sheets from the Excel file
    ad = pd.read_excel(EXCEL_PATH, sheet_name="Ad Platforms")
    sales = pd.read_excel(EXCEL_PATH, sheet_name="Sales")
    ga4 = pd.read_excel(EXCEL_PATH, sheet_name="GA4 Sessions")

    # 2. Ad Platforms: weekly spend and impressions by platform
    ad = add_week_start(ad, "Date")

    # Aggregate daily rows into weekly totals per platform
    ad_weekly = (
        ad.groupby(["week_start", "Platform"], as_index=False)
          .agg(
              weekly_cost=("Cost", "sum"),
              weekly_impressions=("Impressions", "sum"),
          )
    )

    # Create a clean platform identifier to use in column names
    ad_weekly["platform_clean"] = ad_weekly["Platform"].apply(normalize_platform_name)

    # Pivot to wide format: one row per week, one column per platform
    cost_pivot = ad_weekly.pivot_table(
        index="week_start",
        columns="platform_clean",
        values="weekly_cost",
        aggfunc="sum",
        fill_value=0.0,
    )

    imps_pivot = ad_weekly.pivot_table(
        index="week_start",
        columns="platform_clean",
        values="weekly_impressions",
        aggfunc="sum",
        fill_value=0.0,
    )

    # Prefix columns to make their meaning obvious
    cost_pivot.columns = [f"cost_{c}" for c in cost_pivot.columns]
    imps_pivot.columns = [f"imps_{c}" for c in imps_pivot.columns]

    ad_weekly_wide = pd.concat([cost_pivot, imps_pivot], axis=1).reset_index()

    # 3. Sales: weekly KPI (net sales)
    sales = add_week_start(sales, "Date")

    # Sum daily net sales into weekly net sales
    sales_weekly = (
        sales.groupby("week_start", as_index=False)
             .agg(net_sales=("Net_Sales", "sum"))
    )

    # 4. GA4 Sessions: weekly sessions by channel
    ga4 = add_week_start(ga4, "Date")

    # Aggregate daily sessions into weekly sessions per GA4 channel
    ga4_weekly = (
        ga4.groupby(["week_start", "GA4_Channel"], as_index=False)
           .agg(weekly_sessions=("Sessions", "sum"))
    )

    # Create a clean channel identifier for column names
    ga4_weekly["channel_clean"] = ga4_weekly["GA4_Channel"].apply(normalize_channel_name)

    # Pivot to wide format: one row per week, one column per GA4 channel
    ga4_pivot = ga4_weekly.pivot_table(
        index="week_start",
        columns="channel_clean",
        values="weekly_sessions",
        aggfunc="sum",
        fill_value=0.0,
    )

    ga4_pivot.columns = [f"sessions_{c}" for c in ga4_pivot.columns]
    ga4_weekly_wide = ga4_pivot.reset_index()

    # 5. Build the full weekly calendar over the sales date range
    # We use the sales table to define the overall time window
    min_week = sales_weekly["week_start"].min()
    max_week = sales_weekly["week_start"].max()

    # Create a continuous weekly index from min to max (Mondays only)
    all_weeks = pd.DataFrame(
        {"week_start": pd.date_range(start=min_week, end=max_week, freq="W-MON")}
    )

    # 6. Join everything into a single weekly modeling dataset
    weekly = all_weeks.merge(sales_weekly, on="week_start", how="left")
    weekly = weekly.merge(ad_weekly_wide, on="week_start", how="left")
    weekly = weekly.merge(ga4_weekly_wide, on="week_start", how="left")

    # For modeling, weeks with no spend or sessions are better treated as zeros
    # than as missing values. We keep 'week_start' as a proper datetime column.
    value_cols = [c for c in weekly.columns if c != "week_start"]
    weekly[value_cols] = weekly[value_cols].fillna(0.0)

    weekly = weekly.sort_values("week_start").reset_index(drop=True)

    # 7. Save the weekly dataset to CSV
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    weekly.to_csv(OUTPUT_CSV, index=False)

    print(f"Weekly MMM dataset saved to: {OUTPUT_CSV}")
    print("Shape:", weekly.shape)
    print("Columns:", list(weekly.columns))


if __name__ == "__main__":
    main()

