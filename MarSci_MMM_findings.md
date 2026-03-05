# MarSci MMM – Findings and Recommendations

## 1. Context and Goal

The goal of this exercise was to understand how paid media investment contributes to ecommerce net sales using a **Media Mix Model (MMM)**, instead of relying on last-click attribution or simple channel-level ratios.

To do this, I first consolidated **Ad Platform data, Sales data, and GA4 Sessions** into a single weekly dataset. From there I used Google’s open-source MMM framework **Meridian** to estimate a national weekly model using `net_sales` as the main KPI.

The objective was not just to generate channel ROIs, but to create a structured view of how **media interacts with underlying demand and organic behavior over time**.

---

# 2. Modeling Approach (High-Level Overview)

At a high level, I built a weekly dataset combining:

- Paid media **spend and impressions by platform**
- **GA4 sessions by channel**
- **Ecommerce net sales**

Paid media channels included in the model:

- Google Ads  
- Facebook Ads  
- Bing Ads  
- TikTok  
- The Trade Desk  
- Pinterest Ads  

These enter the model as **media variables with associated spend**, while **GA4 sessions act as control variables** capturing baseline demand and organic traffic patterns.

The model was implemented using **Meridian in a GPU-enabled Colab runtime** and passed Meridian’s built-in diagnostic checks:

- **Overall model quality:** PASS  
- **R²:** ~0.99  
- **MAPE:** Low  
- **Baseline diagnostics:** Clean  

From a technical perspective the model behaves as expected and provides a solid starting point to discuss **channel contribution and budget decisions**.

---

# 3. Key Findings

## Media Drives a Meaningful but Not Dominant Share of Sales

The model attributes approximately **$30.9M of incremental revenue to paid media**, representing about **41% of total modeled revenue**.

The remaining **~59% comes from baseline demand and control variables** such as:

- GA4 traffic
- Trend
- Seasonality

This distribution feels directionally reasonable. Media is clearly important, but **it is not the sole driver of sales**. Organic demand and broader market behavior play a meaningful role as well.

---

## Spend is Highly Concentrated in Two Main Channels

Across the entire period:

- **Facebook Ads**
  - ~60% of total paid spend
  - ~80% of impressions

- **Google Ads**
  - ~34% of spend
  - ~15% of impressions

The remaining platforms (Bing, TikTok, The Trade Desk, Pinterest) represent only:

- **~6–7% of total spend**
- **<5% of impressions**

From a budget perspective, the setup is essentially **a Google + Facebook ecosystem with a small experimental long tail**.

---

## Contribution Follows a Similar Pattern (But Not Perfectly)

The MMM suggests both Google and Facebook are strong contributors, though their efficiency profiles differ slightly.

### Google Ads

- ~34% of spend
- ~16.9% of modeled contribution
- Estimated ROI: **~3.6x**  
- Credible interval: **0.6 – 7.6**

### Facebook Ads

- ~60% of spend
- ~22.9% of contribution
- Estimated ROI: **~2.8x**
- Credible interval: **0.5 – 6.9**

Both channels are clearly pulling their weight.

- **Google appears somewhat more efficient**
- **Facebook carries more of the scale** due to its larger budget

This pattern is common in ecommerce:  
Search captures **high intent efficiently**, while social platforms help **sustain reach and scale**.

---

## Smaller Channels Show Positive but Noisy Signals

For smaller platforms the model detects **positive signals but with wide uncertainty**, which is expected given their smaller budgets.

| Channel | Spend Share | Contribution | Estimated ROI |
|-------|-------|-------|-------|
| Bing Ads | ~1.2% | ~0.3% | ~1.7x (0.3–4.5) |
| TikTok | ~1.9% | ~0.3% | ~1.3x (0.2–3.7) |
| The Trade Desk | ~2.0% | ~0.3% | ~1.2x (0.2–3.0) |
| Pinterest Ads | ~0.5% | ~0.1% | ~1.4x (0.2–4.1) |

Given the small scale and wide credible intervals, these should be interpreted as **directional signals rather than precise ROI estimates**.

None of these channels appear clearly broken, but there is **not enough signal yet to make aggressive budget shifts based purely on the MMM output**.

---

## GA4 Controls Help Separate Demand from Media Impact

Including GA4 sessions as control variables helps the model avoid **over-crediting media for demand swings** driven by consumer behavior.

For example, increases in **Paid Search and Direct sessions** often line up with sales changes even when media spend is flat. This is exactly what we would expect if **brand demand and intent** are doing part of the work.

This is also reflected in:

- A **stable baseline component**
- Clean **posterior predictive checks**
- A strong **Bayesian p-value**

Overall the model appears to capture **demand dynamics realistically**, rather than forcing all variation into media coefficients.

---

# 4. Recommended Actions

## Protect and Optimize the Main Workhorse Channels

Since **Google Ads and Facebook Ads account for the majority of both spend and modeled contribution**, large cuts to these channels would not be advisable based on this model alone.

Instead the focus should be **within-channel optimization**:

- Identify underperforming segments inside each platform  
  (e.g. weaker audiences, placements, or ad groups)

- Reallocate budget from weaker segments into stronger performers before reducing total channel investment

This typically produces faster gains than large cross-channel shifts.

---

## Treat Smaller Platforms as Structured Test-and-Learn Channels

For **Bing, TikTok, The Trade Desk, and Pinterest**, the right approach is **structured experimentation** rather than aggressive scaling or elimination.

Recommended approach:

- Maintain **small but intentional test budgets**
- Focus each test on **clear hypotheses**  
  (creative format, audience, funnel stage)

For the most promising platforms (**TikTok and The Trade Desk**), I would also recommend **incrementality tests**, such as:

- Geo experiments
- Step tests

These results can later be used to **calibrate the MMM**, which significantly improves model reliability.

---

## Use the MMM as a Planning Guardrail

Rather than treating the MMM as a final answer, it is most useful as a **decision support tool**.

For example, we can simulate scenarios such as:

- Shifting **10% of budget from a lower-ROI channel to a higher-ROI channel**
- Holding total spend constant and estimating the predicted change in sales

The goal is not to blindly follow the model, but to **avoid clearly suboptimal budget allocations**.

---

## Improve the Model with Richer Business Context

For the next iteration of the MMM, I would incorporate additional business variables such as:

- Promotion flags
- Price changes
- Major product launches
- Competitive pressure proxies

These inputs help separate **media-driven effects from commercial events**, improving both model accuracy and interpretability.

---

# Final Takeaway

Overall, the results suggest a **healthy media ecosystem**.

- **Google and Facebook** remain the primary drivers of media contribution.
- **Smaller channels show early positive signals**, but require additional testing before making major scaling decisions.

The MMM provides a useful framework to understand how **media interacts with demand**, but its real value comes when combined with **experimentation and ongoing iteration**.

Used this way, it becomes a strong foundation for improving media efficiency while supporting both **short-term revenue goals and long-term growth**.
