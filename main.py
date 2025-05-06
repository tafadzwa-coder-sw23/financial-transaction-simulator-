import tkinter as tk
from tkinter import messagebox, scrolledtext
# from tkinter import ttk # ttk was imported but not used, can be added back if you use ttk widgets

class FinancialSimulator:
    def __init__(self, root): # Corrected: double underscores for __init__
        self.transactions = [] # Corrected: consistent naming (plural)
        self.root = root
        self.root.title("Financial Simulator")
        self.root.geometry("500x600") # Added a default size

        # Set the theme colors correctly
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#333333" # Darker text for better contrast
        self.entry_bg_color = "#ffffff"

        self.root.configure(bg=self.bg_color)

        # Setup ui
        self.create_widgets()

    def create_widgets(self):
        # --- Main Frame for padding and organization ---
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        self.title_label = tk.Label(main_frame, text="Financial Simulator", font=("Helvetica", 20, "bold"),
                                    bg=self.bg_color, fg="#003366") # Changed title color
        self.title_label.pack(pady=(0, 20)) # Adjusted padding

        # --- Frame for inputs ---
        self.input_fields_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.input_fields_frame.pack(pady=10, fill=tk.X)

        # Amount Entry
        self.amount_label = tk.Label(self.input_fields_frame, text="Amount:", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10))
        self.amount_label.grid(row=0, column=0, padx=(0,10), pady=5, sticky=tk.W)
        self.amount_entry = tk.Entry(self.input_fields_frame, width=35, font=("Helvetica", 10), bg=self.entry_bg_color, fg=self.text_color)
        self.amount_entry.grid(row=0, column=1, padx=0, pady=5, sticky=tk.EW)

        # Description Entry
        self.description_label = tk.Label(self.input_fields_frame, text="Description:", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10))
        self.description_label.grid(row=1, column=0, padx=(0,10), pady=5, sticky=tk.W) # Corrected: row=1
        self.description_entry = tk.Entry(self.input_fields_frame, width=35, font=("Helvetica", 10), bg=self.entry_bg_color, fg=self.text_color)
        self.description_entry.grid(row=1, column=1, padx=0, pady=5, sticky=tk.EW)

        self.input_fields_frame.grid_columnconfigure(1, weight=1) # Make entry fields expand

        # --- Frame for buttons ---
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

        # Scrolled Text widget for displaying reports
        self.report_text_label = tk.Label(main_frame, text="Report/Log:", font=("Helvetica", 12, "bold"),
                                          bg=self.bg_color, fg=self.text_color)
        self.report_text_label.pack(pady=(10,0), anchor=tk.W)

        self.report_text = scrolledtext.ScrolledText(main_frame, height=15, width=60, wrap=tk.WORD,
                                                     bg=self.entry_bg_color, fg=self.text_color, font=("Courier New", 9))
        self.report_text.pack(pady=(5,0), padx=0, fill=tk.BOTH, expand=True)
        self.report_text.config(state=tk.DISABLED) # Start as read-only

    def add_transaction(self):
        try:
            amount_str = self.amount_entry.get()
            description = self.description_entry.get().strip()

            if not amount_str: # Check if amount string is empty
                raise ValueError("Amount cannot be empty.")
            amount = float(amount_str) # Convert to float after check

            if description == "":
                raise ValueError("Description cannot be empty.")

            transaction_type = "Expense" if amount < 0 else "Income"
            transaction = {
                "amount": amount,
                "description": description,
                "type": transaction_type
            }
            self.transactions.append(transaction) # Corrected: self.transactions

            # Clear entries
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Transaction added successfully.", parent=self.root)
            self.log_to_report(f"Added: {transaction_type} - {description} - ${amount:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}", parent=self.root) # Corrected: messagebox
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}", parent=self.root)


    def view_balance(self):
        if not self.transactions:
            messagebox.showinfo("Current Balance", "No transactions yet. Current Balance: $0.00", parent=self.root)
            return
        balance = sum(t["amount"] for t in self.transactions) # Corrected: self.transactions
        messagebox.showinfo("Current Balance", f"Current Balance: ${balance:.2f}", parent=self.root) # Corrected: display calculated balance

    def generate_report(self):
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete(1.0, tk.END) # Corrected: delete

        if not self.transactions:
            self.report_text.insert(tk.END, "No transactions to report yet.")
            self.report_text.config(state=tk.DISABLED)
            return

        report = "--- Transaction Report ---\n\n" # Corrected: report =
        total_income = 0
        total_expenses = 0

        for t in self.transactions: # Corrected: self.transactions
            # Corrected: f-string syntax and ensuring $ is part of the string
            # Also ensuring the amount reflects its sign naturally
            report += f"{t['type']:<8}: {t['description']:<30} Amount: ${t['amount']:>10.2f}\n"
            if t['amount'] > 0:
                total_income += t['amount']
            else:
                total_expenses += t['amount'] # Expenses are negative

        report += "\n--- Summary ---\n"
        report += f"Total Income:   ${total_income:>10.2f}\n"
        report_expenses_display = abs(total_expenses) # Display expenses as a positive number in summary
        report += f"Total Expenses: ${report_expenses_display:>10.2f}\n"
        report += "--------------------------\n"
        current_balance = total_income + total_expenses # total_expenses is already negative
        report += f"Final Balance:  ${current_balance:>10.2f}\n"
        report += "--------------------------\n"

        self.report_text.insert(tk.END, report)
        self.report_text.config(state=tk.DISABLED)
        messagebox.showinfo("Report Generated", "Transaction report has been updated in the report panel.", parent=self.root)

    def get_balance(self): # This method seems fine but isn't directly used by buttons
        return sum(t["amount"] for t in self.transactions) # Corrected: self.transactions

    def log_to_report(self, message):
        """Helper function to add a quick log to the report text area"""
        self.report_text.config(state=tk.NORMAL)
        self.report_text.insert(tk.END, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {message}\n")
        self.report_text.see(tk.END) # Scroll to the end
        self.report_text.config(state=tk.DISABLED)

# --- Main part of the program ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialSimulator(root)
    root.mainloop()