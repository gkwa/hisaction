import matplotlib.pyplot as plt
import pandas
import scipy.stats

data = """1,June 05 2024,$74.17
1,May 05 2024,$53.72
1,April 05 2024,$53.72
1,March 05 2024,$53.72
1,February 04 2024,$53.72
1,January 04 2024,$53.72
1,December 03 2023,$53.72
1,November 03 2023,$53.72
1,October 05 2023,$53.72
1,September 04 2023,$53.72
1,August 03 2023,$50.52
1,July 05 2023,$50.52
1,June 03 2023,$50.52
1,May 04 2023,$35.22
1,April 04 2023,$35.22
1,March 04 2023,$35.22"""

df = pandas.DataFrame(
    [row.split(",") for row in data.split("\n")],
    columns=["Statement #", "Date", "Amount"]
)
df = df.drop(columns=["Statement #"])
df["Amount"] = df["Amount"].str.replace("$", "").astype(float)
df["Date"] = pandas.to_datetime(df["Date"], format="%B %d %Y")
df = df.sort_values("Date")
df["Rate of Change"] = df["Amount"].pct_change()
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(
    range(len(df)), df["Amount"]
)

price_changes = df["Amount"].unique()
print(f"Number of price changes: {len(price_changes) - 1}")

durations = df.groupby("Amount").agg({"Date": ["min", "max"]})
durations["Duration"] = durations[("Date", "max")] - durations[("Date", "min")]

for price, duration in zip(durations.index, durations["Duration"]):
    print(f"Price ${price:.2f} remained for {duration.days} days")

first_price = price_changes[0]
previous_price = first_price

for price in price_changes[1:]:
   change_from_first = (price - first_price) / first_price * 100
   change_from_previous = (price - previous_price) / previous_price * 100
   print(f"Price changed to ${price:.2f}")
   if price > first_price:
       print(f"  Change from first price (${first_price:.0f}): {change_from_first:.0f}% increase")
   else:
       print(f"  Change from first price (${first_price:.0f}): {change_from_first:.0f}% decrease")
   if price > previous_price:
       print(f"  Change from previous price (${previous_price:.0f}): {change_from_previous:.0f}% increase")
   else:
       print(f"  Change from previous price (${previous_price:.0f}): {change_from_previous:.0f}% decrease")
   previous_price = price
   
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

axs[0, 0].plot(df["Date"], df["Amount"], marker="o")
axs[0, 0].set_xlabel("Date")
axs[0, 0].set_ylabel("Amount")
axs[0, 0].set_title("Amount Over Time")
axs[0, 0].tick_params(axis="x", rotation=45)
axs[0, 0].grid(True)

axs[0, 1].bar(range(len(price_changes)), price_changes)
axs[0, 1].set_xticks(range(len(price_changes)))
axs[0, 1].set_xticklabels([f"Price {i+1}" for i in range(len(price_changes))])
axs[0, 1].set_ylabel("Price")
axs[0, 1].set_title("Price Changes")
axs[0, 1].grid(True)

durations.plot.bar(y="Duration", ax=axs[1, 0], legend=False)
axs[1, 0].set_xticks(range(len(durations)))
axs[1, 0].set_xticklabels([f"${price:.2f}" for price in durations.index], rotation=45)
axs[1, 0].set_ylabel("Duration (Days)")
axs[1, 0].set_title("Price Durations")
axs[1, 0].grid(True)

price_changes_percent = [0] + [
    (new_price - old_price) / old_price * 100
    for old_price, new_price in zip(price_changes[:-1], price_changes[1:])
]
axs[1, 1].bar(range(len(price_changes_percent)), price_changes_percent)
axs[1, 1].set_xticks(range(len(price_changes_percent)))
axs[1, 1].set_xticklabels([f"Price {i+1}" for i in range(len(price_changes_percent))], rotation=45)
axs[1, 1].set_ylabel("Percentage Change")
axs[1, 1].set_title("Price Change Percentages")
axs[1, 1].grid(True)

plt.tight_layout()
plt.savefig("combined_plots.png")

print(f"Average Rate of Change: {df['Rate of Change'].mean():.4f}")
print(f"Slope (Linear Regression): {slope:.4f}")
print(f"R-squared Value: {r_value**2:.4f}")
