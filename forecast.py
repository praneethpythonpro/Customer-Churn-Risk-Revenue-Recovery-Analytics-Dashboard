import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("transactions.csv")

df["Date"]=pd.to_datetime(df["Date"])

monthly=df.groupby(
    pd.Grouper(
        key="Date",
        freq="M"
    )
)["Amount"].sum().reset_index()

monthly["Month_Index"]=range(len(monthly))

X=monthly[["Month_Index"]]
y=monthly["Amount"]

model=LinearRegression()
model.fit(X,y)

future=np.arange(
    len(monthly),
    len(monthly)+6
).reshape(-1,1)

forecast=model.predict(future)

future_dates=pd.date_range(
    monthly["Date"].max()+pd.offsets.MonthEnd(),
    periods=6,
    freq="M"
)

forecast_df=pd.DataFrame({
    "Date":future_dates,
    "Forecast Revenue":forecast
})

print("\nNext 6 Months Forecast\n")
print(forecast_df)

forecast_df.to_csv(
    "sales_forecast.csv",
    index=False
)

plt.figure(figsize=(10,5))

plt.plot(
    monthly["Date"],
    monthly["Amount"],
    marker="o",
    label="Actual"
)

plt.plot(
    future_dates,
    forecast,
    marker="o",
    linestyle="--",
    label="Forecast"
)

plt.title("Revenue Forecast")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.legend()
plt.tight_layout()

plt.savefig(
    "forecast.png",
    dpi=300
)

plt.show()

print("\nSaved -> sales_forecast.csv")
print("Saved -> forecast.png")
