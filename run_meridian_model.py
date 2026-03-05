import pandas as pd
from pathlib import Path

from meridian import constants
from meridian.data import data_frame_input_data_builder
from meridian.model import model
from meridian.model import prior_distribution
from meridian.model import spec
from meridian.analysis.review import reviewer
import tensorflow_probability as tfp


# Base paths (relative, safe to commit)
PROJECT_ROOT = Path(".")
DATA_DIR = PROJECT_ROOT
CSV_PATH = DATA_DIR / "weekly_mmm_dataset.csv"


def build_input_data():
    """
    Build Meridian InputData from the weekly_mmm_dataset.csv file.

    - KPI: net_sales (treated as revenue)
    - Media: weekly cost and impressions by ad platform
    - Controls: GA4 sessions by channel
    """
    df = pd.read_csv(CSV_PATH, parse_dates=["week_start"])

    # Meridian expects a 'time' column, so I create it from week_start
    df["time"] = df["week_start"]

    # Add a dummy population column so Meridian can scale media if needed.
    df["population"] = 1.0

    # Define media channels based on the weekly dataset
    channels = [
        "google_ads",
        "facebook_ads",
        "bing_ads",
        "tiktok",
        "the_trade_desk",
        "pinterest_ads",
    ]

    # Media exposure metrics and spend per channel
    media_cols = [f"imps_{ch}" for ch in channels]
    media_spend_cols = [f"cost_{ch}" for ch in channels]

    # Controls: all GA4 session metrics
    control_cols = [c for c in df.columns if c.startswith("sessions_")]

    # Build the DataFrameInputDataBuilder
    builder = data_frame_input_data_builder.DataFrameInputDataBuilder(
        kpi_type="revenue",
        default_kpi_column="net_sales",
    )

    builder = (
        builder.with_kpi(df, time_col="time")
        .with_population(df, population_col="population")
        .with_controls(df, control_cols=control_cols, time_col="time")
    )

    builder = builder.with_media(
        df,
        media_cols=media_cols,
        media_spend_cols=media_spend_cols,
        media_channels=channels,
    )

    input_data = builder.build()
    return input_data


def run_meridian_model():
    """
    Configure and fit a basic Meridian model on the weekly dataset.
    """
    input_data = build_input_data()

    # Simple ROI prior shared across media channels.
    roi_mu = 0.2
    roi_sigma = 0.9

    prior = prior_distribution.PriorDistribution(
        roi_m=tfp.distributions.LogNormal(roi_mu, roi_sigma, name=constants.ROI_M)
    )

    model_spec = spec.ModelSpec(
        prior=prior,
        enable_aks=True,  # time-varying intercept to capture trend and seasonality
    )

    mmm = model.Meridian(input_data=input_data, model_spec=model_spec)

    # Smaller numbers than the full demo to keep runtime reasonable.
    mmm.sample_prior(200)
    mmm.sample_posterior(
        n_chains=4,
        n_adapt=1000,
        n_burnin=300,
        n_keep=500,
        seed=0,
    )

    reviewer.ModelReviewer(mmm).run()

    return mmm


if __name__ == "__main__":
    mmm = run_meridian_model()
    print("Meridian model fitted on weekly_mmm_dataset.csv")

import pandas as pd
from pathlib import Path

from meridian import constants
from meridian.data import data_frame_input_data_builder
from meridian.model import model
from meridian.model import prior_distribution
from meridian.model import spec
from meridian.analysis.review import reviewer
import tensorflow_probability as tfp


# Base paths (relative, safe to commit)
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT
CSV_PATH = DATA_DIR / "weekly_mmm_dataset.csv"


def build_input_data():
    """
    Build Meridian InputData from the weekly_mmm_dataset.csv file.

    - KPI: net_sales (treated as revenue)
    - Media: weekly cost and impressions by ad platform
    - Controls: GA4 sessions by channel
    """
    df = pd.read_csv(CSV_PATH, parse_dates=["week_start"])

    # Add a dummy population column so Meridian can scale media if needed.
    # For a single-country model, using 1.0 for all rows is a simple and explicit choice.
    df["population"] = 1.0

    # Define media channels based on the weekly dataset
    channels = [
        "google_ads",
        "facebook_ads",
        "bing_ads",
        "tiktok",
        "the_trade_desk",
        "pinterest_ads",
    ]

    # Media exposure metrics and spend per channel
    media_cols = [f"imps_{ch}" for ch in channels]
    media_spend_cols = [f"cost_{ch}" for ch in channels]

    # Controls: all GA4 session metrics
    control_cols = [c for c in df.columns if c.startswith("sessions_")]

    # Build the DataFrameInputDataBuilder
    builder = data_frame_input_data_builder.DataFrameInputDataBuilder(
        kpi_type="revenue",
        default_kpi_column="net_sales",
        # When kpi_type is "revenue", revenue_per_kpi is not required.
    )

    builder = (
        builder.with_kpi(df, time_col="week_start")
        .with_population(df, population_col="population")
        .with_controls(df, control_cols=control_cols)
    )

    builder = builder.with_media(
        df,
        media_cols=media_cols,
        media_spend_cols=media_spend_cols,
        media_channels=channels,
    )

    input_data = builder.build()
    return input_data


def run_meridian_model():
    """
    Configure and fit a basic Meridian model on the weekly dataset.
    """
    input_data = build_input_data()

    # Simple ROI prior shared across media channels.
    # For a real project, these priors would be calibrated with experiments or business input.
    roi_mu = 0.2
    roi_sigma = 0.9

    prior = prior_distribution.PriorDistribution(
        roi_m=tfp.distributions.LogNormal(roi_mu, roi_sigma, name=constants.ROI_M)
    )

    model_spec = spec.ModelSpec(
        prior=prior,
        enable_aks=True,  # time-varying intercept to capture trend and seasonality
    )

    mmm = model.Meridian(input_data=input_data, model_spec=model_spec)

    # For the assessment I use smaller numbers than the full demo to keep runtime reasonable.
    # In a production run, I would increase these values for more stable posteriors.
    mmm.sample_prior(200)
    mmm.sample_posterior(
        n_chains=4,
        n_adapt=1000,
        n_burnin=300,
        n_keep=500,
        seed=0,
    )

    # Run built-in quality checks to make sure the model is reasonable.
    reviewer.ModelReviewer(mmm).run()

    return mmm


if __name__ == "__main__":
    mmm = run_meridian_model()
    print("Meridian model fitted on weekly_mmm_dataset.csv")

