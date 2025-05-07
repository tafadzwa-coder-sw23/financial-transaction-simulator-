# financial-transaction-simulator-
# Financial Simulator

A simple desktop application built with Python and Tkinter for managing personal finances. It allows users to track income and expenses, view their current balance, and generate a summary report. Transactions are saved locally in a JSON file, so your data persists between sessions.

## Features

* **Add Transactions:**
    * Enter the date (YYYY-MM-DD, defaults to today), amount, and description for each transaction.
    * Positive amounts are treated as income, negative amounts as expenses.
* **View Balance:**
    * Quickly check the current calculated balance based on all entered transactions.
* **Generate Report:**
    * Displays a detailed list of all transactions, sorted by date.
    * Shows a summary of total income, total expenses, and the final balance.
    * Income transactions are highlighted in green, and expenses in red within the report.
* **Data Persistence:**
    * Transactions are automatically saved to a `transactions.json` file when a new transaction is added or when the application is closed.
    * Transactions are loaded from this file when the application starts.
* **User-Friendly Interface:**
    * Clean and intuitive GUI built with Tkinter.
    * Input validation for amount, description, and date format.
    * Informative messages and error handling.
* **Logging:**
    * Key actions (e.g., loading/saving data, adding transactions, errors) are logged in the report area.

## How to Use

1.  **Prerequisites:**
    * Ensure you have Python 3 installed on your system.
    * Tkinter is usually included with standard Python installations. If not, you may need to install it separately (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu, or it might be part of a `python3-devel` or similar package).

2.  **Run the Application:**
    * Save the Python script (e.g., `financial_simulator.py`) to a directory on your computer.
    * Open a terminal or command prompt.
    * Navigate to the directory where you saved the file.
    * Execute the script using the command:
        ```bash
        python financial_simulator.py
        ```

3.  **Using the Interface:**
    * **Date:** Enter the transaction date in `YYYY-MM-DD` format. If left blank or an invalid format is used when adding a transaction, it will default to the current date.
    * **Amount:** Enter the transaction amount. Use positive numbers for income (e.g., `100`) and negative numbers for expenses (e.g., `-25.50`).
    * **Description:** Provide a brief description of the transaction (e.g., "Salary", "Groceries").
    * **Add Transaction Button:** Click to add the entered transaction to your records. Fields will clear, and the date will reset to today.
    * **View Balance Button:** Click to see your current financial balance in a pop-up window.
    * **Generate Report Button:** Click to update the report area with a list of all transactions and a financial summary.
    * **Report/Log Area:** This area displays the transaction report and logs important application events.

4.  **Data Storage:**
    * A file named `transactions.json` will be created in the same directory as the script to store your transaction data. Do not manually edit this file unless you know what you are doing, as incorrect formatting can cause loading errors.

## File Structure
