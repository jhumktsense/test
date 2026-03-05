#MarSci MMM – Findings and Recommendations

1. Context and goal

The goal of this exercise was to understand how paid media investment is actually contributing to ecommerce net sales using a proper Media Mix Model, rather than relying on last-click attribution or simple channel ratios.

To do this, I first consolidated Ad Platform data, Sales data, and GA4 Sessions into a single weekly dataset. From there I used Google’s open-source MMM framework Meridian to estimate a national weekly model using net_sales as the main KPI.

The idea was not just to generate channel ROIs, but to create a structured view of how media interacts with underlying demand and organic behavior over time.


2. Modeling approach (high-level overview)

At a high level, I built a weekly dataset combining:
	•	Paid media spend and impressions by platform
	•	GA4 sessions by channel
	•	Ecommerce net sales

Paid media channels (Google Ads, Facebook Ads, Bing Ads, TikTok, The Trade Desk, and Pinterest Ads) enter the model as media variables with associated spend, while GA4 sessions act as control variables to capture baseline demand and organic traffic patterns.

The model was implemented using Meridian in a GPU-enabled Colab runtime, and it passed Meridian’s built-in diagnostic checks:
	•	Overall model quality: PASS
	•	R² close to 0.99
	•	Low MAPE
	•	Clean baseline diagnostics

In other words, from a technical perspective the model behaves as expected and provides a reasonable starting point to discuss channel contribution and budget decisions.


3. Key findings

Media drives a meaningful but not dominant share of sales

The model attributes roughly $30.9M of incremental revenue to paid media, which represents about 41% of total modeled revenue.

The remaining ~59% comes from baseline demand and control variables such as GA4 traffic, trend, and seasonality.

That distribution feels directionally reasonable. Media is clearly important, but it is not the sole driver of sales. Organic demand and broader market behavior are doing a meaningful part of the work.


Spend is highly concentrated in two main channels

Looking at the spend mix across the period:
	•	Facebook Ads: ~60% of total paid spend and ~80% of impressions
	•	Google Ads: ~34% of spend and ~15% of impressions

The remaining platforms (Bing, TikTok, The Trade Desk, Pinterest) together represent only ~6–7% of total spend and less than 5% of impressions.

So from a budget perspective the setup is essentially a Google + Facebook ecosystem with a small experimental long tail.


Contribution follows a similar pattern, but not perfectly

The MMM suggests that both Google and Facebook are strong contributors, but their efficiency profiles are slightly different.

Google Ads
	•	~34% of spend
	•	~16.9% of modeled contribution
	•	Estimated ROI: ~3.6x (credible interval: 0.6–7.6)

Facebook Ads
	•	~60% of spend
	•	~22.9% of contribution
	•	Estimated ROI: ~2.8x (credible interval: 0.5–6.9)

Both channels are clearly pulling their weight. Google appears somewhat more efficient, while Facebook carries more of the overall scale because of the larger budget behind it.

This is a fairly common pattern in ecommerce: search captures strong intent efficiently, while social platforms help sustain reach and scale.


Smaller channels show positive but noisy signals

For the smaller platforms, the model detects positive signals but with wide uncertainty, which is expected given the relatively small budgets.

Approximate results:
	•	Bing Ads:
~1.2% of spend | ~0.3% of contribution | ROI ~1.7x (0.3–4.5)
	•	TikTok:
~1.9% of spend | ~0.3% of contribution | ROI ~1.3x (0.2–3.7)
	•	The Trade Desk:
~2.0% of spend | ~0.3% of contribution | ROI ~1.2x (0.2–3.0)
	•	Pinterest Ads:
~0.5% of spend | ~0.1% of contribution | ROI ~1.4x (0.2–4.1)

Given the small scale and the wide credible intervals, I would interpret these less as precise ROI estimates and more as early directional signals.

None of these channels appear clearly broken, but there is also not enough signal yet to make aggressive budget shifts based purely on the MMM output.


GA4 controls help separate demand from media impact

Including GA4 sessions as controls helps the model avoid over-crediting media for demand swings that are actually driven by underlying consumer behavior.

For example, increases in Paid Search and Direct sessions often line up with sales changes even when media spend is relatively flat. That is exactly what we would expect if demand and brand interest are driving part of the variation.

This is also reflected in:
	•	a stable baseline component
	•	clean posterior predictive checks
	•	a strong Bayesian p-value

Overall, the model appears to be capturing demand dynamics realistically rather than forcing everything through media coefficients.


4. Recommended actions

Protect and optimize the main workhorse channels

Since Google Ads and Facebook Ads account for the vast majority of both spend and modeled contribution, I would avoid making large budget cuts to either channel based solely on this model.

Instead, the better move is optimization within the channels:
	•	Identify underperforming segments inside each platform
(e.g., weaker audiences, placements, or ad groups)
	•	Reallocate budget from those segments into the strongest performers before reducing total channel investment.

This approach typically produces faster gains than shifting large amounts of spend across platforms.


Treat smaller platforms as structured test-and-learn channels

For Bing, TikTok, The Trade Desk, and Pinterest, the right strategy at this stage is structured experimentation rather than aggressive scaling or elimination.

Recommended approach:
	•	Maintain small but intentional test budgets
	•	Focus each test on specific hypotheses
(creative format, audience, funnel stage, etc.)

For the most promising channels (TikTok and The Trade Desk in particular), I would also recommend incrementality tests such as geo experiments or step tests.

Those results can later be used to calibrate the MMM, which significantly improves model reliability.


Use the MMM as a planning guardrail

Rather than treating the MMM as a final answer, it is most useful as a decision support tool.

For example, we can run scenario simulations such as:
	•	shifting 10% of spend from a lower ROI channel into a higher ROI channel
	•	holding total budget constant and estimating the predicted change in sales

The goal is not to blindly follow the model, but to avoid clearly suboptimal budget allocations.


Improve the model with richer business context

For the next iteration of the MMM, I would add several business variables that typically improve model stability:
	•	Promotion flags
	•	Price changes
	•	Major product launches
	•	Competitive pressure proxies

Including these factors helps separate media-driven effects from commercial events, which usually makes the model both more accurate and easier to explain to stakeholders.


Final takeaway

Overall, the results suggest a fairly healthy media ecosystem.

Google and Facebook remain the primary drivers of media contribution, while smaller channels show early signals but require further testing before scaling decisions can be made.

The MMM provides a useful framework to understand how media interacts with demand, but its real value comes when it is combined with experimentation and ongoing iteration.

Used that way, it becomes a strong foundation for improving media efficiency while supporting both short-term revenue goals and long-term growth.

