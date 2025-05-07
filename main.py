import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime  # <--- ADDED THIS IMPORT
import json      # +++ NEW: For data persistence

# +++ NEW: Transaction Class +++
class Transaction:
    def __init__(self, amount: float, description: str, transaction_type: str, date_str: str = None):
        self.amount = amount
        self.description = description
        self.type = transaction_type
        
        if date_str:
            try:
                self.date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showwarning("Date Warning", f"Invalid date format '{date_str}'. Using today's date instead.", parent=root) # Assuming root is accessible or pass it
                self.date = datetime.date.today()
        else:
            self.date = datetime.date.today()

    def to_dict(self):
        """Converts the Transaction object to a dictionary for JSON serialization."""
        return {
            "amount": self.amount,
            "description": self.description,
            "type": self.type,
            "date": self.date.isoformat()  # Store date as YYYY-MM-DD string
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Transaction object from a dictionary (e.g., from JSON)."""
        return cls(
            amount=data.get("amount", 0.0),
            description=data.get("description", "N/A"),
            transaction_type=data.get("type", "Expense"),
            date_str=data.get("date") # Expects YYYY-MM-DD string
        )

    def __str__(self): # For easier debugging or direct printing
        return f"{self.date} | {self.type:<8} | {self.description:<30} | Amount: ${self.amount:>10.2f}"


class FinancialSimulator:
    def __init__(self, root_window): # --- MODIFIED: Renamed root to root_window for clarity
        self.transactions = []
        self.root = root_window # --- MODIFIED: Consistent use of self.root
        self.root.title("Financial Simulator")
        self.root.geometry("550x700") # --- MODIFIED: Slightly larger for the date field

        self.data_file = "transactions.json" # +++ NEW: Data file name

        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#333333"
        self.entry_bg_color = "#ffffff"

        self.root.configure(bg=self.bg_color)
        self.create_widgets()
        self.load_transactions() # +++ NEW: Load transactions on startup
        
        # +++ NEW: Save transactions when the window is closed +++
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    # +++ NEW: Method to load transactions from JSON file +++
    def load_transactions(self):
        try:
            with open(self.data_file, 'r') as f:
                transactions_data = json.load(f)
                self.transactions = [Transaction.from_dict(data) for data in transactions_data]
            self.log_to_report(f"Loaded {len(self.transactions)} transactions from {self.data_file}")
        except FileNotFoundError:
            self.log_to_report(f"No data file ('{self.data_file}') found. Starting fresh.")
            self.transactions = []
        except json.JSONDecodeError:
            self.log_to_report(f"Error decoding JSON from '{self.data_file}'. Starting fresh or check file.")
            self.transactions = []
        except Exception as e:
            self.log_to_report(f"Error loading transactions: {e}")
            self.transactions = []
        self.generate_report() # Refresh report view

    # +++ NEW: Method to save transactions to JSON file +++
    def save_transactions(self):
        try:
            with open(self.data_file, 'w') as f:
                # Convert list of Transaction objects to list of dictionaries
                transactions_data = [t.to_dict() for t in self.transactions]
                json.dump(transactions_data, f, indent=4)
            self.log_to_report(f"Saved {len(self.transactions)} transactions to {self.data_file}")
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save transactions to '{self.data_file}': {e}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Save Error", f"An unexpected error occurred during save: {e}", parent=self.root)


    # +++ NEW: Handler for window closing +++
    def on_closing(self):
        self.save_transactions()
        self.root.destroy()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(main_frame, text="Financial Simulator", font=("Helvetica", 20, "bold"),
                                    bg=self.bg_color, fg="#003366")
        self.title_label.pack(pady=(0, 20))

        self.input_fields_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.input_fields_frame.pack(pady=10, fill=tk.X)

        # --- MODIFIED: Added Date Entry ---
        self.date_label = tk.Label(self.input_fields_frame, text="Date (YYYY-MM-DD):", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10))
        self.date_label.grid(row=0, column=0, padx=(0,10), pady=5, sticky=tk.W)
        self.date_entry = tk.Entry(self.input_fields_frame, width=35, font=("Helvetica", 10), bg=self.entry_bg_color, fg=self.text_color)
        self.date_entry.grid(row=0, column=1, padx=0, pady=5, sticky=tk.EW)
        self.date_entry.insert(0, datetime.date.today().isoformat()) # Default to today

        self.amount_label = tk.Label(self.input_fields_frame, text="Amount:", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10))
        self.amount_label.grid(row=1, column=0, padx=(0,10), pady=5, sticky=tk.W) # --- MODIFIED: row
        self.amount_entry = tk.Entry(self.input_fields_frame, width=35, font=("Helvetica", 10), bg=self.entry_bg_color, fg=self.text_color)
        self.amount_entry.grid(row=1, column=1, padx=0, pady=5, sticky=tk.EW) # --- MODIFIED: row

        self.description_label = tk.Label(self.input_fields_frame, text="Description:", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10))
        self.description_label.grid(row=2, column=0, padx=(0,10), pady=5, sticky=tk.W) # --- MODIFIED: row
        self.description_entry = tk.Entry(self.input_fields_frame, width=35, font=("Helvetica", 10), bg=self.entry_bg_color, fg=self.text_color)
        self.description_entry.grid(row=2, column=1, padx=0, pady=5, sticky=tk.EW) # --- MODIFIED: row

        self.input_fields_frame.grid_columnconfigure(1, weight=1)

        self.button_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.button_frame.pack(pady=10, fill=tk.X)

        button_font = ("Helvetica", 10, "bold")
        button_padx = 5
        button_pady = 5

        self.add_button = tk.Button(self.button_frame, text="Add Transaction", command=self.add_transaction,
                                    bg=self.button_color, fg="white", font=button_font, relief=tk.RAISED, borderwidth=2)
        self.add_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady, expand=True, fill=tk.X)

        self.balance_button = tk.Button(self.button_frame, text="View Balance", command=self.view_balance,
                                        bg=self.button_color, fg="white", font=button_font, relief=tk.RAISED, borderwidth=2)
        self.balance_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady, expand=True, fill=tk.X)

        self.report_button = tk.Button(self.button_frame, text="Generate Report", command=self.generate_report,
                                    bg=self.button_color, fg="white", font=button_font, relief=tk.RAISED, borderwidth=2)
        self.report_button.pack(side=tk.LEFT, padx=button_padx, pady=button_pady, expand=True, fill=tk.X)

        self.report_text_label = tk.Label(main_frame, text="Report/Log:", font=("Helvetica", 12, "bold"),
                                        bg=self.bg_color, fg=self.text_color)
        self.report_text_label.pack(pady=(10,0), anchor=tk.W)

        self.report_text = scrolledtext.ScrolledText(main_frame, height=15, width=60, wrap=tk.WORD,
                                                    bg=self.entry_bg_color, fg=self.text_color, font=("Courier New", 9))
        self.report_text.pack(pady=(5,0), padx=0, fill=tk.BOTH, expand=True)
        self.report_text.config(state=tk.DISABLED)

    def add_transaction(self):
        try:
            date_str = self.date_entry.get().strip() # +++ NEW
            amount_str = self.amount_entry.get().strip()
            description = self.description_entry.get().strip()

            if not amount_str:
                raise ValueError("Amount cannot be empty.")
            if not description:
                raise ValueError("Description cannot be empty.")
            # Basic date validation (can be more robust)
            if date_str: # If user provided a date
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Date format must be YYYY-MM-DD.")
            else: # If date entry is empty, use today
                date_str = datetime.date.today().isoformat()


            amount = float(amount_str)
            transaction_type = "Income" if amount >= 0 else "Expense" # >=0 for $0 income
            
            # --- MODIFIED: Use Transaction class ---
            new_trans = Transaction(amount, description, transaction_type, date_str)
            self.transactions.append(new_trans)
            self.save_transactions() # +++ NEW: Save after adding

            self.date_entry.delete(0, tk.END) # +++ NEW
            self.date_entry.insert(0, datetime.date.today().isoformat()) # Reset to today
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.amount_entry.focus_set() # Set focus to amount for next entry

            messagebox.showinfo("Success", "Transaction added successfully.", parent=self.root)
            self.log_to_report(f"Added: {new_trans.date} - {transaction_type} - {description} - ${amount:.2f}")
            self.generate_report() # +++ NEW: Update report view immediately
        except ValueError as e:
            messagebox.showerror("Input Error", f"{e}", parent=self.root)
        except Exception as e:
            self.log_to_report(f"ERROR in add_transaction: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=self.root)

    def view_balance(self):
        if not self.transactions:
            messagebox.showinfo("Current Balance", "No transactions yet. Current Balance: $0.00", parent=self.root)
            return
        # --- MODIFIED: Use Transaction objects ---
        balance = sum(t.amount for t in self.transactions)
        messagebox.showinfo("Current Balance", f"Current Balance: ${balance:.2f}", parent=self.root)

    def generate_report(self):
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete(1.0, tk.END)

        if not self.transactions:
            self.report_text.insert(tk.END, "No transactions to report yet.")
            self.report_text.config(state=tk.DISABLED)
            return

        # --- MODIFIED: Sort transactions by date for the report ---
        sorted_transactions = sorted(self.transactions, key=lambda t: t.date)

        report_header = "--- Transaction Report ---\n"
        report_header += f"{'Date':<12}{'Type':<10}{'Description':<30}{'Amount':>12}\n"
        report_header += "-" * 64 + "\n"
        self.report_text.insert(tk.END, report_header)

        total_income = 0
        total_expenses = 0

        # --- MODIFIED: Use Transaction objects and their attributes ---
        for t in sorted_transactions:
            # --- MODIFIED: Using Transaction object attributes ---
            report_line = f"{t.date.isoformat():<12}{t.type:<10}{t.description:<30}${t.amount:>10.2f}\n"
            
            # Example of adding color tags (optional, but makes report nicer)
            tag_to_use = ()
            if t.type == "Income":
                tag_to_use = ("income_tag",)
                total_income += t.amount
            else: # Expense
                tag_to_use = ("expense_tag",)
                total_expenses += t.amount # Expenses are negative, so sum directly

            self.report_text.insert(tk.END, report_line, tag_to_use)
        
        # Configure tags for colors (do this once, maybe in create_widgets or __init__)
        self.report_text.tag_configure("income_tag", foreground="green")
        self.report_text.tag_configure("expense_tag", foreground="red")


        report_summary = "\n--- Summary ---\n"
        report_summary += f"Total Income:   ${total_income:>10.2f}\n"
        report_expenses_display = abs(total_expenses)
        report_summary += f"Total Expenses: ${report_expenses_display:>10.2f}\n" # Display as positive
        report_summary += "--------------------------\n"
        current_balance = total_income + total_expenses # total_expenses is already negative
        report_summary += f"Final Balance:  ${current_balance:>10.2f}\n"
        report_summary += "--------------------------\n"

        self.report_text.insert(tk.END, report_summary)
        self.report_text.config(state=tk.DISABLED)
        # Optionally, remove the messagebox for report generation if it's updated live in the text area
        # messagebox.showinfo("Report Generated", "Transaction report has been updated.", parent=self.root)


    def get_balance(self): # This method is fine
        return sum(t.amount for t in self.transactions)

    def log_to_report(self, message):
        self.report_text.config(state=tk.NORMAL)
        self.report_text.insert(tk.END, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}\n")
        self.report_text.see(tk.END)
        self.report_text.config(state=tk.DISABLED)

# --- Main part of the program ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialSimulator(root)
    root.mainloop()