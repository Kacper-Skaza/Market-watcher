# Copyright 2025 Kacper Skaza
# Licensed under the Apache License, Version 2.0
# Distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS.
# For details see LICENSE file or visit http://www.apache.org/licenses/LICENSE-2.0.


import pandas as pd
import yfinance as yf
from matplotlib.ticker import MaxNLocator

import config as cfg

# Global variables
current_market = list(cfg.market.keys())[0]
current_period = list(cfg.intervals.keys())[4]
current_price = 0


# Function to fetch data and plot graph
def draw_plot(canvas, ax, percentage_label):
	# Set interval from settings, default is "1d"
	interval = cfg.intervals.get(current_period, "1d")

	# Get data
	data = yf.Ticker(cfg.market[current_market]).history(period=current_period, interval=interval)

	# Process data
	new_row = pd.DataFrame({
		"Open": current_price,
		"High": current_price,
		"Low": current_price,
		"Close": current_price,
		"Adj Close": current_price,
		"Volume": 0,
	}, index=[data.index[-1] + pd.Timedelta(minutes=1)])
	data = pd.concat([data, new_row])

	# Calculate change from first to last price
	price_change = current_price - data["Close"].iloc[0]
	price_change_percent = (price_change * 100) / data["Close"].iloc[0]

	# Determine color based on price change
	if price_change_percent >= 0:
		color = "green"
	else:
		color = "red"

	# Clear plot
	ax.clear()

	# Plot the closing prices with line color
	ax.plot(data.index, data["Close"], label=f"Price {current_market} (USD)", color=color)

	# Fill the area under the curve
	ax.fill_between(data.index, data["Close"], color=color, alpha=0.2)

	# Title and labels
	ax.set_title(f"{cfg.market[current_market]} ({current_period})")
	ax.set_ylabel("Price (USD)")
	ax.yaxis.set_label_position('right')
	ax.yaxis.set_ticks_position('right')
	ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
	ax.grid(axis='y')

	# Set x-axis limits
	time_diff = data.index.max() - data.index.min()
	time_offset = time_diff * 0.02
	ax.set_xlim([data.index.min(), data.index.max() + time_offset])

	# Set y-axis limits
	ax.set_ylim([data["Close"].min() * 0.95, data["Close"].max() * 1.05])

	# Set horizontal line on current price
	ax.axhline(current_price, color=color, linestyle='--', linewidth=1)
	ax.text(
		data.index[-1] + (time_offset * 1.6), current_price,
		f'{current_price:.2f}',
		color='white', va='center', ha='left', fontsize=10,
		bbox=dict(facecolor=color, edgecolor=color, boxstyle='round, pad=0.3')
	)

	# Set percentage label
	if price_change_percent >= 0:
		percentage_label.config(text=f"+{price_change:.2f} (+{price_change_percent:.2f}%)", fg=color)
	else:
		percentage_label.config(text=f"{price_change:.2f} ({price_change_percent:.2f}%)", fg=color)

	# Draw plot
	canvas.draw()


# Function to update market information
def update_market_info(price_label, canvas, ax, percentage_label):
	global current_price

	# Get data
	data = yf.Ticker(cfg.market[current_market]).history(period="1d", interval="1m")

	# Update price and redraw plot if needed
	if current_price != data["Close"].iloc[-1]:
		current_price = data["Close"].iloc[-1]
		price_label.config(text=f"{current_market}: {current_price:.2f} USD")
		draw_plot(canvas, ax, percentage_label)


# Function to change market and refresh plot
def change_market(new_market, new_period, market_buttons, period_buttons, price_label, canvas, ax, percentage_label):
	global current_market
	global current_period
	global current_price

	# Update global variables
	if new_market is not None:
		current_market = new_market
	if new_period is not None:
		current_period = new_period

	# Update button state
	update_button_state(market_buttons, current_market)
	update_button_state(period_buttons, current_period)

	# Update current price
	data = yf.Ticker(cfg.market[current_market]).history(period="1d", interval="1m")
	current_price = data["Close"].iloc[-1]
	price_label.config(text=f"{current_market}: {current_price:.2f} USD")

	# Draw plot
	draw_plot(canvas, ax, percentage_label)


# Function to update the selected button's appearance
def update_button_state(button_dict, selected_key):
	for button_key, button in button_dict.items():
		if button_key == selected_key:
			button.config(relief="sunken")
		else:
			button.config(relief="raised")
