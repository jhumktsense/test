# MarSci MMM – Findings and recommendations

## 1. Context and goal

The goal of this exercise is to understand how paid media investment relates to ecommerce net sales for the sample data provided, using a proper Media Mix Model instead of simple last-click or channel-level ratios. I first consolidated Ad Platforms, Sales, and GA4 Sessions into a weekly dataset, and then used Google's open source MMM framework Meridian to fit a national weekly model with `net_sales` as the KPI.

## 2. High-level approach (one-paragraph summary)

In short, I built a single weekly table that combines media spend and impressions by platform, GA4 traffic by channel, and net sales, and then used Meridian to fit a Bayesian MMM on top of that dataset. Paid channels (Google Ads, Facebook Ads, Bing Ads, TikTok, The Trade Desk, Pinterest Ads) enter as media variables with associated spend, while GA4 sessions by channel act as control variables to capture underlying demand and organic behavior. The model runs in a GPU-enabled Colab runtime, passes all of Meridian's built-in quality checks (overall PASS, R-squared close to 0.99, low MAPE), and provides a reasonable starting point to talk about relative channel performance and budget decisions.

## 3. Key findings

- The model assigns most of the incremental revenue to the large, always-on performance channels. In this dataset, search and core paid social behave as the main workhorses, consistently explaining a big share of modeled incremental sales across weeks.

- Newer and upper-funnel channels like TikTok and The Trade Desk show smaller but meaningful contributions once they come online. Their modeled impact grows over time as spend ramps up, which is consistent with a channel that is still in a test-and-learn phase rather than at full maturity.

- GA4 session-based controls explain a lot of the baseline variation in traffic and demand. When traffic from high-intent channels like Paid Search and Direct moves, the model can increase or decrease expected sales even if paid spend is flat, which reduces the risk of over-crediting media for pure demand swings.

- The baseline and goodness-of-fit diagnostics look healthy. The baseline component is not negative, the Bayesian posterior predictive p-value is high, and goodness-of-fit metrics (R-squared, MAPE, wMAPE) are all in a comfortable range. That gives me confidence that the model is not obviously mis-specified for this synthetic example.

## 4. Recommended actions

- Rebalance budget toward the strongest ROI channels  
  Based on the model, I would plan scenarios where budget is gradually reallocated from weaker channels into the best performing workhorse channels (likely high-intent search and the best paid social placements). The goal is to capture more incremental revenue per dollar while keeping total spend roughly flat.

- Protect and cautiously grow promising but newer channels  
  For channels like TikTok and The Trade Desk that show early but smaller impact, I would recommend a controlled uplift in spend rather than a drastic cut or an aggressive scale-up. A reasonable next step would be to set up a few incremental tests (e.x. step-test or geo split) informed by the MMM to learn their response curves more precisely.

- Use Meridian's optimization tools for scenario planning  
  Once stakeholders are comfortable with the base model, I would plug it into Meridian's budget optimization features to run a set of "what-if" scenarios: how much incremental revenue do we expect if we shift X percent of budget from channel A to channel B, while holding total budget constant. This makes the MMM directly actionable in the planning process.

- Plan a second model iteration with richer controls  
  As a follow-up, I would extend the model to include promotions, pricing, and simple indicators of competitive pressure. This helps avoid giving too much credit to media when a big promo, a price change, or a competitor campaign is actually driving part of the observed lift, and it usually improves the trust stakeholders have in the MMM results.

# MarSci MMM – Findings and recommendations

## 1. Context and goal

The goal of this exercise is to understand how paid media investment relates to ecommerce net sales for the sample data provided, using a proper Media Mix Model instead of simple last-click or channel-level ratios. I first consolidated Ad Platforms, Sales, and GA4 Sessions into a weekly dataset, and then used Google's open source MMM framework Meridian to fit a national weekly model with `net_sales` as the KPI.

## 2. High-level approach (one-paragraph summary)

In short, I built a single weekly table that combines media spend and impressions by platform, GA4 traffic by channel, and net sales, and then used Meridian to fit a Bayesian MMM on top of that dataset. Paid channels (Google Ads, Facebook Ads, Bing Ads, TikTok, The Trade Desk, Pinterest Ads) enter as media variables with associated spend, while GA4 sessions by channel act as control variables to capture underlying demand and organic behavior. The model runs in a GPU-enabled Colab runtime, passes all of Meridian's built-in quality checks (overall PASS, R-squared close to 0.99, low MAPE), and provides a reasonable starting point to talk about relative channel performance and budget decisions.

## 3. Key findings

- The model assigns most of the incremental revenue to the large, always-on performance channels. In this dataset, search and core paid social behave as the main workhorses, consistently explaining a big share of modeled incremental sales across weeks.

- Newer and upper-funnel channels like TikTok and The Trade Desk show smaller but meaningful contributions once they come online. Their modeled impact grows over time as spend ramps up, which is consistent with a channel that is still in a test-and-learn phase rather than at full maturity.

- GA4 session-based controls explain a lot of the baseline variation in traffic and demand. When traffic from high-intent channels like Paid Search and Direct moves, the model can increase or decrease expected sales even if paid spend is flat, which reduces the risk of over-crediting media for pure demand swings.

- The baseline and goodness-of-fit diagnostics look healthy. The baseline component is not negative, the Bayesian posterior predictive p-value is high, and goodness-of-fit metrics (R-squared, MAPE, wMAPE) are all in a comfortable range. That gives me confidence that the model is not obviously mis-specified for this synthetic example.

## 4. Recommended actions

- Rebalance budget toward the strongest ROI channels  
  Based on the model, I would plan scenarios where budget is gradually reallocated from weaker channels into the best performing workhorse channels (likely high-intent search and the best paid social placements). The goal is to capture more incremental revenue per dollar while keeping total spend roughly flat.

- Protect and cautiously grow promising but newer channels  
  For channels like TikTok and The Trade Desk that show early but smaller impact, I would recommend a controlled uplift in spend rather than a drastic cut or an aggressive scale-up. A reasonable next step would be to set up a few incremental tests (e.x. step-test or geo split) informed by the MMM to learn their response curves more precisely.

- Use Meridian's optimization tools for scenario planning  
  Once stakeholders are comfortable with the base model, I would plug it into Meridian's budget optimization features to run a set of \"what-if\" scenarios: how much incremental revenue do we expect if we shift X percent of budget from channel A to channel B, while holding total budget constant. This makes the MMM directly actionable in the planning process.

- Plan a second model iteration with richer controls  
  As a follow-up, I would extend the model to include promotions, pricing, and simple indicators of competitive pressure. This helps avoid giving too much credit to media when a big promo, a price change, or a competitor campaign is actually driving part of the observed lift, and it usually improves the trust stakeholders have in the MMM results.

