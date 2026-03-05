# MarSci MMM – Technical Notes

## 1. Data review

I started by reviewing the three raw tables in the Excel file: "Ad Platforms", "Sales", and "GA4 Sessions".

- Ad Platforms  
  The "Ad Platforms" tab contains daily media data at the (Date, Platform) level with `Cost` and `Impressions`. I checked for duplicated (Date, Platform) keys, null values, and gaps in the date series per platform. There were no duplicates and no nulls. Google Ads has continuous daily data across the full period (2023-01-01 to 2025-05-31). Other platforms (e.x. Facebook Ads, Bing Ads, TikTok, The Trade Desk, Pinterest Ads) start later in the timeline and/or have days with no spend, which is expected behavior for channels that are not always on.

- Sales  
  The "Sales" tab contains one row per calendar date with a `Net_Sales` value. I verified that there is exactly one row per day, no duplicated dates, no missing dates between 2023-01-01 and 2025-05-31, and no null values. This gives us a clean, continuous daily KPI time series for modeling.

- GA4 Sessions  
  The "GA4 Sessions" tab contains daily session data at the (Date, GA4_Channel) level from 2023-07-01 to 2025-05-31. I checked for duplicated (Date, GA4_Channel) pairs and null values; none were found. For each date, there are typically 14-17 distinct GA4 channels with non-zero sessions (e.x. Direct, Paid Search, Organic Search, Paid Social, Email). There are no missing dates within the GA4 date range, but GA4 starts later than the media and sales series, which I account for when building the modeling dataset.

I wrapped these checks in a small helper script (`check_raw_data.py`) so they can be re-run easily if the input file changes.

## 2. Data preparation for modeling

To get the data ready for Media Mix Modeling, I first wanted a single, clean table where every row is a week and every column has a clear meaning (spend, traffic, or sales). I chose a weekly grain instead of daily because weekly data is a common best practice in MMM and in Google's Meridian documentation. In practice, weekly aggregation smooths out day-to-day noise, gives more stable parameter estimates, and better matches how media budgets and reporting are usually managed.

For the weekly dataset (`weekly_mmm_dataset.csv`) I followed these steps:

- Align dates and create a weekly key
- Aggregate Ad Platforms to weekly spend and impressions
- Aggregate Sales to weekly net sales
- Aggregate GA4 Sessions to weekly sessions by channel
- Build a complete weekly calendar and join all sources, filling missing values with 0 for weeks with no spend or no sessions

All of these steps are implemented in Python using pandas in the `build_weekly_dataset.py` script, which reads the raw Excel file and writes out `weekly_mmm_dataset.csv` as the modeling-ready dataset.

## 3. Tools and process

For this assessment I used Python and pandas to keep the workflow reproducible and easy to extend into a full MMM pipeline. All of the code lives in small, focused scripts so it can be re-used or reviewed independently.

- I started by loading the Excel file into pandas and running basic data quality checks in `check_raw_data.py` (nulls, duplicate keys, date ranges, and missing calendar dates per table).
- After confirming the raw data was clean enough to model, I moved to `build_weekly_dataset.py`, where I aggregated the three tabs to a weekly grain and joined them into a single modeling-ready table.
- I then used `run_meridian_model.py` in a GPU-enabled Colab notebook to fit a Meridian model on top of the weekly dataset and run model diagnostics.
- Throughout the process I kept everything in plain Python scripts so the same steps can be run locally or in Colab with the same input files and a simple `pip install -r requirements.txt` plus `pip install "google-meridian[colab,and-cuda,schema]"` on Colab.

## 4. Additional data I would bring into the model

With only media spend, GA4 sessions, and net sales, the model can already learn some relationships, but it will mix true media effects with other drivers that are not explicitly modeled. In a real MMM I would try to add at least the following types of data:

- Promotions and pricing  
  Flags for promotions, discount depth, and key price changes by week and product category. This helps separate the impact of price and promo pressure from the impact of media, so we do not over-credit ads when a sale was actually driven by a big discount.

- Seasonality and calendar  
  Simple calendar features like holidays, paydays, and major events that affect baseline demand (e.x. Black Friday, Cyber Monday, Christmas week). Meridian can handle seasonality internally, but explicit calendar signals can still help interpretability and debugging.

- Organic and onsite signals  
  Organic search volume, organic social activity, email sends, and onsite metrics like add-to-cart rate or conversion rate. These variables capture demand that is not directly paid and provide context when paid media is stable but sales move.

- Competitive and category demand  
  Proxies for competitive pressure (e.x. share-of-voice from auction insights, competitor promotion flags) and category-level demand (e.x. Google query volume for key generic terms). These help control for shifts in the market that affect both spend decisions and sales.

- Macro and logistic constraints  
  Simple macro indicators like unemployment, inflation, or consumer confidence, and any known capacity constraints (e.x. stock-outs, shipping delays). These reduce the risk that the model attributes macro-driven swings in sales to changes in media spend.

## 5. Meridian model setup

For the modeling step I used Google's open source MMM framework Meridian (version 1.5.3) in a GPU Colab notebook. I kept the setup simple on purpose: a national, weekly model with `net_sales` as the revenue KPI and one media variable per paid channel. Each platform (Google Ads, Facebook Ads, Bing Ads, TikTok, The Trade Desk, Pinterest Ads) comes in with weekly spend and impressions, and all the GA4 session metrics are treated as control variables. That lets the model separate "real" media impact from shifts in underlying demand and organic traffic.

I used the `DataFrameInputDataBuilder` to read my weekly dataset (`weekly_mmm_dataset.csv`) and wire up the right columns, then configured a basic Bayesian model with a shared LogNormal ROI prior across channels and a time-varying intercept (AKS) to handle trend and seasonality. After sampling the posterior with MCMC, I ran `ModelReviewer`, which passed all the checks (overall PASS, R-squared close to 0.99, low MAPE, and a healthy prior–posterior shift). For this synthetic case the model is behaving nicely and is good enough to reason about channel-level effects.
