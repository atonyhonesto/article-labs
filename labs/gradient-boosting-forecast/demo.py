from forecast import backtest, daily_sales

res = backtest(daily_sales())
print("Rolling-origin backtest, 7-day horizon (MAPE):")
print(res.to_string(index=False, float_format=lambda v: f"{v:.1%}"))
print(f"\nAverage: model {res.mape_model.mean():.1%} vs naive same-day-last-week {res.mape_naive.mean():.1%}")
