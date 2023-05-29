import tkinter as tk

# Global variables for valuation and spread
valuation = 0
spread = 0

def update_labels():
    data_label.config(text="Valuation: " + str(valuation) + " Spread: " + str(spread))

def on_button_click():
	global valuation
	global spread

	valuation = valuation_entry.get()
	spread = spread_entry.get()
	update_labels()

# Create the main window
window = tk.Tk()
window.title("Value Calculator")

# Calculate the default size of the window as 40% of the screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = int(screen_width * 0.4)
window_height = int(screen_height * 0.4)

# Set the default window size
window.geometry(f"{window_width}x{window_height}")

# Create labels for valuation and spread
valuation_label = tk.Label(window, text="Valuation:")
valuation_label.pack()

valuation_entry = tk.Entry(window)
valuation_entry.pack()

spread_label = tk.Label(window, text="Spread:")
spread_label.pack()

spread_entry = tk.Entry(window)
spread_entry.pack()

button = tk.Button(window, text="Send Values", command=on_button_click)
button.pack(pady=10)

data_label = tk.Label(window, text="Valuation: " + str(valuation) + " Spread: " + str(spread))
data_label.pack()

# Start the main event loop
window.mainloop()


"""
import tkinter as tk

def on_button_click():
    valuation = valuation_entry.get()
    spread = spread_entry.get()
    print("Valuation:", valuation)
    print("Spread:", spread)

# Create the main window
window = tk.Tk()
window.title("Value Calculator")

# Create a label and an entry widget for "valuation"
valuation_label = tk.Label(window, text="Valuation:")
valuation_label.pack()

valuation_entry = tk.Entry(window)
valuation_entry.pack()

# Create a label and an entry widget for "spread"
spread_label = tk.Label(window, text="Spread:")
spread_label.pack()

spread_entry = tk.Entry(window)
spread_entry.pack()

# Create a button widget
button = tk.Button(window, text="Print Values", command=on_button_click)
button.pack(pady=10)

# Start the main event loop
window.mainloop()
"""