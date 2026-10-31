import csv
from pathlib import Path
from datetime import datetime

FILE = Path("expenses.csv")
FIELDS = ["date", "category", "amount", "note"]

def setup_file():
    if not FILE.exists():
        with FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def add_expense():
    date = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date, "%Y-%m-%d")
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid date and a positive amount.")
        return
    category = input("Category (Food/Travel/Study/Other): ").strip().title()
    note = input("Short note: ").strip()
    with FILE.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow({
            "date": date, "category": category,
            "amount": f"{amount:.2f}", "note": note
        })
    print("Expense saved successfully.")

def view_expenses():
    with FILE.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("No expenses recorded yet.")
        return
    print("\nDate         Category       Amount       Note")
    print("-" * 60)
    for r in rows:
        print(f'{r["date"]:<12} {r["category"]:<14} {r["amount"]:>9}   {r["note"]}')

def show_summary():
    totals = {}
    grand_total = 0.0
    with FILE.open("r", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            amount = float(r["amount"])
            totals[r["category"]] = totals.get(r["category"], 0.0) + amount
            grand_total += amount
    if not grand_total:
        print("No expenses available for summary.")
        return
    print("\n=== EXPENSE SUMMARY ===")
    for category, total in sorted(totals.items()):
        print(f"{category:<15}: {total:.2f}")
    print("-" * 25)
    print(f"{'Total':<15}: {grand_total:.2f}")

def main():
    setup_file()
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Show category-wise summary")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Thank you for using the tracker.")
            break
        else:
            print("Invalid choice. Select 1 to 4.")

if __name__ == "__main__":
    main()
