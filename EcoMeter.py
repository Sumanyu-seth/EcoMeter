import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

IDEAL_CO2 = 5.0
ECO_TIPS = [
    "Turn off lights when you leave the room.",
    "Use public transport or carpool when possible.",
    "Unplug chargers when not in use.",
    "Switch to LED bulbs for lower energy use.",
    "Carry a reusable water bottle to cut plastic waste.",
    "Avoid using single-use plastic bags.",
    "Use a fan instead of air conditioning when possible.",
    "Buy local fruits and vegetables to reduce transport emissions."
]

def calculate_co2():
    try:
        personal_km = float(entry_personal.get())
        public_km = float(entry_public.get())
        electricity_hours = float(entry_electricity.get())

        electricity_kwh = electricity_hours * 0.5

        total_co2 = (personal_km * 0.21) + (public_km * 0.08) + (electricity_kwh * 0.9)

        diff = ((total_co2 - IDEAL_CO2) / IDEAL_CO2) * 100

        if diff > 0:
            msg = f"Your daily CO₂ footprint is {total_co2:.2f} kg.\n⚠️ {abs(diff):.1f}% above the ideal limit."
            result_label.config(text=msg, fg="red")
        else:
            msg = f"Your daily CO₂ footprint is {total_co2:.2f} kg.\n✅ {abs(diff):.1f}% below the ideal limit."
            result_label.config(text=msg, fg="green")

        show_bar_chart(total_co2)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

def show_bar_chart(user_value):
    for widget in chart_frame.winfo_children():
        widget.destroy()  # to clear previous chart

    categories = ["Your Emission", "Ideal Limit"]
    values = [user_value, IDEAL_CO2]
    colors = ['#E53935' if user_value > IDEAL_CO2 else '#43A047', '#43A047']

    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(categories, values, color=colors)
    ax.set_title("CO₂ Emission Comparison", fontsize=12, fontweight='bold')
    ax.set_ylabel("CO₂ (kg/day)")
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_tip():
    tip = random.choice(ECO_TIPS)
    messagebox.showinfo("Eco Tip of the Day 🌱", tip)

def clear_all():
    entry_personal.delete(0, tk.END)
    entry_public.delete(0, tk.END)
    entry_electricity.delete(0, tk.END)
    result_label.config(text="")
    for widget in chart_frame.winfo_children():
        widget.destroy()

# --- UI Setup ---
root = tk.Tk()
root.title("EcoMeter - Personal Carbon Footprint Tracker")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

root.config(bg="#E8F5E9")

title_label = tk.Label(root, text="🌍 EcoMeter 🌿",
                       font=("Helvetica", 22, "bold"),
                       bg="#E8F5E9", fg="#2E7D32")
title_label.pack(pady=10)

# --- Input Fields ---
tk.Label(root, text="Distance by personal transport (km/day):",
         bg="#E8F5E9", font=("Helvetica", 12)).pack(pady=5)
entry_personal = tk.Entry(root, justify="center", font=("Helvetica", 11))
entry_personal.insert(0, "0")
entry_personal.pack(pady=3)

tk.Label(root, text="Distance by public transport (km/day):",
         bg="#E8F5E9", font=("Helvetica", 12)).pack(pady=5)
entry_public = tk.Entry(root, justify="center", font=("Helvetica", 11))
entry_public.insert(0, "0")
entry_public.pack(pady=3)

tk.Label(root, text="Electricity usage (hours/day):",
         bg="#E8F5E9", font=("Helvetica", 12)).pack(pady=5)
entry_electricity = tk.Entry(root, justify="center", font=("Helvetica", 11))
entry_electricity.insert(0, "0")
entry_electricity.pack(pady=3)

# --- Buttons ---
btn_calc = tk.Button(root, text="Calculate CO₂", command=calculate_co2,
                     bg="#66BB6A", fg="white", font=("Helvetica", 12, "bold"))
btn_calc.pack(pady=10)

btn_tip = tk.Button(root, text="Show Eco Tip", command=show_tip,
                    bg="#42A5F5", fg="white", font=("Helvetica", 12, "bold"))
btn_tip.pack(pady=5)

btn_clear = tk.Button(root, text="Clear All", command=clear_all,
                      bg="#FFA726", fg="white", font=("Helvetica", 12, "bold"))
btn_clear.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.quit,
                     bg="#EF5350", fg="white", font=("Helvetica", 12, "bold"))
exit_btn.pack(pady=5)

# --- Result Label ---
result_label = tk.Label(root, text="", bg="#E8F5E9",
                        fg="#1B5E20", font=("Helvetica", 12, "bold"), wraplength=450, justify="center")
result_label.pack(pady=10)

# --- Chart Frame ---
chart_frame = tk.Frame(root, bg="#E8F5E9")
chart_frame.pack(pady=10)

# --- Footer ---
footer = tk.Label(root, text="Supports SDG 13: Climate Action 🌎",
                  bg="#E8F5E9", fg="#388E3C", font=("Helvetica", 10))
footer.pack(side="bottom", pady=10)

root.mainloop()
