import tkinter as tk
from tkinter import messagebox, scrolledtext 
from tkinter import ttk

class FinancialSimulator:
    def _init_(self, root):
        self.transaction = []
        self.root = root
        self.root.title("Financial Simulator")

        #set the teme color 
        set.bg_color = "#f0f0f0"
        set.button_color = "#4CAF50"
        self.text_color = "#333"
        #setup ui
        self.create_widgets()

    def create_widgets(self):  
        #Title label  
        self.title_label = tk.Label(self.root, text="Financial Simulator", font=("Helvetica", 18, "bold"), bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=20)
        # Frame for inputs
        self.input_frame = tk.Frame(self.root, bg=self.bg_color)
        self.input_frame.pack(pady=10, padx=20 , fill=tk.X)
        #amount Entry 
        self.amount_label = tk.Label(self.input_frame, text="Amount:", bg=self.bg_color, fg=self.text_color)
        self.amount_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.amount_entry = tk.Entry(self.input_frame, width=30)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        # Description Entry 
        self.description_label = tk.Label(self.input_frame, text="Description:", bg=self.bg_color, fg=self.text_color)
        self.description_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.description_entry = tk.Entry(self.input_frame, width=30)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)
        #Buttons
        self.add_button = tk.Button(self.root, text="Add Transaction", command=self.add_transaction, bg=self.button_color, fg="white")
        self.add_button.pack(pady=5, padx=20, fill=tk.X)
        self.balance_button = tk.Button(self.root, text="View Balance", command=self.view_balance, bg=self.button_color, fg="white")
        self.balance_button.pack(pady=5, padx=20, fill=tk.X)
        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report, bg=self.button_color, fg="white")
        self.report_button.pack(pady=5, padx=20, fill=tk.X)
        #Scrolled Text widget for displaying reports 
        self.report_text = scrolledtext.ScrolledText(self.root, height=15, width=60, wrap=tk.WORD, bg="white", fg=self.text_color)
        self.report_text.pack(pady=10, padx=20)

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get().strip()
            if description == "":
                raise ValueError("Description cannot be empty.")

            transaction_type = "Expense" if amount < 0 else "income"
            transaction = {
                "amount": amount,
                "description": description,
                "type": transaction_type
            } 
            self.transaction.append(transaction)

            #clear entries    
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Transaction added successfully.")
        except ValueError as e:
            message.showerror("Error", f"Invalid input: {e}")

    def view_balance(self):
        balance = sum(t["amount"] for t in self.transactions)
        messagebox.showinfo("Current Balance", f"Current Balance: ${t["amount"]:}")     

    def generate_report(self):
        report "Transaction Report:\n"  
        for t in self.transactions:
            report += f"{t["type"]}: {t["description"]}" - ${t["amount"]:.2f}\n"   

            self.report_text.config(state=tk.NORMAL)
            self.report_text.delect(1.0, tk.END)
            self.report_text.insert(tk.END,report)
            self.report_text.config(state=tk.DISABLED)

    def get_balance(self):
        return sum(t["amount"] for t in self.transactions) 


root = tk.Tk()
app = FinancialSimulator(root)
root.mainloop()             
                