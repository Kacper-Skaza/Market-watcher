# Copyright 2025 Kacper Skaza
# Licensed under the Apache License, Version 2.0
# Distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS.
# For details see LICENSE file or visit http://www.apache.org/licenses/LICENSE-2.0.


import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config as cfg
import data_manager as dm


# To compile use:
# pyinstaller src/Market_watcher.spec --distpath .


# Call update_market_info() every 5 seconds
def periodic_update():
	dm.update_market_info(price_label, canvas, ax, percentage_label)
	root.after(5000, periodic_update)


# Adjusts UI to the window size
def on_resize():
	info_label.config(wraplength=root.winfo_width() - 20)


# Close the application
def on_close():
	root.quit()
	root.destroy()


# Create the Tkinter window
root = tk.Tk()
root.title("Market watcher")
root.minsize(600, 400)
root.bind("<Configure>", lambda event=None: on_resize())
root.protocol("WM_DELETE_WINDOW", on_close)

# Create info label
info_label = tk.Label(
	root, text=
	"v.1.0.0" + " <|> " +
	"© 2025 Kacper Skaza" + " <|> " +
	"Apache License 2.0" + " <|> " +
	"Market data provided by Yahoo Finance API." + " <|> " +
	"Author is not responsible for any trading losses or financial decisions" + " " +
	"made based on the displayed data. Invest at your own risk.",
	font=("Arial", 8),
	anchor="w",
	fg="gray"
)
info_label.pack(side=tk.BOTTOM, padx=10, pady=1, fill=tk.X)

# Frame for market buttons (right)
frame_market = tk.Frame(root, bg="white")
frame_market.pack(side=tk.RIGHT, padx=(0, 10), pady=(10, 0), fill=tk.Y)

# Frame for label with market name and value (top)
frame_info = tk.Frame(root, bg="white")
frame_info.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

# Frame for time range buttons (bottom)
frame_time = tk.Frame(root, bg="white")
frame_time.pack(side=tk.BOTTOM, padx=10, pady=(10, 0), fill=tk.X)

# Create the Matplotlib figure (center)
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=0, fill=tk.BOTH, expand=True)

# Create label to display price information
price_label = tk.Label(frame_info, text="", font=("Arial", 20, "bold"), bg="white")
price_label.pack()

# Create label to display percentage change
percentage_label = tk.Label(frame_info, text="", font=("Arial", 16), bg="white")
percentage_label.pack()

# Track buttons for each category (market and period)
market_buttons = {}
period_buttons = {}

# Create buttons to select market
for name, ticker in cfg.market.items():
	btn = tk.Button(
		frame_market, text=name,
		command=lambda n=name: dm.change_market(
			n, None, market_buttons, period_buttons, price_label, canvas, ax, percentage_label
		),
		height=2, width=15, font=("Arial", 12), relief="solid"
	)
	btn.pack(padx=10, pady=(10, 0))
	market_buttons[name] = btn

# Create buttons to select period
for period in cfg.intervals:
	btn = tk.Button(
		frame_time, text=period,
		command=lambda p=period: dm.change_market(
			None, p, market_buttons, period_buttons, price_label, canvas, ax, percentage_label
		),
		height=2, width=8, font=("Arial", 12), relief="solid"
	)
	btn.pack(side=tk.LEFT, padx=(10, 0), pady=10)
	period_buttons[period] = btn

# Set default market
dm.change_market(
	None, None, market_buttons, period_buttons, price_label, canvas, ax, percentage_label
)
periodic_update()

# Start the application loop
root.mainloop()
