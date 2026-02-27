import tkinter as tk
from tkinter import ttk, messagebox
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Hardcoded stock prices
dictionary = {
    "AAPL": 200,
    "GOOGL": 3500,
    "MSFT": 300,
    "TSLA": 250,
    "AMZN": 3300,
    "META": 280,
    "NFLX": 450,
    "NVDA": 600,
    "IBM": 140,
    "ORCL": 120
}
portfolio = []

# Functions #
def add_portfolio():
    # --- INPUT Section ---
    symbol = symbol_entry.get().upper()
    try:
        qty = int(quantity_entry.get())
        purchase_price = float(purchase_entry.get())
        current_price = float(current_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numbers for quantity and prices.")
        return

    # Input demonstration (echo user entries)
    print(f"[INPUT] User entered -> Symbol={symbol}, Quantity={qty}, Purchase Price={purchase_price}, Current Price={current_price}")

    # --- VALIDATIONS ---
    if symbol not in dictionary:
        messagebox.showwarning("Warning", "Stock not found in price list.")
        return
    if qty <= 0:
        messagebox.showwarning("Warning", "Quantity must be positive.")
        return
    if purchase_price < 0 or current_price < 0:
        messagebox.showerror("Error", "Prices cannot be negative.")
        return

    # --- ARITHMETIC Section ---
    invested = purchase_price * qty
    current_value = current_price * qty
    profit_loss_percent = ((current_value - invested) / invested) * 100

    # Output demonstration (show calculated results)
    print(f"[OUTPUT] Calculated -> Invested={invested}, Current Value={current_value}, Profit/Loss={profit_loss_percent:.2f}%")

    # --- DATA STORAGE Section ---
    portfolio.append([symbol, qty, purchase_price, current_price, round(profit_loss_percent, 2)])

    # --- UI Update Section ---
    if profit_loss_percent >= 0:
        tree.insert("", "end", values=(symbol, qty, purchase_price, current_price, f"{profit_loss_percent:.2f}%"), tags=("profit",))
    else:
        tree.insert("", "end", values=(symbol, qty, purchase_price, current_price, f"{profit_loss_percent:.2f}%"), tags=("loss",))

    update_summary()
    update_graph()
    messagebox.showinfo("Success", f"{symbol} added successfully!")


def update_summary():
    invested = sum(item[1] * item[2] for item in portfolio)
    current_value = sum(item[1] * item[3] for item in portfolio)
    invested_label.config(text=f"Invested: ₹{invested:.2f}")
    current_label.config(text=f"Current Value: ₹{current_value:.2f}")

def delete_stock():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No row selected.")
        return
    selected_item = selected_items[0]

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this stock?")
    if not confirm:
        return

    symbol = tree.item(selected_item)["values"][0]
    portfolio[:] = [item for item in portfolio if item[0] != symbol]
    tree.delete(selected_item)
    update_summary()
    update_graph()
    messagebox.showinfo("Success", f"{symbol} deleted successfully!")
    
def edit_stock():
    #Load selected stock into input fields for editing.#
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No row selected.")
        return
    selected_item = selected_items[0]
    values = tree.item(selected_item)["values"]

    # Load values into input fields
    symbol_entry.delete(0, tk.END)
    symbol_entry.insert(0, values[0])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, values[1])

    purchase_entry.delete(0, tk.END)
    purchase_entry.insert(0, values[2])

    current_entry.delete(0, tk.END)
    current_entry.insert(0, values[3])

def update_stock():
    """Update selected stock with new values from input fields."""
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No row selected.")
        return
    selected_item = selected_items[0]

    symbol = symbol_entry.get().upper()
    try:
        qty = int(quantity_entry.get())
        purchase_price = float(purchase_entry.get())
        current_price = float(current_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numbers for quantity and prices.")
        return

    # Validations
    if qty <= 0:
        messagebox.showwarning("Warning", "Quantity must be positive.")
        return
    if purchase_price < 0 or current_price < 0:
        messagebox.showerror("Error", "Prices cannot be negative.")
        return

    invested = purchase_price * qty
    current_value = current_price * qty
    profit_loss_percent = ((current_value - invested) / invested) * 100

    # Update portfolio list
    old_symbol = tree.item(selected_item)["values"][0]
    for item in portfolio:
        if item[0] == old_symbol:
            item[0], item[1], item[2], item[3], item[4] = symbol, qty, purchase_price, current_price, round(profit_loss_percent, 2)
            break

    # Update Treeview row
    if profit_loss_percent >= 0:
        tree.item(selected_item, values=(symbol, qty, purchase_price, current_price, f"{profit_loss_percent:.2f}%"), tags=("profit",))
    else:
        tree.item(selected_item, values=(symbol, qty, purchase_price, current_price, f"{profit_loss_percent:.2f}%"), tags=("loss",))

    update_summary()
    update_graph()
    messagebox.showinfo("Success", f"{symbol} updated successfully!")


def save_portfolio():
    """Save portfolio to CSV file at a fixed path."""
    if not portfolio:
        messagebox.showwarning("Warning", "Portfolio is empty.")
        return

    # Custom path (your internship folder)
    file_path = r"C:\Users\User\Documents\CodeAlpha Python Internship\portfolio.csv"

    try:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Quantity", "Purchase Price", "Current Price", "Profit/Loss %"])
            writer.writerows(portfolio)

        messagebox.showinfo("Success", f"Portfolio saved successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")
        
def load_portfolio():
    """Load portfolio data from CSV file into the table and graph."""
    file_path = r"C:\Users\User\Documents\CodeAlpha Python Internship\portfolio.csv"
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            portfolio.clear()
            for row in reader:
                symbol, qty, purchase_price, current_price, pl_percent = row
                qty = int(qty)
                purchase_price = float(purchase_price)
                current_price = float(current_price)
                pl_percent = float(pl_percent)

                portfolio.append([symbol, qty, purchase_price, current_price, pl_percent])

                # Insert into Treeview
                if pl_percent >= 0:
                    tree.insert("", "end", values=(symbol, qty, purchase_price, current_price, f"{pl_percent:.2f}%"), tags=("profit",))
                else:
                    tree.insert("", "end", values=(symbol, qty, purchase_price, current_price, f"{pl_percent:.2f}%"), tags=("loss",))

        update_summary()
        update_graph()
        messagebox.showinfo("Success", f"Portfolio loaded successfully!")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved portfolio file found.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load portfolio:\n{e}")



def update_graph():
    """Update embedded bar chart inside Tkinter window."""
    for widget in graph_frame.winfo_children():
        widget.destroy()

    if not portfolio:
        return

    symbols = [item[0] for item in portfolio]
    invested = [item[1]*item[2] for item in portfolio]
    current = [item[1]*item[3] for item in portfolio]

    fig, ax = plt.subplots(figsize=(7,3))
    x = range(len(symbols))
    ax.bar(x, invested, width=0.4, label="Invested", color="#F39C12")
    ax.bar([i+0.4 for i in x], current, width=0.4, label="Current", color="#2E86C1")
    ax.set_xticks([i+0.2 for i in x])
    ax.set_xticklabels(symbols)
    ax.set_ylabel("Value (₹)")
    ax.set_title("Portfolio Summary")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# UI Setup #

root = tk.Tk()
root.title("Stock Portfolio Tracker")

# Center window
w, h = 1000, 700
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

# Heading
heading = tk.Label(root, text="📈 Stock Portfolio Tracker", font=("Arial", 20, "bold"), fg="#2E86C1", bg="#f0f0f0")
heading.pack(fill="x", pady=15)

# Styling
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
    background="#f9f9f9",
    foreground="black",
    rowheight=28,
    fieldbackground="#f9f9f9"
)
style.map("Treeview",
    background=[("selected", "#2E86C1")],
    foreground=[("selected", "white")]
)

style.configure("TButton",
    font=("Arial", 11, "bold"),
    padding=8
)

# Input Frame
input_frame = tk.LabelFrame(root, text="Add New Portfolio", bg="#f0f0f0", font=("Arial", 13, "bold"))
input_frame.pack(pady=10, fill="x", padx=20)

tk.Label(input_frame, text="Symbol:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=8)
symbol_entry = tk.Entry(input_frame)
symbol_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(input_frame, text="Quantity:", bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=8)
quantity_entry = tk.Entry(input_frame)
quantity_entry.grid(row=0, column=3, padx=10, pady=8)

tk.Label(input_frame, text="Purchase Price:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=8)
purchase_entry = tk.Entry(input_frame)
purchase_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(input_frame, text="Current Price:", bg="#f0f0f0").grid(row=1, column=2, padx=10, pady=8)
current_entry = tk.Entry(input_frame)
current_entry.grid(row=1, column=3, padx=10, pady=8)

# Buttons Frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Load Portfolio", command=load_portfolio, bg="#3498DB", fg="white").grid(row=0, column=5, padx=10)


tk.Button(button_frame, text="Add Portfolio", command=add_portfolio, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Delete Stock", command=delete_stock, bg="#E74C3C", fg="white").grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Save Portfolio", command=save_portfolio, bg="#F39C12", fg="white").grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Edit Stock", command=edit_stock, bg="#2E86C1", fg="white").grid(row=0, column=3, padx=10)
tk.Button(button_frame, text="Update Stock", command=update_stock, bg="#4CAF50", fg="white").grid(row=0, column=4, padx=10)


# Portfolio Table
tree = ttk.Treeview(root, columns=("Symbol", "Quantity", "Purchase Price", "Current Price", "Profit/Loss %", "Actions"), show="headings")
tree.heading("Symbol", text="Symbol")
tree.heading("Quantity", text="Quantity")
tree.heading("Purchase Price", text="Purchase Price")
tree.heading("Current Price", text="Current Price")
tree.heading("Profit/Loss %", text="Profit/Loss %")
tree.heading("Actions", text="Actions")
tree.pack(pady=10, fill="both", expand=True, padx=20)

# Profit/Loss highlighting
tree.tag_configure("profit", foreground="green")
tree.tag_configure("loss", foreground="red")

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Summary Section
summary_frame = tk.Frame(root, bg="#f0f0f0")
summary_frame.pack(pady=10, fill="x", padx=20)

current_label = tk.Label(summary_frame, text="Current Value: ₹0.00",
                         font=("Arial", 13, "bold"), fg="#2E86C1", bg="#f0f0f0")
current_label.pack(side="left", padx=40)

invested_label = tk.Label(summary_frame, text="Invested: ₹0.00",
                          font=("Arial", 13, "bold"), fg="#2E86C1", bg="#f0f0f0")
invested_label.pack(side="right", padx=40)

# Graph Frame (embedded chart)
graph_frame = tk.LabelFrame(root, text="Portfolio Graph", bg="#f0f0f0", font=("Arial", 13, "bold"))
graph_frame.pack(pady=15, fill="both", expand=True, padx=20)

root.mainloop()
