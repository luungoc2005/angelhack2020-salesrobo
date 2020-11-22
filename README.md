## AngelHack 2020 Submission - tobtob
---

# AI business advisory service

- Optimal product pricing suggestion (based on price elasticity)
- Product sales forecast: Note - we originally intended to use `fbprophet` but had an installation issue with `pystan`, therefore moved to using ARIMA as a makeshift replacement
- User-desired features suggestion (using a BERT-based token classification model)

# Project structure
`backend/`: Main service backend
`frontend/`: Main service frontend
`crawler/`: Product listing & reviews crawler for Amazon/Shopee
`nlp/`: Labeling tool & model training for product features suggestion model